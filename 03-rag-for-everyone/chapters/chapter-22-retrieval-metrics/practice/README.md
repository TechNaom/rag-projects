# Practice Bank: Retrieval Metrics

Use metric symptoms to decide what to inspect.

## The Production Habit

When a retrieval dashboard changes, do not jump directly to "change the model." First ask what kind of failure you are seeing.

## Diagnosis Map

- Low recall: candidate discovery problem.
- High recall but low MRR: ranking or reranking problem.
- Low precision: final context noise problem.
- Filtered gold: metadata, access, tenant, or freshness policy problem.
- Stale hits: index freshness or source-version problem.
- Slice regression: release-gate problem, not only search tuning.

## What To Return

For every symptom, return:

- likely root cause
- metric to watch
- first engineering action
- release decision

The best RAG engineers do not only read metrics. They convert metrics into the next safest engineering move.
