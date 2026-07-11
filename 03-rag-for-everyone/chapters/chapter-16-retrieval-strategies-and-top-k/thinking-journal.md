# GenAI Thought Process Journal: Retrieval Strategies and Top-K

## Builder Reflection

Retrieval is the discipline of deciding what the model is allowed to know for one answer.

Ask:

- Was the right evidence in top-k?
- Was the right evidence filtered out?
- Did top-k add useful recall or just noise?
- Did rewrite preserve intent?
- Did multi-query improve coverage enough to justify cost?
- Did context assembly keep exact citations?

## Prompt Testing Habit

```text
Given a retrieval trace with query, rewrite, filters, top-k, scores, ranks,
selected chunks, and expected gold evidence, diagnose the retrieval decision.

Return:
1. whether top-k was sufficient
2. whether filters caused a miss
3. whether rewrite changed intent
4. whether duplicates reduced context quality
5. what retrieval control to adjust
6. what metric should be monitored
```

## Mentor Reminder

The model answers from what retrieval gives it. Better retrieval is often better prompting before the prompt even begins.
