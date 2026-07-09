# GenAI Thought Process Journal: Metadata Design

## Builder Reflection

Before trusting retrieval, I will ask:

1. Does the chunk know where it came from?
2. Does it know who can see it?
3. Does it know whether it is approved, draft, historical, or retired?
4. Does it know which version and date it belongs to?
5. Does it know how to cite itself?
6. Does it follow the current metadata schema?

## Prompt Testing Habit

Test near-identical questions that differ only by role, region, product version, or date. Good metadata should make those answers behave differently when the business rules require it.

## Production Mindset

Metadata turns RAG from "find similar text" into "find the right evidence for this user, this context, and this moment."
