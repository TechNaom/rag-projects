# Post 05 — The API Key Mistake

**Theme:** Security — practical lesson
**Target audience:** Developers and career-switchers who are one `git add .` away from leaking a credential; anyone building their first API-connected project in public
**Posting week:** Week 5
**Source project:** [01-policy-rag-poc](../../01-policy-rag-poc/)

---

## LinkedIn Post

🔑 The mistake isn't leaking an API key. The mistake is designing a project where leaking one is *possible* in the first place.

I built this RAG project knowing it would end up on public GitHub from day one. That changes how you write config code. Here's the actual setup. 👇

---

**The naive way (that I didn't do) ❌**

```python
GROQ_API_KEY = "gsk_abc123..."
```

Right in the source file. Works fine on your laptop. Then you `git add .`, commit, push — and it's public, forever, in the git history, even if you delete it in the next commit.

This isn't a hypothetical. It's one of the most common real-world leak patterns, and scanners crawl public GitHub for exactly this.

---

**What I actually built ✅**

Three layers, each one closing off a different way this goes wrong:

**1. A gitignored config file.**
`config/config.ini` never gets committed — it's in `.gitignore` from the first commit, not added later as an afterthought.

**2. A committed example, with no real values.**
`config/config.example.ini` ships in the repo with `groq_api_key = YOUR_GROQ_API_KEY_HERE`. Anyone cloning the project copies it, fills in their own key, and never touches a file git tracks.

**3. An environment variable fallback.**
`get_setting()` checks the config file first, then falls back to `os.environ`. So the exact same code works whether you're running locally with a config file or deploying somewhere that injects secrets as environment variables — no code change needed either way.

---

**Why this matters more with AI-assisted coding, not less 🤖**

When an AI tool is writing or editing your code, it will often reach for the fastest path that makes something *work* — and hardcoding a value is the fastest path. It won't know your project is going public on GitHub unless the project's structure already makes the safe path the easy path.

That's the actual design goal: make the secure pattern the *default* one, not a rule you have to remember to enforce every time.

---

**The rule I'd give a beginner 💡**

If a project will ever be public, treat every secret as already leaked from the very first line of code you write — not from the moment before you push. Gitignore the config file before you write the first key into it. Not after.

---

🔗 See the actual config setup in the repo:
[github.com/TechNaom/rag-projects](https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc)

👇 What's your go-to setup for secrets in a public repo? Curious if people are using something better than `.env` + `.gitignore` these days.

---

*#CyberSecurity #SoftwareEngineering #GenAI #BuildInPublic #DevSecOps #AIEngineering #OpenSource*

---

## Carousel Storyboard

> Build this in Canva — 8 slides, ~16 minutes.
> Suggested color palette: **Deep navy (#0A1628) + Electric blue (#0066FF) + White (#FFFFFF)** — consistent with the other 01-policy-rag-poc posts. Consider a warning-red accent (#E53E3E) on the "naive way" slide only, to visually separate the anti-pattern from the rest.
> Font: Bold sans-serif (Poppins or Inter recommended)

---

### Slide 1 — Cover / Hook

**Background:** Deep navy
**Big text (white, bold):**
> "The mistake isn't leaking a key."

**Subtext (electric blue):**
> "It's building a project where leaking one is possible."

---

### Slide 2 — The Naive Way

**Background:** Dark red-tinted navy
**Heading (white):** "What NOT to do ❌"
**Body (monospace-style, white):**
> `GROQ_API_KEY = "gsk_abc123..."`
>
> Right in the source file. One `git push` from being public — forever, in history.

---

### Slide 3 — Layer 1

**Background:** Off-white
**Big number:** "01"
**Heading:** "Gitignore the config file first ✅"
**Body:**
> `config/config.ini` is ignored from commit one.
> Not added later. From the start.

---

### Slide 4 — Layer 2

**Background:** Navy
**Big number:** "02"
**Heading (electric blue):** "Ship an example, not real values"
**Body (white):**
> `config.example.ini` with `YOUR_GROQ_API_KEY_HERE`.
> Anyone cloning fills in their own — never touches a tracked file.

---

### Slide 5 — Layer 3

**Background:** Off-white
**Big number:** "03"
**Heading:** "Environment variable fallback 🔄"
**Body:**
> Same code works locally with a config file, or deployed with injected env vars.
> No code change needed either way.

---

### Slide 6 — Why It Matters More Now

**Background:** Navy
**Heading (electric blue):** "AI-assisted coding raises the stakes 🤖"
**Body (white):**
> AI tools reach for the fastest working path.
> Hardcoding is fastest — unless your project structure makes the safe path the easy one.

---

### Slide 7 — The Rule

**Background:** Off-white
**Heading:** "Treat every secret as already leaked 💡"
**Body:**
> From line one, not from the moment before you push.
> Gitignore the config file before you write the first key into it.

---

### Slide 8 — CTA

**Background:** Electric blue
**Heading (white, bold):**
> "See the real config setup."

**Link (white, underlined):**
> github.com/TechNaom/rag-projects

**Bottom CTA:**
> 💬 What's your go-to setup for secrets in a public repo?

---

## Production Notes

| Item | Detail |
|------|--------|
| Canva template size | 1080 x 1080 px (square) or 1080 x 1350 px (portrait) |
| Slides | 8 |
| Export as | PDF (required for LinkedIn carousel) |
| Post format | Upload PDF as document post, paste text post in caption |
| Best posting time | Tuesday–Thursday, 8–10am or 12–1pm local time |
| Accuracy note | This post frames the three-layer config setup as deliberate prevention, not recovery from an actual leak — because no real leak happened on this project. Keep that framing; don't rewrite it into a "here's what happened when I leaked a key" story, which would be fabricated. |
