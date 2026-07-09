# Thinking Journal: RAG Execution Pipelines

Use this after the project.

## Prompt to try

> You are reviewing a production RAG pipeline. Given this trace, identify the first failed gate, the likely root cause, and the safest next action. Do not recommend answering if required evidence is missing.

## Reflection

1. Which stage failed first?
2. Was the issue offline, online, or answer-policy related?
3. Which trace field made the failure visible?
4. What would have been impossible to debug without the trace?
5. What release gate would prevent this issue next time?

## Builder note

The goal is not to make GenAI sound confident. The goal is to make the system inspectable enough that confidence can be earned.
