/*
  Single source of truth for the RAG for Everyone chapter roster.
  Mirrors the python-for-everyone pattern: sidebar.js renders navigation from
  this file, and roadmap pages are kept in sync with it.
*/

window.RFE_MODULES = [
  {
    title: "Module 1 — RAG Foundations",
    summary: "Build the mental model: why RAG exists, how a query moves through the system, and how to read the architecture.",
    examPath: "assessments/written-exams/module-1-exam.md",
    chapters: [
      {
        id: "chapter-01",
        num: 1,
        title: "Why RAG Exists",
        path: "chapters/chapter-01-why-rag-exists/lesson.html",
        description: "Hallucinations, private knowledge, trusted context, citations, refusal behavior, and the builder mindset.",
        subtopics: [
          { id: "problem", title: "The problem RAG solves" },
          { id: "memory-vs-context", title: "Model memory vs. trusted context" },
          { id: "northkeep", title: "Northkeep policy assistant" },
          { id: "thought-process", title: "GenAI builder thought process" },
          { id: "recap", title: "Points to remember" }
        ]
      },
      {
        id: "chapter-02",
        num: 2,
        title: "The RAG Query Lifecycle",
        path: "chapters/chapter-02-rag-query-lifecycle/lesson.html",
        description: "Question understanding, retrieval query, metadata filters, context assembly, grounded prompts, citations, traces, and eval loops.",
        subtopics: [
          { id: "problem", title: "Why the lifecycle matters" },
          { id: "analogy", title: "Receptionist analogy" },
          { id: "technical", title: "Technical lifecycle" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production considerations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-03",
        num: 3,
        title: "Types of RAG",
        path: "chapters/chapter-03-types-of-rag/lesson.html",
        description: "Naive, advanced, modular, corrective, adaptive, agentic, graph, and multimodal RAG as production architecture choices.",
        subtopics: [
          { id: "problem", title: "Why types matter" },
          { id: "analogy", title: "Real-life analogy" },
          { id: "patterns", title: "Pattern map" },
          { id: "architecture", title: "Architecture view" },
          { id: "decision", title: "Decision framework" },
          { id: "production", title: "Production trade-offs" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-04",
        num: 4,
        title: "RAG Execution Pipelines",
        path: "chapters/chapter-04-rag-execution-pipelines/lesson.html",
        description: "Offline indexing, online query execution, pipeline contracts, gates, fallbacks, traces, and production operations.",
        subtopics: [
          { id: "problem", title: "Why pipelines matter" },
          { id: "analogy", title: "Kitchen analogy" },
          { id: "offline", title: "Offline indexing pipeline" },
          { id: "online", title: "Online query pipeline" },
          { id: "contracts", title: "Pipeline contracts" },
          { id: "fallbacks", title: "Fallbacks and gates" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production operations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      }
    ]
  },
  {
    title: "Module 2 — Documents and Ingestion",
    summary: "Turn messy real-world documents into governed, searchable knowledge that a RAG system can trust.",
    examPath: null,
    chapters: [
      {
        id: "chapter-05",
        num: 5,
        title: "Source Documents",
        path: "chapters/chapter-05-source-documents/lesson.html",
        description: "Markdown, PDF, HTML, DOCX, CSV, JSON, APIs, databases, structured vs unstructured sources, domain corpora, and synthetic data.",
        subtopics: [
          { id: "problem", title: "Why sources matter" },
          { id: "analogy", title: "Library analogy" },
          { id: "formats", title: "Source formats" },
          { id: "structured", title: "Structured vs unstructured" },
          { id: "domain", title: "Domain corpora" },
          { id: "synthetic", title: "Synthetic data" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-06",
        num: 6,
        title: "Parsing and Cleaning",
        path: "chapters/chapter-06-parsing-and-cleaning/lesson.html",
        description: "Format-aware parsing, cleaning without losing meaning, parser contracts, quality gates, OCR/table risks, and parser regression tests.",
        subtopics: [
          { id: "problem", title: "Why parsing matters" },
          { id: "analogy", title: "Chef analogy" },
          { id: "pipeline", title: "Parsing pipeline" },
          { id: "formats", title: "Format-specific risks" },
          { id: "cleaning", title: "Cleaning strategy" },
          { id: "contracts", title: "Parser contracts" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-07",
        num: 7,
        title: "Metadata Design",
        path: "chapters/chapter-07-metadata-design/lesson.html",
        description: "Source, section, policy id, role, access, version, timestamp, authority, freshness, schema validation, and metadata-driven retrieval behavior.",
        subtopics: [
          { id: "problem", title: "Why metadata matters" },
          { id: "analogy", title: "Passport analogy" },
          { id: "schema", title: "Metadata schema" },
          { id: "fields", title: "Field families" },
          { id: "access", title: "Access and safety" },
          { id: "versioning", title: "Versioning and freshness" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-08",
        num: 8,
        title: "Ingestion and Indexing Pipelines",
        path: "chapters/chapter-08-ingestion-and-indexing-pipelines/lesson.html",
        description: "Batch ingestion, incremental updates, re-indexing, pipeline logs, quality gates, failure recovery, rollback, and index release operations.",
        subtopics: [
          { id: "problem", title: "Why pipelines matter" },
          { id: "analogy", title: "Assembly line analogy" },
          { id: "pipeline", title: "Pipeline stages" },
          { id: "batch", title: "Batch vs incremental" },
          { id: "indexing", title: "Indexing and re-indexing" },
          { id: "observability", title: "Logs and recovery" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      }
    ]
  },
  {
    title: "Module 3 — Chunking",
    summary: "Learn how document slices shape retrieval quality, context noise, latency, and answer grounding.",
    examPath: null,
    chapters: [
      {
        id: "chapter-09",
        num: 9,
        title: "Fixed and Recursive Chunking",
        path: "chapters/chapter-09-fixed-and-recursive-chunking/lesson.html",
        description: "Token size, overlap, separators, fixed splitting, recursive splitting, chunk count, context size, citations, and retrieval-quality trade-offs.",
        subtopics: [
          { id: "problem", title: "Why chunking matters" },
          { id: "analogy", title: "Pizza slice analogy" },
          { id: "fixed", title: "Fixed chunking" },
          { id: "recursive", title: "Recursive chunking" },
          { id: "overlap", title: "Overlap and separators" },
          { id: "tradeoffs", title: "Production trade-offs" },
          { id: "architecture", title: "Architecture view" },
          { id: "evaluation", title: "Chunk evaluation" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-10",
        num: 10,
        title: "Semantic and Hierarchical Chunking",
        path: "chapters/chapter-10-semantic-and-hierarchical-chunking/lesson.html",
        description: "Topic-aware boundaries, parent-child retrieval, section-aware chunks, hierarchy metadata, context expansion, and when simple chunking is enough.",
        subtopics: [
          { id: "problem", title: "Why advanced chunking matters" },
          { id: "analogy", title: "Book chapter analogy" },
          { id: "semantic", title: "Semantic chunking" },
          { id: "hierarchical", title: "Hierarchical chunking" },
          { id: "parent-child", title: "Parent-child retrieval" },
          { id: "simple-enough", title: "When simple is enough" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-11",
        num: 11,
        title: "Chunking Failure Analysis",
        path: "chapters/chapter-11-chunking-failure-analysis/lesson.html",
        description: "Lost context, mixed-topic chunks, overlap noise, tiny chunks, giant chunks, stale chunks, trace inspection, eval gates, and controlled fixes.",
        subtopics: [
          { id: "problem", title: "Why failure analysis matters" },
          { id: "analogy", title: "Doctor diagnosis analogy" },
          { id: "symptoms", title: "Failure symptoms" },
          { id: "root-causes", title: "Root causes" },
          { id: "trace", title: "Trace inspection" },
          { id: "decision", title: "Decision framework" },
          { id: "architecture", title: "Architecture view" },
          { id: "examples", title: "Production examples" },
          { id: "metrics", title: "Metrics and evals" },
          { id: "fixes", title: "Fix playbook" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      }
    ]
  },
  {
    title: "Module 4 — Embeddings and Similarity",
    summary: "Make meaning searchable by understanding embeddings, similarity, and the limits of vector matching.",
    examPath: null,
    chapters: [
      {
        id: "chapter-12",
        num: 12,
        title: "What Embeddings Are",
        path: "chapters/chapter-12-what-embeddings-are/lesson.html",
        description: "Text-to-vector intuition, semantic similarity, cosine similarity, dense vs sparse retrieval, model consistency, re-indexing, privacy, and embedding evals.",
        subtopics: [
          { id: "problem", title: "Why embeddings exist" },
          { id: "analogy", title: "Map analogy" },
          { id: "mental-model", title: "Mental model" },
          { id: "technical", title: "Technical explanation" },
          { id: "similarity", title: "Similarity" },
          { id: "dense-sparse", title: "Dense vs sparse" },
          { id: "architecture", title: "Architecture view" },
          { id: "code", title: "Practical example" },
          { id: "production", title: "Production considerations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-13",
        num: 13,
        title: "Local TF-IDF + SVD Embeddings",
        path: "chapters/chapter-13-local-tfidf-svd-embeddings/lesson.html",
        description: "Local lexical embeddings, TF-IDF weighting, SVD/latent-topic compression, exact-term strengths, paraphrase limits, rebuilds, and hybrid positioning.",
        subtopics: [
          { id: "problem", title: "Why local embeddings matter" },
          { id: "analogy", title: "Library shelf analogy" },
          { id: "tfidf", title: "TF-IDF" },
          { id: "svd", title: "SVD and latent topics" },
          { id: "workflow", title: "End-to-end workflow" },
          { id: "strengths", title: "What it is good at" },
          { id: "limits", title: "What it misses" },
          { id: "architecture", title: "Architecture view" },
          { id: "code", title: "Practical example" },
          { id: "production", title: "Production considerations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-14",
        num: 14,
        title: "Neural Embeddings",
        path: "chapters/chapter-14-neural-embeddings/lesson.html",
        description: "Neural embedding model choice, provider trade-offs, dimensions, privacy, latency, cost, hybrid retrieval, evals, re-indexing, and rollout planning.",
        subtopics: [
          { id: "problem", title: "Why neural embeddings matter" },
          { id: "analogy", title: "Translator analogy" },
          { id: "how", title: "How they work" },
          { id: "providers", title: "Provider and model choices" },
          { id: "dimensions", title: "Dimensions and vector stores" },
          { id: "selection", title: "Selection framework" },
          { id: "architecture", title: "Architecture view" },
          { id: "evals", title: "Evaluation plan" },
          { id: "migration", title: "Re-indexing and migration" },
          { id: "production", title: "Production considerations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      }
    ]
  },
  {
    title: "Module 5 — Vector Stores and Retrieval",
    summary: "Build retrieval judgment: indexes, top-k, hybrid search, reranking, and why the first results matter.",
    examPath: null,
    chapters: [
      {
        id: "chapter-15",
        num: 15,
        title: "Vector Stores and Indexing Strategies",
        path: "chapters/chapter-15-vector-stores-and-indexing-strategies/lesson.html",
        description: "Collections, ids, metadata, embeddings, flat vs approximate indexes, persistence, deletes, rebuilds, blue-green releases, and vector-store operations.",
        subtopics: [
          { id: "problem", title: "Why vector stores matter" },
          { id: "analogy", title: "Warehouse analogy" },
          { id: "concepts", title: "Core concepts" },
          { id: "collections", title: "Collections and schemas" },
          { id: "indexes", title: "Index strategies" },
          { id: "lifecycle", title: "Index lifecycle" },
          { id: "architecture", title: "Architecture view" },
          { id: "operations", title: "Production operations" },
          { id: "release", title: "Release strategies" },
          { id: "metrics", title: "Metrics" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-16",
        num: 16,
        title: "Retrieval Strategies and Top-K",
        path: "chapters/chapter-16-retrieval-strategies-and-top-k/lesson.html",
        description: "Similarity search, top-k tuning, score calibration, metadata filters, query rewriting, multi-query retrieval, dedupe, traces, and retrieval policies.",
        subtopics: [
          { id: "problem", title: "Why retrieval strategy matters" },
          { id: "analogy", title: "Receptionist analogy" },
          { id: "similarity", title: "Similarity search" },
          { id: "topk", title: "Top-k" },
          { id: "scores", title: "Scores and thresholds" },
          { id: "filters", title: "Metadata filters" },
          { id: "query-rewriting", title: "Query rewriting" },
          { id: "multi-query", title: "Multi-query retrieval" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production considerations" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-17",
        num: 17,
        title: "Hybrid Search and Query Routing",
        path: "chapters/chapter-17-hybrid-search-and-query-routing/lesson.html",
        description: "Dense vs sparse retrieval, BM25, hybrid search, reciprocal rank fusion, query routing, exact-term protection, risk routing, and route traces.",
        subtopics: [
          { id: "problem", title: "Why hybrid matters" },
          { id: "analogy", title: "Two-lens analogy" },
          { id: "dense-sparse", title: "Dense vs sparse" },
          { id: "bm25", title: "BM25" },
          { id: "fusion", title: "Fusion strategies" },
          { id: "routing", title: "Query routing" },
          { id: "risk", title: "Risk-based routing" },
          { id: "architecture", title: "Architecture view" },
          { id: "examples", title: "Production examples" },
          { id: "metrics", title: "Metrics" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      {
        id: "chapter-18",
        num: 18,
        title: "Reranking and Retrieval Optimization",
        path: "chapters/chapter-18-reranking-and-retrieval-optimization/lesson.html",
        description: "Retrieve many return few, cross-encoder intuition, candidate pools, reranking, dedupe, latency/cost trade-offs, metrics, and optimization loops.",
        subtopics: [
          { id: "problem", title: "Why reranking matters" },
          { id: "analogy", title: "Hiring shortlist analogy" },
          { id: "first-stage", title: "First-stage retrieval" },
          { id: "reranking", title: "Reranking" },
          { id: "cross-encoder", title: "Cross-encoder intuition" },
          { id: "when", title: "When reranking helps" },
          { id: "architecture", title: "Architecture view" },
          { id: "optimization", title: "Optimization loop" },
          { id: "latency", title: "Cost and latency" },
          { id: "metrics", title: "Metrics" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      }
    ]
  },
  {
    title: "Module 6 — Prompting for RAG",
    summary: "Teach the model how to use retrieved evidence clearly, safely, and testably.",
    examPath: null,
    chapters: [
      {
        id: "chapter-19",
        num: 19,
        title: "Context Injection",
        path: "chapters/chapter-19-context-injection/lesson.html",
        description: "Context packs, evidence ordering, compression, prompt boundaries, citations, token budgets, conflict handling, and traceable prompt assembly.",
        subtopics: [
          { id: "problem", title: "Why context injection matters" },
          { id: "analogy", title: "Chef plating analogy" },
          { id: "definition", title: "What context injection is" },
          { id: "context-pack", title: "Context pack design" },
          { id: "ordering", title: "Ordering and grouping" },
          { id: "compression", title: "Compression" },
          { id: "boundaries", title: "Prompt boundaries" },
          { id: "citations", title: "Citations and traceability" },
          { id: "budget", title: "Token budget" },
          { id: "architecture", title: "Architecture view" },
          { id: "production", title: "Production controls" },
          { id: "mistakes", title: "Common mistakes" },
          { id: "interview", title: "Interview understanding" },
          { id: "assignment", title: "Mini assignment" },
          { id: "summary", title: "Summary" }
        ]
      },
      { id: "chapter-20", num: 20, title: "Grounded System Prompts", path: null },
      { id: "chapter-21", num: 21, title: "Prompt Testing", path: null }
    ]
  },
  {
    title: "Module 7 — Evaluation",
    summary: "Move beyond vibes with retrieval metrics, answer quality checks, and failure-analysis habits.",
    examPath: null,
    chapters: [
      { id: "chapter-22", num: 22, title: "Retrieval Metrics", path: null },
      { id: "chapter-23", num: 23, title: "Answer Quality Metrics", path: null },
      { id: "chapter-24", num: 24, title: "Failure Analysis", path: null }
    ]
  },
  {
    title: "Module 8 — Production RAG",
    summary: "Ship RAG like a real product: access control, observability, cost, deployment, and portfolio polish.",
    examPath: null,
    chapters: [
      { id: "chapter-25", num: 25, title: "Access Control and Safety", path: null },
      { id: "chapter-26", num: 26, title: "Observability and Cost", path: null },
      { id: "chapter-27", num: 27, title: "Deployment Patterns", path: null },
      { id: "chapter-28", num: 28, title: "End-to-End Production RAG Capstone", path: null }
    ]
  }
];
