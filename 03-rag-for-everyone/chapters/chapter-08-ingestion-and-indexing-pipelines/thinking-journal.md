# GenAI Thought Process Journal: Ingestion and Indexing Pipelines

## Builder Reflection

Before publishing a RAG index, I will ask:

1. Which run produced this index?
2. Which sources changed?
3. Which records failed?
4. Did metadata, access, freshness, and golden query gates pass?
5. What index can we roll back to?
6. What will we monitor after publish?

## Prompt Testing Habit

When an answer fails, ask:

> Which index version was searched, and what ingestion run created it?

## Production Mindset

RAG quality is not only a prompt problem. It is also a release pipeline problem. If the knowledge release is weak, the assistant inherits that weakness.
