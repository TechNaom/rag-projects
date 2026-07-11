# RAG for Everyone Curriculum Map

This roadmap mirrors the `python-for-everyone` teaching model: chapters grouped
into modules, each chapter ending with exercises, practice, interview prep, and
a project increment.

RAG for Everyone Live UI: <https://technaom.github.io/rag-projects/rag-for-everyone/>

Each chapter also includes a GenAI thought-process journal. Learners practice
how to frame problems, write prompts, test assumptions, critique model answers,
turn failures into eval cases, and document engineering decisions.

## Module 1: RAG Foundations

Goal: Build a clear mental model of why RAG exists and how a query moves through
the system.

### Chapter 1: Why RAG Exists

- Hallucinations and missing knowledge.
- Knowledge cutoff vs private knowledge.
- Why long context alone is not enough.
- When RAG is the right pattern.
- Project link: Northkeep policy assistant overview.

### Chapter 2: The RAG Query Lifecycle

- User question.
- Intent classification.
- Retrieval query.
- Metadata filters.
- Retrieval strategy.
- Reranking.
- Context assembly.
- Grounded prompt.
- Generated answer, refusal, or escalation.
- Citations, trace logs, and evaluation loop.

### Chapter 3: Types of RAG

- Naive RAG.
- Advanced RAG.
- Agentic RAG.
- Graph RAG.
- Corrective and adaptive RAG.
- How to choose the simplest useful architecture.

### Chapter 4: RAG Execution Pipelines

- Runtime pipeline stages.
- Access checks.
- Cache lookup.
- Query rewriting.
- Retrieval and reranking.
- Safety checks.
- Sync vs async execution.
- Latency, cost, and failure paths.

### Module 1 Exam

Written exam plus architecture explanation: learners explain the Northkeep
assistant from source document to grounded answer.

## Module 2: Documents and Ingestion

Goal: Turn raw source material into clean, traceable knowledge units.

### Chapter 5: Source Documents

- Markdown, PDF, HTML, DOCX, CSV, JSON, APIs, databases.
- Structured vs unstructured data.
- Domain-specific corpora.
- Why synthetic data is useful for public learning projects.

### Chapter 6: Parsing and Cleaning

- Extracting text.
- Removing noise.
- Preserving headings and hierarchy.
- Normalizing content.
- Keeping source traceability.

### Chapter 7: Metadata Design

- Source file.
- Section.
- Policy ID.
- Role and access metadata.
- Version and timestamp.
- Why metadata controls production behavior.

### Chapter 8: Ingestion Pipelines

- Batch ingestion.
- Incremental updates.
- Re-indexing.
- Pipeline logs.
- Failure recovery.

## Module 3: Chunking

Goal: Understand how chunk boundaries affect retrieval quality.

### Chapter 9: Fixed and Recursive Chunking

- Token size.
- Overlap.
- Separators.
- Chunk count vs context size.

### Chapter 10: Semantic and Hierarchical Chunking

- Topic-aware boundaries.
- Parent-child retrieval.
- Section-aware chunks.
- When simple chunking is enough.

### Chapter 11: Chunking Failure Analysis

- Lost context.
- Overlap noise.
- Tiny chunks.
- Giant chunks.
- Mixed-topic chunks.
- Stale chunks and old-policy wins.
- Trace inspection and gold evidence comparison.
- Failure labels, controlled fixes, eval gates, and rollback.

## Module 4: Embeddings and Similarity

Goal: Explain vector search clearly enough to debug it.

### Chapter 12: What Embeddings Are

- Text to vectors.
- Similarity.
- Dense vs sparse intuition.
- Cosine similarity.
- Embeddings as candidate retrieval, not proof of truth.
- Model consistency, dimensions, privacy, latency, cost, and drift.
- Re-indexing and embedding versioning.
- Retrieval evals such as Recall@K and gold chunk rank.

### Chapter 13: Local TF-IDF + SVD Embeddings

- Why the current project uses a local embedding method.
- What lexical retrieval is good at.
- What it misses.
- Why this is honest engineering under constraints.
- TF-IDF term weighting and inverse document frequency.
- SVD/latent-topic compression.
- Tokenizer, vocabulary, IDF, projection, and index versioning.
- Local retrieval as baseline, fallback, exact-term engine, or hybrid partner.

### Chapter 14: Neural Embeddings

- Sentence-transformers.
- OpenAI embeddings.
- Voyage and other providers.
- Model choice trade-offs.
- Re-indexing when embeddings change.
- Corpus-specific golden-query evals.
- Dimensions, vector-store compatibility, and model versioning.
- Privacy, latency, rate limits, cost, and fallback planning.
- Hybrid retrieval for semantic plus exact-term needs.

## Module 5: Vector Stores and Retrieval

Goal: Build retrieval systems that can be reasoned about and improved.

### Chapter 15: Vector Stores and Indexing Strategies

- ChromaDB.
- Collections.
- Persistence.
- IDs, documents, metadata, embeddings.
- Flat indexes vs approximate indexes.
- Refresh, rebuild, and versioning strategies.
- How indexing decisions affect retrieval quality.
- Metadata filters for tenant, access, freshness, and source status.
- Blue-green index releases, shadow testing, canary rollout, and rollback.
- Deletes, stale-content audits, dimension checks, and retrieval traces.

### Chapter 16: Retrieval Strategies and Top-K

- Similarity search.
- Ranking.
- Scores.
- How `k` changes answer quality.
- Query rewriting.
- Metadata filtering.
- Multi-query retrieval.
- Score calibration and thresholds.
- Dedupe, parent expansion, reranking, and context budget control.
- Retrieval traces with filters, ranks, selected chunks, and gold evidence.
- Dynamic top-k by intent, risk, and evaluation metrics.

### Chapter 17: Hybrid Search and Query Routing

- BM25.
- Dense retrieval.
- Sparse retrieval.
- Reciprocal Rank Fusion.
- Routing by intent, domain, and risk.
- When to combine search strategies.
- Exact-term protection for IDs, SKUs, clauses, and error codes.
- Route traces with route reason, retrievers used, fusion method, and selected chunks.
- Route-specific evals for paraphrase, exact-term, domain, and high-risk queries.

### Chapter 18: Reranking and Retrieval Optimization

- Retrieve many, return few.
- Cross-encoder rerankers.
- Cost and latency trade-offs.
- When reranking fixes real misses.
- Retrieval eval loops.
- Production tuning playbooks.
- Candidate-k vs final-k decisions.
- Before-rerank and after-rerank metrics.
- Dedupe, diversity, timeout fallback, and rollout strategy.

## Module 6: Prompting for RAG

Goal: Make prompts grounded, testable, and resistant to unsupported answers.

### Chapter 19: Context Injection

- How retrieved chunks become a structured context pack.
- Evidence ordering by relevance, authority, freshness, and diversity.
- Prompt boundaries that treat documents as data, not instructions.
- Compression without losing conditions, exceptions, dates, or thresholds.
- Citation ids, dropped-context reasons, and traceable audit logs.
- Token budget decisions, conflict handling, and context-injection evals.

### Chapter 20: Grounded System Prompts

- Evidence-only source-of-truth rules.
- Claim-level citation discipline.
- Refusal behavior for missing, conflicting, restricted, or out-of-scope evidence.
- Conflict handling using authority and freshness metadata.
- Prompt templates with style, scope, and output contracts.
- Prompt versioning, traces, regression tests, and rollout controls.

### Chapter 21: Prompt Testing

- Golden questions.
- Bad prompts vs good prompts.
- Citation behavior.
- Refusal behavior.
- Regression tests for prompts.

## Module 7: Evaluation

Goal: Measure the system instead of demoing it by vibes.

### Chapter 22: Retrieval Metrics

- Recall@K.
- MRR.
- Precision@K.
- NDCG.
- Reading eval output.

### Chapter 23: Answer Quality Metrics

- Faithfulness.
- Groundedness.
- Answer relevancy.
- Citation correctness.
- Human review.

### Chapter 24: Failure Analysis

- False positives.
- Missing documents.
- Ambiguous questions.
- Corpus gaps.
- What to fix first.

## Module 8: Production RAG

Goal: Move from working demo to responsible system design.

### Chapter 25: Access Control and Safety

- Role-based retrieval.
- Metadata filters.
- Audit logs.
- Sensitive data handling.

### Chapter 26: Observability and Cost

- Latency.
- Token usage.
- Provider cost.
- Query logs.
- Caching.

### Chapter 27: Deployment Patterns

- Static course.
- Local CLI.
- FastAPI wrapper.
- Hosted frontend.
- Vector DB choices.

### Chapter 28: End-to-End Production RAG Capstone

- Choose a domain.
- Build the corpus.
- Design metadata.
- Implement indexing.
- Implement retrieval.
- Add execution pipeline.
- Add citations and refusal behavior.
- Test prompts.
- Run evals.
- Add observability.
- Package the project for public review.
- Explain production trade-offs.

## Content Tracks

Each chapter can also produce:

- LinkedIn post.
- Carousel.
- Newsletter.
- YouTube script.
- Interview question set.
- Architecture diagram.
- Cheat sheet.
- Workshop plan.
- GenAI thought-process journal.
- Prompt-testing notes.
- Failure-analysis post.

This keeps the RAG project and the RAG content system growing together.
