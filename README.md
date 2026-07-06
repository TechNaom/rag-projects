# rag-projects

Applied GenAI projects built end to end — architecture through evaluation,
not notebook demos. This repo collects hands-on RAG (Retrieval-Augmented
Generation) systems and the write-ups documenting how they were built.

## What should you run?

This repository contains more than one project.

- **Want the interactive course site?** Open `03-rag-for-everyone/index.html` in a browser, or serve that folder locally with `python3 -m http.server 8000`.
- **Want the runnable Python app?** Use `01-policy-rag-poc/src/main.py` after installing its dependencies and building the vector store.
- **Looking for `app.py` at the repo root?** There is no root `app.py`. The Python entry point is inside `01-policy-rag-poc/src/main.py`.

## Quick start

Pick one of these:

- **Course site:** `cd 03-rag-for-everyone && python3 -m http.server 8000`
- **Python RAG CLI:** `cd 01-policy-rag-poc && pip install -r requirements.txt && python3 src/vectorstore.py && python3 src/main.py`

## Projects

| | |
|---|---|
| **[01-policy-rag-poc](01-policy-rag-poc/)** | End-to-end RAG system over a synthetic banking HR & compliance policy corpus — Markdown-aware chunking, a local TF-IDF/SVD embedding pipeline, ChromaDB retrieval, generation via Ollama (local) or Groq (Llama 3.3 70B), and a golden-set retrieval evaluation (Recall@3, MRR). See its own [README](01-policy-rag-poc/README.md) for the full architecture, evaluation results, and what would change for a production deployment. |
| **[02-linkedin-content](02-linkedin-content/)** | Build-in-public write-ups documenting the real engineering decisions and honest trade-offs behind the projects in this repo. |
| **[03-rag-for-everyone](03-rag-for-everyone/)** | Structured, example-driven RAG course content modeled after python-for-everyone: interactive lessons, quizzes, labs, notebooks, interview prep, and creator-ready content assets for all 12 modules. |

### Run the course site

```bash
cd 03-rag-for-everyone
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

You can also open `03-rag-for-everyone/index.html` directly in a browser for the main course pages, but the styled markdown viewer works best when the folder is served over HTTP.

### Run the Python RAG CLI

```bash
cd 01-policy-rag-poc
pip install -r requirements.txt
python3 src/vectorstore.py
python3 src/main.py
```

## Stack

Python &middot; LangChain &middot; ChromaDB &middot; scikit-learn (TF-IDF + Truncated SVD embeddings) &middot; Ollama &middot; Groq (Llama 3.3 70B)

## License

MIT — see [LICENSE](LICENSE).
