# RAG for Everyone Course Architecture

## Reference Pattern

The reference implementation is `TechNaom/python-for-everyone`.

Use it as a reference for product design, not as a content source. Preserve the
architecture and learner journey:

- Root `index.html` as the GitHub Pages entry point.
- Shared `assets/` for design, sidebar, progress, quizzes, and playgrounds.
- `docs/curriculum/CURRICULUM_MAP.md` as the readable source roadmap.
- `docs/curriculum/index.html` as the styled roadmap.
- `chapters/chapter-XX-topic/` for each chapter.
- Per-chapter lesson, quiz, exercises, practice bank, interview prep, and project.
- Written exams at module boundaries.
- Progress stored in browser local storage.
- No backend for the default learning path.

Do not reuse Python-course lesson content, examples, project stories, exercises,
or interview answers. RAG for Everyone needs its own original content system
based on GenAI, RAG architecture, prompt testing, retrieval evaluation, and
production trade-offs.

## RAG-Specific Additions

RAG needs interactive system thinking, but that should be built on the same
static course stack. These are extensions inside `assets/`, not a different
frontend architecture:

- `rag-lifecycle.js`: visualizes query flow from user question to answer.
- `chunk-viewer.js`: shows source documents split into chunks.
- `retrieval-playground.js`: compares top-k results and scores.
- `prompt-lab.js`: tests prompt variants against fixed context.
- `eval-dashboard.js`: explains Recall@K, MRR, and failure cases.
- `thinking-journal.js`: helps learners capture assumptions, prompt versions,
  checks, critiques, and engineering decisions.

The course must work as static files first. Any live Python-backed lab is a
future optional enhancement and must not replace the static learning path.

## GenAI Thought-Process Layer

Every chapter should contain a visible builder-thinking section. This is where
learners practice the habits of modern AI engineers:

- Problem framing: what are we trying to improve, and why?
- Prompt framing: what should the model do, what evidence should it use, and
  what should it refuse?
- Hypothesis: what do we expect to happen?
- Test: what query, prompt, dataset, or eval proves it?
- Critique: what failed, what was unsupported, what was too vague?
- Decision: what will we change in the system?
- Reflection: what did this teach us about building with GenAI?

This section should show professional reasoning without pretending the model's
private internal reasoning is visible. We teach the learner's thought process:
clear assumptions, careful tests, and evidence-backed decisions.

## Production Depth Standard

This course is for senior professionals and serious builders as much as it is
for new learners. Keep the language approachable, but make the substance
production-grade.

Every chapter should include:

- At least 10 meaningful examples, checks, or scenario prompts for core concepts.
- Two layers of assessment when useful: a concept check and a production judgment
  check.
- Practice-bank problems grounded in real product, platform, compliance,
  latency, cost, support, and evaluation situations.
- At least five realistic project or scenario options for portfolio thinking.
- Explicit failure modes and what the learner would inspect first.
- Trade-offs that a senior engineer or architect would care about.

Avoid generic "what is X" content by itself. Every explanation should connect to
how a real GenAI system behaves, fails, improves, or gets shipped.

## TechNaom Content Experience Standard

Do not write dry textbook content. The course should feel like a personal mentor
is explaining the concept clearly, simply, and practically.

For every major topic, follow this teaching flow:

1. Start with the problem.
2. Explain why the concept exists.
3. Use a real-life analogy.
4. Explain the mental model.
5. Introduce the technical term.
6. Show where it fits in real engineering.
7. Give a simple example.
8. Give a production-level example.
9. Explain trade-offs.
10. Mention common mistakes.
11. Add interview-level understanding.
12. End with a crisp summary.

Each topic should include these blocks when the page type allows it:

- Title.
- Why this topic matters.
- Simple explanation.
- Real-life analogy.
- Technical explanation.
- Architecture view.
- Code or practical example.
- Production considerations.
- Common mistakes.
- Interview questions.
- Mini assignment.
- Summary.

Use analogies that help the learner feel the idea: pizza slices for chunking,
library shelves for indexing, Google Maps for routing/search, a receptionist for
query routing, a chef preparing ingredients for pipelines, a security guard for
guardrails, a manager assigning work for agents, a warehouse for vector
databases, and a spotlight for attention.

Simple outside. Production-grade inside.

## Conversational Clarity Standard

The course should read like a strong ChatGPT learning conversation: warm,
direct, practical, and easy to follow. The learner should feel guided, not
lectured.

Use this voice:

- Start with the situation before the definition.
- Explain the idea in plain language first.
- Add the professional term after the intuition lands.
- Use "you" and "we" naturally.
- Keep examples close to real work.
- Make diagrams do teaching work, not decoration.
- Give senior trade-offs without sounding academic.

Avoid this voice:

- Dense textbook paragraphs.
- Bullet lists with no story or context.
- Generic tutorial examples that do not resemble production.
- Jargon without a plain-language bridge.

## Content Contract

Every chapter should include:

- `lesson.html`: interactive mini-textbook.
- `quiz.html`: fill-in-the-blank quiz with instant checks.
- `interview-questions.md`: source version for editing.
- `interview-questions.html`: styled learner version.
- `exercises/README.md`: task list and learning goals.
- `exercises/starter.py`: learner code.
- `exercises/solution.py`: reference solution.
- `practice/README.md`: deeper problem bank.
- `practice/starter.py`: practice scaffold.
- `practice/solution.py`: practice solution.
- `project/README.md`: chapter project brief.
- `project/starter.py`: project scaffold.
- `project/solution.py`: reference implementation.
- `thinking-journal.md`: prompts, assumptions, tests, critique notes, and
  architecture decisions for the chapter.
- `diagrams/`: visual learning assets for the chapter.
  - `architecture.txt`: plain-text diagram that works in Markdown, terminals,
    and low-bandwidth contexts.
  - `architecture.mmd`: Mermaid source for rendered diagrams.
  - `architecture.svg`: image-style diagram for learner-facing pages when useful.

For non-code chapters, replace Python scripts with datasets, prompt files, or
evaluation fixtures, but keep the same folder names.

## Exercise and Interview Minimums

Every chapter must give the learner enough reps to build production instinct:

- Exercises: at least 8 hands-on tasks, with at least 5 production-gear tasks.
- Practice bank: at least 10 realistic scenarios.
- Interview questions: at least 15 questions, grouped by concept, production
  judgment, evaluation, and architecture.
- Each interview question should include a strong answer, a red flag answer, a
  follow-up, and what the question proves about the learner.

## Template Contract

Reusable templates live in `templates/`. For future chapters, start from these
templates and only replace the content placeholders. Do not rebuild each page
from scratch.

- `lesson.template.html`
- `quiz.template.html`
- `exercises-index.template.html`
- `practice-index.template.html`
- `interview-questions.template.html`
- `project-index.template.html`
- `thinking-journal.template.md`
- `diagram-readme.template.md`

This keeps the course aligned with the `python-for-everyone` standard while
preserving original RAG/GenAI content.

## Visual Learning Contract

Architecture-heavy content must include visual support. Learners should be able
to understand the same idea in more than one form:

- Conversational explanation: what is happening and why it matters.
- Textual diagram: quick ASCII/system-flow view.
- Image or rendered diagram: architecture overview for visual learners.
- Step-by-step walkthrough: how data moves through the system.
- Failure-point view: where the system can break and what to inspect.

Use diagrams to teach engineering judgment, not decoration. A useful diagram
should answer at least one of these questions:

- What are the moving parts?
- What flows into what?
- Where does evidence enter the model?
- Where can the system fail?
- What would we measure or test?

## Module Boundary Contract

Each module should end with:

- A written exam in `assessments/written-exams/`.
- A portfolio milestone.
- A "systems thinking review" where learners explain trade-offs.
- A public content artifact: blog post, LinkedIn post, diagram, or demo.

## Engineering Rules

- Keep generated artifacts out of Git.
- Keep visual assets reusable and small.
- Use the same static HTML/CSS/JS stack as `python-for-everyone`.
- Tie every concept to a working code path in `01-policy-rag-poc`.
- Avoid a large empty shell. Build one complete vertical slice first, then scale.
- Treat content as source: markdown for roadmaps and editable notes, HTML for learner-facing pages.

## First Vertical Slice

The first slice should prove the entire pattern:

1. Chapter 1 lesson: Why RAG exists.
2. Chapter 1 quiz.
3. Chapter 1 exercises: inspect a failure case where an LLM needs external context.
4. Chapter 1 practice: classify questions as model-memory, search, or RAG problems.
5. Chapter 1 interview prep.
6. Chapter 1 project: explain the Northkeep policy assistant architecture.
7. Chapter 1 GenAI thought-process journal.
8. Chapter 1 diagrams: text, Mermaid, and SVG architecture views.
9. Roadmap page.
10. Landing page.

After this, scaling chapters becomes mechanical and safe.
