# RAG for Everyone

Free, interactive RAG course and build-in-public engineering track for
new-age learners: visual lessons, prompt-testing labs, retrieval experiments,
evaluation practice, interview prep, and portfolio projects.

This course should follow the same philosophy as `python-for-everyone`:

- Plain-language first, without hiding the real engineering.
- One chapter at a time, validated before scaling.
- No signup required.
- Browser-first learning pages.
- Hands-on code and projects.
- Interview-ready explanations.
- Strong architecture and trade-off thinking.

The reference repo is used only for course design and engineering structure,
not for lesson content. All examples, stories, exercises, projects, and
thought-process journals in this course must be original to RAG, GenAI systems,
prompt testing, retrieval, evaluation, and production AI engineering.

## What this is

`RAG for Everyone` is the learning layer on top of the existing
`01-policy-rag-poc` implementation. The Python project proves the pipeline;
this course explains it, visualizes it, tests it, and turns it into a guided
learning path.

Every chapter should follow a consistent format:

1. A real-world hook before any jargon.
2. A plain-language explanation of the concept.
3. A visual system walkthrough.
4. A hands-on lab tied to the `01-policy-rag-poc` project.
5. A prompt or retrieval testing exercise.
6. A fill-in-the-blank quiz with instant feedback.
7. Exercises, including at least one debugging or failure-analysis task.
8. A practice bank with scenario-based questions.
9. Interview questions using strong-answer, red-flag, and follow-up format.
10. A small portfolio project or project increment.
11. A GenAI thought-process journal: how to frame the problem, ask better
    questions, test model outputs, critique answers, and document decisions.
12. Textual and visual diagrams wherever architecture, flow, retrieval, or
    evaluation would be easier to understand visually.

## GenAI thought-process layer

This course should model how strong new-age builders work with AI:

- Frame the problem before prompting.
- State assumptions clearly.
- Ask the model for options, then compare trade-offs.
- Test outputs against evidence, not vibes.
- Turn failures into eval cases.
- Keep a decision journal so future learners can see why the system changed.
- Use AI as a thinking partner while still owning the engineering judgment.

The goal is not to expose hidden model chain-of-thought. The goal is to teach
visible, professional reasoning habits: prompts, hypotheses, checks, critiques,
evals, and architecture decisions.

## Status

This course is in design foundation state.

- Existing engine: `../01-policy-rag-poc`
- Existing content channel: `../02-linkedin-content`
- Course architecture: `docs/course-architecture.md`
- Roadmap: `docs/curriculum/CURRICULUM_MAP.md`

## Repo structure

```text
03-rag-for-everyone/
├── README.md
├── index.html                         -> future course landing page
├── assets/                            -> shared CSS/JS, quiz engine, progress, playgrounds
├── docs/
│   ├── course-architecture.md          -> engineering and content architecture
│   └── curriculum/
│       ├── CURRICULUM_MAP.md           -> plain-text roadmap
│       └── index.html                  -> future styled roadmap page
├── chapters/
│   └── chapter-01-why-rag-exists/
│       ├── lesson.html                 -> mini-textbook
│       ├── quiz.html                   -> instant-check quiz
│       ├── interview-questions.md
│       ├── interview-questions.html
│       ├── diagrams/                   -> text, Mermaid, and image-style diagrams
│       ├── exercises/
│       ├── practice/
│       └── project/
└── assessments/
    └── written-exams/
```

## Relationship to the RAG project

The course should not become detached from the working project. Every major
concept should point back to a real implementation detail:

- Ingestion -> `01-policy-rag-poc/src/ingest.py`
- Embeddings -> `01-policy-rag-poc/src/embeddings.py`
- Vector store -> `01-policy-rag-poc/src/vectorstore.py`
- Retrieval and prompting -> `01-policy-rag-poc/src/rag_chain.py`
- Evaluation -> `01-policy-rag-poc/src/eval.py`

That connection is the differentiator: learners see both the explanation and
the code behind it.

## Build order

1. Build Chapter 1 completely.
2. Add the course landing page and roadmap page.
3. Add shared assets copied/adapted from `python-for-everyone`.
4. Add interactive RAG-specific components: document-to-chunk visualizer,
   retrieval playground, prompt tester, and eval dashboard.
5. Publish the static course with GitHub Pages.
