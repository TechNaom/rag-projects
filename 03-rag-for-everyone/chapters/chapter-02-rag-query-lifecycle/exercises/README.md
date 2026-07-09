# Chapter 2 Exercises: Map the RAG Query Lifecycle

These exercises train you to think like a production RAG debugger. Do not only
write "retrieve then generate." Write the lifecycle clearly enough that another
engineer can implement, log, and evaluate it.

## Exercise 1 — Map the stages

For each user question in `starter.py`, fill in the lifecycle stages:

- user question
- intent
- retrieval query
- metadata filters
- expected source
- context rule
- answer rule
- refusal rule
- metric to inspect

## Exercise 2 — Add metadata filters

Add realistic filters for at least five questions. Use region, role, policy
version, product tier, confidentiality level, incident severity, or customer
segment.

## Exercise 3 — Identify the first failure point

For each failure scenario, decide whether the first issue is:

- query understanding
- retrieval
- metadata filtering
- context assembly
- prompt grounding
- generation
- citation
- evaluation

## Exercise 4 — Create a trace log

For three questions, write the log fields you would store in production.

## Exercise 5 — Add an execution pipeline step

Add one step that a real production system would need, such as cache lookup,
access check, reranking, safety check, or human escalation.

## Exercise 6 — Write refusal behavior

Write a refusal for a case where the right source is not retrieved.

## Exercise 7 — Add a golden test case

Create one golden question with expected source, expected answer behavior, and
metric.

## Exercise 8 — Explain the lifecycle to a teammate

Write a short explanation that a frontend engineer, PM, or QA engineer could use
to understand the flow.

## Checking your work

```bash
python3 starter.py
python3 solution.py
```
