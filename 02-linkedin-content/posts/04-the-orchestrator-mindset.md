# Post 04 — The Orchestrator Mindset

**Theme:** Mindset — AI + human collaboration
**Target audience:** People deciding whether to learn to code deeply vs. learn to direct AI systems well; engineering leaders thinking about how roles are shifting
**Posting week:** Week 4
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

🎯 I didn't write most of the code in this RAG system line by line. I directed it.

That sentence used to feel like a confession. I've stopped treating it like one. Here's why. 👇

---

**The old model of "real" engineering 🧱**

For a long time, "being technical" meant: you personally type every line, you personally hold the whole implementation in your head, and if you didn't, you weren't really the one who built it.

That model made sense when writing code *was* the bottleneck.

---

**What actually happened building this project 🛠️**

I made the architecture decisions. Markdown-header-aware chunking, not naive fixed-size splitting. ChromaDB over a plain vector list. A clean interface boundary so the embedding model could be swapped without touching the rest of the pipeline. Two generation providers, chosen deliberately — Ollama for zero-cost local runs, Groq for fast hosted inference when I needed it.

I didn't hand-type every function. I specified what each piece needed to do, reviewed what came back, caught what was wrong, and redirected. Repeatedly. That loop — decide, delegate, verify, correct — was the actual work.

---

**Where the real skill moved 🧠**

Writing syntax was never the hard part of engineering. Knowing *what* to build, *why* a design choice matters, and *whether* the output in front of you is actually correct — that was always the hard part. It just used to be hidden inside the hours it took to type everything out by hand.

Take the hours away, and what's left is the actual skill: judgment.

---

**The part that still has to be yours 🔍**

When my evaluation suite came back at 86.7% recall with two specific misses, no AI tool told me that was good enough — or that it wasn't. I had to know what "good" means for a policy Q&A system, decide the two misses were explainable and acceptable for a POC, and write down exactly what a production fix would look like.

That judgment call doesn't get automated. It's the actual job.

---

**This isn't "AI replaces engineers" 🚫**

It's closer to: the job was always "know what correct looks like and verify it ruthlessly." Typing was just the visible 80% that used to hide the invisible 20% that actually mattered.

I'd rather be honest about which 20% I did.

---

🔗 The project this mindset built, fully open source:
[github.com/TechNaom/rag-projects](https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc)

👇 Where do you land on this? Genuinely asking — I know this is a live debate right now, not a settled one.

---

*#AI #SoftwareEngineering #FutureOfWork #GenAI #BuildInPublic #Leadership #TechCareers*

---

## Carousel Storyboard

> Build this in Canva — 8 slides, ~16 minutes.
> Suggested color palette: **Deep navy (#0A1628) + Electric blue (#0066FF) + White (#FFFFFF)** — consistent with the other 01-policy-rag-poc posts.
> Font: Bold sans-serif (Poppins or Inter recommended)

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Big text (white, bold):**
> "I didn't write most of this code line by line."

**Subtext (electric blue):**
> "I directed it. Here's why that's not a confession."

---

### Slide 2 — The Old Model

**Background:** Off-white
**Heading:** "Being 'technical' used to mean one thing 🧱"
**Body:**
> You personally typed every line.
> If you didn't, you didn't really build it.
>
> That made sense when typing was the bottleneck.

---

### Slide 3 — What I Actually Did

**Background:** Navy
**Heading (electric blue):** "The decisions were mine 🛠️"
**Body (white):**
> Markdown-aware chunking, not naive splitting.
> A swappable embedding interface.
> Two generation providers, chosen deliberately.

---

### Slide 4 — The Real Loop

**Background:** Off-white
**Heading:** "Decide → delegate → verify → correct 🔁"
**Body:**
> Repeated, constantly.
> That loop was the actual work — not the typing.

---

### Slide 5 — Where the Skill Moved

**Background:** Navy
**Heading (electric blue):** "Syntax was never the hard part 🧠"
**Body (white):**
> Knowing what to build, and whether the output is right —
> that was always the real skill.
> It was just hidden inside hours of typing.

---

### Slide 6 — The Part That's Still Mine

**Background:** Off-white
**Heading:** "86.7% recall. Good enough? 🔍"
**Body:**
> No AI tool tells you that.
> I had to decide what "good" means here — and write down what production needs.

---

### Slide 7 — Not a Replacement Story

**Background:** Navy
**Heading (electric blue):** "This isn't 'AI replaces engineers' 🚫"
**Body (white):**
> It's: the job was always judgment.
> Typing just used to hide that.

---

### Slide 8 — CTA

**Background:** Electric blue
**Heading (white, bold):**
> "I'd rather be honest about which 20% I did."

**Link (white, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 Where do you land on this? I'm genuinely asking.

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait) |
| Slides | 8 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
| Tone note | This is a mindset/opinion post, not a technical deep-dive — it will draw disagreement in the comments. That's fine, even good; the closing question is written to invite it, not avoid it. Don't soften the framing to preempt pushback. |
