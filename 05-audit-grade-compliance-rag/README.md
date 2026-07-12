# Audit-Grade Compliance RAG

Goes beyond "cites its source" — what [`01-policy-rag-poc`](../01-policy-rag-poc/) already
does — to full audit-grade traceability: every answer proves which evidence supported
which claim, proves the evidence was the **current** authoritative policy version (not a
superseded one), and renders a human-readable report a compliance reviewer can act on
without understanding the system underneath it.

## Why audit-grade traceability matters

"The answer cited a document" is not the same claim as "the answer is safe to rely on."
A citation can point at the right document but the wrong version. It can point at a real
excerpt that doesn't actually support the sentence attached to it. In a regulated
environment, an answer that mixes a superseded six-year retention rule with a current
ten-year rule — and cites both as if they agree — is worse than an answer with no
citations at all, because it *looks* trustworthy. This project's citation auditor exists
to catch exactly that.

## Architecture

```
data/raw_docs/*.md              versioned compliance documents (YAML frontmatter:
        |                       doc_id, version, status, effective_date, superseded_by)
        v
src/ingest.py                   parses version/status metadata + chunks the body
        |
        v
src/embeddings.py                TF-IDF + SVD -> dense vectors (same technique as
        |                        01-policy-rag-poc)
        v
src/vectorstore.py               Chroma collection, every chunk carries its full
        |                        version/lifecycle metadata
        v
src/currency_filter.py           retrieval defaults to status=="current" only;
        |                        include_superseded=True is an explicit override for
        |                        historical/audit queries; verify_currency() proves
        |                        a chunk's version status
        v
src/rag_chain.py                 retrieve (via currency_filter) -> generate -> trace
        |                        generation: Ollama / Groq / an offline extractive
        |                        fallback (works with zero external services)
        v
src/citation_auditor.py          grades the answer L1-L4: cited at all -> every claim
        |                        cited -> citations support the claim (heuristic) ->
        |                        cited source is current
        v
src/trace_store.py               every query logged: evidence, versions, audit result
        v
src/report_generator.py          renders the Markdown "audit report" a reviewer reads
```

### The versioned corpus

A fictional healthcare org, **Aventine Health Network** — 8 compliance documents, 2 of
which have a superseded v1 alongside a current v2 (a patient-records retention policy
whose retention period changed from 6 to 10 years, and a patient-data-access policy),
plus 4 current-only documents (audit logging, breach notification, incident response,
vendor access).

## The citation-support framework (L1-L4)

| Level | Check | What it catches |
|---|---|---|
| L1 | Cited at all | An answer with zero citations |
| L2 | Every claim cited | A claim smuggled in without a citation |
| L3 | Citation supports the claim (heuristic: keyword/number overlap) | A citation bolted onto a claim the chunk doesn't actually mention |
| L4 | Cited source is current | An answer that cites a **superseded** policy as if it were current |

L3 is explicitly labeled a heuristic, not semantic entailment — see the docstring in
`citation_auditor.py` for exactly what it can and can't catch.

## Real output: a clean L4 pass

```
$ python src/main.py
compliance> audit How long must adult patient medical records be retained?
```

- **Citation grade:** **L4**
- **Answer:** Adult patient medical records must be retained for a minimum of
  **ten (10) years** from the date of the patient's last treatment or discharge [1]
  (per RETEN-002 v2.0)...
- **Reviewer verdict:** TRUSTED (L4). This answer is grounded in currently-effective
  policy RETEN-002 v2.0, every claim is cited, and each citation's key facts were found
  in the cited excerpt. No superseded material was used.

Full L1-L4 table from this run:

| Level | Check | Result | Detail |
|-------|-------|--------|--------|
| L1 | Cited at all | PASS | 6 citation marker(s) resolved to retrieved chunks. |
| L2 | Every claim cited | PASS | All 2 claim sentence(s) carry a citation. |
| L3 | Citations support the claim (heuristic) | PASS | All 2 cited claim(s) share ≥40% of their distinctive terms with the cited chunk. |
| L4 | Cited source is current | PASS | Every cited source is the current authoritative version: RETEN-002 v2.0. |

## Real output: catching a superseded citation

Same corpus, `include_superseded=True` (the historical-query override), asked "What is
the retention period for adult patient records?" — retrieval surfaces **both** the
superseded v1.0 (six years) and current v2.0 (ten years):

- **Citation grade:** **L3** (dropped from L4)
- **Answer:** "...must be retained for a minimum of **six (6) years**... [1] (per
  RETEN-001 v1.0)" and "...**ten (10) years**... [2] (per RETEN-002 v2.0)" — both stated,
  disagreeing.
- **L4 result:** **FAIL** — "Answer cites SUPERSEDED source(s): RETEN-001 v1.0
  (superseded by RETEN-002)."
- **Reviewer verdict:** SUPPORTED (L3). Every claim is cited and the citations' key
  terms match the evidence, but at least one cited source was not confirmed current —
  review the currency proofs below before relying on it.

This is the actual point of the project: the system doesn't just fail to notice the
conflict, it names exactly which citation is stale and downgrades its own trust grade
automatically.

## Test suite (real output, this run)

```
tests/test_citation_levels.py::test_l0_uncited_answer_fails_l1 PASSED    [  9%]
tests/test_citation_levels.py::test_l1_passes_when_some_citation_present PASSED [ 18%]
tests/test_citation_levels.py::test_l4_full_pass_on_current_supported_answer PASSED [ 27%]
tests/test_citation_levels.py::test_fails_l3_when_citation_does_not_support_claim PASSED [ 36%]
tests/test_citation_levels.py::test_fails_l4_when_citing_superseded_source PASSED [ 45%]
tests/test_citation_levels.py::test_result_serializes_to_dict PASSED     [ 54%]
tests/test_version_currency.py::test_default_retrieval_excludes_superseded PASSED [ 63%]
tests/test_version_currency.py::test_default_retrieval_surfaces_current_retention_policy PASSED [ 72%]
tests/test_version_currency.py::test_include_superseded_returns_superseded_version PASSED [ 81%]
tests/test_version_currency.py::test_verify_currency_flags_current_and_superseded PASSED [ 90%]
tests/test_version_currency.py::test_current_and_superseded_disagree_on_retention_period PASSED [100%]

============================= 11 passed in 8.98s ==============================
```

## Running it

```bash
pip install -r requirements.txt

python src/vectorstore.py       # build the index (parses version frontmatter)
pytest tests/ -v                # run both test files

python src/main.py              # interactive CLI
# inside the prompt:
#   <question>            normal answer, current-policy only
#   audit <question>       full Markdown audit report
#   history <question>     include superseded versions (for historical queries)
```

No Ollama/Groq configured? The offline extractive fallback still runs the full
retrieve -> audit -> trace -> report pipeline end to end, as shown above.

## What would change for production

- **Real digital signatures** on audit reports, so a report can't be edited after the
  fact and still look valid — the `signature` field here is a trace-content hash, a
  starting point, not cryptographic proof of authorship.
- **A proper audit database** instead of a local JSON-lines trace file, with retention
  and access controls on the audit trail itself.
- **Integration with a real document management system's version control**, so
  `status`/`superseded_by` metadata is pulled from the source of truth instead of
  hand-maintained frontmatter.
- **Replace the L3 heuristic** with an NLI/entailment model or an LLM-as-judge check for
  genuine semantic support verification, not keyword overlap.
- **Embeddings**: same swap-in point as `01-policy-rag-poc` for a neural embedding model.

## Contributing

Issues and PRs welcome. To run the test suite locally:

```bash
pip install -r requirements.txt
python src/vectorstore.py
pytest tests/ -v
```

## License

MIT — see [LICENSE](LICENSE).
