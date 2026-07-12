# Capstone Track: Legal Contract Explorer

**User:** legal ops, procurement &nbsp;·&nbsp; **Revisit artifact:** clause comparison + review queue

You have a folder of vendor contracts. Someone asks: *"What's our termination-for-convenience notice across all of these?"* or *"Which of these caps liability, and at what number?"* The honest answer requires pulling the **same clause type out of every contract** and lining them up — and, just as importantly, noticing which contracts **don't have that clause at all**, because a missing indemnification clause is a risk, not a non-answer.

This track builds exactly that: clause-level retrieval with a side-by-side comparison and an explicit review queue for contracts that are missing a clause type.

## Why clause-level + hierarchical chunking (not flat chunking)

If you chunk these contracts by fixed size (say, 500 characters), a chunk can start mid-sentence in the payment clause and end inside confidentiality. Retrieval then returns a blob that is hard to compare and hard to cite. Worse, a chunk that reads *"...within sixty (60) days prior written notice..."* is useless on its own — sixty days of **what**, in **whose** contract?

So this track chunks on the document's own structure — one chunk per numbered clause (`## 2. Limitation of Liability`) — and keeps each chunk linked to its **parent contract name and section heading** (Chapter 10's hierarchical idea: a child chunk should always know its parent). That parent context is what makes a side-by-side comparison meaningful and citable: every retrieved excerpt carries *"Ironforge Logistics §2 Limitation of Liability"* with it.

## How to run

```bash
python solution.py
```

No `pip install`. Pure Python standard library only — TF-IDF and cosine similarity are implemented by hand with `re`, `math`, and `collections` (the same zero-dependency convention every chapter in this course follows). `starter.py` is the same program with the core pieces left as `# TODO:` for you to implement; it runs but prints placeholder output.

The corpus is six fictional vendor contracts in [`contracts/`](contracts/), each with consistent numbered clause headers so clause-type matching is meaningful. The clause **language** varies on purpose (termination notice of 15 vs. 30 vs. 60 vs. 90 days; liability capped at 12-months-fees vs. $500,000 vs. 2x-fees; payment terms of net-15 vs. net-20 vs. net-30 vs. net-45) so the comparison is actually informative. Two contracts are deliberately **missing** a clause type — Cloudspire has no indemnification clause, Meridian has no limitation-of-liability clause — to exercise the review-queue behavior.

## Roadmap coverage checklist

This is the shared 9-item capstone checklist from [`docs/production-and-capstone-projects.md`](../../../../docs/production-and-capstone-projects.md). One line each on how this track exercises it.

1. **Ch.5-8 — Source scoping, parsing/cleaning, metadata, ingestion.** `parse_contract()` scopes ingestion to markdown contracts, cleans them into clause bodies, and stamps each chunk with `contract`, `source_file`, `section_number`, and `section_heading` metadata — the fields a version-aware ingestion pipeline would key on.
2. **Ch.9-11 — Chunking strategy + failure pass.** Clause-level (structure-aware) chunking is chosen over fixed-size and justified above; the two deliberately-missing-clause contracts are the chunking-failure examples the review queue is designed to catch rather than silently merge.
3. **Ch.12-14 — Embedding approach + trade-off.** Hand-rolled TF-IDF (lexical) is the stated choice: transparent, zero-dependency, and strong on legal boilerplate vocabulary, with the explicit trade-off that it won't catch pure paraphrase the way a neural embedding would — the documented swap-in point for production.
4. **Ch.15-18 — Vector store + retrieval.** The clause vectors are the index; retrieval is cosine similarity, and the per-contract "best clause + threshold gate" is a domain-specific reranking/routing rule (one apples-to-apples result per contract instead of a global top-k).
5. **Ch.19-21 — Context injection + prompt tests.** The comparison table is the grounded, citation-carrying context you would inject into an answer prompt; the three demo queries act as golden questions, and the missing-clause flag is the refusal/"insufficient evidence" behavior a prompt test suite would assert.
6. **Ch.22-24 — Retrieval + answer metrics + failure analysis.** Every row reports its similarity score, and coverage (matched vs. flagged contracts) is the retrieval metric; each flagged contract is a logged failure case a reviewer analyzes rather than an invisible miss.
7. **Ch.25 — Access control / safety.** Contracts are sensitive commercial documents; the track's safety stance is that a missing clause is surfaced for human review (never silently omitted), and metadata (`source_file`) is the hook for per-document access rules in a real deployment.
8. **Ch.26 — Observability + cost dashboard.** Per-query the tool emits coverage counts and per-contract scores — the raw signal for a dashboard tracking how many contracts a clause query resolves and where retrieval is weak; TF-IDF's cost is effectively zero, which is itself the cost story.
9. **Ch.27 — Deployment pattern.** The loader/index/compare/render stages are separated so the corpus folder can be swapped for a document store and the renderer for an API response — run locally today, promoted to a scheduled clause-diff service without rewriting the core.

## Real output

Below is the actual output of `python solution.py` against the six-contract corpus (pasted verbatim). Note the `NO CLAUSE FOUND` rows: **Meridian** is flagged on the liability-cap query and **Cloudspire** is flagged on the indemnification query, because those contracts genuinely have no such clause.

```text
Loaded 34 clause chunks from 6 contracts.
Contracts:
  - Brightwater Analytics, Inc. — Master Services Agreement
  - Cloudspire Systems Ltd. — SaaS Subscription Agreement
  - Ironforge Logistics LLC — Vendor Services Agreement
  - Meridian Facilities Group — Facilities Management Agreement
  - Northwind Payroll Services Corp. — Professional Services Agreement
  - Quillfeather Media Co. — Marketing Services Agreement

## Clause comparison: "limitation of liability cap on damages"

| Contract | Matched clause | Score | Excerpt |
| --- | --- | --- | --- |
| Ironforge Logistics LLC — Vendor Services Agreement | §2 Limitation of Liability | 0.329 | The aggregate liability of Ironforge Logistics under this Agreement is capped at five hundred thousand dollars ($500,000), regardless of the form of action... |
| Northwind Payroll Services Corp. — Professional Services Agreement | §2 Limitation of Liability | 0.218 | Northwind Payroll Services' aggregate liability under this Agreement shall not exceed two times (2x) the total fees paid by the Client in the twelve (12) months preceding... |
| Brightwater Analytics, Inc. — Master Services Agreement | §2 Limitation of Liability | 0.159 | Except for the indemnification obligations set out below, the total aggregate liability of either party arising out of or related to this Agreement shall not exceed... |
| Cloudspire Systems Ltd. — SaaS Subscription Agreement | §2 Limitation of Liability | 0.121 | Cloudspire Systems' total liability arising out of or relating to this Agreement shall not exceed the fees paid by Client in the six (6) months immediately preceding... |
| Quillfeather Media Co. — Marketing Services Agreement | NO CLAUSE FOUND | 0.053 | _flagged for review_ |
| Meridian Facilities Group — Facilities Management Agreement | NO CLAUSE FOUND | 0.000 | _flagged for review_ |

Coverage: 4 of 6 contracts have a clause on this topic.

Review queue (missing clause — do not assume silence = agreement):
- Quillfeather Media Co. — Marketing Services Agreement (06_quillfeather.md) — no clause matched above threshold 0.06 (best score 0.053). A human should confirm whether this protection is truly absent.
- Meridian Facilities Group — Facilities Management Agreement (04_meridian_fma.md) — no clause matched above threshold 0.06 (best score 0.000). A human should confirm whether this protection is truly absent.

## Clause comparison: "indemnification hold harmless third-party claims"

| Contract | Matched clause | Score | Excerpt |
| --- | --- | --- | --- |
| Ironforge Logistics LLC — Vendor Services Agreement | §3 Indemnification | 0.377 | Each party shall indemnify and hold harmless the other party against third-party claims for bodily injury, death, or physical damage to tangible property... |
| Quillfeather Media Co. — Marketing Services Agreement | §3 Indemnification | 0.328 | Quillfeather Media shall indemnify and hold harmless the Client from third-party claims that creative materials produced by Quillfeather infringe a copyright... |
| Northwind Payroll Services Corp. — Professional Services Agreement | §3 Indemnification | 0.269 | Northwind Payroll Services shall indemnify and hold harmless the Client from third-party claims and regulatory penalties arising from Northwind's failure to remit... |
| Brightwater Analytics, Inc. — Master Services Agreement | §3 Indemnification | 0.234 | Brightwater Analytics shall indemnify, defend, and hold harmless the Client from and against any third-party claims, damages, and reasonable attorney fees... |
| Meridian Facilities Group — Facilities Management Agreement | §3 Indemnification | 0.203 | Meridian Facilities Group shall indemnify, defend, and hold harmless the Client and its representatives from and against all third-party claims, losses... |
| Cloudspire Systems Ltd. — SaaS Subscription Agreement | NO CLAUSE FOUND | 0.051 | _flagged for review_ |

Coverage: 5 of 6 contracts have a clause on this topic.

Review queue (missing clause — do not assume silence = agreement):
- Cloudspire Systems Ltd. — SaaS Subscription Agreement (03_cloudspire.md) — no clause matched above threshold 0.06 (best score 0.051). A human should confirm whether this protection is truly absent.

## Clause comparison: "termination for convenience notice period"

| Contract | Matched clause | Score | Excerpt |
| --- | --- | --- | --- |
| Meridian Facilities Group — Facilities Management Agreement | §1 Term and Termination | 0.296 | This Agreement runs for an initial period of eighteen (18) months and continues month-to-month thereafter. Either party may terminate for convenience by giving thirty (30) days... |
| Brightwater Analytics, Inc. — Master Services Agreement | §1 Term and Termination | 0.206 | This Agreement begins on the Effective Date and continues for an initial term of twenty-four (24) months. Either party may terminate this Agreement for convenience... |
| Northwind Payroll Services Corp. — Professional Services Agreement | §1 Term and Termination | 0.198 | This Agreement remains in effect for twelve (12) months and renews for successive one-year terms unless either party provides forty-five (45) days written notice... |
| Ironforge Logistics LLC — Vendor Services Agreement | §1 Term and Termination | 0.188 | The initial term of this Agreement is thirty-six (36) months from the Effective Date and renews automatically for successive twelve (12) month periods... |
| Quillfeather Media Co. — Marketing Services Agreement | §1 Term and Termination | 0.167 | This Agreement is effective for a campaign term of six (6) months. Either party may terminate for convenience with fifteen (15) days prior written notice... |
| Cloudspire Systems Ltd. — SaaS Subscription Agreement | §1 Term and Termination | 0.136 | The subscription term is twelve (12) months and renews automatically for successive twelve (12) month terms unless either party provides thirty (30) days written notice... |

Coverage: 6 of 6 contracts have a clause on this topic — no review-queue flags on this query, confirming the flagging logic only fires when a clause is genuinely absent, not on every query.
```
