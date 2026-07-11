# Production-Grade Projects & Capstone Tracks

This is the full spec sheet referenced by [Chapter 28's project brief](../chapters/chapter-28-end-to-end-production-rag-capstone/project/README.md). It has two tiers:

- **3 Production-Grade Projects** — broader, resume-grade builds meant to sit at the very end of the course, past "I completed the curriculum" into "I built something a company could actually run." Each is in a different domain from the Northkeep policy-RAG example used throughout the course.
- **5 Capstone Tracks** — scoped to prove curriculum mastery. Each track exercises the full pipeline once, and comes with a roadmap coverage checklist so you can self-verify you've exercised the entire curriculum by finishing one.

---

## 3 Production-Grade Projects

### 1. Multi-Tenant Documentation Copilot
**Domain:** SaaS / Platform &nbsp;·&nbsp; **User:** multiple customer teams sharing one hosted RAG service, each with their own private knowledge base

**Problem:** Build a RAG-as-a-service platform where many tenants each upload their own docs, and the system must never let one tenant's retrieval touch another tenant's index — while still sharing infrastructure to keep cost per tenant low.

**Required corpus:** At least 3 simulated tenants, each with a distinct document set (e.g. a fictional startup's product docs, a fictional agency's client playbooks, a fictional nonprofit's grant guidelines) — different formats and structures per tenant on purpose.

**Must apply:**
- Ch.7 metadata design (`tenant_id` as a first-class field)
- Ch.17 hybrid search
- Ch.18 reranking
- Ch.25 access control (hard tenant isolation)
- Ch.26 per-tenant cost dashboard
- Ch.27 deployment pattern

**Deliverable:** A hosted multi-tenant API with a per-tenant cost/latency dashboard and a written proof that a cross-tenant retrieval leak is architecturally impossible, not just unlikely.

---

### 2. Audit-Grade Compliance RAG
**Domain:** Regulated Industry &nbsp;·&nbsp; **User:** a compliance or legal reviewer who must be able to justify every answer to an external auditor

**Problem:** Go beyond "cites its source" (what the Northkeep POC already does) to full audit-grade traceability: every answer must carry a signed explanation of exactly which evidence supported which claim, at the sentence level, plus proof the source was the current authoritative version at answer time.

**Required corpus:** A versioned document set where some documents are deliberately superseded by newer ones, so the system must prove it used the current version and can explain what changed.

**Must apply:**
- Ch.7 metadata (version/currency fields)
- Ch.21 citation-support test levels (L1-L4)
- Ch.24 failure analysis + replay tests
- Ch.25 prompt-injection defenses
- Ch.22-23 retrieval + answer-quality metrics

**Deliverable:** A full trace store plus a "why this answer" report generator that an actual auditor could read without needing to understand the underlying system.

---

### 3. Real-Time On-Call Ops Copilot
**Domain:** Latency-Critical &nbsp;·&nbsp; **User:** an on-call engineer during an active incident, where every extra second matters

**Problem:** Retrieve over runbooks and past incident notes that change frequently (documents get edited mid-incident), under a hard latency budget, with cost-aware routing so cheap questions don't pay for expensive reranking.

**Required corpus:** A set of runbook documents plus a simulated stream of "incident note" updates that mutate the index while the system is live.

**Must apply:**
- Ch.2 query lifecycle (latency budget per stage)
- Ch.4 execution pipelines (fast online path)
- Ch.8 versioned ingestion (live-updating index)
- Ch.26 cost-aware routing
- Ch.27 blue/green deployment
- Ch.24 incident-triage failure loop

**Deliverable:** A Slack- or CLI-integrated copilot with a published p95 latency budget per pipeline stage, and a demo of the index staying correct while being updated live.

---

## 5 Capstone Tracks

Each track shares the same **roadmap coverage checklist** — the point is that by finishing any one track, you've exercised the entire curriculum:

1. **Ch.5-8** — Source scoping, parsing/cleaning, metadata design, and versioned ingestion applied to the track's real document types
2. **Ch.9-11** — A chunking strategy chosen and justified for this domain's document structure, with a chunking-failure pass on at least 2 real examples
3. **Ch.12-14** — An embedding approach chosen and justified (TF-IDF/SVD vs. neural) with a stated trade-off
4. **Ch.15-18** — Vector store + retrieval strategy implemented, including hybrid search and reranking
5. **Ch.19-21** — Context injection + a grounded system prompt, backed by a prompt test suite (golden questions, refusal tests, injection tests)
6. **Ch.22-24** — Retrieval metrics and answer-quality metrics measured on a real test set, with a failure-analysis pass on every miss
7. **Ch.25** — An access-control/safety layer appropriate to the track's sensitivity level
8. **Ch.26** — An observability + cost dashboard covering latency and spend per query
9. **Ch.27** — A deployment pattern chosen and documented (not just run locally)

### 1. Enterprise Policy RAG (Policy Intelligence Desk)
**User:** employee, HR, compliance &nbsp;·&nbsp; **Revisit artifact:** policy answer with audit trail
**Track focus:** Emphasize citation-to-clause traceability and a superseded-policy test case.

### 2. Incident Runbook Copilot
**User:** on-call engineer &nbsp;·&nbsp; **Revisit artifact:** incident checklist and post-incident notes
**Track focus:** Emphasize freshness — runbooks and incident notes must reflect live edits, not a static index.

### 3. Legal Contract Explorer
**User:** legal ops, procurement &nbsp;·&nbsp; **Revisit artifact:** clause comparison and review queue
**Track focus:** Emphasize clause-level chunking (Ch.10 hierarchical chunking) and side-by-side contract version comparison.

### 4. Customer Support Knowledge Hub
**User:** support lead, agent &nbsp;·&nbsp; **Revisit artifact:** answer draft, ticket pattern, knowledge gap
**Track focus:** Emphasize the knowledge-gap signal — track questions the corpus cannot yet answer as a backlog input.

### 5. Research Briefing Studio (Research Knowledge Studio)
**User:** analyst, student, researcher &nbsp;·&nbsp; **Revisit artifact:** evidence board and exportable brief
**Track focus:** Emphasize multi-source synthesis and an exportable, cited evidence board rather than a single chat answer.
