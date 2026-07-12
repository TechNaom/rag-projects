# Project: Production RAG Capstone Planner

Choose one capstone track and generate a milestone backlog. Full specs, required-corpus notes, and chapter-mapped roadmap checklists for every project below live in [`docs/production-and-capstone-projects.md`](../../../docs/production-and-capstone-projects.md).

## 5 Capstone Tracks

Pick one. Each is scoped to prove full curriculum mastery — completing any one exercises the whole pipeline, from source scoping (Ch.5-8) through deployment (Ch.27).

1. **Policy Intelligence Desk** (Enterprise Policy RAG) — employee/HR/compliance user, policy answer with audit trail. Bridges to [`01-policy-rag-poc`](../../../../01-policy-rag-poc/) — see the coverage table in `docs/production-and-capstone-projects.md` for what it already covers vs. what's left for you to add.
2. **Incident Runbook Copilot** — on-call engineer, incident checklist and post-incident notes. Bridges to [`06-realtime-oncall-copilot`](../../../../06-realtime-oncall-copilot/) — same deal, coverage table + gaps in the doc above.
3. **Research Knowledge Studio** (Research Briefing Studio) — analyst/student/researcher, evidence board and exportable brief. → [`project/tracks/research-knowledge-studio`](tracks/research-knowledge-studio/)
4. **Legal Contract Explorer** — legal ops/procurement, clause comparison and review queue. → [`project/tracks/legal-contract-explorer`](tracks/legal-contract-explorer/)
5. **Customer Support Knowledge Hub** — support lead/agent, answer draft, ticket pattern, knowledge gap. → [`project/tracks/customer-support-knowledge-hub`](tracks/customer-support-knowledge-hub/)

Tracks 3-5 are real, working, zero-dependency scaffolds (pure Python standard library — no `pip install`, matching every other chapter's exercises in this course). Each has a `starter.py` (runnable, with `# TODO:`s for you to complete) and a `solution.py` (a full working reference) plus a README with real captured output and the roadmap coverage checklist.

## 3 Production-Grade Projects

For after the capstone track — broader, resume-grade builds meant to prove you can ship something a company could actually run, not just complete an exercise. **All 3 are real, working, open-source reference implementations** — clone one, run its tests, read its README's real output, then build your own on top of it or in the same style.

1. **Multi-Tenant Documentation Copilot** — hard tenant isolation across shared infrastructure. → [`04-multi-tenant-docs-copilot`](../../../../04-multi-tenant-docs-copilot/)
2. **Audit-Grade Compliance RAG** — citation-support traceability (L1-L4) with superseded-version detection for an external auditor. → [`05-audit-grade-compliance-rag`](../../../../05-audit-grade-compliance-rag/)
3. **Real-Time On-Call Ops Copilot** — hard latency budget over a live-updating index. → [`06-realtime-oncall-copilot`](../../../../06-realtime-oncall-copilot/)

See [`docs/production-and-capstone-projects.md`](../../../docs/production-and-capstone-projects.md) for the full brief on each: problem statement, required corpus, the specific chapters' techniques each must apply, and the deliverable artifact.
