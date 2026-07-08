# rag-projects

Applied GenAI projects built end to end — architecture through evaluation,
not notebook demos. This repo collects hands-on RAG (Retrieval-Augmented
Generation) systems and the write-ups documenting how they were built.

## Projects

| | |
|---|---|
| **[01-policy-rag-poc](01-policy-rag-poc/)** | End-to-end RAG system over a synthetic banking HR & compliance policy corpus — Markdown-aware chunking, a local TF-IDF/SVD embedding pipeline, ChromaDB retrieval, generation via Ollama (local) or Groq (Llama 3.3 70B), and a golden-set retrieval evaluation (Recall@3, MRR). See its own [README](01-policy-rag-poc/README.md) for the full architecture, evaluation results, and what would change for a production deployment. |
| **[02-linkedin-content](02-linkedin-content/)** | Build-in-public write-ups documenting the real engineering decisions and honest trade-offs behind the projects in this repo. |
| **[03-rag-for-everyone](03-rag-for-everyone/)** | Planned interactive RAG course and content system modeled after `python-for-everyone`: roadmap, chapters, lessons, quizzes, exercises, prompt labs, retrieval labs, interview prep, and portfolio projects built around the working RAG POC. |

## Stack

Python &middot; LangChain &middot; ChromaDB &middot; scikit-learn (TF-IDF + Truncated SVD embeddings) &middot; Ollama &middot; Groq (Llama 3.3 70B)

## License

MIT — see [LICENSE](LICENSE).
