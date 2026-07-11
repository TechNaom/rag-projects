# Post 13 — GenAI Deep R&D Journal, Episode #06: Why Chunking Breaks RAG Before the Model Ever Sees the Question

**Theme:** Technical deep-dive / recurring R&D journal series — closing the 6-episode arc by showing that most "model" failures are actually chunking failures in disguise
**Target audience:** Engineers and architects building or evaluating RAG systems; anyone who's blamed the LLM for an answer that was never given the right evidence
**Posting week:** Flexible — sixth and closing entry in this arc of the R&D journal series
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/) — the RAG system this journal draws its real lessons from; also mirrors [03-rag-for-everyone Chapters 9 and 11](../../03-rag-for-everyone/chapters/chapter-09-fixed-and-recursive-chunking/)

---

## LinkedIn Post

🧠 **GenAI Deep R&D Journal | Episode #06**

# 🍕 A Retriever Never Searches Your Document. It Searches the Pieces You Cut It Into.

Five episodes in, we've covered why vector databases exist, why they can't brute-force search, how HNSW makes them fast, what's actually inside an embedding, and dense vs. sparse retrieval.

All of that assumes something we never questioned: that the *chunks* being searched were cut correctly in the first place.

They usually aren't. And it's the most common RAG bug that gets blamed on the model instead.

---

**🍕 The pizza-slice problem**

Slice a pizza into pieces too tiny, and every bite is incomplete. Slice it into one giant piece, and nobody can handle it. Chunking a document works the same way — a chunk should be small enough to retrieve precisely, and large enough to still make sense on its own.

Cut it wrong, and a rule ends up in one chunk while its exception lands in the next one. Retrieval finds the rule. The exception never gets seen. The model didn't hallucinate — it was never shown the whole picture.

---

**✂️ Fixed vs. recursive chunking**

**Fixed chunking** splits by raw size — characters or tokens, often with overlap. Simple, predictable, and blind to structure. It will cut a sentence in half without noticing.

**Recursive chunking** tries structural boundaries first — paragraphs, then sentences, then words, only falling back to a hard cut if nothing else fits. It's structure-aware, and it's usually the safer default for real documents.

Overlap helps protect boundary context either way — but it's not free. Too much overlap means near-duplicate chunks compete for the same retrieval slots and crowd out actually-different evidence.

---

**🩺 When it breaks, don't guess — diagnose**

The instinct when a RAG answer is wrong is "the model hallucinated." A better instinct, borrowed straight from how a doctor works a symptom: ask what evidence the model actually had.

Six named chunking failure modes I've learned to check for, in order:

1. **Lost context** — the chunk has the rule but not the exception around it
2. **Mixed-topic chunks** — one chunk crams refund rules, cancellation steps, and legal notes together, confusing both retrieval and generation
3. **Overlap noise** — near-duplicate chunks crowd the prompt and push out real evidence
4. **Tiny chunks** — fragments of meaning, not usable answers
5. **Giant chunks** — broad matches that bury the one sentence that actually mattered
6. **Stale chunks** — an outdated version wins because freshness metadata was never tracked

---

**🔬 The actual debugging loop**

Capture the bad answer with its full trace — question, retrieved chunks, scores, citations, index version. Check whether the *evidence* was even sufficient before blaming the *reasoning*. Label which of the six failure modes it matches. Then change exactly one variable and re-run the golden query set.

Chunk size is a lever, not a diagnosis. Tuning it blindly can fix one query and break ten others you weren't watching.

---

**🎤 Interview answer (30 seconds)**

*"Chunking directly determines what evidence a retriever can find — it's not formatting, it's a retrieval design decision. Fixed chunking splits by size and is predictable but structure-blind; recursive chunking respects natural boundaries and is usually safer for real documents. When a RAG answer is wrong, the first question isn't 'did the model hallucinate' — it's 'was the right chunk even retrieved,' since most apparent model failures are actually chunking or retrieval failures in disguise."*

---

**💎 My biggest takeaway across this whole arc**

Every episode in this series has been about the same idea from a different angle: a RAG system's quality is decided long before generation happens. Vector databases, embeddings, sparse vs. dense retrieval, chunking — all of it is upstream engineering that determines what the model is even allowed to see. Fix the model's prompt all you want; if the evidence was cut wrong, the answer was never going to be right.

That's six episodes and one real, open-source system to show for it. Thanks for reading this far into the weeds with me.

🔗 The actual RAG system this whole series comes from, fully open source:
github.com/TechNaom/rag-projects

---

*#GenAI #RAG #Chunking #VectorDatabases #LLM #SoftwareArchitecture #AIEngineering #MachineLearning*

---

## Carousel Storyboard

> Build this in Canva — 10 slides, ~19 minutes.
> Suggested color palette: **Deep navy (#101B33) + bright blue (#2E6BB8) + warm yellow accent (#FFC93C)** on off-white (#F6F7FB) — same palette as Episodes #01–#05, closing out the arc visually consistent from start to finish.
> Font: Bold geometric sans for headings (Space Grotesk/Poppins), clean sans-serif for body (Inter).

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Eyebrow (yellow):** GenAI Deep R&D Journal · Episode #06
**Big text (white, bold):**
> "A retriever never searches your document. It searches the pieces you cut it into."

**Subtext (light blue-grey):** The most common RAG bug that gets blamed on the model.

---

### Slide 2 — The Pizza-Slice Problem

**Background:** Off-white
**Heading:** "Cut it wrong, and the rule loses its exception 🍕"
**Body:** Too tiny: every bite is incomplete. Too big: nobody can handle it. Same for chunks.

---

### Slide 3 — Fixed vs. Recursive

**Background:** Deep navy
**Heading (yellow):** "Two ways to cut ✂️"
**Body (white):** Fixed = size-based, predictable, structure-blind. Recursive = tries paragraphs and sentences first, safer for real documents.

---

### Slide 4 — Overlap Isn't Free

**Background:** Off-white
**Heading:** "Overlap protects boundaries — at a cost"
**Body:** Too much overlap means near-duplicate chunks compete for the same retrieval slots.

---

### Slide 5 — Diagnose, Don't Guess

**Background:** Deep navy
**Heading (yellow):** "Ask what evidence the model actually had 🩺"
**Body (white):** "The model hallucinated" is a symptom, not a diagnosis.

---

### Slide 6 — Six Failure Modes

**Background:** Off-white
**Heading:** "Name the failure before you fix it"
**Body:**
> Lost context · Mixed-topic chunks · Overlap noise
> Tiny chunks · Giant chunks · Stale chunks

---

### Slide 7 — The Debugging Loop

**Background:** Deep navy
**Heading (yellow):** "Change one variable at a time 🔬"
**Body (white):** Capture the trace, check the evidence, label the failure, test one fix against golden queries.

---

### Slide 8 — Interview Corner

**Background:** Off-white
**Heading:** "🎤 30-second interview answer"
**Body:** "Was the right chunk even retrieved? — most apparent model failures are actually chunking failures in disguise."

---

### Slide 9 — The Whole Arc, In One Line

**Background:** Deep navy
**Heading (yellow):** "RAG quality is decided before generation ever happens 💎"
**Body (white):** Vector DBs, embeddings, sparse vs. dense, chunking — all upstream of the model.

---

### Slide 10 — CTA / Series Close

**Background:** Warm yellow
**Heading (navy, bold):**
> "Six episodes. One real, open-source system."

**Link (navy, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 Which episode in this series changed how you think about RAG the most?

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait) |
| Slides | 10 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
| Series note | This closes the initial 6-episode arc (vector DBs → brute-force limits → HNSW → embeddings → dense/sparse → chunking). If the series continues, a natural next arc is reranking, evaluation/RAGAS, or production failure modes — don't commit to a specific Episode #07 topic in this post's copy, since the arc intentionally closes on a "biggest takeaway across the whole series" beat rather than teasing forward. |
| Accuracy note | Chunking mechanics, the pizza analogy, and the six failure-mode taxonomy are drawn directly from 03-rag-for-everyone's Chapters 9 and 11 lesson content — keep consistent with both if either chapter is revised. |
