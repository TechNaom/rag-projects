# Chapter 2 Thinking Journal

## Builder Frame

We are not building a chatbot response. We are building an execution path that
can be inspected, tested, and improved.

## Hypothesis

If learners can map the lifecycle clearly, they will debug RAG failures more
professionally. They will stop blaming the model first and inspect the stages in
order.

## Prompt To Use With GenAI

> Act as a senior RAG architect. For this user question, map the query lifecycle:
> intent, retrieval query, metadata filters, expected source, context assembly,
> answer rule, refusal rule, trace fields, and first metric to inspect.

## Critique Checklist

- Did we retrieve the right source?
- Did metadata filtering protect region, role, version, and access?
- Did context assembly include enough evidence without too much noise?
- Did the answer cite only supporting sources?
- Did the assistant refuse when evidence was missing?
- Did the trace contain enough detail for debugging?

## Decision Record

Chapter 2 introduces execution pipelines early because production RAG is not a
single model call. Indexing strategies, retrieval strategies, reranking, and
execution pipelines will each get deeper chapters later, but learners need the
full lifecycle map now.
