# Post 03 — The Honest Build

**Theme:** Credibility — showing failures
**Target audience:** Engineers and builders who are tired of polished AI demos that hide the hard parts
**Posting week:** Week 3
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

🚧 My RAG system can't download an embedding model.

Not "chose not to." Can't. The sandbox it's built in blocks huggingface.co at the network layer. No sentence-transformers. No hosted embeddings API either.

Most tutorials would just... not mention this. Here's what I actually did. 👇

---

**The constraint 🔒**

A production RAG system uses a neural embedding model — local (sentence-transformers) or hosted (OpenAI, Voyage AI). That's step one in basically every RAG tutorial on the internet.

I couldn't do step one.

---

**The tempting shortcut 😅**

I could've faked it. Hardcoded some "results." Written the README like the constraint never happened. Nobody reviewing a portfolio project checks that closely.

I didn't, because the constraint *is* the interesting part.

---

**What I built instead 🛠️**

A fully local, pip-only embedding method: TF-IDF vectorization reduced to a 128-dimension dense vector via Truncated SVD — classic Latent Semantic Analysis, from before deep learning existed.

It's legitimate. It's just **lexical, not semantic** — it matches shared vocabulary, not paraphrased meaning. "Vacation" and "annual leave" don't automatically land close together the way they would with a neural embedding.

---

**Where it actually broke 📉**

I ran a 15-question golden evaluation set. Recall@3: 86.7% (13/15). Two real misses:

*"What training do branch tellers need that other employees don't?"*
*"Is workplace harassment training mandatory?"*

Both failed to retrieve the training policy doc. Why? Almost every policy document *mentions* training somewhere in its closing section. A lexical method can't tell "mentions training" apart from "is about training." A neural embedding — or a reranking step — would catch this instantly.

---

**Why I'm posting the failure, not hiding it 💡**

A demo where everything works perfectly isn't a demo. It's marketing.

An 86.7% recall with two explainable, specific misses tells you more about how RAG actually behaves than a cherry-picked "look, it works!" screenshot ever could.

---

**The actual lesson 🎯**

I built one clearly marked swap-in point in the code — the exact snippet to drop in `HuggingFaceEmbeddings` or `VoyageAIEmbeddings` the moment this runs somewhere with network access. Nothing else in the pipeline changes, because everything talks to the embedder through one standard interface.

That pluggability — designing so the workaround can be *removed* later without a rewrite — is the real skill. Not the workaround itself.

---

🔗 Full project, including the eval results and the swap-in code:
[github.com/TechNaom/rag-projects](https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc)

👇 What's a constraint you had to build around instead of away? Genuinely curious what other people's version of this looks like.

---

*#RAG #GenAI #SoftwareEngineering #BuildInPublic #MachineLearning #AIEngineering #OpenSource #LLM*

---

## Carousel Storyboard

> Build this in Canva — 9 slides, ~18 minutes.
> Suggested color palette: **Deep navy (#0A1628) + Electric blue (#0066FF) + White (#FFFFFF)** — same palette as Post 01, keeps the RAG project posts visually consistent.
> Font: Bold sans-serif (Poppins or Inter recommended)

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Big text (white, bold):**
> "My RAG system can't download an embedding model."

**Subtext (electric blue):**
> "Here's what I built instead — and where it broke."

---

### Slide 2 — The Constraint

**Background:** Dark red-tinted navy (tension feel)
**Heading:** "The sandbox blocks huggingface.co 🔒"
**Body:**
> No sentence-transformers.
> No hosted embeddings API either.
>
> Step one of every RAG tutorial — off the table.

---

### Slide 3 — The Tempting Shortcut

**Background:** Off-white
**Heading:** "I could've faked it. 😅"
**Body:**
> Hardcode some results.
> Write the README like it never happened.
>
> I didn't. The constraint is the interesting part.

---

### Slide 4 — What I Built

**Background:** Navy
**Heading (electric blue):** "TF-IDF + Truncated SVD 🛠️"
**Body (white):**
> Fully local. Pip-only.
> Classic Latent Semantic Analysis — pre-deep-learning, but legitimate.
>
> Lexical, not semantic. That distinction matters.

---

### Slide 5 — Where It Broke

**Background:** Off-white
**Heading:** "Recall@3: 86.7% (13/15) 📉"
**Body:**
> Two misses — both training-related questions.
> Cause: nearly every doc *mentions* training in passing.
> Lexical search can't tell "mentions" from "is about."

---

### Slide 6 — Why Post the Failure

**Background:** Navy
**Heading (electric blue):** "A perfect demo isn't a demo. 💡"
**Body (white):**
> It's marketing.
>
> Two explainable misses teach you more about RAG than a cherry-picked screenshot ever will.

---

### Slide 7 — The Actual Lesson

**Background:** Off-white
**Heading:** "Design for the swap, not just the workaround 🎯"
**Body:**
> One clearly marked point in the code to drop in a real embedding model.
> Nothing else changes.
>
> That's the skill — not the workaround itself.

---

### Slide 8 — Real Numbers Recap

**Background:** Navy
**Heading (electric blue):** "The honest numbers 📊"
**Stats:**
> 📄 12 policy documents, 111 chunks
> ✅ 86.7% Recall@3, MRR 0.789
> ❌ 2 explainable misses
> 🔌 1 swap-in point, zero pipeline rewrite

---

### Slide 9 — CTA

**Background:** Electric blue
**Heading (white, bold):**
> "Read the honest build, not the highlight reel."

**Link (white, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 What constraint did YOU have to build around?

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait — more feed space) |
| Slides | 9 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
| Tone note | This post's entire credibility rests on being specific about the failure (exact recall number, exact two questions, exact cause). Do not soften or generalize these numbers when adapting the copy. |
