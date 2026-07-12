# RAG for Everyone

Applied GenAI projects built end to end — architecture through evaluation,
not notebook demos. This repo collects hands-on RAG (Retrieval-Augmented
Generation) systems and the write-ups documenting how they were built.

🔗 **RAG for Everyone Live UI:** <https://technaom.github.io/rag-projects/rag-for-everyone/>

## Projects

| | |
|---|---|
| **[01-policy-rag-poc](01-policy-rag-poc/)** | End-to-end RAG system over a synthetic banking HR & compliance policy corpus — Markdown-aware chunking, a local TF-IDF/SVD embedding pipeline, ChromaDB retrieval, generation via Ollama (local) or Groq (Llama 3.3 70B), and a golden-set retrieval evaluation (Recall@3, MRR). See its own [README](01-policy-rag-poc/README.md) for the full architecture, evaluation results, and what would change for a production deployment. |
| **[02-linkedin-content](02-linkedin-content/)** | Build-in-public write-ups documenting the real engineering decisions and honest trade-offs behind the projects in this repo. |
| **[03-rag-for-everyone](03-rag-for-everyone/)** | Interactive RAG course and content system modeled after `python-for-everyone`'s design and engineering structure: roadmap, chapters, lessons, quizzes, exercises, prompt labs, retrieval labs, interview prep, diagrams, GenAI thought-process journals, and portfolio projects built around the working RAG POC. **RAG for Everyone Live UI:** <https://technaom.github.io/rag-projects/rag-for-everyone/> |
| **[04-multi-tenant-docs-copilot](04-multi-tenant-docs-copilot/)** | RAG-as-a-service with *structural* tenant isolation — each of 3 tenants gets its own Chroma collection and its own independently-fitted embedder, not a shared index with a filter. Includes a per-tenant cost/latency dashboard and a pytest suite that proves cross-tenant leakage is impossible. See its [README](04-multi-tenant-docs-copilot/README.md) for real test/demo output. |
| **[05-audit-grade-compliance-rag](05-audit-grade-compliance-rag/)** | Goes beyond citing a source to proving it: a 4-level citation-support auditor (L1-L4) that verifies a cited chunk is the **current**, non-superseded policy version, plus a trace store and a Markdown "audit report" generator for a compliance reviewer. See its [README](05-audit-grade-compliance-rag/README.md) — includes a real example of the system catching a superseded-source citation. |
| **[06-realtime-oncall-copilot](06-realtime-oncall-copilot/)** | Retrieval over runbooks and incident notes that change mid-incident — an incremental upsert re-indexes one edited file in milliseconds with no full rebuild, under a hard per-stage latency budget and a cost-aware query router. See its [README](06-realtime-oncall-copilot/README.md) for a real before/after live-update demo and latency report. |

## Stack

Python &middot; LangChain &middot; ChromaDB &middot; scikit-learn (TF-IDF + Truncated SVD embeddings) &middot; Ollama &middot; Groq (Llama 3.3 70B)

## License

MIT — see [LICENSE](LICENSE).
