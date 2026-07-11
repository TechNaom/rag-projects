# Post 06 — Why I Built This for Banking

**Theme:** Domain framing
**Target audience:** People evaluating which industry/domain to build their portfolio project in; engineers curious about regulated-industry AI
**Posting week:** Week 6
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

🏦 I could've built this RAG project on movie reviews, or recipes, or some other dataset that's easy to find. I picked banking compliance instead. On purpose.

Here's why the domain you pick matters as much as the code you write. 👇

---

**The lazy version of this project 😴**

Most RAG tutorials use whatever dataset is easiest to download — Wikipedia dumps, product reviews, some public FAQ. Nothing wrong with that for learning the mechanics. But it doesn't teach you the part that actually shows up in real jobs: **what happens when being wrong has a cost.**

---

**Why internal policy Q&A, specifically 🎯**

It's one of the most common real-world RAG deployments inside banks — alongside RM/advisor copilots and underwriting assistants. And it's one of the easiest domains to build *honestly*, because:

✔️ The documents are self-contained — no external knowledge required
✔️ The questions have unambiguous correct answers — you can actually measure accuracy
✔️ There's zero pretense of giving regulated financial advice to a real customer — this is an internal HR/compliance assistant, not a robo-advisor

---

**What made it feel real, not generic 📄**

I built a corpus that's deliberately a blend: generic HR content (leave policy, benefits, performance reviews) *plus* banking-specific compliance material — insider trading policy, customer NPI handling, AML training requirements, whistleblower protections under Dodd-Frank and Sarbanes-Oxley.

That mix is what makes it read as "a bank's internal knowledge base" instead of a generic company FAQ with a banking label stuck on it.

To be direct: **Northkeep National Bank doesn't exist.** Every document, employee, and policy is fictional, invented specifically for this project. Nothing here represents or is modeled on any real financial institution.

---

**Why the domain choice changes the engineering 🔍**

Pick a regulated domain and design decisions stop being abstract:

- Every answer needs a source citation — "trust me" isn't good enough when the topic is compliance
- Retrieval failures aren't just annoying, they're a specific, named risk (imagine a wrong answer about insider trading rules)
- "What would change for production" has real answers: access control by role (a branch teller shouldn't retrieve Wealth Management compliance content), audit logging on every query, human review triggers on regulatory-threshold answers

None of that shows up if your dataset is movie reviews.

---

**The actual point 💡**

The domain isn't set dressing. It's what forces you to build the parts of RAG that tutorials skip — evaluation, traceability, and "what happens when this is wrong."

---

🔗 Full project, fictional bank and all:
[github.com/TechNaom/rag-projects](https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc)

👇 If you were picking a domain for your next AI portfolio project, what would you choose — and why?

---

*#RAG #GenAI #BankingTech #FinTech #Compliance #AIEngineering #BuildInPublic #MachineLearning*

---

## Carousel Storyboard

> Build this in Canva — 9 slides, ~18 minutes.
> Suggested color palette: **Deep navy (#0A1628) + Electric blue (#0066FF) + White (#FFFFFF)** — consistent with the other 01-policy-rag-poc posts.
> Font: Bold sans-serif (Poppins or Inter recommended)

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Big text (white, bold):**
> "I could've used movie reviews. I picked banking compliance."

**Subtext (electric blue):**
> "The domain you pick matters as much as the code."

---

### Slide 2 — The Lazy Version

**Background:** Off-white
**Heading:** "What most RAG tutorials do 😴"
**Body:**
> Wikipedia dumps. Product reviews. Whatever's easiest to download.
>
> Fine for mechanics. Teaches nothing about what happens when being wrong has a cost.

---

### Slide 3 — Why This Domain

**Background:** Navy
**Heading (electric blue):** "Internal policy Q&A 🎯"
**Body (white):**
> ✔️ Self-contained documents
> ✔️ Unambiguous correct answers — measurable
> ✔️ No pretense of real customer financial advice

---

### Slide 4 — The Corpus

**Background:** Off-white
**Heading:** "A deliberate blend 📄"
**Body:**
> Generic HR policy + banking-specific compliance —
> insider trading, NPI handling, AML training, Dodd-Frank whistleblower protections.

---

### Slide 5 — The Disclaimer, Upfront

**Background:** Navy
**Heading (electric blue):** "To be direct ⚠️"
**Body (white):**
> Northkeep National Bank doesn't exist.
> Every document and policy is fictional, invented for this project.

---

### Slide 6 — Why the Domain Changes the Engineering

**Background:** Off-white
**Heading:** "Regulated domains force real decisions 🔍"
**Body:**
> Citations aren't optional.
> Retrieval failures become named risks.
> "Production-ready" has to mean something specific.

---

### Slide 7 — What Production Would Add

**Background:** Navy
**Heading (electric blue):** "What changes for production"
**Body (white):**
> 🔐 Role-based access control
> 📝 Audit logging on every query
> 🚩 Human review on regulatory-threshold answers

---

### Slide 8 — The Actual Point

**Background:** Off-white
**Heading:** "The domain isn't set dressing 💡"
**Body:**
> It's what forces you to build the parts tutorials skip —
> evaluation, traceability, consequence.

---

### Slide 9 — CTA

**Background:** Electric blue
**Heading (white, bold):**
> "See the full fictional-bank project."

**Link (white, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 What domain would YOU pick for your next AI project?

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait) |
| Slides | 9 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
| Accuracy note | Keep the fictional-bank disclaimer explicit and early in both the post and slide 5 — this project's credibility depends on never reading as if it represents a real institution. |
