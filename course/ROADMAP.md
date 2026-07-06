# RAG Masterclass — Complete Roadmap

## Module 1 — Foundation

### Topic 1.1: Why RAG Exists
- **Concepts**: LLM limitations, hallucinations, knowledge cutoff, long-tail facts
- **Why it matters**: Understand the problem RAG solves
- **Real example**: ChatGPT making up facts vs. RAG with sources
- **Content**: Master chapter, YouTube script, notebook, interview Qs

### Topic 1.2: Why LLMs Hallucinate
- **Concepts**: Prediction vs. knowledge, token probability, memorization vs. reasoning
- **Why it matters**: Design better prompts and retrieval strategies
- **Real example**: Why Claude can't remember your birthday but can reason about it
- **Content**: Master chapter, speaker notes, blog post, flashcards

### Topic 1.3: Context Windows & Their Limits
- **Concepts**: Attention, token counting, compression, what fits?
- **Why it matters**: Design retrieval to fit context limits
- **Real example**: GPT-4 Turbo (128K) vs. Claude 3 (200K) vs. open models
- **Content**: Comparison matrices, YouTube script, cheat sheet

### Topic 1.4: Types of RAG
- **Concepts**: Naive RAG, Advanced RAG, Agentic RAG, Graph RAG, Corrective, Adaptive
- **Why it matters**: Choose the right architecture for your problem
- **Real example**: When to use each type (examples from industry)
- **Content**: Architecture diagrams, comparison table, interview questions

### Topic 1.5: The Complete Lifecycle of a Query
- **Concepts**: Ingestion → Retrieval → Reranking → Prompt → Generation → Evaluation
- **Why it matters**: See how all pieces fit together
- **Real example**: A real query flowing through a complete system
- **Content**: Flowchart, workshop guide, lab walkthrough

**Module 1 Project**: Build a naive RAG system over a synthetic dataset  
**Module 1 Exam**: Written assessment covering all 5 topics

---

## Module 2 — Documents & Data Ingestion

### Topic 2.1: Unstructured Data Sources
- PDFs, DOCX, HTML, Markdown, JSON, plain text
- Parsing strategies and gotchas
- Real example: Extracting from 10K financial reports

### Topic 2.2: Structured Data & APIs
- Databases (SQL, NoSQL), real-time APIs
- Incremental ingestion strategies
- Real example: Building a RAG over Salesforce CRM data

### Topic 2.3: Data Preprocessing
- Cleaning, normalization, validation
- OCR and scanned documents
- Metadata extraction
- Real example: Cleaning messy customer support tickets

### Topic 2.4: Production Data Pipelines
- Incremental updates without reindexing
- Versioning and rollback
- Monitoring data quality
- Real example: Enterprise data lake to RAG pipeline

### Topic 2.5: Privacy & Compliance
- PII detection and redaction
- Data retention policies
- GDPR/HIPAA compliance
- Real example: Healthcare RAG with patient privacy

**Module 2 Project**: Build an ingestion pipeline for 3+ data sources  
**Module 2 Exam**: Written assessment

---

## Module 3 — Chunking (Deep Dive)

### Topic 3.1: Fixed-Size Chunking
- Token-based and character-based
- Overlap strategies
- Real example: Chunking a 500-page manual

### Topic 3.2: Recursive & Hierarchical Chunking
- Splitting on logical boundaries
- Building chunk trees
- Real example: Code documentation chunks

### Topic 3.3: Semantic Chunking
- Using embeddings to find natural breaks
- Similarity-based splitting
- Real example: Chunking research papers

### Topic 3.4: Advanced Chunking
- Parent-child relationships
- Agentic chunking (LLM-based)
- Dynamic chunking based on query
- Real example: Multi-level product manuals

### Topic 3.5: Chunking Trade-Offs
- Speed vs. quality
- Chunk size impact on retrieval
- Interview question: How to choose chunk size?
- Real example: Comparing strategies on real data

**Module 3 Project**: Implement multiple chunking strategies and compare  
**Module 3 Exam**: Written assessment

---

## Module 4 — Embeddings

### Topic 4.1: What Are Embeddings?
- Vectors and semantic space
- Similarity metrics (cosine, Euclidean, dot product)
- Real example: "King - Man + Woman" visualized

### Topic 4.2: Embedding Models
- OpenAI, Cohere, Google, open source (Sentence Transformers)
- Dimensionality and performance trade-offs
- Real example: Comparing models on your data

### Topic 4.3: Domain-Specific Embeddings
- Fine-tuning on custom data
- When to fine-tune vs. use pre-trained
- Real example: Medical embeddings for healthcare RAG

### Topic 4.4: Embedding Drift & Re-indexing
- When embeddings change
- Detecting drift
- Re-indexing strategies
- Real example: Upgrading to a new embedding model

### Topic 4.5: Embeddings in Production
- Caching embeddings
- Batch processing
- Monitoring embedding quality
- Real example: Scaling embeddings to millions of chunks

**Module 4 Project**: Fine-tune embeddings on your domain data  
**Module 4 Exam**: Written assessment

---

## Module 5 — Vector Databases

### Topic 5.1: Approximate Nearest Neighbor Search
- HNSW, IVF, PQ algorithms
- Speed vs. accuracy trade-offs
- Real example: Why HNSW beats brute force

### Topic 5.2: Vector Database Comparison
- Pinecone, Weaviate, Qdrant, Milvus, Chroma
- Feature matrix (filtering, replication, cost)
- Real example: Choosing for your use case

### Topic 5.3: Filtering & Metadata Search
- Pre-filtering vs. post-filtering
- Hybrid search (dense + sparse)
- Real example: "Find relevant documents about ML from 2023"

### Topic 5.4: Scaling Vector Databases
- Sharding, replication, backup
- Multi-tenancy
- Real example: Scaling to billions of vectors

### Topic 5.5: Vector DB in Your Stack
- Self-hosted vs. managed
- Cost analysis
- Monitoring and alerting
- Real example: Building a production deployment

**Module 5 Project**: Set up and optimize a vector database  
**Module 5 Exam**: Written assessment

---

## Module 6 — Retrieval Strategies

### Topic 6.1: Basic Similarity Search
- Dense retrieval (vectors)
- K-nearest neighbors
- Real example: "Find chapters about authentication"

### Topic 6.2: Hybrid & Sparse Retrieval
- BM25 keyword search
- Combining dense + sparse (RRF, linear combination)
- Real example: When pure semantic search fails

### Topic 6.3: Multi-Query & Self-Query Retrieval
- Query expansion (asking multiple variations)
- LLM-based query rewriting
- Real example: "Show me everything related to..."

### Topic 6.4: Context Compression & Reranking
- LLMChain for compression
- Cross-encoders for reranking
- Real example: Top-K=50 down to K=3

### Topic 6.5: Advanced Retrieval
- Multi-vector retrieval (different granularities)
- Parent-document retrieval (retrieve parent, return children)
- Adaptive retrieval (dynamic K based on query complexity)
- Real example: Enterprise knowledge base retrieval

**Module 6 Project**: Implement multi-stage retrieval pipeline  
**Module 6 Exam**: Written assessment

---

## Module 7 — Re-ranking

### Topic 7.1: What Is Re-ranking?
- Why retrieve more than you need
- Bi-encoders vs. cross-encoders
- Real example: Top-K=100 reranked to K=5

### Topic 7.2: Cross-Encoder Models
- How they work
- Models from BAAI, Cohere, others
- Real example: Comparing cross-encoder accuracy

### Topic 7.3: Late Interaction & Dense Passage Retrieval
- ColBERT and friends
- When to use
- Real example: Speed vs. quality benchmarks

### Topic 7.4: Re-ranking Trade-Offs
- Latency impact
- Cost (inference)
- Accuracy gains
- Real example: Is 5% better quality worth 2x latency?

### Topic 7.5: Building a Re-ranking Pipeline
- Retrieval → Re-rank → Generation
- Multi-stage ranking
- Real example: Production deployment with monitoring

**Module 7 Project**: A/B test reranking strategies  
**Module 7 Exam**: Written assessment

---

## Module 8 — Prompt Engineering for RAG

### Topic 8.1: Context Injection Strategies
- How to feed retrieved docs to the LLM
- Document formatting
- Real example: Formatting legal documents for analysis

### Topic 8.2: System Prompts & Instructions
- Setting LLM behavior
- Citation and grounding
- Real example: "Always cite your sources"

### Topic 8.3: Preventing Hallucinations
- Explicit guardrails
- Confidence scoring
- Refusing out-of-context questions
- Real example: "I don't know" detection

### Topic 8.4: Structured Output
- JSON, XML formatting
- Schema enforcement
- Real example: RAG that returns structured data

### Topic 8.5: Advanced Prompting Techniques
- Chain-of-thought prompting
- Few-shot examples
- Persona-based prompting
- Real example: Expert systems via prompting

**Module 8 Project**: Build a RAG with structured output and citations  
**Module 8 Exam**: Written assessment

---

## Module 9 — Evaluation

### Topic 9.1: Retrieval Metrics
- Recall@K, Precision@K, MRR, NDCG
- When to use each
- Real example: Evaluating search quality

### Topic 9.2: Generation Metrics
- Faithfulness (does answer match context?)
- Answer relevancy
- Context precision / recall
- Real example: Comparing LLMs on your data

### Topic 9.3: End-to-End Evaluation Frameworks
- Ragas (RAG evaluation)
- DeepEval
- Custom evaluation pipelines
- Real example: Building an eval suite

### Topic 9.4: A/B Testing RAG Systems
- Designing experiments
- Statistical significance
- Real example: Testing retrieval vs. generation changes

### Topic 9.5: Latency & Cost Metrics
- Measuring end-to-end latency
- Cost per query
- SLA tracking
- Real example: Monitoring production RAG

**Module 9 Project**: Build a complete evaluation pipeline  
**Module 9 Exam**: Written assessment

---

## Module 10 — Production RAG

### Topic 10.1: Caching & Optimization
- Query caching
- Embedding caching
- LLM response caching
- Real example: 50% latency reduction via caching

### Topic 10.2: Streaming & Real-Time Updates
- Streaming generation to user
- Real-time index updates
- Real example: Live knowledge base sync

### Topic 10.3: Monitoring & Observability
- Metrics and alerts
- Logging retrieval & generation
- Debugging failed queries
- Real example: Production dashboard

### Topic 10.4: Security & Authentication
- API authentication
- Document-level access control
- Data privacy
- Real example: Multi-tenant RAG

### Topic 10.5: CI/CD & Deployment
- Testing RAG systems
- Canary deployments
- Rollback strategies
- Real example: Safe deployment of new embeddings

**Module 10 Project**: Deploy a production RAG system  
**Module 10 Exam**: Written assessment

---

## Module 11 — Advanced RAG

### Topic 11.1: Agentic RAG
- ReAct framework (Reasoning + Acting)
- Tool use for RAG agents
- Real example: "Search, analyze, decide" loop

### Topic 11.2: Graph RAG
- Knowledge graph construction
- Graph traversal for retrieval
- Real example: Entity relationships in customer data

### Topic 11.3: Multi-Modal RAG
- Images, video, audio as context
- Combining modalities
- Real example: Retrieval from scanned documents with charts

### Topic 11.4: SQL RAG & Code RAG
- Querying databases as retrieval
- Code generation with RAG
- Real example: "Query the database" vs. "retrieve docs"

### Topic 11.5: Long-Context & Recursive Retrieval
- Using 100K+ context windows
- Recursive retrieval (retrieve → augment query → retrieve more)
- Real example: Full document analysis with long context

**Module 11 Project**: Build an advanced RAG (agentic or graph)  
**Module 11 Exam**: Written assessment

---

## Module 12 — Capstone Projects

### Project 1: Customer Support RAG
- Ingest support tickets, docs, FAQs
- Retrieve similar issues
- Generate responses with citations

### Project 2: Research Paper Analyzer
- Ingest 100+ papers
- Query for specific findings
- Generate summaries and comparisons

### Project 3: Enterprise Knowledge Base
- Multi-source data ingestion
- Complex retrieval (metadata filtering, hybrid search)
- Production deployment with monitoring

### Project 4: Real-Time Financial RAG
- Live market data + historical docs
- Query for insights
- Structured output for trading systems

### Project 5: Healthcare RAG (HIPAA-compliant)
- Patient data access control
- Clinical decision support
- Audit logging

**Module 12 Capstone**: Choose and build one capstone, deploy to production
**Module 12 Final Exam**: Comprehensive assessment

---

## Learning Outcomes

After completing all 12 modules, you will:

✅ Understand every layer of RAG systems  
✅ Know trade-offs at each stage (speed, accuracy, cost)  
✅ Build production-ready RAG systems  
✅ Evaluate and optimize RAG pipelines  
✅ Answer RAG system design interview questions  
✅ Choose the right architecture for your problem  
✅ Deploy and monitor RAG in production  
✅ Build advanced RAG (agentic, graph, multi-modal)  
✅ Create content about RAG (YouTube, blogs, talks)  

---

## Time Estimate

- **Per module**: 40-50 hours (reading, coding, projects)
- **Complete course**: 500+ hours
- **Intensive (full-time)**: 3-4 months
- **Part-time (10h/week)**: 1-1.5 years

---

## Next Steps

1. Start with [Module 1 — Foundation](course/module-01-foundation/)
2. Follow the learning path that fits your style (foundations-first, hands-on-first, or system-design-focus)
3. Build projects as you go
4. Share your work, discuss trade-offs
5. Contribute content back to the course

---

**Let's build the future of RAG systems together.** 🚀
