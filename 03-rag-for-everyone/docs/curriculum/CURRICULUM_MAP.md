# RAG for Everyone Curriculum

## Module 1: Foundation

**Outcome:** Understand why RAG exists, how a query moves through a RAG system, and how the major RAG families differ.

### Subtopics
- Why LLMs hallucinate
- Why context windows are limited
- Why RAG exists
- Different types of RAG
- Naive RAG
- Advanced RAG
- Agentic RAG
- Graph RAG
- Corrective RAG
- Adaptive RAG
- Complete lifecycle of a query

## Module 2: Documents and Data Ingestion

**Outcome:** Learn how raw enterprise data becomes clean, structured, retrievable knowledge with metadata and repeatable ingestion jobs.

### Subtopics
- PDFs
- DOCX
- HTML
- Markdown
- JSON
- APIs
- Databases
- Incremental ingestion
- Metadata
- Data cleaning
- OCR
- Parsing
- Unstructured vs structured data
- Why preprocessing matters
- What production pipelines look like

## Module 3: Chunking Deep Dive

**Outcome:** Choose chunking strategies based on accuracy, latency, memory, and the shape of the source documents.

### Subtopics
- Fixed-size chunking
- Recursive chunking
- Sentence chunking
- Paragraph chunking
- Semantic chunking
- Sliding window chunking
- Parent-child chunking
- Hierarchical chunking
- Agentic chunking
- LLM-based chunking

## Module 4: Embeddings

**Outcome:** Explain vector similarity, compare embedding models, and reason about drift, dimensionality, and re-indexing.

### Subtopics
- What embeddings are
- Vector spaces
- Similarity
- Dimensionality
- Distance metrics
- Cosine similarity
- Euclidean distance
- Dot product
- Embedding models
- Domain-specific embeddings
- Fine-tuning
- Embedding drift
- Re-indexing
- Provider comparisons: OpenAI, Cohere, Google, and BAAI

## Module 5: Vector Databases

**Outcome:** Understand ANN indexing, filtering, distributed design, and practical trade-offs across popular vector databases.

### Subtopics
- ANN vs Exact Search
- HNSW
- IVF
- PQ
- OPQ
- DiskANN
- ScaNN
- Filtering
- Metadata search
- Hybrid search
- Distributed vector databases
- Sharding
- Replication
- Database comparisons: Pinecone, Weaviate, Qdrant, Milvus, and Chroma

## Module 6: Retrieval

**Outcome:** Design retrieval stacks that combine dense, sparse, metadata-aware, and query-rewriting strategies.

### Subtopics
- Similarity search
- Hybrid search
- BM25
- Sparse retrieval
- Dense retrieval
- Reciprocal Rank Fusion (RRF)
- Multi-query retrieval
- Multi-vector retrieval
- Parent-document retrieval
- Self-query retrieval
- Metadata filtering
- Context compression
- Query rewriting
- Query expansion

## Module 7: Re-ranking

**Outcome:** Explain why rerankers improve relevance and how to balance speed, cost, and accuracy.

### Subtopics
- Cross-encoders
- Bi-encoders
- Late interaction
- Why re-ranking improves quality
- Trade-offs between speed and accuracy

## Module 8: Prompt Engineering for RAG

**Outcome:** Write grounded prompts that force citation behavior, structure outputs, and reduce hallucinations.

### Subtopics
- Context injection
- System prompts
- Citation prompts
- Grounding
- Structured output
- Guardrails
- Hallucination prevention

## Module 9: Evaluation

**Outcome:** Measure retrieval quality, answer faithfulness, latency, and cost using practical metrics and frameworks.

### Subtopics
- Recall@K
- Precision@K
- MRR
- NDCG
- Faithfulness
- Context Precision
- Answer Relevancy
- Groundedness
- Latency
- Cost
- Evaluation frameworks: Ragas and DeepEval

## Module 10: Production RAG

**Outcome:** Reason about reliability, observability, security, and cost control in a real production deployment.

### Subtopics
- Caching
- Streaming
- Observability
- Logging
- Versioning
- Security
- Authentication
- Rate limiting
- Cost optimization
- Monitoring
- CI/CD
- Failure handling

## Module 11: Advanced RAG

**Outcome:** Compare advanced RAG patterns and explain when added complexity is actually justified.

### Subtopics
- Agentic RAG
- Graph RAG
- Knowledge Graph RAG
- Multi-modal RAG
- SQL RAG
- Code RAG
- Long-context RAG
- Recursive retrieval
- Adaptive retrieval
- Multi-agent RAG

## Module 12: Hands-on Projects

**Outcome:** Turn the earlier modules into a portfolio of RAG builds you can explain, defend, and iterate on publicly.

### Subtopics
- Basic RAG
- Production-ready RAG
- Hybrid Search RAG
- Parent-Child RAG
- Multi-query RAG
- Agentic RAG
- Graph RAG
- Enterprise RAG
- Architecture diagrams
- Python implementation
- Performance discussion
- Interview questions
- Design trade-offs
