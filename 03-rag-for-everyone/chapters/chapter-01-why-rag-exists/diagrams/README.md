# Chapter 1 Diagrams

This folder gives the same idea in three visual formats:

- `architecture.txt`: plain-text version for Markdown, terminal reading, and
  quick explanation.
- `architecture.mmd`: Mermaid source for maintainers who want rendered diagrams.
- `architecture.svg`: learner-facing image used in `lesson.html`.

## Teaching Goal

Learners should see that RAG is not "ask the model and hope." It is a system:

1. Prepare trusted documents.
2. Chunk and embed them.
3. Store them in a vector database.
4. Retrieve relevant chunks for a user question.
5. Build a grounded prompt.
6. Generate a cited answer.
7. Evaluate what worked and what failed.

## Facilitator Note

When teaching this chapter, ask learners to point at the diagram and answer:

- Where does evidence enter the system?
- Where can retrieval fail?
- Where do prompt rules matter?
- Where do evaluation metrics tell us what to improve?

