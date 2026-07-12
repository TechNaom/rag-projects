# Real-Time On-Call Ops Copilot (live-updating RAG)

A working, end-to-end Retrieval-Augmented Generation system built for the one
thing most RAG demos quietly ignore: **the source documents keep changing while
you're using it.** This copilot retrieves over on-call runbooks and incident
notes for a fictional SaaS company, and it re-indexes an edited document *live*
— in milliseconds, without a full rebuild — because that's exactly what happens
during a real incident.

It also runs under a **hard per-stage latency budget** (an on-call tool that's
slow when the pager fires is useless) and uses a **cost-aware router** so simple
lookups skip the expensive path.

> The company, services, runbooks, and incidents are entirely fictional,
> invented for this project. Any resemblance to a real company's infrastructure
> is coincidental.

## Why live-updating retrieval matters for on-call

Picture a SEV1 at 3am. The on-call engineer opens the incident note and starts
typing what they're seeing: "writes failing on orders-prod", then a minute later
"root cause: replication slot retaining WAL", then "mitigation: manual failover
+ drop the slot". Meanwhile a teammate asks the copilot: *"what's the confirmed
mitigation for the orders-prod incident?"*

If the index was frozen at build time, the copilot answers from a stale
snapshot and confidently gives the wrong (or empty) mitigation. That's worse
than no tool at all. The index has to reflect the note **as it is right now**.

A naive fix — rebuild the whole index on every edit — refits the embedding
model and re-embeds the entire corpus. That's seconds to minutes, and it shifts
every vector in the store. You cannot do that on every keystroke. The real
answer is **incremental upsert**: freeze the embedder, and when one file
changes, re-chunk and re-embed *only that file*, swapping its chunks in place.
That's the core of this project (`vectorstore.upsert_document` +
`live_updater.apply_update`).

## Architecture

```
data/runbooks/*.md          6 runbooks (change rarely)
data/incident_notes/*.md    incident notes (change CONSTANTLY, mid-incident)
        |
        v
src/ingest.py               Markdown-header-aware chunking; tags every chunk
        |                   with doc_type (runbook|incident_note) + source_file
        v
src/embeddings.py           TF-IDF + SVD -> dense vectors, FIT ONCE then frozen
        |                   (freezing is what makes incremental upsert cheap)
        v
src/vectorstore.py          Initial build -> ChromaDB (persisted on disk)
        |                   + upsert_document(file): re-index ONE file, no rebuild
        |
        |   .................................................................
        |   : src/live_updater.py  (LIVE SIDE-PATH)                         :
        |   :   apply_update(file, new_content):                           :
        |   :     write file to disk  -->  vectorstore.upsert_document()   :
        |   :   deletes that file's old chunks, embeds new ones with the   :
        |   :   FROZEN embedder, adds them back.  NO build_vectorstore().  :
        |   :................................................................:
        v
src/cost_router.py          classify(query) -> simple (k=3, no rerank)
        |                                    -> complex (k=6, rerank)
        v
src/rag_chain.py            retrieve() [embed_query | vector_search | rerank]
        |                   -> build_context_block() -> generate_answer()
        |                   every stage wrapped in a latency_budget timer
        |                   generation via local Ollama (default) or Groq
        v
src/latency_budget.py       StageTimer: p50/p95 per stage vs a documented budget
src/main.py                 Interactive CLI (+ simulate-update, latency report)
```

## A real constraint, handled honestly: the embedding model

A production RAG system would use a neural embedding model — local
(sentence-transformers) or hosted (OpenAI, or Voyage AI, Anthropic's
recommended embeddings partner). The sandbox this was built in blocks
`huggingface.co` at the network layer, so weights can't be downloaded at
runtime.

Rather than fake that away, `src/embeddings.py` implements a **fully local,
pip-only** method: TF-IDF reduced to a 128-dim dense vector via Truncated SVD
(classic Latent Semantic Analysis). It's a legitimate pre-deep-learning
retrieval technique — lexical, not deeply semantic. `embeddings.py` has a
clearly marked swap-in point with the exact code to drop in
`HuggingFaceEmbeddings` or `VoyageAIEmbeddings` once you have full network
access; nothing else in the pipeline changes, because everything talks to the
embedder through LangChain's standard interface. That pluggability *is* the
lesson.

There's a second, project-specific reason the choice matters here: the embedder
is **fit once and frozen**. Live upserts embed new incident-note text with that
same frozen model (`transform`, never `fit`), which is exactly what keeps an
incremental update O(one file) instead of O(whole corpus). See the long note at
the top of `embeddings.py`.

## A real constraint, handled honestly: generation

`rag_chain.py`'s generation step supports two providers:

- **Ollama, run locally** — the default; no API key, no cost, but you need a
  local Ollama server with a model pulled.
- **Groq** (Llama 3.3 70B) — fast hosted inference; set `GROQ_API_KEY` (or fill
  `config/config.ini`, copied from `config/config.example.ini`).

Without either configured, the CLI still shows retrieval, routing, and latency
for every query — which is most of what's interesting about this system. The
live-update demo and the latency report **do not require any LLM** — they
exercise the retrieval/index path, which is the whole point.

## Running it

```bash
pip install -r requirements.txt

# Optional: configure a generation provider
cp config/config.example.ini config/config.ini   # then fill in GROQ_API_KEY
# or just run a local Ollama server with a model pulled — it's the default

# 1. Build the index (run once, or whenever data/ changes wholesale)
python src/vectorstore.py

# 2. Interactive copilot
python src/main.py
#    inside: ask a question, or run `simulate-update`, or `latency report`

# 3. Run the live-update demo directly (proves live re-index, no LLM needed)
python src/live_updater.py

# 4. Latency report over a batch of real queries
python src/bench.py

# 5. Tests
python -m pytest tests/ -v
```

## The live-update demo (real output)

This is the actual output of `python src/live_updater.py` on this build. A new
incident note is indexed with *no confirmed mitigation*; the same query is run
before and after an engineer writes the real mitigation. The marker string
`MITIGATION-XYZ-777` is absent before the edit and present after — with **no
full rebuild**.

```text
##########################################################################
# LIVE-UPDATE DEMO
##########################################################################
Query under test:
  "What is the current mitigation for the payment reconciliation incident?"

[1] Indexing initial incident note (no mitigation yet) via incremental upsert...
    upsert: +3 chunks, -0 removed, collection now 67 chunks

[2] Retrieval BEFORE the live update:
    [1] score=0.682  2026-07-12-live-demo.md  (Summary)
    [2] score=0.533  elevated-latency-checklist.md  (6. Verification)
    [3] score=0.381  payment-processor-timeout.md  (6. Verification)
    ...
    top-1 mitigation line: 'charges and local confirmations. Under investigation. No mitigation confirmed yet.'
    contains marker 'MITIGATION-XYZ-777'? False

[3] Applying LIVE update (engineer writes the confirmed mitigation)...
    upsert: +3 chunks, -3 removed, collection now 67 chunks
    NOTE: no build_vectorstore() call - only this one file was re-indexed.

[4] Retrieval AFTER the live update (SAME query):
    [1] score=0.533  elevated-latency-checklist.md  (6. Verification)
    [2] score=0.368  2026-07-12-live-demo.md  (Current Mitigation)
    [3] score=0.381  payment-processor-timeout.md  (6. Verification)
    ...
    top-1 mitigation line: '- Record which mitigation actually moved the metric, for the post-incident review.'
    contains marker 'MITIGATION-XYZ-777'? True

==========================================================================
RESULT: PASS - retrieval changed live. The updated mitigation (marker MITIGATION-XYZ-777) was
        absent before the edit and present after, with NO full rebuild.
==========================================================================
```

Note: the demo deliberately uses a wide retrieval decision (k=8, rerank on) rather
than routing the demo query through `cost_router.classify()` — on a ~65-chunk
corpus, the router's "simple" path (k=3, no rerank) is narrow enough that a
single new document can miss the candidate pool depending on exact phrasing.
That's a retrieval-breadth property of the router, not of the incremental-upsert
mechanism this demo exists to prove — see the comment in `live_updater._sources`.

## Latency report (real output)

Actual output of `python src/bench.py`, which runs a batch of real queries
through the routed, timed pipeline and prints a p50/p95 breakdown per stage
against the documented budget. (Generation isn't exercised here since no LLM
provider is configured in the sandbox, so only the retrieval stages report.)

The documented budget (p95, milliseconds), from `latency_budget.py`:

| stage         | p95 budget |
|---------------|-----------:|
| embed_query   |      50 ms |
| vector_search |     100 ms |
| generation    |    4000 ms |

```text
==========================================================================
LATENCY REPORT  (per-stage, across 30 recorded call(s))
==========================================================================
stage               count     p50 ms     p95 ms   budget p95    status
--------------------------------------------------------------------------
embed_query            30       2.03       3.45           50      PASS
vector_search          30       2.27       6.88          100      PASS
rerank                 15       0.14       0.36            -  (no SLO)
--------------------------------------------------------------------------
Overall (stages with an SLO): MEETS BUDGET
==========================================================================
```

(30 = 10 unique on-call queries x 3 repeats, run through the real routed pipeline.)

## The cost router

Not every question needs the full pipeline. `cost_router.classify()` routes:

- **simple** (short, lookup-style, no analytical keywords) → `k=3`, no rerank
- **complex** (contains `why` / `root cause` / `compare` / …, or > 18 words)
  → `k=6` + a lexical-overlap rerank pass

This is a **documented heuristic, not ML** — length thresholds plus a keyword
list, deliberately auditable. The value is the routing *seam*: the pipeline asks
the router which path to take, so the classifier can later be swapped for a
trained model without touching retrieval. Example classifications:

```text
[simple ] k=3 rerank=False  What's the command to manually fail over orders-prod?
            reason: short lookup-style query (8 words, no complex keywords)
[simple ] k=3 rerank=False  certificate expiry mitigation command
            reason: short lookup-style query (4 words, no complex keywords)
[complex] k=6 rerank=True   Why did checkout start returning 504s after the payments deploy?
            reason: matched complex keyword 'why'
[complex] k=6 rerank=True   What is the root cause of the June 21 queue backlog incident?
            reason: matched complex keyword 'root cause'
[complex] k=6 rerank=True   Compare the database storage-full incident to the standard failover runbook
            reason: matched complex keyword 'compare'
```

## Tests (real output)

Two real pytest files:

- `tests/test_live_update.py` — builds the index, queries, applies a live update
  via `live_updater`, and asserts retrieval now contains a marker string only
  present in the update — **while monkeypatching `build_vectorstore` to raise if
  it's ever called**, so a full reindex disguised as an upsert fails the test.
  Also asserts shrinking a file removes its orphaned chunks.
- `tests/test_latency_budget.py` — asserts the stage timer records timings and
  that the p50/p95 nearest-rank math is exactly correct on synthetic data.

```text
tests/test_latency_budget.py::test_percentile_nearest_rank_known_values PASSED [ 12%]
tests/test_latency_budget.py::test_percentile_unsorted_input PASSED      [ 25%]
tests/test_latency_budget.py::test_timer_records_counts_and_stats PASSED [ 37%]
tests/test_latency_budget.py::test_context_manager_accumulates_across_calls PASSED [ 50%]
tests/test_latency_budget.py::test_report_pass_fail_against_budget PASSED [ 62%]
tests/test_latency_budget.py::test_reset_clears_timings PASSED           [ 75%]
tests/test_live_update.py::test_live_update_changes_retrieval_without_rebuild PASSED [ 87%]
tests/test_live_update.py::test_upsert_removes_old_chunks_on_shrink PASSED [100%]

======================== 8 passed in 88.73s (0:01:28) =========================
```

## What would change for production

- **Incident-note ingestion via a real message queue.** Here, `apply_update`
  is called in-process. In production, edits arrive as events (a webhook from
  the incident tool, a chat-ops bot, a file watcher) onto a queue; a consumer
  runs the upsert. This decouples authoring from indexing and lets you scale,
  retry, and order updates. The `upsert_document(file)` seam is already the
  right shape for a queue consumer to call.
- **A proper latency SLO with alerting.** `latency_budget.py` is in-memory
  wall-clock timing printed to stdout. Production emits these as histograms to
  Prometheus/OpenTelemetry, defines the budget as an SLO, and alerts when the
  rolling p95 breaches it — the same discipline this copilot helps engineers
  apply to *their* services.
- **A real reranker.** The complex path's rerank is a cheap lexical-overlap
  tiebreaker. Replace it with a cross-encoder reranker (e.g. `bge-reranker`) or
  a hosted rerank API for a real relevance lift on the analytical queries.
- **Neural embeddings** (see `embeddings.py` swap-in point) — and, because live
  upsert freezes the embedder, a periodic offline *refit* job to fold in new
  vocabulary that accumulated in incident notes since the last fit.
- **A smarter router.** Swap the keyword heuristic for a tiny trained classifier
  or a fast small-model intent call; keep the routing seam unchanged.
- **Access control + audit.** Filter retrieval by team/service on the vector
  query, and log every query/answer/retrieved-source for the post-incident
  review.

## Contributing

Contributions are welcome. This is a learning-oriented reference project, so
clarity beats cleverness.

1. Fork and create a feature branch.
2. Keep the existing structure: retrieval logic in `rag_chain.py`, index logic
   in `vectorstore.py`, and anything that touches the live-update path must keep
   `build_vectorstore` off the hot path (the test enforces this).
3. Add or update a test under `tests/` for any behavior change and make sure
   `python -m pytest tests/ -v` passes.
4. Run `python src/live_updater.py` and `python src/bench.py` and confirm both
   still work end to end.
5. Open a PR describing what changed and why.

## License

MIT — see [LICENSE](LICENSE).
