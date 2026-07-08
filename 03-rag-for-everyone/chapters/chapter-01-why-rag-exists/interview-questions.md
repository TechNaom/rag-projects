# Chapter 1 Interview Questions

Use these questions like a conversation with a senior engineer. Do not memorize
the wording. Practice explaining the problem, the mental model, the production
risk, and the trade-off.

## Concept Foundations

### 1. What problem does RAG solve?

Strong answer: RAG lets an AI system answer from trusted external context
instead of relying only on model memory. It is especially useful for private,
current, or domain-specific knowledge where citation and traceability matter.

Red flag: "RAG just makes the model smarter."

Follow-up: When would long context be enough, and when would retrieval still be
better?

What this proves: You understand RAG as a system design pattern, not a magic
accuracy button.

### 2. Why is model memory not enough for company policy questions?

Strong answer: Model memory may be outdated, generic, or trained without the
company's private documents. A policy assistant needs the approved source, the
right version, and often the user's region or role.

Red flag: "A stronger model should know it."

Follow-up: What would you do if two policy versions are retrieved?

What this proves: You can separate general knowledge from governed business
knowledge.

### 3. What is the simplest mental model for RAG?

Strong answer: A RAG system is like asking a librarian to bring the right pages
before asking a writer to draft the answer. Retrieval finds evidence; generation
explains it.

Red flag: "RAG is a vector database."

Follow-up: Which part fails if the system brings the wrong pages?

What this proves: You can explain the architecture without hiding behind tools.

### 4. When should a system use web search instead of RAG?

Strong answer: Use web search for public, current information such as today's
weather, live sports, or recent news. Use RAG when the trusted source is a
private or curated corpus.

Red flag: "RAG and search are the same thing."

Follow-up: Could a product use both web search and RAG?

What this proves: You understand source boundaries.

## Production Judgment

### 5. Why are citations important in policy assistants?

Strong answer: Citations let users and reviewers verify that the answer came
from the approved policy source. They also support auditing, debugging, and
compliance review.

Red flag: "The model is usually right, so citations are optional."

Follow-up: What should the assistant do if the retrieved context does not
contain the answer?

What this proves: You understand trust, auditability, and user confidence.

### 6. What should a RAG assistant do when context is missing?

Strong answer: It should say the answer is not available from the retrieved
sources, ask for missing details if useful, or escalate to a human owner. It
should not invent a policy answer.

Red flag: "It should answer from common sense."

Follow-up: How would you make this behavior testable?

What this proves: You know that refusal behavior is a product feature.

### 7. Why can a good prompt still produce a bad RAG answer?

Strong answer: If retrieval fails, the prompt may receive irrelevant or missing
context. The generation step can only be as grounded as the evidence it sees.

Red flag: "Just tell the model not to hallucinate."

Follow-up: Which metrics would you use to evaluate retrieval?

What this proves: You know prompt quality cannot compensate for weak evidence.

### 8. What metadata matters in a production RAG system?

Strong answer: Metadata depends on the domain, but common fields include source,
version, region, department, user role, effective date, confidentiality level,
and approval owner.

Red flag: "Embeddings are enough."

Follow-up: Give one example where metadata filtering prevents a wrong answer.

What this proves: You understand retrieval as governed data access, not just
semantic similarity.

### 9. How would you handle access control in RAG?

Strong answer: Retrieval should only return documents the user is allowed to
see. Access checks should happen before or during retrieval, and sensitive
citations should not leak hidden content.

Red flag: "Retrieve everything, then ask the model not to reveal secrets."

Follow-up: Where would you enforce permissions: ingestion, retrieval, generation,
or all three?

What this proves: You can reason about security boundaries.

### 10. How do you explain RAG to a product manager?

Strong answer: RAG helps the assistant answer from approved knowledge instead of
guessing. It lets the product cite sources, stay current when documents change,
and refuse safely when evidence is missing.

Red flag: "It is an AI technique that improves embeddings."

Follow-up: What product metric would show RAG is working?

What this proves: You can translate engineering value into product value.

## Evaluation and Failure Modes

### 11. What is a golden question set?

Strong answer: A golden question set is a small, trusted set of test questions
with expected sources and expected behavior. It helps teams catch regressions in
retrieval and answer quality.

Red flag: "Ask a few random questions and see if they sound right."

Follow-up: What should be included besides the question text?

What this proves: You understand repeatable evaluation.

### 12. What is the first thing you inspect when a RAG answer is wrong?

Strong answer: Inspect the retrieved context first. If the right source was not
retrieved, fix retrieval. If the right source was retrieved but the answer was
wrong, inspect prompting, grounding, or answer formatting.

Red flag: "Tune the prompt first."

Follow-up: How would you debug wrong-document retrieval?

What this proves: You can debug the pipeline in order.

### 13. What does Recall@k tell you in RAG?

Strong answer: Recall@k tells whether the correct source appears within the top
k retrieved results. It is useful because generation cannot cite or use evidence
that retrieval never provides.

Red flag: "It tells whether the final answer is good."

Follow-up: Why might high Recall@k still produce a poor answer?

What this proves: You understand retrieval metrics and their limits.

### 14. What is a dangerous false positive in RAG?

Strong answer: A dangerous false positive is when the assistant gives a confident
answer from weak, wrong, or unauthorized context. In policy, legal, finance, or
healthcare workflows, that can create real-world risk.

Red flag: "A false positive is just a minor accuracy issue."

Follow-up: How would you design an eval to catch it?

What this proves: You think about risk, not only demos.

### 15. Why should refusal answers be evaluated?

Strong answer: Refusal is part of correctness. A good assistant should refuse
when evidence is missing, policy is ambiguous, or the user asks beyond its
authority.

Red flag: "Refusals reduce user experience, so avoid them."

Follow-up: What does a helpful refusal sound like?

What this proves: You understand safety as useful product behavior.

## Architecture and Trade-offs

### 16. What are the main steps in a basic RAG pipeline?

Strong answer: Ingest trusted documents, chunk them, index them, retrieve
relevant chunks for a user query, build a grounded prompt, generate an answer,
cite sources, and evaluate the result.

Red flag: "Put documents in a vector database and call the model."

Follow-up: Which step would you add first for production observability?

What this proves: You see the full system, not only the happy path.

### 17. When might RAG be the wrong choice?

Strong answer: RAG may be unnecessary for stable general knowledge, simple
classification, deterministic business rules, or workflows that require tools
and transactions rather than document-grounded answers.

Red flag: "Use RAG for every GenAI product."

Follow-up: Give an example where a normal API or rules engine is better.

What this proves: You can choose architecture instead of following hype.

### 18. What trade-off appears when you add more retrieved context?

Strong answer: More context can improve recall, but it can also add noise,
increase latency and cost, and make the model focus on irrelevant text. The goal
is enough evidence, not maximum text.

Red flag: "Always retrieve as much as possible."

Follow-up: How would you test the right top-k value?

What this proves: You understand quality, cost, and latency trade-offs.

### 19. How should a RAG system handle changing policy documents?

Strong answer: It needs versioned ingestion, document freshness checks, effective
dates, and a way to remove or deprecate old content. Evaluations should include
questions that catch stale-policy answers.

Red flag: "Re-upload documents whenever someone remembers."

Follow-up: What metadata would you store for policy versions?

What this proves: You think about lifecycle and operations.

### 20. What makes a Chapter 1 RAG project production-aware?

Strong answer: Even a simple project can include source boundaries, citations,
metadata, refusal behavior, golden evals, and a clear escalation rule. Those
habits make later engineering work stronger.

Red flag: "Production only matters after the demo works."

Follow-up: Which one production habit would you add first to a prototype?

What this proves: You understand that production thinking starts at design time.
