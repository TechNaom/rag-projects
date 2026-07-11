# Exercises: Answer Quality Metrics

Practice scoring generated answers with a production rubric.

## Your Tasks

- Score faithfulness, relevance, citation support, completeness, refusal correctness, and safety.
- Detect unsupported terms and missing expected terms.
- Return failed checks, severity, and release gate.
- Explain why a high-risk answer can block even if some checks pass.

## Production Mindset

Answer evaluation is not grammar checking. It is product risk evaluation.

A concise answer that drops a required condition can be dangerous. A cited answer with the wrong source can mislead reviewers. A refusal that happens too often can make the product unusable.
