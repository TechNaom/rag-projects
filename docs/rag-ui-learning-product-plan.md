# RAG UI Learning Product Plan

## Current State

This repository is currently strongest as an applied RAG engineering portfolio:

- `01-policy-rag-poc/` is a working CLI-based RAG proof of concept over a synthetic banking HR and compliance corpus.
- `02-linkedin-content/` documents the build-in-public narrative and technical learning journey.
- Remote branches contain early course/UI experiments:
  - `origin/copilot/build-rag-roadmap` adds a large `03-rag-for-everyone/` static course shell.
  - `origin/feature/rag-course-foundation` adds a smaller `course/` foundation track.

The verified local RAG POC already has the right learning shape: ingestion, chunking, embeddings, vector storage, retrieval, generation, and evaluation. The next product should turn that pipeline into a polished interactive learning experience.

## Product Direction

Build `03-rag-for-everyone` as a UI-first, engineering-first GenAI learning platform where learners do not just read about RAG. They inspect the moving parts:

- See documents become chunks.
- Watch chunks become embeddings.
- Compare retrieval results.
- Test prompts against retrieved context.
- Observe hallucination guardrails.
- Run evaluation metrics and understand misses.
- Progress from naive RAG to production-grade RAG patterns.

The product should feel like "Python for Everyone" in accessibility, but more ambitious in systems design: visual, testable, explainable, and grounded in real engineering trade-offs.

It should also include a GenAI thought-process layer. Learners should feel they
are learning the new way of building: not passively consuming answers, but
framing problems, prompting carefully, testing outputs, critiquing failures,
and documenting decisions like responsible AI-era builders.

## Reference Repo Pattern

The reference repo is `TechNaom/python-for-everyone`. The RAG course should
mirror its durable architecture:

- Root landing page as the GitHub Pages entry point.
- Shared `assets/` for style, sidebar navigation, progress, quizzes, and playground behavior.
- `docs/curriculum/CURRICULUM_MAP.md` as the source roadmap.
- `docs/curriculum/index.html` as the styled roadmap page.
- `chapters/chapter-XX-topic/` as the repeatable learning unit.
- Each chapter includes lesson, quiz, exercises, practice bank, interview prep, and project.
- Module-level written exams live under `assessments/written-exams/`.
- Progress is stored only in browser local storage.

The reference is for design, structure, and engineering discipline only. Do not
reuse Python-course content. The RAG course needs original examples, stories,
labs, exercises, and projects built around RAG, GenAI thought process, prompt
testing, retrieval evaluation, and production AI engineering.

## Recommended Architecture

### Phase 1: Static Interactive Course

Use the same static app stack as `python-for-everyone`:

- HTML/CSS/JS.
- `assets/chapters-data.js` as the course roster.
- `assets/sidebar.js` for persistent navigation.
- `assets/progress.js` for localStorage completion.
- `assets/quiz-engine.js` for instant-check quizzes.
- No login.
- Browser-local progress tracking.
- Interactive diagrams, quizzes, prompt sandboxes, and retrieval explainers.
- Reuse `01-policy-rag-poc` content and eval results as the source project.

This keeps publishing simple through GitHub Pages and avoids backend complexity too early.

### Phase 2: RAG-Specific Static Labs

Add RAG-specific browser-side learning components:

- Query lifecycle visualizer.
- Document-to-chunk viewer.
- Retrieval playground with saved sample outputs.
- Prompt testing workbench with fixed context examples.
- Evaluation dashboard explaining Recall@K and MRR.

### Phase 3: Optional Live Engineering Labs

Only after the static course is strong, add optional local Python-backed labs:

- Local API wrapper around `01-policy-rag-poc`.
- Live retrieval experiments.
- Live eval runs.
- Embedding swap experiments.
- Hybrid search and reranking comparisons.

## Curriculum Spine

The best module structure from the remote branches is:

1. Foundation: why RAG exists, hallucinations, context windows, query lifecycle.
2. Documents and ingestion: file types, parsing, metadata, cleaning.
3. Chunking: fixed, recursive, semantic, parent-child, trade-offs.
4. Embeddings: vectors, similarity, model choices, drift, reindexing.
5. Vector databases: exact vs ANN, HNSW, filtering, hybrid search.
6. Retrieval: dense, sparse, metadata-aware, query rewriting.
7. Reranking: cross-encoders, cost, latency, accuracy.
8. Prompt engineering for RAG: context formatting, citations, refusal behavior.
9. Evaluation: Recall@K, MRR, faithfulness, groundedness, latency, cost.
10. Production RAG: access control, monitoring, caching, versioning, CI/CD.
11. Advanced RAG: agentic, graph, multimodal, SQL, code, adaptive RAG.
12. Capstone projects: learners build portfolio-grade RAG systems.

Each module should include:

- A clean lesson.
- A visual explainer.
- Textual architecture diagrams for quick comprehension.
- Image-style or rendered diagrams for visual learners.
- A hands-on lab.
- A small quiz.
- A prompt or retrieval experiment.
- A GenAI thought-process journal.
- A "what breaks in production" section.
- A portfolio artifact the learner can share.

## Engineering Standards

Do not merge the generated remote branches wholesale. They include useful ideas, but also generated artifacts such as `__pycache__` files and many shallow placeholder pages.

Instead:

- Keep the repo clean and source-only.
- Add a root `.gitignore` if generated artifacts continue appearing.
- Use one consistent frontend framework or one intentionally simple static pattern.
- Separate curriculum content from app components.
- Treat `01-policy-rag-poc` as the executable reference implementation.
- Add tests for any shared JavaScript logic and Python API layer.
- Keep every module tied to a working demo, eval, or clear engineering decision.

## Suggested First Build Slice

Start with a single excellent vertical slice instead of a large empty course shell:

1. Create `03-rag-for-everyone/` with a polished home screen and Module 1.
2. Add an interactive "RAG Query Lifecycle" page.
3. Add a document-to-chunk visualizer using the Northkeep policy corpus.
4. Add a retrieval playground with static sample results from the existing eval.
5. Add a prompt-testing panel showing grounded vs ungrounded answers.
6. Add a learner progress sidebar stored in local storage.
7. Publish through GitHub Pages.

This gives learners a real product immediately and gives the project a strong public story.

## Strategic Positioning

The project should be framed as:

"A free, visual, engineering-first RAG course where learners build intuition by testing every part of the pipeline."

The differentiator is not just curriculum volume. The differentiator is transparency:

- Show why systems fail.
- Show how prompts change behavior.
- Show how retrieval metrics expose weak spots.
- Show trade-offs instead of pretending there is one perfect architecture.

That matches the repo's current voice and turns the existing POC into a serious learning platform.
