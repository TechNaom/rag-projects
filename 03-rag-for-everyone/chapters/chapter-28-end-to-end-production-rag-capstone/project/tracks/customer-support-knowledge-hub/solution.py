"""Customer Support Knowledge Hub — reference solution (pure standard library).

Capstone track 4: support lead / agent. The distinguishing behavior of this track
is the KNOWLEDGE-GAP SIGNAL. When a support question cannot be answered confidently
from the knowledge base, the system does NOT force a low-quality answer. It flags the
question as a knowledge gap and appends it to a backlog the support lead can work
through — turning "we don't have an article for that" into a prioritized to-do list.

Everything here is hand-rolled with the standard library only:
- re / collections for tokenizing and counting
- a dict-based sparse TF-IDF vector per chunk (term -> weight)
- cosine similarity computed by hand (dot product over shared terms / norms)

No numpy, scikit-learn, or vector database. Run it with:

    python solution.py
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
QUESTIONS_FILE = DATA_DIR / "questions.md"

# --- Confidence threshold -----------------------------------------------------
# The single most important knob in this track: the confidence the top match must
# beat for us to draft an answer. Below it, we refuse and log a knowledge gap.
#
# WHY COSINE ALONE IS NOT ENOUGH (this is the real lesson of the track):
# TF-IDF cosine is purely lexical. A genuinely out-of-scope question can still
# score a high cosine just by sharing common words with an article. For example
# "Can I sync my tasks to Google Calendar?" scores cosine 0.38 against the sync
# article purely on "sync"/"tasks" — HIGHER than a real answerable question about
# exporting a backup (0.24). No single cosine cutoff can separate those two.
#
# What actually distinguishes an out-of-scope question is that it is loaded with
# words the knowledge base has NEVER seen — the real topic of the question
# ("google", "calendar", "slack", "saml", "voice", "memo", "transcribe"). Those
# absent words are the signal. So we discount cosine by how much of the question's
# vocabulary the corpus actually knows:
#
#     coverage   = (# question content-words present in the KB) / (# content-words)
#     confidence = cosine * coverage ** 2
#
# Squaring coverage makes the penalty bite: a high-cosine match riding on a
# question that is half unknown vocabulary collapses toward zero. Measured on this
# corpus (run the file and read the printed scores), every answerable question
# lands at confidence >= 0.15 and every out-of-scope one at <= 0.10. 0.12 sits in
# the empty gap between those two clusters. Re-tune it against your own corpus
# rather than trusting this number blindly.
CONFIDENCE_THRESHOLD = 0.12
TOP_K = 3

# Words too generic to carry topical meaning. Dropping them is what keeps an
# out-of-scope question from scoring against an article purely on filler.
STOPWORDS = {
    "a", "an", "and", "the", "to", "of", "in", "on", "for", "is", "are", "do",
    "does", "how", "i", "my", "me", "you", "your", "it", "its", "this", "that",
    "with", "can", "will", "be", "or", "if", "so", "what", "when", "at", "as",
    "from", "up", "out", "not", "no", "there", "here", "we", "our", "they",
    "have", "has", "should", "would", "want", "get", "keeps",
}


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-word characters, drop stopwords and 1-char tokens."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


# --- Corpus + chunking --------------------------------------------------------

@dataclass
class Chunk:
    """One retrievable unit: a ## section of a KB article."""
    article: str          # source article title (the citation)
    heading: str          # the ## section heading
    text: str             # the section body
    tokens: list[str] = field(default_factory=list)
    vector: dict[str, float] = field(default_factory=dict)  # sparse TF-IDF


def load_articles() -> list[Path]:
    """Every .md in data/ except the sample-questions file is a KB article."""
    return sorted(p for p in DATA_DIR.glob("*.md") if p.name != QUESTIONS_FILE.name)


def chunk_article(path: Path) -> list[Chunk]:
    """Split one article into chunks by `## ` section headers.

    The `# ` title becomes the article name used for citations. Text before the
    first `## ` (the intro paragraph) is attached to an "Overview" chunk so no
    content is dropped.
    """
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    article_title = path.stem.replace("-", " ").title()
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            article_title = line[2:].strip()
            break

    chunks: list[Chunk] = []
    heading = "Overview"
    buffer: list[str] = []

    def flush() -> None:
        body = "\n".join(buffer).strip()
        if body:
            chunks.append(Chunk(article=article_title, heading=heading, text=body))

    for line in lines:
        if line.startswith("## "):
            flush()
            heading = line[3:].strip()
            buffer = []
        elif line.startswith("# "):
            continue  # the title line, already captured
        else:
            buffer.append(line)
    flush()
    return chunks


# --- Hand-rolled TF-IDF -------------------------------------------------------

def build_index(chunks: list[Chunk]) -> dict[str, float]:
    """Compute a sparse TF-IDF vector for every chunk, in place.

    Returns the IDF table so query vectors can reuse the exact same weights.

        tf(term, chunk)  = count(term) / total_terms_in_chunk
        idf(term)        = log((N + 1) / (df(term) + 1)) + 1   (smoothed)
        weight           = tf * idf

    Vectors are dicts {term: weight}; absent terms are implicitly zero, which is
    what makes this sparse and cheap without numpy.
    """
    n_docs = len(chunks)
    doc_freq: dict[str, int] = defaultdict(int)
    for ch in chunks:
        ch.tokens = tokenize(ch.text)
        for term in set(ch.tokens):
            doc_freq[term] += 1

    idf = {
        term: math.log((n_docs + 1) / (df + 1)) + 1.0
        for term, df in doc_freq.items()
    }

    for ch in chunks:
        ch.vector = tf_idf_vector(ch.tokens, idf)
    return idf


def tf_idf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    """Build one sparse TF-IDF vector from tokens using a shared IDF table."""
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    vector: dict[str, float] = {}
    for term, count in counts.items():
        weight = idf.get(term)
        if weight:  # skip terms unseen in the corpus (idf undefined -> zero signal)
            vector[term] = (count / total) * weight
    return vector


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity of two sparse vectors, iterating only shared terms."""
    if not a or not b:
        return 0.0
    # iterate the smaller dict for the dot product
    if len(a) > len(b):
        a, b = b, a
    dot = sum(weight * b.get(term, 0.0) for term, weight in a.items())
    if dot == 0.0:
        return 0.0
    norm_a = math.sqrt(sum(w * w for w in a.values()))
    norm_b = math.sqrt(sum(w * w for w in b.values()))
    return dot / (norm_a * norm_b)


# --- Retrieval + answer / knowledge-gap decision ------------------------------

@dataclass
class Retrieved:
    chunk: Chunk
    score: float


def retrieve(question: str, chunks: list[Chunk], idf: dict[str, float],
             top_k: int = TOP_K) -> list[Retrieved]:
    """Return the top_k chunks by cosine similarity to the question.

    Retrieval RANKING is pure cosine — coverage is a confidence gate applied
    afterwards (see draft_answer), not a ranking signal. We still want the best
    lexical match even for an out-of-scope question, so we can report it as the
    "closest but insufficient" hint on the backlog.
    """
    q_vec = tf_idf_vector(tokenize(question), idf)
    scored = [Retrieved(ch, cosine(q_vec, ch.vector)) for ch in chunks]
    scored.sort(key=lambda r: r.score, reverse=True)
    return scored[:top_k]


def query_coverage(question: str, vocab: set[str]) -> tuple[float, list[str]]:
    """Fraction of the question's content words that the KB vocabulary contains.

    Returns (coverage, absent_terms). A low coverage means the question is about
    something the corpus has never mentioned — the knowledge-gap signal.
    """
    tokens = tokenize(question)
    if not tokens:
        return 0.0, []
    absent = [t for t in tokens if t not in vocab]
    coverage = (len(tokens) - len(absent)) / len(tokens)
    return coverage, sorted(set(absent))


@dataclass
class Result:
    question: str
    status: str            # "answered" or "knowledge_gap"
    cosine: float          # raw top-chunk cosine similarity
    coverage: float        # fraction of query words the KB knows
    confidence: float      # cosine * coverage**2 — the value gated on
    answer: str = ""
    citation: str = ""
    closest_match: str = ""     # for gaps: the best-but-insufficient article, if any
    absent_terms: list[str] = field(default_factory=list)  # unknown query words


def draft_answer(question: str, hits: list[Retrieved], vocab: set[str]) -> Result:
    """Apply the confidence threshold, then either answer or flag a gap.

    Confidence = cosine * coverage**2 (see the CONFIDENCE_THRESHOLD note above).
    A confident answer is assembled EXTRACTIVELY from the retrieved chunk text and
    cites its source article. We never generate claims that are not in the corpus —
    that is what makes refusing the honest move when confidence is low.
    """
    top = hits[0]
    coverage, absent = query_coverage(question, vocab)
    confidence = top.score * coverage ** 2

    if confidence >= CONFIDENCE_THRESHOLD:
        # Assemble from the top chunk, plus a supporting second chunk from the same
        # article if it is also a solid cosine match.
        parts = [top.chunk.text]
        for extra in hits[1:]:
            if extra.score >= top.score * 0.6 and extra.chunk.article == top.chunk.article:
                parts.append(extra.chunk.text)
                break
        citation = f"{top.chunk.article} > {top.chunk.heading}"
        return Result(
            question=question, status="answered",
            cosine=top.score, coverage=coverage, confidence=confidence,
            answer="\n\n".join(parts), citation=citation, absent_terms=absent,
        )

    # Below threshold: refuse to force an answer. Record the closest thing we saw
    # so the support lead knows whether this is "no article at all" or "an article
    # that grazes the topic but does not actually answer it".
    closest = ""
    if top.score > 0:
        closest = f"{top.chunk.article} > {top.chunk.heading} (cosine {top.score:.3f})"
    return Result(
        question=question, status="knowledge_gap",
        cosine=top.score, coverage=coverage, confidence=confidence,
        closest_match=closest, absent_terms=absent,
    )


# --- Sample questions ---------------------------------------------------------

def load_questions() -> list[tuple[str, str]]:
    """Parse `expected | question` lines from sample-questions.md."""
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


# --- Pipeline -----------------------------------------------------------------

def run() -> None:
    chunks: list[Chunk] = []
    for path in load_articles():
        chunks.extend(chunk_article(path))
    idf = build_index(chunks)
    vocab = set(idf)

    print("=" * 74)
    print("Customer Support Knowledge Hub")
    print(f"Loaded {len(chunks)} chunks from {len(load_articles())} KB articles.")
    print(f"Confidence = cosine * coverage**2   Answer threshold: {CONFIDENCE_THRESHOLD}")
    print("=" * 74)

    questions = load_questions()
    backlog: list[Result] = []   # the knowledge-gap backlog the support lead works
    answered = 0
    correct = 0                  # matches the `expected` sanity label

    for expected, question in questions:
        hits = retrieve(question, chunks, idf)
        result = draft_answer(question, hits, vocab)

        predicted_scope = "answerable" if result.status == "answered" else "out-of-scope"
        if predicted_scope == expected:
            correct += 1

        print()
        print(f"Q: {question}")
        print(f"   cosine {result.cosine:.3f} x coverage {result.coverage:.2f}^2 "
              f"= confidence {result.confidence:.3f}   (expected: {expected})")
        if result.status == "answered":
            answered += 1
            print(f"   STATUS: ANSWERED (confidence high)  [source: {result.citation}]")
            first_line = result.answer.splitlines()[0]
            snippet = first_line[:96] + ("..." if len(first_line) > 96 else "")
            print(f"   answer draft: {snippet}")
        else:
            backlog.append(result)
            print("   STATUS: KNOWLEDGE GAP - refused to force an answer, logged to backlog")
            if result.closest_match:
                print(f"   closest but insufficient: {result.closest_match}")
            else:
                print("   closest but insufficient: (nothing in the corpus came close)")
            if result.absent_terms:
                print(f"   unknown terms driving the gap: {', '.join(result.absent_terms)}")

    # --- Summary + the knowledge-gap backlog ---
    print()
    print("=" * 74)
    print("SUMMARY")
    print(f"  questions run : {len(questions)}")
    print(f"  answered      : {answered}")
    print(f"  knowledge gaps: {len(backlog)}")
    print(f"  scope decision matched expected label: {correct}/{len(questions)}")
    print("=" * 74)
    print("KNOWLEDGE-GAP BACKLOG (content the support lead should create):")
    if not backlog:
        print("  (none - every question was answerable from the current KB)")
    for i, gap in enumerate(backlog, start=1):
        print(f"  {i}. {gap.question}")
        hint = gap.closest_match or "no related article - likely a brand-new topic"
        print(f"     nearest existing content: {hint}")
        if gap.absent_terms:
            print(f"     missing coverage for: {', '.join(gap.absent_terms)}")
    print("=" * 74)


if __name__ == "__main__":
    run()
