# RAG for Everyone

Free, interactive RAG course for everyone — from first principles to production trade-offs.

## Contents

- [What this is](#what-this-is)
- [Status](#status)
- [Repo structure](#repo-structure)
- [Running locally](#running-locally)
- [Maintenance](#maintenance)
- [License](#license)

## What this is

A self-paced RAG course built as a series of small, interactive HTML mini-textbooks. Every module follows the same cross-linked pattern:

- A lesson page that introduces concepts through failure modes, trade-offs, and concrete system examples
- A fill-in-the-blank quiz with instant browser-side feedback
- Interview preparation pages, practice banks, exercises, hands-on labs, flashcards, notebooks, and a project
- Supporting content assets such as speaker notes, slide outlines, workshop material, and creator-ready drafts

Quiz completion is stored only in the browser's local storage. There is no backend, no sign-up, and no tracking.

## Status

The full 12-module course shell is live:

- ✅ Module 1: Foundation
- ✅ Module 2: Documents and Data Ingestion
- ✅ Module 3: Chunking Deep Dive
- ✅ Module 4: Embeddings
- ✅ Module 5: Vector Databases
- ✅ Module 6: Retrieval
- ✅ Module 7: Re-ranking
- ✅ Module 8: Prompt Engineering for RAG
- ✅ Module 9: Evaluation
- ✅ Module 10: Production RAG
- ✅ Module 11: Advanced RAG
- ✅ Module 12: Hands-on Projects

See the live roadmap page at [docs/curriculum/index.html](docs/curriculum/index.html) for the full structure.

## Repo structure

```text
03-rag-for-everyone/
├── index.html                        → course landing page
├── document.html                     → styled markdown viewer
├── assets/                           → shared visual design and browser-side JS
├── docs/curriculum/                  → roadmap page + curriculum source
└── chapters/module-XX-*/             → lesson, quiz, interview prep, practice, lab, project
```

Every module page is cross-linked back into the course shell.

## Running locally

From this directory:

```bash
cd 03-rag-for-everyone
```

- You can open `index.html`, lessons, quizzes, and the other HTML pages directly in a browser.
- For the best experience, especially the styled markdown viewer used for README-style documents, serve the folder over HTTP:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

If you are looking for the runnable Python app in this repository, that lives in `../01-policy-rag-poc/` and starts with:

```bash
cd ../01-policy-rag-poc
pip install -r requirements.txt
python3 src/vectorstore.py
python3 src/main.py
```

## Maintenance

This course is maintained inside the `rag-projects` repository alongside other RAG projects and content assets.

## License

MIT — see [../LICENSE](../LICENSE).
