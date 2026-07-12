# Capstone Track 4: Customer Support Knowledge Hub

**User:** a support lead or agent. **Revisit artifact:** an answer draft, a ticket
pattern, and — the point of this track — a **knowledge gap**.

This is one of the five capstone tracks for [Chapter 28](../../README.md). Like every
exercise in this course, it runs on the **pure Python standard library** — no pip
install, no numpy, no scikit-learn, no vector database. TF-IDF and cosine similarity
are hand-rolled with `re`, `math`, and `collections` so you can read every line and
run it anywhere Python is installed.

## Why "refuse to force an answer" is the whole point

A support bot that always produces an answer is dangerous, not helpful. When a customer
asks about something the knowledge base does not actually cover — a Slack integration,
SAML sign-on, a Google Calendar sync that does not exist — a naive system will still
retrieve the "closest" article and confidently hand back a wrong answer stitched from
unrelated text. That is how a support tool tells a customer to reset their password when
they asked about SSO.

This track does the opposite. When retrieval confidence is too low, it **stops**:

- it does **not** draft an answer,
- it flags the question as a **KNOWLEDGE GAP**,
- it names the closest-but-insufficient article and the specific unknown terms, and
- it appends the question to a **backlog** the support lead can turn into real content.

So every question the corpus cannot answer becomes a prioritized to-do item — "we have
no article on SSO, three customers asked this week" — instead of a silently wrong reply.
The refusal is the safety-relevant behavior, not a limitation.

## How to run

```
python solution.py
```

No setup, no dependencies. `starter.py` is the same pipeline with the core pieces left
as `# TODO:` markers — it runs and prints stub output, and you fill it in.

- `data/*.md` — a small fictional SaaS ("Notedeck", a notes + tasks app) knowledge base:
  6 articles (password reset, data export, billing, team members, sync troubleshooting,
  API rate limits) plus `questions.md`, the test set.
- `questions.md` — 10 sample questions: 6 answerable from the KB and 4 deliberately
  out-of-scope. The `expected` label on each line is only used to score the run; it is
  **not** fed into retrieval or the confidence decision.

## The confidence signal (why cosine alone is not enough)

The interesting engineering problem here: **TF-IDF cosine similarity is purely lexical,
so a genuinely out-of-scope question can still score a high cosine** just by sharing
common words. In this corpus, *"Can I sync my tasks to Google Calendar?"* scores cosine
**0.384** against the sync article — **higher** than the real, answerable question about
exporting a backup (**0.241**). No single cosine cutoff can separate them.

What actually distinguishes an out-of-scope question is that it is loaded with words the
knowledge base has never seen — `google`, `calendar`, `slack`, `saml`, `voice`, `memo`.
Those absent words *are* the topic. So we discount cosine by how much of the question's
vocabulary the corpus knows:

```
coverage   = (# question content-words present in the KB) / (# content-words)
confidence = cosine * coverage ** 2
```

Squaring makes the penalty bite. Measured on this corpus, every answerable question lands
at confidence ≥ 0.15 and every out-of-scope one at ≤ 0.10, so the threshold **0.12** sits
in a real empty gap — not a number hand-tuned to force a pass. Re-tune it against your own
corpus.

## Roadmap coverage checklist

The nine-item checklist shared by all five capstone tracks (see
[`docs/production-and-capstone-projects.md`](../../../../../docs/production-and-capstone-projects.md)),
and how this track's code exercises each:

1. **Ch.5-8 — Source scoping, parsing/cleaning, metadata, versioned ingestion.** The 6
   `data/*.md` articles are the scoped, cleaned source; `load_articles()` and
   `chunk_article()` parse the markdown and derive per-chunk metadata (source article
   title + section heading) that becomes the citation on every answer.
2. **Ch.9-11 — A chunking strategy chosen and justified, with a failure pass.** Chunking
   is by `## ` section header — justified because support articles are already written as
   discrete task-sized sections. The chunking-failure case (text before the first `## `)
   is handled by an explicit "Overview" chunk, exercised on 2 real examples (the sync and
   API-limits intros) so no content is silently dropped.
3. **Ch.12-14 — An embedding approach chosen and justified, with a trade-off.** Hand-rolled
   TF-IDF sparse vectors are chosen over neural embeddings for zero-dependency
   transparency. The stated trade-off is explicit in the code: TF-IDF is lexical, so it
   *cannot* tell by cosine that "sync to Google Calendar" is out of scope — which is
   exactly what motivates the coverage gate below.
4. **Ch.15-18 — Vector store + retrieval, including hybrid/rerank.** An in-memory sparse
   index (`build_index`) plus cosine retrieval (`retrieve`); the coverage-discounted
   confidence then acts as a lightweight re-scoring gate over the top cosine hit before
   anything is shown to the user.
5. **Ch.19-21 — Context injection + grounded prompt, backed by a prompt test suite.**
   Answers are strictly **extractive** — assembled only from retrieved chunk text and
   citing the source article, so nothing is hallucinated. `questions.md` is the golden +
   refusal test set: 6 must-answer and 4 must-refuse questions.
6. **Ch.22-24 — Retrieval + answer-quality metrics with a failure-analysis pass.** The run
   scores its scope decision against the expected labels (10/10 here) and prints the full
   `cosine x coverage = confidence` breakdown per question, which is the surface you use to
   analyze any miss.
7. **Ch.25 — An access-control/safety layer appropriate to sensitivity.** The
   refuse-when-unconfident branch *is* the safety layer for this domain: it structurally
   prevents confidently-wrong answers on unsupported topics from reaching a customer.
8. **Ch.26 — Observability + cost dashboard.** Every query logs its cosine, coverage,
   confidence, decision, and the unknown terms driving a gap; corpus and chunk counts are
   logged at startup. Spend is zero — pure stdlib, no API calls.
9. **Ch.27 — A deployment pattern chosen and documented.** The intended deployment is a
   batch triage job / CLI that runs the day's unanswered tickets through the pipeline and
   emits the knowledge-gap backlog for the support lead's weekly content review. The
   swap-in point for scale is documented: replace the hand-rolled TF-IDF with a neural
   embedder and the in-memory index with a real vector DB, keeping the coverage/confidence
   gate unchanged.

## Real output

Actual output of `python solution.py` against the real corpus and questions (one
confidently-answered question, one genuine knowledge gap, and the full backlog):

```
==========================================================================
Customer Support Knowledge Hub
Loaded 25 chunks from 6 KB articles.
Confidence = cosine * coverage**2   Answer threshold: 0.12
==========================================================================

Q: I forgot my password and the reset link says it is no longer valid, what do I do?
   cosine 0.516 x coverage 0.86^2 = confidence 0.379   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: Resetting Your Notedeck Password > Password reset link expired or invalid]
   answer draft: Reset links are single-use and expire after 60 minutes. If you see "This link is no longer valid...

Q: How do I export all my notes and tasks as a backup?
   cosine 0.241 x coverage 0.80^2 = confidence 0.154   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: Exporting Your Notes and Tasks > Export your entire account]
   answer draft: To download everything at once:

Q: I want to cancel my subscription, will I lose my notes and can I get a refund?
   cosine 0.291 x coverage 0.80^2 = confidence 0.186   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: Billing and Subscription Changes > Refunds and invoices]
   answer draft: Every charge generates an invoice you can download from **Settings > Billing > Invoices**. Noted...

Q: How do I invite a coworker as a read-only viewer?
   cosine 0.361 x coverage 0.80^2 = confidence 0.231   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: Inviting and Managing Team Members > Invite someone to your workspace]
   answer draft: 1. Go to **Settings > Members**.

Q: My notes are not showing up on my other device, how do I fix syncing?
   cosine 0.470 x coverage 0.67^2 = confidence 0.209   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: Troubleshooting Sync Issues > Overview]
   answer draft: Notedeck syncs your notes across every device you sign in on. If a change on one device is not s...

Q: The API keeps returning 429, how should my integration handle rate limits?
   cosine 0.604 x coverage 0.86^2 = confidence 0.444   (expected: answerable)
   STATUS: ANSWERED (confidence high)  [source: API Rate Limits > Overview]
   answer draft: Notedeck offers a REST API for Pro and Team accounts. This article explains the rate limits and ...

Q: How do I connect Notedeck to Slack so new tasks post to a channel?
   cosine 0.206 x coverage 0.43^2 = confidence 0.038   (expected: out-of-scope)
   STATUS: KNOWLEDGE GAP - refused to force an answer, logged to backlog
   closest but insufficient: Exporting Your Notes and Tasks > Export your entire account (cosine 0.206)
   unknown terms driving the gap: channel, connect, post, slack

Q: Does Notedeck support single sign-on with SAML for my company?
   cosine 0.154 x coverage 0.67^2 = confidence 0.069   (expected: out-of-scope)
   STATUS: KNOWLEDGE GAP - refused to force an answer, logged to backlog
   closest but insufficient: Resetting Your Notedeck Password > Reset a forgotten password (cosine 0.154)
   unknown terms driving the gap: company, saml

Q: Can I sync my Notedeck tasks to my Google Calendar automatically?
   cosine 0.384 x coverage 0.50^2 = confidence 0.096   (expected: out-of-scope)
   STATUS: KNOWLEDGE GAP - refused to force an answer, logged to backlog
   closest but insufficient: Troubleshooting Sync Issues > Sync is stuck or paused (cosine 0.384)
   unknown terms driving the gap: automatically, calendar, google

Q: How do I record a voice memo and have Notedeck transcribe it into a note?
   cosine 0.248 x coverage 0.43^2 = confidence 0.046   (expected: out-of-scope)
   STATUS: KNOWLEDGE GAP - refused to force an answer, logged to backlog
   closest but insufficient: Resetting Your Notedeck Password > Overview (cosine 0.248)
   unknown terms driving the gap: memo, record, transcribe, voice

==========================================================================
SUMMARY
  questions run : 10
  answered      : 6
  knowledge gaps: 4
  scope decision matched expected label: 10/10
==========================================================================
KNOWLEDGE-GAP BACKLOG (content the support lead should create):
  1. How do I connect Notedeck to Slack so new tasks post to a channel?
     nearest existing content: Exporting Your Notes and Tasks > Export your entire account (cosine 0.206)
     missing coverage for: channel, connect, post, slack
  2. Does Notedeck support single sign-on with SAML for my company?
     nearest existing content: Resetting Your Notedeck Password > Reset a forgotten password (cosine 0.154)
     missing coverage for: company, saml
  3. Can I sync my Notedeck tasks to my Google Calendar automatically?
     nearest existing content: Troubleshooting Sync Issues > Sync is stuck or paused (cosine 0.384)
     missing coverage for: automatically, calendar, google
  4. How do I record a voice memo and have Notedeck transcribe it into a note?
     nearest existing content: Resetting Your Notedeck Password > Overview (cosine 0.248)
     missing coverage for: memo, record, transcribe, voice
==========================================================================
```

The four out-of-scope questions are not answered — they land in the backlog with the exact
missing vocabulary, which is precisely the content-gap signal a support lead needs.
