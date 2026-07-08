# Chapter 1 Project: Production RAG Architecture Brief

Pick one of the scenarios below and write a short architecture brief. This is
not a toy write-up. Write it like you are explaining a real system to an
engineering manager, product owner, or platform review board.

## Scenario Options

1. **Northkeep HR & Compliance Assistant**: employees ask leave, benefits,
   whistleblower, privacy, and expense-policy questions.
2. **Customer Support Refund Assistant**: support agents need country-specific,
   product-tier-specific refund policy answers.
3. **Security Incident Runbook Assistant**: engineers ask what to do during API
   key leaks, suspicious access, and production incidents.
4. **Sales & Contract Risk Assistant**: sales teams ask what they can promise
   based on approved pricing, contract, and compliance rules.
5. **Developer Platform Assistant**: engineers ask deployment, environment,
   runbook, and troubleshooting questions from internal docs.

## Your Architecture Brief Must Cover

1. User and risk profile.
2. Trusted source documents.
3. Metadata needed for retrieval and access control.
4. Retrieval flow.
5. Prompt rules and refusal behavior.
6. Evaluation cases and metrics.
7. Human escalation path.
8. One engineering decision you would make next.

## Deliverable

Complete `starter.py` so it prints your architecture brief. Use `solution.py`
as one reference version, not the only valid answer.
