"""Customer Support Knowledge Hub — STARTER (runnable but incomplete).

Fill in the TODOs to turn this skeleton into the full pipeline. Compare with
solution.py once you have taken a real swing at it yourself.

The whole track is pure standard library — no pip installs. You will hand-roll
TF-IDF + cosine similarity with re / math / collections. Do NOT reach for numpy,
scikit-learn, or a vector DB.

The point of THIS track is the knowledge-gap signal: when the corpus cannot
answer a question confidently, do not force an answer — flag it as a gap and add
it to a backlog the support lead can work through.

Run it now:  python starter.py
It prints stub output and does not crash — your job is to make it real.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
QUESTIONS_FILE = DATA_DIR / "questions.md"

# TODO: pick a real threshold once you can see your actual confidence scores.
# Cosine alone will NOT separate answerable from out-of-scope questions (an
# out-of-scope question can share common words and score a high cosine). Read the
# note in solution.py about discounting cosine by query-term coverage.
CONFIDENCE_THRESHOLD = 0.0  # placeholder — everything "passes" until you set this

STOPWORDS = {
    "a", "an", "and", "the", "to", "of", "in", "on", "for", "is", "are", "do",
    "does", "how", "i", "my", "me", "you", "your", "it", "its", "this", "that",
    "with", "can", "will", "be", "or", "if", "so", "what", "when", "at", "as",
    "from", "up", "out", "not", "no", "there", "here", "we", "our", "they",
    "have", "has", "should", "would", "want", "get", "keeps",
}


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-word chars, drop stopwords and 1-char tokens."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


@dataclass
class Chunk:
    article: str
    heading: str
    text: str
    tokens: list[str] = field(default_factory=list)
    vector: dict[str, float] = field(default_factory=dict)


def load_articles() -> list[Path]:
    return sorted(p for p in DATA_DIR.glob("*.md") if p.name != QUESTIONS_FILE.name)


def chunk_article(path: Path) -> list[Chunk]:
    """Split one article into chunks by `## ` section headers.

    TODO: implement real chunking. Right now this returns the WHOLE article as a
    single chunk, which is bad for retrieval precision. Split on `## ` headings,
    use the `# ` title as the article name (the citation), and keep the intro
    paragraph as an "Overview" chunk so no text is dropped.
    """
    raw = path.read_text(encoding="utf-8")
    title = path.stem.replace("-", " ").title()
    return [Chunk(article=title, heading="(whole article)", text=raw)]


def build_index(chunks: list[Chunk]) -> dict[str, float]:
    """Compute a sparse TF-IDF vector for each chunk; return the IDF table.

    TODO: implement TF-IDF by hand.
      tf(term, chunk) = count(term) / total_terms_in_chunk
      idf(term)       = log((N + 1) / (df(term) + 1)) + 1   (smoothed)
      weight          = tf * idf
    For now every chunk just gets an empty vector, so nothing retrieves.
    """
    for ch in chunks:
        ch.tokens = tokenize(ch.text)
        ch.vector = {}  # TODO: fill with {term: tf * idf}
    return {}  # TODO: return {term: idf}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """TODO: cosine similarity of two sparse dict vectors.

    dot / (||a|| * ||b||), iterating only the terms the two vectors share.
    """
    return 0.0


def query_coverage(question: str, vocab: set[str]) -> float:
    """TODO: fraction of the question's content words that appear in the KB vocab.

    This is the knowledge-gap signal. A question full of words the corpus has
    never seen (an unsupported integration) should score LOW coverage.
    """
    return 1.0  # placeholder: pretends the KB knows every word


@dataclass
class Result:
    question: str
    status: str
    confidence: float
    citation: str = ""
    closest_match: str = ""


def answer_or_gap(question: str, chunks: list[Chunk], idf: dict[str, float]) -> Result:
    """Retrieve, score confidence, then either answer or flag a knowledge gap.

    TODO:
      1. Build the query TF-IDF vector and cosine-rank the chunks.
      2. confidence = top_cosine * coverage ** 2  (see solution.py for why).
      3. If confidence >= CONFIDENCE_THRESHOLD: assemble an extractive answer from
         the top chunk(s) and cite the source article.
      4. Otherwise: return a knowledge_gap result naming the closest-but-
         insufficient match — do NOT force an answer.
    """
    # Stub: always flags a gap so the pipeline runs end to end without crashing.
    return Result(question=question, status="knowledge_gap", confidence=0.0,
                  closest_match="(retrieval not implemented yet)")


def load_questions() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for line in QUESTIONS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        expected, question = line.split("|", 1)
        expected, question = expected.strip(), question.strip()
        if expected in {"answerable", "out-of-scope"} and question:
            pairs.append((expected, question))
    return pairs


def run() -> None:
    chunks: list[Chunk] = []
    for path in load_articles():
        chunks.extend(chunk_article(path))
    idf = build_index(chunks)

    print("Customer Support Knowledge Hub (STARTER - mostly stubs)")
    print(f"Loaded {len(chunks)} chunks from {len(load_articles())} KB articles.")

    backlog: list[Result] = []
    for expected, question in load_questions():
        result = answer_or_gap(question, chunks, idf)
        print(f"\nQ: {question}")
        print(f"   expected: {expected}  ->  status: {result.status}")
        if result.status == "knowledge_gap":
            backlog.append(result)

    # TODO: real summary — count answered vs gaps and confirm the out-of-scope
    # questions actually land in the backlog.
    print(f"\nSUMMARY (stub): {len(backlog)} gaps, 0 answered - implement the TODOs.")


if __name__ == "__main__":
    run()
