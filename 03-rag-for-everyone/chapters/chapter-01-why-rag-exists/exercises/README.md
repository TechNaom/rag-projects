# Chapter 1 Exercises: Why RAG Exists

These exercises use only Chapter 1 concepts: model memory, web search, trusted
context, citations, retrieval, refusal, and evaluation.

Think of this like learning to drive in production traffic. The first few tasks
are simple, then we slowly add real-world pressure: policy changes, missing
sources, access control, audit trails, and business risk.

## Exercise 1 — Classify the question

Open `starter.py`. For each sample question, classify it as:

- `model_memory`
- `web_search`
- `rag`

Use `rag` when the question needs private, trusted, or source-cited context.

## Exercise 2 — Explain your reasoning

For every question, write one short reason explaining why you chose that route.
Good reasoning matters more than the label.

## Exercise 3 — Add two policy questions

Add two new questions that would fit the Northkeep policy assistant:

- One low-risk question, such as cafeteria reimbursement or equipment policy.
- One high-risk question, such as whistleblower, privacy, payroll, or legal
  reporting.

## Exercise 4 — Add source requirements

For each `rag` question, name the source that should be retrieved. Example:
`parental_leave_policy_2026.pdf` or `security_incident_runbook.md`.

## Exercise 5 — Add citation behavior

For each `rag` question, decide whether the assistant must cite a policy section,
page, paragraph, version, or approval owner.

## Exercise 6 — Add refusal behavior

Choose two questions where the assistant should refuse or ask for more context if
retrieval is weak. Write the refusal in a calm, helpful tone.

## Exercise 7 — Add metadata

For three `rag` questions, add the metadata filters you would use in a real
system. Think about country, department, role, policy version, product tier, or
security classification.

## Exercise 8 — Add one production failure

Create one failure case where the assistant retrieves the wrong document but
still answers confidently. Write what you would inspect first.

## Exercise 9 — Create a golden eval question

Write one test question with:

- Expected source.
- Expected behavior.
- Bad answer to catch.
- Metric you would inspect first.

## Exercise 10 — Explain it to a product manager

Write a five-sentence explanation of why this product should use RAG instead of
only a prompt. Keep it simple, but include risk and trust.

## Checking your work

Run:

```bash
python3 starter.py
python3 solution.py
```

Your wording does not need to match the solution exactly. The important part is
that you can defend the classification.
