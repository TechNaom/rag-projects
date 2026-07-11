# Project: Context Pack Builder

Build a small prompt-pack component that behaves like a real RAG service boundary.

The builder should:

- Reject inaccessible or stale evidence.
- Order by authority and relevance.
- Fit evidence within a token budget.
- Render clear prompt sections.
- Include citation ids.
- Report dropped evidence for auditability.
