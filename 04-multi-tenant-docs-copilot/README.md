# Multi-Tenant Documentation Copilot

A RAG-as-a-service pattern: many tenants share one hosted copilot, each with their own
private knowledge base, and one tenant can never retrieve another tenant's content —
not because of a filter you have to remember to apply, but because it's structurally
impossible. Built as the second production-grade project in this repo, after
[`01-policy-rag-poc`](../01-policy-rag-poc/).

## Why this pattern

The moment you host a RAG system for more than one customer, "does tenant isolation
actually hold" becomes the question that matters most — more than retrieval quality,
more than which LLM you call. A single shared vector collection with a `tenant_id`
metadata filter *works*, right up until a query is built without that filter, or a
migration script forgets it, or a new code path is added by someone who didn't know
the rule existed. That's a soft boundary.

This project uses a hard one: **each tenant gets its own Chroma collection, in its own
directory, with its own independently-fitted embedding model.** There is no query you
can construct against tenant A's collection that returns tenant B's rows — the rows
simply are not there.

## Architecture

```
data/tenants/<slug>/*.md         3 fictional tenants, 4 docs each (see below)
        |
        v
src/ingest.py                    loads + chunks ONE tenant's docs at a time
        |
        v
src/embeddings.py                TF-IDF + SVD -> dense vectors (same technique as
        |                        01-policy-rag-poc; see that project's README for
        |                        why, and the production swap-in point)
        v
src/vectorstore.py               fits a PER-TENANT embedder, writes to a PER-TENANT
        |                        Chroma collection: data/chroma_db/<slug>/
        v
src/tenant_gateway.py            the only doorway to retrieval — TenantGateway is
        |                        bound to exactly one tenant at construction, with
        |                        no method to switch, plus a belt-and-suspenders
        |                        runtime assertion that a bound gateway can never
        |                        return a chunk stamped with another tenant's id
        v
src/cost_tracker.py              wraps every query in a timer + token estimate,
        |                        accumulates per-tenant totals, prints a dashboard
        v
src/rag_chain.py                 retrieve (via the gateway) -> build_context_block
        |                        -> generate_answer, via local Ollama or Groq
        v
src/main.py                      interactive CLI: pick a tenant, ask questions,
                                  or run `cost report` for the dashboard
```

### The 3 tenants (synthetic, fictional)

| Tenant | Type | Docs |
|---|---|---|
| `starlight-robotics` | startup | onboarding, API reference, deployment guide, troubleshooting — for a fictional consumer drone, the "Skylark X2" |
| `aldergate-partners` | consulting agency | client onboarding, engagement pricing, deliverable standards, escalation process |
| `riverbend-trust` | nonprofit | grant eligibility criteria, application process, reporting requirements, disbursement schedule |

Different domains, different vocabularies, different document shapes — on purpose,
so isolation is being tested against genuinely distinct corpora, not three copies of
the same document with the names changed.

## The isolation proof

`tests/test_tenant_isolation.py` is the point of this whole project. It builds all
three tenants' vector stores, queries each one, and asserts that no result ever
carries another tenant's `source_file` or `tenant_id`. Real output from this repo,
this run:

```
tests/test_cost_tracker.py::test_estimate_tokens_is_word_based PASSED    [ 11%]
tests/test_cost_tracker.py::test_record_query_accumulates_per_tenant PASSED [ 22%]
tests/test_cost_tracker.py::test_tenants_do_not_bleed_into_each_other PASSED [ 33%]
tests/test_cost_tracker.py::test_track_context_manager_records_latency_and_completion PASSED [ 44%]
tests/test_cost_tracker.py::test_dashboard_renders_and_reset_clears PASSED [ 55%]
tests/test_tenant_isolation.py::test_all_tenants_built PASSED            [ 66%]
tests/test_tenant_isolation.py::test_no_cross_tenant_leakage PASSED      [ 77%]
tests/test_tenant_isolation.py::test_source_file_sets_are_disjoint PASSED [ 88%]
tests/test_tenant_isolation.py::test_unknown_tenant_fails_closed PASSED  [100%]

======================== 9 passed in 300.37s (0:05:00) ========================
```

`test_unknown_tenant_fails_closed` matters as much as the leakage tests: an
unrecognized `tenant_id` raises `UnknownTenantError` immediately rather than silently
returning nothing (or, worse, falling back to some default tenant's data).

## Running it

```bash
pip install -r requirements.txt

# 1. Build all 3 tenants' isolated indexes (run once, or when a tenant's docs change)
python src/vectorstore.py

# 2. Run the isolation test suite yourself
pytest tests/ -v

# 3. Ask questions interactively (you'll be asked to pick a tenant first)
python src/main.py

# 4. See the cost/latency dashboard after some queries
python src/cost_tracker.py
```

### Real retrieval output (this run, one query per tenant)

```
[starlight-robotics] query: 'How do I set up telemetry webhooks for the Skylark X2?'
  [1] score=0.67   onboarding.md  (1. What the Skylark X2 Is)
  [2] score=0.522  onboarding.md  ()
  [3] score=0.485  onboarding.md  (2. Unboxing and Hardware Checklist)

[aldergate-partners] query: 'What happens if a client disputes an invoice?'
  [1] score=0.663  escalation-process.md  (5. Commercial Disputes)
  [2] score=0.636  client-onboarding.md  (4. Defining Success Metrics)
  [3] score=0.258  client-onboarding.md  (3. Access and Tooling)

[riverbend-trust] query: 'What are the review criteria for a grant application?'
  [1] score=0.652  eligibility-criteria.md  (5. Ineligible Costs)
  [2] score=0.476  eligibility-criteria.md  (6. Conflict of Interest)
  [3] score=0.437  application-process.md  (4. Review Criteria)
```

Every result stayed inside its own tenant's document set — exactly what the
isolation tests check systematically, not just spot-checked here.

### Real cost dashboard output (from the 3 queries above)

```
===================================================================
PER-TENANT COST & LATENCY DASHBOARD
===================================================================
tenant                  queries     tokens  avg latency   est. cost
-------------------------------------------------------------------
aldergate-partners            1         93      0.0591s $   0.00006
riverbend-trust               1         94      0.0777s $   0.00006
starlight-robotics             1         95      0.1436s $   0.00006
-------------------------------------------------------------------
TOTAL                          3        282      0.0935s $   0.00017
===================================================================
note: token counts are approximate (words * 1.3); cost assumes $0.0006/1K tokens.
```

Token counts are word-count-based estimates (see `cost_tracker.py`'s docstring) —
for real billing, swap in the actual provider's token usage figures, which is a
one-line change since `record_query()` already separates "measure" from "attribute."

## What would change for production

- **Auth**: `tenant_id` here is just a CLI prompt. Production needs real request-time
  authentication (a JWT claim, an API key mapped to a tenant) resolved *before*
  `TenantGateway` is ever constructed, so a caller can't simply pass whichever
  `tenant_id` they like.
- **Rate limiting**: per-tenant request quotas, enforced at the gateway, so one noisy
  tenant can't starve shared infrastructure for the others.
- **Managed vector DB**: ChromaDB-per-directory scales fine for a handful of tenants;
  at real scale you'd want a vector DB with native multi-tenant namespaces (Pinecone,
  Qdrant, Weaviate) so isolation is enforced by the database itself, not by directory
  structure.
- **Real billing**: swap the word-count token estimate for the provider's actual
  usage response, and persist the cost log to a real datastore instead of a local
  JSON file.
- **Embeddings**: same swap-in point as `01-policy-rag-poc` — replace
  `LocalTfidfEmbeddings` with a neural embedding model once you have full network
  access; nothing else in the pipeline needs to change.

## Contributing

Issues and PRs welcome. To run the test suite locally:

```bash
pip install -r requirements.txt
python src/vectorstore.py   # build the indexes tests depend on
pytest tests/ -v
```

## License

MIT — see [LICENSE](LICENSE).
