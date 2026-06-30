# Post 01 — What is RAG?

**Theme:** Education — core concept
**Target audience:** Professionals curious about AI, non-technical and semi-technical
**Posting week:** Week 1
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

Most AI chatbots hallucinate because they're answering from memory.

RAG fixes this. Here's how it works in plain English:

---

**The problem:**

You ask ChatGPT "What's our company's leave policy?" — it guesses.

It doesn't know your policy. It makes something up that sounds right.

---

**What RAG does differently:**

→ Step 1 — Store your documents in a vector database
(a database that understands *meaning*, not just keywords)

→ Step 2 — When a question comes in, find the most relevant chunks from your documents

→ Step 3 — Hand those chunks to the LLM and say:
*"Answer ONLY from this. Don't guess."*

The LLM becomes a reasoning engine over **your** data — not a guesser.

---

**Real numbers from my project:**

- 12 banking policy documents loaded
- 111 chunks stored in ChromaDB
- 86.7% retrieval accuracy on a 15-question test set

The system retrieves the right policy section 13 out of 15 times —
and it tells you *which document* it used to answer.

That's the difference between a chatbot and a trustworthy internal assistant.

---

Full code is open source — build it yourself or study the architecture:
🔗 https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc

What problem in your organisation could RAG solve?

---

## Notes

- **Hook:** Opens with the core pain (hallucination) before introducing the solution
- **Format:** Short paragraphs, arrows for steps — optimised for LinkedIn mobile
- **CTA:** Question at the end to drive comments
- **Hashtags to add before posting:** `#AI #RAG #LLM #MachineLearning #BuildInPublic #OpenSource`
