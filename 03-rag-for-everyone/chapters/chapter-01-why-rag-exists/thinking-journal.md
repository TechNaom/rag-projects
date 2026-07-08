# GenAI Thought-Process Journal: Chapter 1

Use this journal to practice the builder mindset behind RAG. The point is not
to copy an AI answer. The point is to learn how to frame, test, critique, and
improve an AI system.

## 1. Problem Frame

What problem are we solving?

> We need an assistant that can answer questions from trusted policy documents,
> not from model memory or guesses.

Why is this a RAG problem?

- The answers may be private to an organization.
- The answers must cite source documents.
- The assistant should refuse when the policy corpus does not contain the answer.
- The system needs to be evaluated against known questions.

## 2. Prompt Frame

Draft the behavior we want from the assistant:

```text
Answer only from the provided policy excerpts.
If the context does not contain the answer, say that clearly.
Cite the policy document used.
Be precise with numbers, deadlines, and thresholds.
```

## 3. Assumptions

Write assumptions before testing:

- The corpus contains the relevant policy.
- The chunker preserves enough section context.
- The retriever can find the correct source in the top results.
- The prompt will prevent unsupported answers.

## 4. Test Questions

Use questions that reveal whether RAG is actually working:

- "How many vacation days do I get after 5 years here?"
- "Can I report fraud directly to the SEC?"
- "What training do branch tellers need?"
- "Can I ask the assistant for stock advice?"

## 5. Critique

After running the system, ask:

- Did retrieval find the right source?
- Did the answer cite the source?
- Did the answer invent anything not in context?
- Did the system refuse out-of-scope questions?
- Did a failure point to chunking, embeddings, retrieval, prompt design, or missing data?

## 6. Decision Log

Record one engineering decision:

```text
Decision:
Why:
Evidence:
Trade-off:
Follow-up test:
```

Example:

```text
Decision: Keep TF-IDF + SVD embeddings for the first public version.
Why: It works offline and makes constraints visible to learners.
Evidence: Recall@3 is 86.7% on the golden retrieval set.
Trade-off: It misses some paraphrased training questions.
Follow-up test: Add a reranking or neural embedding chapter and compare eval results.
```

## 7. Reflection

What did this teach you about building with GenAI?

- Good prompts are not enough if retrieval fails.
- Confident answers need evidence.
- Failures are learning assets when captured as eval cases.
- The builder owns the judgment, even when AI helps with implementation.

