# Project: Retrieval Metrics Dashboard Seed

Build the first version of a production retrieval quality dashboard.

## What You Will Build

1. A benchmark evaluator that compares retrieved ids against gold evidence.
2. Per-query metrics:
   - Recall@K
   - Precision@K
   - MRR
   - first relevant rank
   - stale-hit count
   - filtered-gold count
3. Slice summaries by domain and query type.
4. A release gate that blocks high-risk retrieval regressions.
5. Diagnostic recommendations that tell the team what to inspect next.

## Production Scenarios

- Policy lookup: gold evidence must appear in final context.
- Exact-term support: error codes and IDs must not be lost by semantic search.
- PDF/table lookup: parser and chunking quality can dominate retrieval quality.
- Access-filtered legal content: gold evidence may be correctly denied, but the trace must explain it.

## Acceptance Criteria

- High-risk queries with missing gold evidence block release.
- Filtered-out gold evidence is reported separately from search failure.
- Stale hits are visible in the report.
- Metrics are summarized by slice, not only overall average.
- Each failure includes a recommendation.
