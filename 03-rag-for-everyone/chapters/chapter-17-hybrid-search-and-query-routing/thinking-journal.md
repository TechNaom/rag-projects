# GenAI Thought Process Journal: Hybrid Search and Query Routing

## Builder Reflection

Hybrid search is not a badge. It is a decision.

Ask:

- Does this query need meaning, exact terms, or both?
- Is the domain high risk?
- Will hybrid improve evidence quality enough to justify latency?
- Are dense and sparse scores being fused safely?
- Did dedupe remove repeated chunks after fusion?
- Can we explain the route in a trace?

## Prompt Testing Habit

```text
Given a query, route decision, dense results, sparse results, fusion method,
selected chunks, and expected gold evidence, review hybrid retrieval quality.

Return:
1. whether the route was correct
2. whether dense or sparse missed important evidence
3. whether fusion was safe
4. whether duplicates were handled
5. what metric should be monitored
6. one route improvement
```

## Mentor Reminder

The mature move is not always "use more retrieval." It is "use the right retrieval for this question."
