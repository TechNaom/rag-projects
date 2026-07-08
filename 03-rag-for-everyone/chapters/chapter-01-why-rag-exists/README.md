# Chapter 1: Why RAG Exists

This chapter is the first vertical slice for the course. Build it completely
before scaling the rest of the roadmap.

## Learning Outcomes

Learners should be able to:

- Explain why LLMs need external context for private or changing information.
- Distinguish model memory, web search, and RAG.
- Describe the Northkeep policy assistant in one clear paragraph.
- Identify where retrieval enters the answer-generation flow.
- Explain why citations matter in internal policy assistants.

## Required Assets

- `lesson.html`
- `quiz.html`
- `interview-questions.md`
- `interview-questions.html`
- `exercises/README.md`
- `exercises/starter.py`
- `exercises/solution.py`
- `practice/README.md`
- `practice/starter.py`
- `practice/solution.py`
- `project/README.md`
- `project/starter.py`
- `project/solution.py`
- `thinking-journal.md`

## Project Increment

Learners write a small architecture explainer for the Northkeep policy
assistant:

1. What documents it uses.
2. How documents become chunks.
3. How retrieval finds relevant chunks.
4. How the prompt forces grounded answers.
5. How evaluation catches weak spots.

## GenAI Thought-Process Journal

The journal for this chapter should help learners practice:

1. Problem framing: "What kind of question should not rely on model memory?"
2. Prompt framing: "What should the assistant be allowed to answer from?"
3. Assumption tracking: "What do we assume is inside the policy corpus?"
4. Testing: "Which questions reveal whether RAG is needed?"
5. Critique: "Where could the model sound confident but unsupported?"
6. Decision: "What system rule would reduce that risk?"
