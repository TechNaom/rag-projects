# Practice Bank: Why RAG Exists

This practice bank is intentionally production-minded. Do not stop at "RAG
means retrieve then generate." Practice deciding when RAG is useful, what can go
wrong, and what a serious builder would test.

## Scenario 1: HR Policy Assistant

An employee asks, "How many paid weeks do I get if I am not the primary parent?"

- Should this use model memory, web search, or RAG?
- What source should be retrieved?
- What would a bad answer look like?

## Scenario 2: Customer Support Refund Bot

A customer asks about a refund policy that changes by country and product tier.

- What metadata would you need?
- What should the assistant cite?
- What should happen if the policy is missing?

## Scenario 3: Sales Enablement Assistant

A salesperson asks, "Can I promise this enterprise discount to a healthcare
customer?"

- Why is this not a generic model-memory question?
- What approval or policy document should be retrieved?
- What risk appears if the answer is unsupported?

## Scenario 4: Security Runbook Assistant

An engineer asks, "What is the first step when a production API key is leaked?"

- What source should the system retrieve?
- What access controls might apply?
- What would you log for audit?

## Scenario 5: Legal Contract Assistant

A product manager asks whether a customer contract allows model-output logging.

- What clauses should be retrieved?
- What should the assistant refuse to decide?
- When should it escalate to legal review?

## Scenario 6: Healthcare Knowledge Assistant

A clinician asks for policy guidance about handling patient data in a demo.

- What makes this high-risk?
- What sources and permissions matter?
- What should be reviewed by a human?

## Scenario 7: Engineering Design Assistant

A platform engineer asks, "What are our latency targets for the checkout RAG
assistant?"

- Is this RAG, search, or model memory?
- What system-design document should be retrieved?
- What metrics would you compare?

## Scenario 8: Finance Compliance Assistant

An analyst asks, "Can this report include customer account identifiers?"

- What compliance policy should be retrieved?
- What answer shape would reduce risk?
- What would you include in the audit trail?

## Scenario 9: Developer Documentation Assistant

A developer asks why a deployment failed after a new environment variable was
added.

- Which docs, logs, or runbooks could be retrieved?
- What is outside pure RAG and closer to tool use?
- What would the assistant ask next?

## Scenario 10: RAG Failure Case

The assistant retrieves three chunks, all from the wrong policy, but still gives
a confident answer.

- What failed first: retrieval, prompting, or UI?
- What eval case would you add?
- What engineering change would you test next?
