# Chapter 2 Project: Build a Traceable RAG Execution Pipeline

Build a small but serious Python project that shows how a RAG request moves
through an execution pipeline. This is still intentionally lightweight, but it
should feel like the foundation of a production system: documents, metadata,
access checks, retrieval scoring, reranking, context assembly, answer/refusal
behavior, trace logs, and golden evals.

The goal is not to print one nice answer. The goal is to produce an artifact a
real team could inspect and improve.

## Requirements

Your simulator should:

1. Accept a user question.
2. Classify intent.
3. Build a retrieval query.
4. Apply metadata and access filters.
5. Score candidate sources with a simple retrieval strategy.
6. Rerank candidates.
7. Assemble a context block with source labels.
8. Decide answer, refusal, or escalation.
9. Return citations.
10. Emit a trace log with useful diagnostics.
11. Include golden evals for answer, refusal, and escalation paths.
12. Report simple evaluation results.

## Production Scenarios

- HR policy assistant.
- Customer refund bot.
- Security incident runbook assistant.
- Developer documentation assistant.
- Contract-risk assistant.

## Success Criteria

The project is successful when another engineer can read the trace and understand
why the assistant answered, refused, or escalated.

## Production Upgrade Ideas

- Replace lexical scoring with embeddings.
- Add BM25 or hybrid retrieval.
- Persist traces as JSONL.
- Add role-based document visibility.
- Add latency and cost budgets.
- Add a release gate that fails if golden evals fail.
