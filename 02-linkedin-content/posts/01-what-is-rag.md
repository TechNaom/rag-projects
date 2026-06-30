# Post 01 — What is RAG?

**Theme:** Education — core concept
**Target audience:** Professionals curious about AI, non-technical and semi-technical
**Posting week:** Week 1
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

🚨 Your AI chatbot is lying to you.

Not maliciously. It just doesn't know your data — so it guesses.

There's a fix. It's called **RAG**.
And once you understand it, you'll never look at AI the same way again. 👇

---

**The problem with standard AI 🤖**

You ask ChatGPT:
*"What's our company's leave policy?"*

It has no idea. It's never seen your policy.

So it does what it always does —
it generates something that *sounds* right.

That's hallucination. And in a bank? That's a compliance risk.

---

**What RAG does differently ⚡**

RAG = Retrieval Augmented Generation

Three steps. That's it.

→ 📂 **Step 1 — Store** your documents in a vector database
*(a database that understands meaning, not just keywords)*

→ 🔍 **Step 2 — Retrieve** the most relevant chunks when a question arrives

→ 🧠 **Step 3 — Generate** an answer grounded ONLY in what was retrieved
*"Answer from this. Don't guess."*

Your LLM stops hallucinating.
It becomes a reasoning engine over **your** data.

---

**Real numbers. Real project. 📊**

I built this for a fictional bank — Northkeep National Bank.
12 policy documents. HR + compliance content.

Results:
✅ 111 document chunks stored in ChromaDB
✅ 86.7% retrieval accuracy
✅ 13 out of 15 test questions answered correctly
✅ Every answer cites *which document* it came from

That last part matters most.
Traceability = trust. And trust is everything in regulated industries.

---

**The bottom line 💡**

RAG isn't just a technique.

It's the bridge between a generic AI
and an AI that actually knows your business.

---

🔗 Full open source project — build it yourself:
[github.com/TechNaom/rag-projects](https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc)

👇 What problem in your organisation could RAG solve? Drop it in the comments.

---

*#AI #RAG #GenerativeAI #LLM #BankingTech #MachineLearning #BuildInPublic #OpenSource #ArtificialIntelligence #FinTech*

---

## Carousel Storyboard

> Build this in Canva — 10 slides, ~20 minutes.
> Suggested color palette: **Deep navy (#0A1628) + Electric blue (#0066FF) + White (#FFFFFF)**
> Font: Bold sans-serif (Poppins or Inter recommended)

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Big text (white, bold):**
> "Your AI is lying to you."

**Subtext (electric blue):**
> "Here's the fix — RAG explained in 60 seconds"

**Visual:** Glowing brain icon or chat bubble with ❌ on it
**Bottom:** Your name + LinkedIn handle

---

### Slide 2 — The Problem

**Background:** Dark red gradient (danger feel)
**Heading:** "The hallucination problem 🤖"
**Body:**
> You ask your AI chatbot:
> *"What's our leave policy?"*
>
> It has never seen your documents.
> So it makes something up.
> Confidently. Wrongly.

**Visual:** Chat bubble with a ❌ answer highlighted

---

### Slide 3 — What is RAG?

**Background:** Navy
**Heading (electric blue):** "RAG = Retrieval Augmented Generation"
**Body (white):**
> Stop asking AI to guess.
> Start making it READ your documents first.

**Visual:** Simple diagram — Document → Vector DB → LLM → Answer

---

### Slide 4 — Step 1: Store

**Background:** Navy with blue accent left border
**Big number:** "01"
**Heading:** "Store 📂"
**Body:**
> Load your documents into a vector database.
> It doesn't just store words —
> it stores *meaning*.

**Visual:** Document icons flowing into a cylinder (database)

---

### Slide 5 — Step 2: Retrieve

**Background:** Navy with blue accent left border
**Big number:** "02"
**Heading:** "Retrieve 🔍"
**Body:**
> A question comes in.
> The system finds the most relevant chunks
> from your documents — not from the internet.

**Visual:** Magnifying glass over document chunks, top 3 highlighted

---

### Slide 6 — Step 3: Generate

**Background:** Navy with blue accent left border
**Big number:** "03"
**Heading:** "Generate 🧠"
**Body:**
> Those chunks go to the LLM with one instruction:
> *"Answer ONLY from this. Don't guess."*
>
> Hallucination eliminated.

**Visual:** Chunks → LLM → Clean answer with source citation

---

### Slide 7 — Real Results

**Background:** Dark green (success feel)
**Heading:** "Real project. Real numbers. 📊"
**Stats (large, bold):**
> 📄 12 policy documents
> 🧩 111 chunks indexed
> ✅ 86.7% retrieval accuracy
> 🏦 Built for banking compliance

**Subtext:** "Northkeep National Bank — fictional, but the architecture is real."

---

### Slide 8 — Why it Matters

**Background:** Navy
**Heading:** "Why does this matter? 💡"
**Body:**
> Every answer cites its source document.
>
> In banking, healthcare, legal —
> traceability isn't a nice-to-have.
> It's the whole point.

**Visual:** Answer box with "Source: HR Policy v3.2 — Section 4" citation highlighted

---

### Slide 9 — Where RAG Works Best

**Background:** Navy
**Heading:** "RAG is perfect for... 🎯"
**List:**
> 🏦 Internal policy & compliance Q&A
> ⚕️ Healthcare knowledge bases
> ⚖️ Legal document search
> 🛠️ Product support & documentation
> 📊 Financial research assistants

---

### Slide 10 — CTA

**Background:** Electric blue (stands out)
**Heading (white, bold):**
> "Ready to build your own?"

**Body:**
> Full project is open source.
> Code, docs, evaluation suite — all free.

**Link (white, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 What would YOU build RAG for?
> Comment below ↓

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait — more feed space) |
| Slides | 10 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
