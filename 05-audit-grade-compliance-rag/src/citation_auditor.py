"""
citation_auditor.py
--------------------
Grades how well an answer is *actually* supported by the evidence it cites,
using a four-level framework (L1-L4). Each level is strictly stronger than the
one below it, so the highest level an answer clears is a compact, auditable
quality score.

    L1  Cited at all        -> the answer contains at least one citation marker.
    L2  Every claim cited   -> every sentence/claim carries a citation marker.
    L3  Citations support   -> the cited chunk's text actually contains the key
                               terms/facts of the claim it is attached to.
    L4  Source is current   -> every cited chunk is the CURRENT authoritative
                               version (reuses currency_filter.verify_currency).

IMPORTANT — L3 is a HEURISTIC, not ground truth. It uses keyword/number overlap
between a claim's distinctive terms and the cited chunk's text. That catches
the common failure mode (a citation bolted onto a claim the chunk doesn't
mention) but it cannot verify semantic entailment — a claim can share
vocabulary with a chunk and still misread it. A production system would replace
the L3 heuristic with an NLI/entailment model or an LLM-as-judge check. The
level is deliberately labelled so a reviewer never mistakes overlap for proof.

Citation markers recognized:
  * bracketed indices like [1] / [2], 1-based into the retrieved-chunk list
  * a chunk's doc_id appearing literally in the text, e.g. "per RETEN-002"
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from currency_filter import RetrievedChunk, verify_currency

# Small stopword set for the L3 keyword-overlap heuristic. Kept intentionally
# short — we only need to strip the most common non-distinctive words so that
# overlap reflects content terms (and, crucially, numbers) rather than glue.
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "for", "to", "of", "in", "on", "at",
    "by", "is", "are", "be", "was", "were", "as", "that", "this", "these",
    "those", "it", "its", "with", "from", "must", "may", "will", "shall",
    "not", "no", "any", "all", "per", "than", "then", "you", "your", "we",
    "our", "their", "they", "have", "has", "had", "which", "who", "whom",
    "within", "after", "before", "under", "over", "into", "out", "if",
}

# Number words that commonly encode compliance thresholds; treated as content.
_NUMBER_WORDS = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "sixty", "ninety",
    "hundred",
}

_MARKER_RE = re.compile(r"\[(\d+)\]")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_L3_OVERLAP_THRESHOLD = 0.4  # fraction of a claim's distinctive terms that must appear in a cited chunk


@dataclass
class LevelResult:
    level: str
    name: str
    passed: bool
    detail: str


@dataclass
class CitationAuditResult:
    highest_level: int  # 0 = failed L1; otherwise the strongest level cleared
    levels: List[LevelResult] = field(default_factory=list)

    @property
    def summary(self) -> str:
        if self.highest_level == 0:
            return "L0 — uncited (fails L1)"
        return f"L{self.highest_level}"

    def as_dict(self) -> Dict:
        return {
            "highest_level": self.highest_level,
            "summary": self.summary,
            "levels": [
                {"level": r.level, "name": r.name, "passed": r.passed, "detail": r.detail}
                for r in self.levels
            ],
        }


def _content_terms(text: str) -> set:
    """Distinctive lower-cased tokens of a piece of text: content words, number
    words, and any digit sequences (retention periods, deadlines, counts)."""
    tokens = re.findall(r"[A-Za-z0-9\-]+", text.lower())
    terms = set()
    for tok in tokens:
        if tok.isdigit():
            terms.add(tok)
        elif tok in _NUMBER_WORDS:
            terms.add(tok)
        elif len(tok) >= 4 and tok not in _STOPWORDS:
            terms.add(tok)
    return terms


def _split_sentences(answer: str) -> List[str]:
    parts = [s.strip() for s in _SENTENCE_SPLIT_RE.split(answer)]
    # Drop empties and trivially short fragments (e.g. a stray "OK.")
    return [s for s in parts if len(s) >= 15]


def _referenced_chunks(text: str, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
    """Resolve every citation marker in `text` to the chunk(s) it points at."""
    referenced: List[RetrievedChunk] = []
    seen = set()

    for m in _MARKER_RE.findall(text):
        idx = int(m) - 1
        if 0 <= idx < len(chunks):
            c = chunks[idx]
            key = (c.chunk_id, "idx")
            if key not in seen:
                seen.add(key)
                referenced.append(c)

    for c in chunks:
        if c.doc_id and re.search(rf"\b{re.escape(c.doc_id)}\b", text):
            key = (c.chunk_id, "docid")
            if key not in seen:
                seen.add(key)
                referenced.append(c)

    return referenced


def audit_answer(answer: str, chunks: List[RetrievedChunk]) -> CitationAuditResult:
    """Grade (answer, retrieved_chunks) against L1-L4 and return a structured result."""
    sentences = _split_sentences(answer)
    all_referenced = _referenced_chunks(answer, chunks)

    levels: List[LevelResult] = []
    highest = 0

    # --- L1: cited at all ---
    l1_pass = len(all_referenced) > 0
    levels.append(LevelResult(
        "L1", "Cited at all", l1_pass,
        f"{len(all_referenced)} citation marker(s) resolved to retrieved chunks."
        if l1_pass else "No citation markers found in the answer.",
    ))
    if not l1_pass:
        return CitationAuditResult(highest_level=0, levels=levels)
    highest = 1

    # --- L2: every claim cited ---
    uncited = [s for s in sentences if not _referenced_chunks(s, chunks)]
    l2_pass = len(uncited) == 0 and len(sentences) > 0
    levels.append(LevelResult(
        "L2", "Every claim cited", l2_pass,
        f"All {len(sentences)} claim sentence(s) carry a citation."
        if l2_pass else f"{len(uncited)} of {len(sentences)} claim sentence(s) lack a citation: "
                        + "; ".join(s[:60] + ("..." if len(s) > 60 else "") for s in uncited),
    ))
    if l2_pass:
        highest = 2

    # --- L3: citations actually support the claim (keyword-overlap HEURISTIC) ---
    unsupported = []
    checked = 0
    for s in sentences:
        cited = _referenced_chunks(s, chunks)
        if not cited:
            continue  # L2 already accounts for uncited sentences
        checked += 1
        claim_terms = _content_terms(s)
        if not claim_terms:
            continue
        evidence_terms = set()
        for c in cited:
            evidence_terms |= _content_terms(c.text)
        overlap = len(claim_terms & evidence_terms) / len(claim_terms)
        if overlap < _L3_OVERLAP_THRESHOLD:
            unsupported.append((s, round(overlap, 2)))
    l3_pass = l2_pass and checked > 0 and not unsupported
    if unsupported:
        detail = ("HEURISTIC keyword overlap below "
                  f"{_L3_OVERLAP_THRESHOLD:.0%} for {len(unsupported)} claim(s): "
                  + "; ".join(f'"{s[:50]}..." (overlap {o:.0%})' for s, o in unsupported))
    elif not l2_pass:
        detail = "Not evaluated as passing because L2 did not pass."
    else:
        detail = (f"All {checked} cited claim(s) share >= {_L3_OVERLAP_THRESHOLD:.0%} of their "
                  "distinctive terms with the cited chunk (heuristic, not entailment).")
    levels.append(LevelResult("L3", "Citations support the claim (heuristic)", l3_pass, detail))
    if l3_pass:
        highest = 3

    # --- L4: every cited source is the current authoritative version ---
    superseded = [c for c in all_referenced if not verify_currency(c)["is_current"]]
    l4_pass = l3_pass and not superseded
    if superseded:
        detail = "Answer cites SUPERSEDED source(s): " + "; ".join(
            f"{c.doc_id} v{c.version} (superseded by {c.superseded_by or 'unknown'})" for c in superseded
        )
    elif not l3_pass:
        detail = "Not evaluated as passing because L3 did not pass."
    else:
        detail = "Every cited source is the current authoritative version: " + ", ".join(
            f"{c.doc_id} v{c.version}" for c in all_referenced
        )
    levels.append(LevelResult("L4", "Cited source is current", l4_pass, detail))
    if l4_pass:
        highest = 4

    return CitationAuditResult(highest_level=highest, levels=levels)


if __name__ == "__main__":
    from currency_filter import retrieve
    from rag_chain import answer_question  # noqa: F401  (only imported for manual demo)

    demo_answer = "Adult patient medical records must be retained for ten (10) years per RETEN-002 [1]."
    demo_chunks = retrieve("How long are adult patient records retained?", k=2)
    result = audit_answer(demo_answer, demo_chunks)
    print(f"Highest level cleared: {result.summary}")
    for lvl in result.levels:
        print(f"  {lvl.level} {lvl.name}: {'PASS' if lvl.passed else 'FAIL'} — {lvl.detail}")
