# Interview Questions: Answer Quality Metrics

1. What is the difference between faithfulness and relevance?
   - Faithfulness checks whether the answer is supported by evidence.
   - Relevance checks whether the answer solves the user's actual task.

2. What is groundedness?
   - Groundedness means the answer can be traced to source chunks, citations, versions, and authority metadata.

3. Why is citation correctness more important than citation presence?
   - A citation can exist but still fail to support the claim. Production review must check claim-to-citation support.

4. What are false refusals and missed refusals?
   - A false refusal happens when the system refuses despite enough evidence.
   - A missed refusal happens when the system answers despite insufficient evidence or policy risk.

5. What should an answer-quality rubric include?
   - Faithfulness, relevance, citation support, completeness, refusal correctness, safety, severity, and release decision.

6. How do you prevent reviewer drift?
   - Use examples, calibration rounds, disagreement reviews, and clear pass/warn/block definitions.

7. How do answer metrics connect to retrieval metrics?
   - Retrieval metrics show whether evidence was available. Answer metrics show whether the model used it correctly.

8. Which failures should block release?
   - High-risk unsupported claims, contradicted claims, missed refusals, unsafe guidance, and serious citation-support regressions.

9. Why keep an incident replay set?
   - It prevents historical answer-quality failures from returning after prompt, model, retriever, or corpus changes.

10. What is a senior-level answer quality strategy?
    - Separate quality dimensions, score with calibrated rubrics, slice by risk and workflow, keep score traces, and gate releases by severity.
