# Exercises: Retrieval Metrics

Practice measuring retrieval before generation.

## Why This Exercise Exists

In a production RAG system, a beautiful final answer can still be unsafe if the evidence was weak, stale, or missing. This exercise trains you to inspect the retrieval layer before blaming the LLM.

## Your Tasks

- Compute Recall@K, Precision@K, MRR, hit rate, and first relevant rank.
- Report stale hits and filtered gold separately.
- Add a diagnosis for each case.
- Return an overall release signal.

## Production Thinking

- Low recall usually means the retriever did not find the evidence.
- High recall with low MRR usually means the evidence was found but buried.
- Stale hits mean the index may be serving old truth.
- Filtered gold means access, tenant, metadata, or freshness logic may be the root cause.

The goal is not only to get the math right. The goal is to tell the engineering team where to look next.
