# RAG for Everyone Templates

These templates define the standard chapter flow. Use them for every new
chapter so the course stays consistent and fast to build.

The reference is `python-for-everyone` for structure and UI pattern only. The
content must always be original to RAG, GenAI systems, prompt testing,
retrieval, evaluation, and production AI engineering.

## Standard Chapter Flow

1. `lesson.html`
2. `quiz.html`
3. `exercises/index.html`
4. `practice/index.html`
5. `interview-questions.html`
6. `project/index.html`

Supporting source files:

- `README.md`
- `thinking-journal.md`
- `interview-questions.md`
- `exercises/README.md`
- `exercises/starter.py`
- `exercises/solution.py`
- `practice/README.md`
- `practice/starter.py`
- `practice/solution.py`
- `project/README.md`
- `project/starter.py`
- `project/solution.py`
- `diagrams/architecture.txt`
- `diagrams/architecture.mmd`
- `diagrams/architecture.svg`

## How To Use

1. Copy the relevant template into a new chapter folder.
2. Replace placeholders like `{{CHAPTER_ID}}`, `{{CHAPTER_TITLE}}`, and
   `{{CHAPTER_SLUG}}`.
3. Keep the navigation flow unchanged unless there is a strong reason.
4. Add original RAG/GenAI content.
5. Stop after the chapter is complete and wait for review before building the
   next chapter.

## Required Page Pattern

Every learner-facing page should have:

- Sidebar navigation.
- Top navigation.
- Back link to previous step.
- Page metadata.
- Conversational opening.
- Clear next-step chapter navigation.
- Footer.

## Relative Paths

For files directly under a chapter folder:

- CSS/assets root: `../../assets/...`
- Course root: `../../index.html`

For files inside nested folders such as `exercises/`, `practice/`, and
`project/`:

- CSS/assets root: `../../../assets/...`
- Course root: `../../../index.html`

