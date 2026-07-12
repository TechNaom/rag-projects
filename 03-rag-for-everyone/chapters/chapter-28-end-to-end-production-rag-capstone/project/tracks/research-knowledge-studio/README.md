# Capstone Track: Research Knowledge Studio

**User:** analyst, student, researcher &nbsp;·&nbsp; **Revisit artifact:** an evidence board and an exportable, cited brief.

This track builds a small research assistant over a corpus of separate source
documents. It answers a research question the way a good analyst would: not with
one confident paragraph, but by pulling the strongest evidence **from several
sources at once**, laying it out on an evidence board, and writing a short brief
that cites each source and says plainly **where the sources agree and where they
disagree or add caveats**.

## What makes it different from a single-answer RAG bot

A typical RAG chatbot retrieves a few chunks and fuses them into one smooth
answer. That is exactly the wrong shape for research: it hides which source said
what, and it papers over disagreement. This track deliberately does the
opposite:

- **Multi-source retrieval.** Retrieval is capped per document so the board
  spans *distinct* sources, instead of returning five chunks from the one
  document that happened to match best.
- **An evidence board, not a chat reply.** Every item keeps its source
  filename, section heading, the most relevant sentence, a similarity score,
  and whether it reinforces or qualifies the picture.
- **A cited, exportable brief.** The synthesized answer cites each source as
  `[filename]` and separates points of convergence from points of divergence,
  so a reader can audit the reasoning and follow it back to the evidence.

The corpus (`data/*.md`) is a fictional decision: *should the mid-size city of
Riverton invest in dockless e-bike sharing or expand bus rapid transit?* Six
"source" documents (a cost comparison, a rider survey, a peer-city case study,
an environmental estimate, an operations report, and a public-feedback summary)
partly agree and partly conflict on purpose — one even rejects the either/or
framing entirely — so synthesis is real work, not concatenation.

## How to run

```bash
python solution.py
```

No `pip install` — **pure Python standard library only** (`re`, `math`,
`collections`, `pathlib`, `dataclasses`). TF-IDF and cosine similarity are
implemented by hand; there is no numpy, scikit-learn, or vector database. Start
from `starter.py` (runnable, with `# TODO:` markers) and check yourself against
`solution.py`.

## Roadmap coverage checklist

The nine-item checklist below is the shared capstone rubric from
[`docs/production-and-capstone-projects.md`](../../../../docs/production-and-capstone-projects.md).
One sentence each on how this track exercises it:

1. **Ch.5-8 — source scoping, parsing/cleaning, metadata, versioned ingestion:**
   `load_corpus()` scopes the six research sources in `data/`, and every chunk
   carries its `source` filename and section `heading` as first-class metadata
   used for citation and per-source diversity.
2. **Ch.9-11 — chunking strategy + failure pass:** `chunk_markdown()` splits on
   `## ` section headers so each research finding stays intact, and it handles
   the failure case of pre-header intro text by capturing it as a `Summary`
   chunk instead of dropping it.
3. **Ch.12-14 — embedding approach + trade-off:** embeddings are hand-rolled
   TF-IDF vectors (`build_index()`), chosen because they are transparent and
   dependency-free; the stated trade-off is that lexical TF-IDF matches shared
   wording well but won't capture paraphrase the way a neural embedding would.
4. **Ch.15-18 — vector store + retrieval, hybrid + rerank:** chunks form an
   in-memory dict-vector store, `retrieve()` ranks them by `cosine()` and then
   re-ranks for source diversity via a per-source cap — a lightweight rerank
   that guarantees breadth across documents.
5. **Ch.19-21 — context injection + grounded prompt + tests:**
   `synthesize_brief()` injects only the retrieved evidence and forces a
   grounded, citation-bearing output (`[filename]` after every claim); the
   evidence board is the auditable golden-answer surface a prompt test suite
   would assert against.
6. **Ch.22-24 — retrieval + answer-quality metrics, failure analysis:** every
   evidence item exposes a cosine `score` for retrieval inspection, and the
   converge/diverge split makes weak or off-topic matches visible for a
   failure-analysis pass.
7. **Ch.25 — access control / safety layer:** the corpus is public research, so
   the appropriate safety posture is grounding and provenance — the brief never
   asserts a claim without a source citation, preventing unsourced synthesis.
8. **Ch.26 — observability + cost dashboard:** the evidence-board table reports
   per-source similarity scores and stance, the run-time signal an
   observability view would chart; cost here is trivial and local (no API
   spend), which is itself the documented cost profile.
9. **Ch.27 — deployment pattern:** it ships as a single zero-dependency script
   runnable in any Python 3 environment, and the brief is emitted as portable
   Markdown suitable for export to a docs pipeline, wiki, or report generator.

## Real output

Produced by running `python solution.py` against the corpus in `data/`
(pasted verbatim):

```
Loaded 30 chunks from the research corpus.

# Research Brief

**Research question:** Should Riverton invest in dockless e-bike sharing or expand bus rapid transit?

**Sources synthesized:** [cost-comparison.md], [rider-survey.md], [case-study-brentwell.md], [environmental-impact.md], [maintenance.md], [public-feedback.md]

## Synthesized answer

Drawing on 6 sources, the evidence does not resolve to a single clean answer. 2 source(s) reinforce a shared line of reasoning, while 4 surface tensions or caveats. Recurring themes across sources include: bike, bus, e, transit, 000, residents. Each source's strongest claim is cited below, and the divergences matter as much as the agreements.

- Riverton has roughly 180,000 residents and a current annual transit budget of $42 million. [cost-comparison.md]
- 71 percent said they would use improved bus rapid transit, and that figure stays above 60 percent across every age group and disability status. [rider-survey.md]
- Brentwell is a comparable mid-size city of about 200,000 residents that launched a dockless e-bike program four years ago. [case-study-brentwell.md]
- A BRT trip that replaces a car trip saves about 0.55 kg of CO2 per rider, and a full articulated bus removes far more cars from the road per vehicle than any single bike. [environmental-impact.md]
- Dockless e-bikes offer no guarantee that a working bike will be nearby when a rider needs one, which peer surveys flag as the top complaint. [maintenance.md]
- Many wanted a small e-bike pilot as a downtown connector feeding into an upgraded bus network. [public-feedback.md]

## Where sources converge

- **Summary:** Riverton has roughly 180,000 residents and a current annual transit budget of $42 million. [cost-comparison.md]
- **Summary:** Brentwell is a comparable mid-size city of about 200,000 residents that launched a dockless e-bike program four years ago. [case-study-brentwell.md]

## Where sources diverge or add caveats

- **Willingness to Use:** 71 percent said they would use improved bus rapid transit, and that figure stays above 60 percent across every age group and disability status. [rider-survey.md]
- **Emissions Per Trip:** A BRT trip that replaces a car trip saves about 0.55 kg of CO2 per rider, and a full articulated bus removes far more cars from the road per vehicle than any single bike. [environmental-impact.md]
- **Reliability For Riders:** Dockless e-bikes offer no guarantee that a working bike will be nearby when a rider needs one, which peer surveys flag as the top complaint. [maintenance.md]
- **The Different Angle:** Many wanted a small e-bike pilot as a downtown connector feeding into an upgraded bus network. [public-feedback.md]

## Evidence board

| # | Source | Section | Similarity | Stance |
|---|--------|---------|-----------:|--------|
| 1 | cost-comparison.md | Summary | 0.248 | converge |
| 2 | rider-survey.md | Willingness to Use | 0.206 | diverge |
| 3 | case-study-brentwell.md | Summary | 0.186 | converge |
| 4 | environmental-impact.md | Emissions Per Trip | 0.106 | diverge |
| 5 | maintenance.md | Reliability For Riders | 0.105 | diverge |
| 6 | public-feedback.md | The Different Angle | 0.085 | diverge |
```

Note that the evidence board spans **all six source documents**, and the brief
surfaces the genuinely different angle from `public-feedback.md` — that some
residents reject the either/or framing and want a sequenced "both" approach —
rather than smoothing it away into a single recommendation.
