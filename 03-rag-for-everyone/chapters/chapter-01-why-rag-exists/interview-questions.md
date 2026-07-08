# Chapter 1 Interview Questions

## 1. What problem does RAG solve?

Strong answer: RAG lets an AI system answer from trusted external context
instead of relying only on model memory. It is especially useful for private,
current, or domain-specific knowledge where citation and traceability matter.

Red flag: "RAG just makes the model smarter."

Follow-up: When would long context be enough, and when would retrieval still be
better?

## 2. Why are citations important in policy assistants?

Strong answer: Citations let users and reviewers verify that the answer came
from the approved policy source. They also support auditing, debugging, and
compliance review.

Red flag: "The model is usually right, so citations are optional."

Follow-up: What should the assistant do if the retrieved context does not
contain the answer?

## 3. Why can a good prompt still produce a bad RAG answer?

Strong answer: If retrieval fails, the prompt may receive irrelevant or missing
context. The generation step can only be as grounded as the evidence it sees.

Red flag: "Just tell the model not to hallucinate."

Follow-up: Which metrics would you use to evaluate retrieval?

