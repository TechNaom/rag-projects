"""Legal Contract Explorer — STARTER (incomplete, but runnable).

Capstone track: clause-level retrieval + side-by-side contract comparison for
legal ops / procurement.

This file runs today, but it only prints placeholder output. Your job is to
fill in the four TODOs so that, given a clause topic (e.g. "liability cap"),
the tool retrieves the best-matching clause from EVERY contract and flags the
contracts that have no such clause as a review-queue item.

Rules of the course: pure Python standard library only. No pip install, no
numpy, no scikit-learn. You implement TF-IDF and cosine similarity by hand with
re / math / collections. See solution.py once you have attempted it.

Run it:

    python starter.py
"""

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

RELEVANCE_THRESHOLD = 0.06
DATA_DIR = Path(__file__).parent / "contracts"

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "at", "by",
    "with", "as", "is", "are", "be", "shall", "will", "may", "not", "this",
    "that", "any", "all", "party", "parties", "agreement", "client",
    "services", "service",
}


@dataclass
class Clause:
    """One clause-level chunk. Keep the parent context on the chunk itself:
    a chunk should never be just "60 days notice" without knowing WHICH
    contract and WHICH section it came from."""

    contract: str
    source_file: str
    section_number: str
    section_heading: str
    text: str
    vector: dict = field(default_factory=dict)


def parse_contract(path):
    """Split one markdown contract into clause-level chunks.

    TODO 1 — HIERARCHICAL / CLAUSE-LEVEL CHUNKING (Ch.10):
      * Read the file.
      * Pull the contract name from the "# Contract: ..." title line.
      * For every "## N. Heading" section, create one Clause whose text is that
        section's body AND that remembers its parent contract + section heading.
      Right now this returns a single fake chunk so the script still runs.
    """
    contract_name = path.stem
    return [
        Clause(
            contract=contract_name,
            source_file=path.name,
            section_number="0",
            section_heading="STUB — not chunked yet",
            text="(clause parsing not implemented)",
        )
    ]


def load_corpus(data_dir=DATA_DIR):
    clauses = []
    for path in sorted(data_dir.glob("*.md")):
        clauses.extend(parse_contract(path))
    return clauses


def tokenize(text):
    tokens = re.findall(r"[a-z]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def compute_idf(clauses):
    """TODO 2 — INVERSE DOCUMENT FREQUENCY (by hand):
      idf(term) = log(N / df(term)). Count how many clause chunks each term
      appears in, then return {term: idf}. No numpy — just collections.
    """
    return {}


def tfidf_vector(text, idf):
    """TODO 3 — TF-IDF VECTOR (sparse dict):
      Tokenize, count term frequencies, and return {term: tf * idf} using the
      idf map. This is the shared representation for both clauses and queries.
    """
    return {}


def cosine_similarity(a, b):
    """Cosine similarity between two sparse {term: weight} dicts.
    (Provided for you — this part is not a TODO.)"""
    if not a or not b:
        return 0.0
    dot = sum(w * b.get(t, 0.0) for t, w in a.items())
    if dot == 0.0:
        return 0.0
    norm_a = math.sqrt(sum(w * w for w in a.values()))
    norm_b = math.sqrt(sum(w * w for w in b.values()))
    return dot / (norm_a * norm_b)


def build_index(clauses):
    idf = compute_idf(clauses)
    for clause in clauses:
        clause.vector = tfidf_vector(clause.text, idf)
    return idf


def compare_clause_across_contracts(query, clauses, idf, threshold=RELEVANCE_THRESHOLD):
    """TODO 4 — ONE RESULT PER CONTRACT + REVIEW-QUEUE FLAGGING:
      * Vectorize the query.
      * For EACH contract independently, find its single best-matching clause.
      * If that best score >= threshold, record it as a match; otherwise record
        the contract as "NO CLAUSE FOUND — flag for review" (do not drop it).
      Return a list of result rows (one per contract).
    """
    return []


def render_comparison(query, results):
    if not results:
        return f'(no results yet for "{query}" — finish the TODOs in starter.py)'
    lines = [f'Clause comparison: "{query}"']
    for r in results:
        lines.append(f"  {r}")
    return "\n".join(lines)


def main():
    clauses = load_corpus()
    idf = build_index(clauses)
    print(f"Loaded {len(clauses)} clause chunks (stub chunker — expected 1 per file).")
    for query in ["liability cap", "termination for convenience"]:
        results = compare_clause_across_contracts(query, clauses, idf)
        print(render_comparison(query, results))
        print()


if __name__ == "__main__":
    main()
