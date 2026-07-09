# Practice Bank: The RAG Query Lifecycle

Use these scenarios to practice lifecycle judgment. For each one, write:

- user intent
- retrieval query
- metadata filters
- expected sources
- context assembly rule
- answer/refusal rule
- logs to capture
- metric to inspect first

## Scenario 1: HR Leave Policy

An employee asks about parental leave after moving from the US to Germany.

## Scenario 2: Customer Refund Bot

A customer asks for a refund, but eligibility depends on product tier, country,
purchase date, and policy version.

## Scenario 3: Security Runbook

An engineer asks what to do when a production API key is leaked.

## Scenario 4: Developer Docs

A developer asks why a deployment failed after a new environment variable.

## Scenario 5: Contract Assistant

A product manager asks whether a customer contract allows model-output logging.

## Scenario 6: Sales Enablement

A seller asks if they can promise a restricted enterprise discount.

## Scenario 7: Healthcare Demo

A clinician asks whether real patient data can be used in a product demo.

## Scenario 8: Finance Compliance

An analyst asks whether customer account identifiers can be included in a report.

## Scenario 9: Stale Policy

The assistant answers from last quarter's policy after the index missed a new
upload.

## Scenario 10: Wrong Reranking

Hybrid search retrieves the right document, but reranking pushes it below the
context cutoff.

## Scenario 11: Access-Control Leak

The retrieved context includes a confidential contract clause the user should
not be able to see.

## Scenario 12: Multi-Hop Question

The user asks a question that needs both the incident runbook and the customer
communication template.
