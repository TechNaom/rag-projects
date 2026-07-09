# Chapter 3 Interview Questions

## 1. What does "types of RAG" mean?
Strong answer: It means architecture patterns for different retrieval and answer needs.
Red flag: "RAG is one fixed architecture."
Follow-up: When is naive RAG enough?
What this proves: You can classify patterns.

## 2. What is naive RAG?
Strong answer: Top-k retrieval plus generation, usually without advanced correction or routing.
Red flag: "Naive means useless."
Follow-up: Give a good use case.
What this proves: You respect simplicity.

## 3. What makes RAG advanced?
Strong answer: Better chunking, metadata, hybrid search, reranking, compression, evals, and grounding controls.
Red flag: "A bigger model."
Follow-up: Which improvement would you add first?
What this proves: You know concrete upgrades.

## 4. What is corrective RAG?
Strong answer: A pattern that detects weak evidence and retries, refuses, or escalates.
Red flag: "It always fixes itself."
Follow-up: What signal triggers correction?
What this proves: You understand failure handling.

## 5. What is adaptive RAG?
Strong answer: Routing queries to different retrieval paths based on intent, risk, or complexity.
Red flag: "Every query gets the most expensive pipeline."
Follow-up: What are routing signals?
What this proves: You can optimize cost and quality.

## 6. What is agentic RAG?
Strong answer: RAG with planning, tool use, follow-up questions, and controlled actions.
Red flag: "Let the agent do anything."
Follow-up: What guardrail is essential?
What this proves: You know workflow risk.

## 7. What is graph RAG?
Strong answer: RAG that uses entities and relationships when connected knowledge matters.
Red flag: "Graph RAG is always better."
Follow-up: When is it overkill?
What this proves: You understand relationship-heavy domains.

## 8. What is multimodal RAG?
Strong answer: Retrieval over text plus images, tables, slides, audio, or video.
Red flag: "Convert everything blindly to text."
Follow-up: What eval would you add?
What this proves: You understand source format complexity.

## 9. How do you choose a RAG type?
Strong answer: Start from product risk, corpus shape, user workflow, eval needs, latency, and cost.
Red flag: "Use the newest architecture."
Follow-up: Give a decision example.
What this proves: You are product-minded.

## 10. Why not always use agentic RAG?
Strong answer: It adds cost, latency, unpredictability, tool risk, and debugging complexity.
Red flag: "Agents are always more advanced."
Follow-up: When is an agent justified?
What this proves: You understand trade-offs.

## 11. How does evaluation change by RAG type?
Strong answer: Naive RAG needs source recall; graph RAG needs relationship recall; agentic RAG needs tool-use evals.
Red flag: "Same evals for all."
Follow-up: What eval for corrective RAG?
What this proves: You connect architecture to validation.

## 12. What is the most common architecture mistake?
Strong answer: Overbuilding before proving the simple baseline fails.
Red flag: "Complexity is maturity."
Follow-up: How do you prove baseline failure?
What this proves: You have engineering discipline.

## 13. What is modular RAG?
Strong answer: A design where ingestion, retrieval, reranking, prompting, safety, and evals are separate components.
Red flag: "A single script with many features."
Follow-up: Why modularize?
What this proves: You can design maintainable systems.

## 14. What production risk appears in graph RAG?
Strong answer: Wrong entity resolution or missing relationship edges can produce wrong conclusions.
Red flag: "Graphs make truth automatic."
Follow-up: How would you test it?
What this proves: You understand graph failure.

## 15. What production risk appears in adaptive RAG?
Strong answer: Wrong routing can send a high-risk question down a weak path.
Red flag: "Routing is always accurate."
Follow-up: What logs matter?
What this proves: You understand routing risk.

## 16. What should be logged for architecture selection?
Strong answer: Intent, selected path, reason, sources, scores, answer status, refusal reason, latency, and cost.
Red flag: "Only final answer."
Follow-up: Which log helps improve routing?
What this proves: You think operationally.

## 17. When is hybrid search useful?
Strong answer: When exact terms and semantic meaning both matter.
Red flag: "Vector search always wins."
Follow-up: What is a policy example?
What this proves: You understand retrieval strategy.

## 18. When is corrective RAG useful?
Strong answer: When unsupported answers are risky and the system needs confidence checks.
Red flag: "When we want the answer to sound better."
Follow-up: What correction action would you use?
What this proves: You understand safety.

## 19. How do you explain RAG types to a PM?
Strong answer: They are product operating modes: simple answer, safer answer, routed answer, action-taking answer, relationship-aware answer.
Red flag: "Technical jargon only."
Follow-up: What metric matters to PM?
What this proves: You can translate architecture.

## 20. What should Chapter 3 project prove?
Strong answer: That the learner can choose and justify a RAG type using risk, corpus, workflow, and evals.
Red flag: "It prints architecture names."
Follow-up: What output artifact matters?
What this proves: You value decision quality.
