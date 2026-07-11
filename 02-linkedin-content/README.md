# LinkedIn Content — Build-in-Public Series

A collection of LinkedIn posts created to educate and enable people on
building AI systems, RAG pipelines, and developer workflows — documented
as open source alongside the projects that inspired them.

## Purpose

- Share real learnings from real projects, not tutorial demos
- Build in public, one post at a time
- Help others learn AI development through honest, grounded content

## Source Projects

Posts in this series are mirrored from real, working projects:

- 👉 [01-policy-rag-poc](../01-policy-rag-poc/) — A working RAG system over
  banking compliance policy documents built with ChromaDB, TF-IDF embeddings,
  and the Groq API.
  GitHub: <https://github.com/TechNaom/rag-projects/tree/main/01-policy-rag-poc>

- 👉 [GenAI for Everyone](https://github.com/TechNaom/genai-for-everyone) — a
  free, complete 7-week / 42-session GenAI curriculum (standalone repo,
  separate from this monorepo).
  GitHub: <https://github.com/TechNaom/genai-for-everyone>

- 👉 [Python for Everyone](https://github.com/TechNaom/python-for-everyone) — a
  free, interactive Python course built chapter by chapter, in public
  (standalone repo, separate from this monorepo).
  GitHub: <https://github.com/TechNaom/python-for-everyone> &middot;
  Live: <https://technaom.github.io/python-for-everyone/>

## Posts

| # | Title | Theme | Source | Status |
|---|-------|-------|--------|--------|
| 01 | [What is RAG?](posts/01-what-is-rag.md) | Education — core concept | 01-policy-rag-poc | ✅ Ready |
| 02 | [GenAI for Everyone (Course Launch)](posts/02-genai-for-everyone-launch.md) | Personal journey — giving away free education | genai-for-everyone | ✅ Ready |
| 03 | [The Honest Build](posts/03-the-honest-build.md) | Credibility — showing failures | 01-policy-rag-poc | ✅ Ready |
| 04 | [The Orchestrator Mindset](posts/04-the-orchestrator-mindset.md) | Mindset — AI + human collaboration | 01-policy-rag-poc | ✅ Ready |
| 05 | [The API Key Mistake](posts/05-the-api-key-mistake.md) | Security — practical lesson | 01-policy-rag-poc | ✅ Ready |
| 06 | [Why I Built This for Banking](posts/06-why-i-built-this-for-banking.md) | Domain framing | 01-policy-rag-poc | ✅ Ready |
| 07 | [Python for Everyone: 11 Chapters, 2 Modules](posts/07-python-for-everyone-milestone.md) | Build-in-public milestone — proof of depth | python-for-everyone | ✅ Ready |
| 08 | [GenAI Deep R&D Journal, Ep. 01: Why Vector Databases?](posts/08-genai-rd-journal-ep01-vector-databases.md) | Technical deep-dive — recurring R&D journal series | 01-policy-rag-poc | ✅ Ready |
| 09 | [GenAI Deep R&D Journal, Ep. 02: Why Brute-Force Search Doesn't Scale](posts/09-genai-rd-journal-ep02-vector-search-at-scale.md) | Technical deep-dive — recurring R&D journal series | 01-policy-rag-poc | ✅ Ready |
| 10 | [GenAI Deep R&D Journal, Ep. 03: Why HNSW Exists](posts/10-genai-rd-journal-ep03-hnsw.md) | Technical deep-dive — recurring R&D journal series | 01-policy-rag-poc | ✅ Ready |
| 11 | [GenAI Deep R&D Journal, Ep. 04: What's Actually Inside an Embedding](posts/11-genai-rd-journal-ep04-embeddings.md) | Technical deep-dive — recurring R&D journal series | 01-policy-rag-poc | ✅ Ready |
| 12 | [GenAI Deep R&D Journal, Ep. 05: Dense vs. Sparse Retrieval](posts/12-genai-rd-journal-ep05-dense-vs-sparse.md) | Technical deep-dive — recurring R&D journal series | 01-policy-rag-poc | ✅ Ready |
| 13 | [GenAI Deep R&D Journal, Ep. 06: Why Chunking Breaks RAG](posts/13-genai-rd-journal-ep06-chunking.md) | Technical deep-dive — recurring R&D journal series (closes the 6-episode arc) | 01-policy-rag-poc | ✅ Ready |

## RAG for Everyone — 30-Day Series (Posts 14–42)

A daily companion series to the [`03-rag-for-everyone`](../03-rag-for-everyone/) course — one post per day, one chapter per post, `📘 RAG for Everyone | Day X/30`. Day 1 is [Post 01](posts/01-what-is-rag.md) above (Chapter 1). Days 2–30 are drafted and pending review before posting.

| Day | Post | Chapter | Status |
|---|-------|-------|--------|
| 1 | [What is RAG?](posts/01-what-is-rag.md) | chapter-01-why-rag-exists | ✅ Ready |
| 2 | [The RAG Query Lifecycle](posts/14-day02-rag-query-lifecycle.md) | chapter-02-rag-query-lifecycle | 📝 Draft |
| 3 | [Types of RAG](posts/15-day03-types-of-rag.md) | chapter-03-types-of-rag | 📝 Draft |
| 4 | [RAG Execution Pipelines](posts/16-day04-rag-execution-pipelines.md) | chapter-04-rag-execution-pipelines | 📝 Draft |
| 5 | [Source Documents](posts/17-day05-source-documents.md) | chapter-05-source-documents | 📝 Draft |
| 6 | [Parsing & Cleaning](posts/18-day06-parsing-and-cleaning.md) | chapter-06-parsing-and-cleaning | 📝 Draft |
| 7 | [Metadata Design](posts/19-day07-metadata-design.md) | chapter-07-metadata-design | 📝 Draft |
| 8 | [Ingestion & Indexing Pipelines](posts/20-day08-ingestion-and-indexing-pipelines.md) | chapter-08-ingestion-and-indexing-pipelines | 📝 Draft |
| 9 | [Fixed & Recursive Chunking](posts/21-day09-fixed-and-recursive-chunking.md) | chapter-09-fixed-and-recursive-chunking | 📝 Draft |
| 10 | [Semantic & Hierarchical Chunking](posts/22-day10-semantic-and-hierarchical-chunking.md) | chapter-10-semantic-and-hierarchical-chunking | 📝 Draft |
| 11 | [Chunking Failure Analysis](posts/23-day11-chunking-failure-analysis.md) | chapter-11-chunking-failure-analysis | 📝 Draft |
| 12 | [What Embeddings Are](posts/24-day12-what-embeddings-are.md) | chapter-12-what-embeddings-are | 📝 Draft |
| 13 | [Local TF-IDF/SVD Embeddings](posts/25-day13-local-tfidf-svd-embeddings.md) | chapter-13-local-tfidf-svd-embeddings | 📝 Draft |
| 14 | [Neural Embeddings](posts/26-day14-neural-embeddings.md) | chapter-14-neural-embeddings | 📝 Draft |
| 15 | [Vector Stores & Indexing Strategies](posts/27-day15-vector-stores-and-indexing-strategies.md) | chapter-15-vector-stores-and-indexing-strategies | 📝 Draft |
| 16 | [Retrieval Strategies & Top-K](posts/28-day16-retrieval-strategies-and-top-k.md) | chapter-16-retrieval-strategies-and-top-k | 📝 Draft |
| 17 | [Hybrid Search & Query Routing](posts/29-day17-hybrid-search-and-query-routing.md) | chapter-17-hybrid-search-and-query-routing | 📝 Draft |
| 18 | [Reranking & Retrieval Optimization](posts/30-day18-reranking-and-retrieval-optimization.md) | chapter-18-reranking-and-retrieval-optimization | 📝 Draft |
| 19 | [Context Injection](posts/31-day19-context-injection.md) | chapter-19-context-injection | 📝 Draft |
| 20 | [Grounded System Prompts](posts/32-day20-grounded-system-prompts.md) | chapter-20-grounded-system-prompts | 📝 Draft |
| 21 | [Prompt Testing](posts/33-day21-prompt-testing.md) | chapter-21-prompt-testing | 📝 Draft |
| 22 | [Retrieval Metrics](posts/34-day22-retrieval-metrics.md) | chapter-22-retrieval-metrics | 📝 Draft |
| 23 | [Answer Quality Metrics](posts/35-day23-answer-quality-metrics.md) | chapter-23-answer-quality-metrics | 📝 Draft |
| 24 | [Failure Analysis](posts/36-day24-failure-analysis.md) | chapter-24-failure-analysis | 📝 Draft |
| 25 | [Access Control & Safety](posts/37-day25-access-control-and-safety.md) | chapter-25-access-control-and-safety | 📝 Draft |
| 26 | [Observability & Cost](posts/38-day26-observability-and-cost.md) | chapter-26-observability-and-cost | 📝 Draft |
| 27 | [Deployment Patterns](posts/39-day27-deployment-patterns.md) | chapter-27-deployment-patterns | 📝 Draft |
| 28 | [Capstone: End-to-End Production RAG](posts/40-day28-end-to-end-production-rag-capstone.md) | chapter-28-end-to-end-production-rag-capstone | 📝 Draft |
| 29 | [What Building This Actually Taught Me](posts/41-day29-what-building-this-actually-taught-me.md) | bonus — honest recap | 📝 Draft |
| 30 | [Series Finale](posts/42-day30-series-finale.md) | bonus — series close | 📝 Draft |

## Posting Schedule (Suggested)

| Week | Post |
|------|------|
| 1 | 01 — What is RAG? |
| 2 | 02 — GenAI for Everyone (Course Launch) |
| 3 | 03 — The Honest Build |
| 4 | 04 — The Orchestrator Mindset |
| 5 | 05 — The API Key Mistake |
| 6 | 06 — Why I Built This for Banking |
| 7 | 07 — Python for Everyone Milestone (flexible timing — not tied to the RAG series) |
| 8 | 08 — GenAI Deep R&D Journal Ep. 01 (flexible timing — first entry in a new recurring series) |
| 9 | 09 — GenAI Deep R&D Journal Ep. 02 (post after Ep. 01's comments have had time to land — this episode explicitly builds on reader engagement from it) |
| 10 | 10 — GenAI Deep R&D Journal Ep. 03 (post soon after Ep. 02 while the comment thread on the O(n) question is still warm — this episode resolves it directly) |
| 11 | 11 — GenAI Deep R&D Journal Ep. 04 (resolves the "what is an embedding" thread Ep. 01 opened and Ep. 03 explicitly promised next) |
| 12 | 12 — GenAI Deep R&D Journal Ep. 05 (dense vs. sparse — connects back to Post 03's exact eval numbers, keep the 86.7% figure consistent) |
| 13 | 13 — GenAI Deep R&D Journal Ep. 06 (chunking — closes the 6-episode arc; does not tease a specific Ep. 07 topic) |
