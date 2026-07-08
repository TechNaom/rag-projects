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
      { id: "chapter-02", num: 2, title: "The RAG Query Lifecycle", path: null },
      { id: "chapter-03", num: 3, title: "Types of RAG", path: null },
      { id: "chapter-04", num: 4, title: "Reading a RAG Architecture Diagram", path: null }
    ]
  },
  {
    title: "Module 2 — Documents and Ingestion",
    summary: "Turn messy real-world documents into governed, searchable knowledge that a RAG system can trust.",
    examPath: null,
    chapters: [
      { id: "chapter-05", num: 5, title: "Source Documents", path: null },
      { id: "chapter-06", num: 6, title: "Parsing and Cleaning", path: null },
      { id: "chapter-07", num: 7, title: "Metadata Design", path: null },
      { id: "chapter-08", num: 8, title: "Ingestion Pipelines", path: null }
    ]
  },
  {
    title: "Module 3 — Chunking",
    summary: "Learn how document slices shape retrieval quality, context noise, latency, and answer grounding.",
    examPath: null,
    chapters: [
      { id: "chapter-09", num: 9, title: "Fixed and Recursive Chunking", path: null },
      { id: "chapter-10", num: 10, title: "Semantic and Hierarchical Chunking", path: null },
      { id: "chapter-11", num: 11, title: "Chunking Failure Analysis", path: null }
    ]
  },
  {
    title: "Module 4 — Embeddings and Similarity",
    summary: "Make meaning searchable by understanding embeddings, similarity, and the limits of vector matching.",
    examPath: null,
    chapters: [
      { id: "chapter-12", num: 12, title: "What Embeddings Are", path: null },
      { id: "chapter-13", num: 13, title: "Local TF-IDF + SVD Embeddings", path: null },
      { id: "chapter-14", num: 14, title: "Neural Embeddings", path: null }
    ]
  },
  {
    title: "Module 5 — Vector Stores and Retrieval",
    summary: "Build retrieval judgment: indexes, top-k, hybrid search, reranking, and why the first results matter.",
    examPath: null,
    chapters: [
      { id: "chapter-15", num: 15, title: "Vector Stores", path: null },
      { id: "chapter-16", num: 16, title: "Top-K Retrieval", path: null },
      { id: "chapter-17", num: 17, title: "Hybrid Search", path: null },
      { id: "chapter-18", num: 18, title: "Reranking", path: null }
    ]
  },
  {
    title: "Module 6 — Prompting for RAG",
    summary: "Teach the model how to use retrieved evidence clearly, safely, and testably.",
    examPath: null,
    chapters: [
      { id: "chapter-19", num: 19, title: "Context Injection", path: null },
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
      { id: "chapter-28", num: 28, title: "Capstone Portfolio Project", path: null }
    ]
  }
];
