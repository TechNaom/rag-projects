# Project: Answer Quality Scorer

Build a scorer that can be reused in prompt, model, retriever, and corpus release checks.

## What You Will Build

1. A rubric evaluator for generated RAG answers.
2. Checks for:
   - faithfulness
   - relevance
   - citation support
   - completeness
   - refusal correctness
   - safety
3. Severity-based release gates.
4. Slice summaries by domain and risk.
5. Score traces with prompt, model, and corpus versions.

## Production Scenarios

- Policy answer with complete evidence and correct citation.
- High-risk policy answer with unsupported claim.
- Support answer that falsely refuses despite enough evidence.
- Legal answer that should refuse but answers anyway.

## Acceptance Criteria

- High-risk unsupported claims block release.
- Missed refusals in restricted/high-risk scenarios block release.
- False refusals are visible and reviewable.
- Citation support is checked beyond citation presence.
- Output includes a trace that helps debug which release changed behavior.
