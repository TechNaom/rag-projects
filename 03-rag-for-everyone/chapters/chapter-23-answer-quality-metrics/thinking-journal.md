# GenAI Thought Process Journal: Answer Quality

Use this journal after the lesson and project. The goal is to think like the person responsible for shipping the answer safely.

## Reflection Prompts

1. Which claims in your answer need citation support?
2. Which answer-quality failure would be most dangerous in your domain?
3. What should be deterministic, and what needs human review?
4. Which cases belong in your incident replay set?
5. What would make a high average score misleading?
6. Which answer failures should block release even if other checks pass?
7. How would you explain false refusals to a product manager?
8. How would you explain missed refusals to a security or legal reviewer?

## Builder Notes

- Do not treat answer scoring as style checking.
- Start with source support, then usefulness, then safety.
- Store traces so a future release can be debugged.
- Calibrate reviewers with examples before trusting human labels.
