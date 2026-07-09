# Chapter 2 Project: Build a Traceable RAG Lifecycle Simulator

Build a small Python simulator that shows how a RAG request moves through an
execution pipeline. This is not yet a full vector database implementation. It is
the production mental model: each stage produces a trace you can inspect.

## Requirements

Your simulator should:

1. Accept a user question.
2. Classify intent.
3. Build a retrieval query.
4. Apply metadata filters.
5. Select candidate sources.
6. Assemble context.
7. Decide answer, refusal, or escalation.
8. Return citations.
9. Emit a trace log.
10. Include at least one golden eval.

## Production Scenarios

- HR policy assistant.
- Customer refund bot.
- Security incident runbook assistant.
- Developer documentation assistant.
- Contract-risk assistant.

## Success Criteria

The project is successful when another engineer can read the trace and understand
why the assistant answered, refused, or escalated.
