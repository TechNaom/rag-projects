# Chapter 2 Interview Questions

## Concept Foundations

### 1. What is the RAG query lifecycle?
Strong answer: It is the journey from user question to retrieved evidence,
grounded prompt, answer, citations, and evaluation.
Red flag: "It is just retrieval."
Follow-up: Which stage would you inspect first when an answer is wrong?
What this proves: You see RAG as a pipeline.

### 2. Why should retrieval be evaluated separately from generation?
Strong answer: The model cannot use evidence that retrieval fails to provide.
Red flag: "Only the final answer matters."
Follow-up: What retrieval metric would you start with?
What this proves: You can debug stages independently.

### 3. What is query understanding?
Strong answer: Interpreting intent, missing details, risk, and filters before
searching.
Red flag: "Use the exact user text every time."
Follow-up: When should the assistant ask a clarification question?
What this proves: You understand the request before search.

### 4. Why do metadata filters matter?
Strong answer: They prevent semantically similar but wrong documents from being
retrieved, such as wrong region or policy version.
Red flag: "Embeddings handle everything."
Follow-up: Give one metadata filter for a refund bot.
What this proves: You understand governed retrieval.

## Production Judgment

### 5. What should be logged in a RAG trace?
Strong answer: Request id, question, filters, retrieved source ids, scores,
prompt version, answer status, citations, refusal reason, latency, and cost.
Red flag: "Only log the final answer."
Follow-up: Which logs are sensitive?
What this proves: You think about observability.

### 6. When should a lifecycle include access checks?
Strong answer: Before or during retrieval, and again before showing citations if
sensitive sources are involved.
Red flag: "Retrieve first, hide later."
Follow-up: What can go wrong with post-generation-only access control?
What this proves: You reason about security boundaries.

### 7. How do latency and cost enter the lifecycle?
Strong answer: Query rewrite, retrieval, reranking, context size, and generation
all add latency and cost.
Red flag: "RAG cost is only the model call."
Follow-up: Which step would you optimize first?
What this proves: You understand production trade-offs.

### 8. What is context assembly?
Strong answer: Selecting, ordering, trimming, and formatting retrieved evidence
before sending it to the model.
Red flag: "Paste all chunks into the prompt."
Follow-up: How can bad ordering hurt the answer?
What this proves: You know context is designed.

### 9. What is a helpful refusal in the lifecycle?
Strong answer: A response that explains missing evidence and gives the next safe
step, rather than guessing.
Red flag: "Refuse with no explanation."
Follow-up: Write one refusal for a missing policy source.
What this proves: You see refusal as product UX.

### 10. How does reranking fit into the lifecycle?
Strong answer: It reorders retrieved candidates so the strongest evidence enters
the context window.
Red flag: "Reranking is the same as embedding."
Follow-up: What failure can reranking introduce?
What this proves: You understand retrieval strategies.

## Evaluation and Failure Modes

### 11. What is the first debug step for a wrong answer?
Strong answer: Inspect retrieved context and source ids before changing prompts.
Red flag: "Tune the prompt first."
Follow-up: What if the right source was retrieved?
What this proves: You debug in order.

### 12. How do you catch stale index issues?
Strong answer: Track document version, ingestion timestamp, freshness checks,
and evals that expect the latest approved policy.
Red flag: "Users will report it."
Follow-up: What alert would you create?
What this proves: You think operationally.

### 13. What does citation precision measure?
Strong answer: Whether cited sources actually support the answer.
Red flag: "Any citation is good."
Follow-up: How can a citation be misleading?
What this proves: You care about trust.

### 14. Why are multi-hop questions harder?
Strong answer: They require evidence from multiple sources, and missing one
source can produce an incomplete answer.
Red flag: "Top one chunk is enough."
Follow-up: How would you evaluate multi-hop retrieval?
What this proves: You understand complex enterprise queries.

### 15. What is an execution pipeline?
Strong answer: The ordered runtime path of checks and actions: auth, cache,
query rewrite, retrieval, rerank, prompt, safety, answer, logging.
Red flag: "It is just a script."
Follow-up: Which step can be asynchronous?
What this proves: You can design a shippable system.

## Architecture

### 16. Where do indexing strategies fit?
Strong answer: Before query time, during ingestion and storage, but they shape
retrieval quality during the lifecycle.
Red flag: "Indexing is unrelated to querying."
Follow-up: How does chunking affect indexing?
What this proves: You connect offline and online systems.

### 17. Where do retrieval strategies fit?
Strong answer: In the retrieval stage: vector, keyword, hybrid, filters,
reranking, and query routing.
Red flag: "There is only vector search."
Follow-up: When is hybrid search better?
What this proves: You understand retrieval options.

### 18. How would you explain the lifecycle to a PM?
Strong answer: The system gathers approved evidence before answering, cites its
sources, and refuses when it cannot prove the answer.
Red flag: "It is embeddings plus LLM."
Follow-up: What product metric matters?
What this proves: You can communicate across roles.

### 19. What makes a lifecycle production-ready?
Strong answer: Access control, versioning, evals, logging, latency/cost budgets,
fallbacks, and clear ownership.
Red flag: "It works in a notebook."
Follow-up: Which item would you add first?
What this proves: You can move from demo to product.

### 20. What should a Chapter 2 project prove?
Strong answer: That the learner can map and implement a traceable RAG request
flow end to end.
Red flag: "It only prints an answer."
Follow-up: What should the trace contain?
What this proves: You value engineering artifacts, not only output.
