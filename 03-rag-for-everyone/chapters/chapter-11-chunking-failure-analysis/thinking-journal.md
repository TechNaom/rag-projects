# GenAI Thought Process Journal: Chunking Failure Analysis

## Builder Reflection

When a RAG answer fails, the easiest story is "the model made a mistake." The better engineering story is more specific:

- What evidence did retrieval provide?
- Was the evidence complete?
- Was the evidence current?
- Did the answer cite the right source?
- Did context assembly include noise or conflict?
- What is the smallest fix we can test?

## Prompt Testing Habit

Use this prompt after a bad answer:

```text
You are reviewing a RAG failure. Given the user question, retrieved chunks,
citations, final answer, and gold evidence, classify the failure as one of:
lost_context, mixed_topic, overlap_noise, tiny_chunk, giant_chunk,
stale_chunk, retrieval_ranking, filter_error, or prompt_usage.

Return:
1. failure label
2. evidence from the trace
3. likely root cause
4. one controlled fix
5. metric to prove improvement
6. rollback risk
```

## Mentor Reminder

Great GenAI builders do not only generate answers. They build systems that can explain why an answer happened.
