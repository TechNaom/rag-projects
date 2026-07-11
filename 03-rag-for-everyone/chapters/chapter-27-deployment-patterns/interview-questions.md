# Interview Questions: Deployment Patterns

1. When is a static deployment appropriate?
2. When do you need a backend API for RAG?
3. Why should indexing be separated from online answering?
4. What controls are required for private documents?
5. What should be versioned for rollback?
6. How do canary releases reduce risk?
7. What belongs in a deployment health check?
8. How do you choose between local, hosted, and managed services?
9. What can go wrong when prompts and indexes are not released together?
10. What is the senior engineering answer?

Senior answer: choose the smallest architecture that satisfies privacy, SLO, scale, rollback, and support needs, then prove it with health checks, traces, eval gates, and a documented release path.
