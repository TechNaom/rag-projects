# rag-projects Repository Overview

Applied GenAI projects built end to end — architecture through evaluation, not notebook demos.

## What should you run?

This repository contains more than one project.

- **Want the interactive course site?** Open `03-rag-for-everyone/index.html` in a browser, or serve that folder locally with `python3 -m http.server 8000`.
- **Want the runnable Python app?** Use `01-policy-rag-poc/src/main.py` after installing its dependencies and building the vector store.
- **Looking for `app.py` at the repo root?** There is no root `app.py`. The Python entry point is inside `01-policy-rag-poc/src/main.py`.

## Quick start

- **Course site:** `cd 03-rag-for-everyone && python3 -m http.server 8000`
- **Python RAG CLI:** `cd 01-policy-rag-poc && pip install -r requirements.txt && python3 src/vectorstore.py && python3 src/main.py`

## Projects

- **03-rag-for-everyone** — the interactive HTML/CSS/JS course site you are viewing now. See the [course README](../README.md) or the [curriculum roadmap](curriculum/index.html).
- **01-policy-rag-poc** — end-to-end RAG system over a synthetic banking HR and compliance policy corpus. Use the path `../01-policy-rag-poc/` from the repository root when working locally.
- **02-linkedin-content** — build-in-public write-ups documenting the engineering decisions and trade-offs behind the projects.

## Stack

Python · LangChain · ChromaDB · scikit-learn (TF-IDF + Truncated SVD embeddings) · Ollama · Groq (Llama 3.3 70B)

## License

MIT — see the repository `LICENSE` file at the repository root.
