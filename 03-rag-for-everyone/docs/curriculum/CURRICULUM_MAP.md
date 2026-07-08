# RAG for Everyone Curriculum Map

This roadmap mirrors the `python-for-everyone` teaching model: chapters grouped
into modules, each chapter ending with exercises, practice, interview prep, and
a project increment.

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
- Retrieval query.
- Chunks and metadata.
- Context block.
- Prompt.
- Generated answer with citations.
- Evaluation loop.

### Chapter 3: Types of RAG

- Naive RAG.
- Advanced RAG.
- Agentic RAG.
- Graph RAG.
- Corrective and adaptive RAG.
- How to choose the simplest useful architecture.

### Chapter 4: Reading a RAG Architecture Diagram

- Components.
- Data flow.
- Failure points.
- Latency and cost paths.
- What changes from prototype to production.

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
- Overlapping noise.
- Tiny chunks.
- Giant chunks.
- Training-policy miss from the current eval set.

## Module 4: Embeddings and Similarity

Goal: Explain vector search clearly enough to debug it.

### Chapter 12: What Embeddings Are

- Text to vectors.
- Similarity.
- Dense vs sparse intuition.
- Cosine similarity.

### Chapter 13: Local TF-IDF + SVD Embeddings

- Why the current project uses a local embedding method.
- What lexical retrieval is good at.
- What it misses.
- Why this is honest engineering under constraints.

### Chapter 14: Neural Embeddings

- Sentence-transformers.
- OpenAI embeddings.
- Voyage and other providers.
- Model choice trade-offs.
- Re-indexing when embeddings change.

## Module 5: Vector Stores and Retrieval

Goal: Build retrieval systems that can be reasoned about and improved.

### Chapter 15: Vector Stores

- ChromaDB.
- Collections.
- Persistence.
- IDs, documents, metadata, embeddings.

### Chapter 16: Top-K Retrieval

- Similarity search.
- Ranking.
- Scores.
- How `k` changes answer quality.

### Chapter 17: Hybrid Search

- BM25.
- Dense retrieval.
- Sparse retrieval.
- Reciprocal Rank Fusion.

### Chapter 18: Reranking

- Retrieve many, return few.
- Cross-encoder rerankers.
- Cost and latency trade-offs.
- When reranking fixes real misses.

## Module 6: Prompting for RAG

Goal: Make prompts grounded, testable, and resistant to unsupported answers.

### Chapter 19: Context Injection

- Formatting retrieved chunks.
- Source labels.
- Ordering.
- Context windows.

### Chapter 20: Grounded System Prompts

- Answer only from context.
- Cite sources.
- Refuse when context is insufficient.
- Keep answers concise and precise.

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

### Chapter 28: Capstone Portfolio Project

- Choose a domain.
- Build the corpus.
- Design metadata.
- Implement retrieval.
- Test prompts.
- Run evals.
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
