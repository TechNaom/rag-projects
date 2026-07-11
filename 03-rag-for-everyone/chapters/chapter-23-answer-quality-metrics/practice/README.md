# Practice Bank: Answer Quality Metrics

Use failure symptoms to decide what went wrong and what to inspect first.

## Diagnosis Map

- Unsupported claim: faithfulness failure.
- Related but wrong citation: citation correctness failure.
- Faithful but incomplete answer: completeness failure.
- Refusal with enough evidence: false refusal.
- Answer without enough evidence: missed refusal.
- High-risk serious failure: release gate should block.

## What To Return

For every failure, return:

- labels
- severity
- first engineering action
- release decision

The goal is to make answer evaluation operational. A score without a next action is just decoration.
