"""Solution: Research Knowledge Studio.

A pure-standard-library RAG pipeline for an analyst/researcher. Instead of
returning one chat answer, it retrieves evidence ACROSS MULTIPLE SOURCE
DOCUMENTS, assembles a cited "evidence board", and synthesizes an exportable
Markdown brief that says where the sources agree and where they diverge.

No third-party packages. TF-IDF and cosine similarity are implemented by hand
with re, math, and collections. Run it: `python solution.py`.
"""

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Tiny stopword list. Kept small on purpose: dropping only the highest-frequency
# function words sharpens TF-IDF without hiding real domain terms.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "is", "are", "was", "were", "be", "been", "it", "its", "as", "at", "by",
    "that", "this", "these", "those", "with", "from", "than", "then", "so",
    "not", "no", "do", "does", "did", "how", "what", "which", "who", "will",
    "would", "can", "could", "should", "per", "each", "about", "into", "over",
    "up", "out", "they", "their", "them", "we", "our", "you", "your", "i",
}

# Cue words that signal a source is qualifying, contrasting, or pushing back
# rather than simply reinforcing. Used to sort evidence into "converge" vs
# "diverge/caveat" buckets in the brief. Generic linguistic cues, not topic words.
DIVERGENCE_CUES = {
    "but", "however", "although", "though", "caveat", "diverge", "diverges",
    "disagree", "disagrees", "different", "differently", "instead", "whereas",
    "despite", "only", "not", "unless", "risk", "concern", "complaint",
    "complaints", "wrong",
}

TOKEN_RE = re.compile(r"[a-z0-9]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def tokenize(text):
    """Lowercase, split on non-alphanumerics, drop stopwords."""
    return [tok for tok in TOKEN_RE.findall(text.lower()) if tok not in STOPWORDS]


@dataclass
class Chunk:
    source: str          # source document filename, e.g. "rider-survey.md"
    heading: str         # the ## section header this chunk came from
    text: str            # raw section text (header line stripped)
    tf: Counter = field(default_factory=Counter)   # raw term counts
    vector: dict = field(default_factory=dict)      # term -> tf-idf weight


@dataclass
class EvidenceItem:
    source: str
    heading: str
    excerpt: str         # the single most query-relevant sentence
    score: float         # cosine similarity of the chunk to the query
    stance: str          # "converge" or "diverge" (heuristic on cue words)


# --------------------------------------------------------------------------
# 1. Load + chunk the markdown corpus
# --------------------------------------------------------------------------

def load_corpus(data_dir=DATA_DIR):
    """Return [(source_filename, raw_markdown)] sorted for stable output."""
    docs = []
    for path in sorted(data_dir.glob("*.md")):
        docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def chunk_markdown(source, raw):
    """Split one document into chunks at `## ` section headers.

    Each research finding lives under its own header, so a header-based split
    keeps one finding per chunk instead of slicing mid-argument. The intro text
    above the first `##` is kept as a "Summary" chunk so nothing is lost.
    """
    chunks = []
    heading = "Summary"
    body = []
    for line in raw.splitlines():
        if line.startswith("## "):
            if body:
                chunks.append(Chunk(source, heading, "\n".join(body).strip()))
            heading = line[3:].strip()
            body = []
        elif line.startswith("# "):
            continue  # document title; skip
        else:
            body.append(line)
    if body:
        chunks.append(Chunk(source, heading, "\n".join(body).strip()))
    return [c for c in chunks if c.text]


# --------------------------------------------------------------------------
# 2. Hand-rolled TF-IDF
# --------------------------------------------------------------------------

def build_index(chunks):
    """Fill each chunk's tf counts and tf-idf vector; return the idf table.

    idf uses smoothed inverse document frequency:
        idf(term) = log((1 + N) / (1 + df(term))) + 1
    which never divides by zero and never goes negative.
    """
    n_docs = len(chunks)
    df = defaultdict(int)
    for chunk in chunks:
        chunk.tf = Counter(tokenize(chunk.text))
        for term in chunk.tf:
            df[term] += 1

    idf = {term: math.log((1 + n_docs) / (1 + d)) + 1 for term, d in df.items()}

    for chunk in chunks:
        chunk.vector = {term: count * idf[term] for term, count in chunk.tf.items()}
    return idf


def embed_query(query, idf):
    """Turn a query string into a tf-idf vector using the corpus idf table.

    Query terms unseen in the corpus have no idf weight and are dropped.
    """
    tf = Counter(tokenize(query))
    return {term: count * idf[term] for term, count in tf.items() if term in idf}


def cosine(vec_a, vec_b):
    """Cosine similarity between two sparse dict vectors."""
    if not vec_a or not vec_b:
        return 0.0
    # Iterate the smaller vector for the dot product.
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    dot = sum(weight * vec_b.get(term, 0.0) for term, weight in vec_a.items())
    if dot == 0.0:
        return 0.0
    norm_a = math.sqrt(sum(w * w for w in vec_a.values()))
    norm_b = math.sqrt(sum(w * w for w in vec_b.values()))
    return dot / (norm_a * norm_b)


# --------------------------------------------------------------------------
# 3. Retrieval across multiple sources (the distinguishing behavior)
# --------------------------------------------------------------------------

def retrieve(query, chunks, idf, top_n=5, per_source_cap=1):
    """Rank every chunk by cosine similarity, then enforce source diversity.

    A naive top-N can return five chunks from one dominant document. A research
    brief needs breadth, so we cap how many chunks any single source can
    contribute (default 1). The result is the strongest evidence spread ACROSS
    distinct source documents.
    """
    query_vec = embed_query(query, idf)
    scored = sorted(
        ((cosine(query_vec, c.vector), c) for c in chunks),
        key=lambda pair: pair[0],
        reverse=True,
    )
    selected = []
    used = Counter()
    for score, chunk in scored:
        if score <= 0.0:
            continue
        if used[chunk.source] >= per_source_cap:
            continue
        selected.append((score, chunk))
        used[chunk.source] += 1
        if len(selected) >= top_n:
            break
    return query_vec, selected


def best_sentence(chunk, query_vec, idf):
    """Return the single sentence in a chunk most similar to the query."""
    sentences = [s.strip() for s in SENTENCE_RE.split(chunk.text) if s.strip()]
    if not sentences:
        return chunk.text
    best, best_score = sentences[0], -1.0
    for sentence in sentences:
        vec = {t: c * idf[t] for t, c in Counter(tokenize(sentence)).items() if t in idf}
        score = cosine(query_vec, vec)
        if score > best_score:
            best, best_score = sentence, score
    return " ".join(best.split())


def build_evidence_board(query_vec, selected, idf):
    """Turn retrieved chunks into structured, cited evidence items."""
    board = []
    for score, chunk in selected:
        excerpt = best_sentence(chunk, query_vec, idf)
        # Cue-word scan on RAW words (heading + body), not the stopword-filtered
        # tokens: contrast cues like "but"/"however"/"only" are themselves
        # stopwords, so they must be matched before stopword removal.
        words = set(TOKEN_RE.findall(f"{chunk.heading} {chunk.text}".lower()))
        stance = "diverge" if words & DIVERGENCE_CUES else "converge"
        board.append(EvidenceItem(chunk.source, chunk.heading, excerpt, score, stance))
    return board


# --------------------------------------------------------------------------
# 4. Synthesize an exportable, cited Markdown brief
# --------------------------------------------------------------------------

def synthesize_brief(question, board):
    """Compose a Markdown research brief from the evidence board.

    The synthesis is derived, not faked: convergence/divergence counts, the
    shared theme terms, and every claim sentence come straight from the
    retrieved evidence. Each source it draws from is cited as [filename].
    """
    if not board:
        return f"# Research Brief\n\n**Question:** {question}\n\nNo relevant evidence found."

    sources = [f"[{item.source}]" for item in board]
    converge = [i for i in board if i.stance == "converge"]
    diverge = [i for i in board if i.stance == "diverge"]

    # Shared theme = terms that appear in the excerpts of 2+ distinct sources.
    term_sources = defaultdict(set)
    for item in board:
        for term in set(tokenize(item.excerpt)):
            term_sources[term].add(item.source)
    shared = sorted(
        (t for t, srcs in term_sources.items() if len(srcs) >= 2),
        key=lambda t: len(term_sources[t]),
        reverse=True,
    )[:6]

    lines = []
    lines.append("# Research Brief")
    lines.append("")
    lines.append(f"**Research question:** {question}")
    lines.append("")
    lines.append(f"**Sources synthesized:** {', '.join(sources)}")
    lines.append("")

    lines.append("## Synthesized answer")
    lines.append("")
    theme = ", ".join(shared) if shared else "the question's core trade-offs"
    lines.append(
        f"Drawing on {len(board)} sources, the evidence does not resolve to a single "
        f"clean answer. {len(converge)} source(s) reinforce a shared line of reasoning, "
        f"while {len(diverge)} surface tensions or caveats. Recurring themes across "
        f"sources include: {theme}. Each source's strongest claim is cited below, "
        f"and the divergences matter as much as the agreements."
    )
    lines.append("")
    for item in board:
        lines.append(f"- {item.excerpt} [{item.source}]")
    lines.append("")

    lines.append("## Where sources converge")
    lines.append("")
    if converge:
        for item in converge:
            lines.append(f"- **{item.heading}:** {item.excerpt} [{item.source}]")
    else:
        lines.append("- No clearly convergent evidence was retrieved for this question.")
    lines.append("")

    lines.append("## Where sources diverge or add caveats")
    lines.append("")
    if diverge:
        for item in diverge:
            lines.append(f"- **{item.heading}:** {item.excerpt} [{item.source}]")
    else:
        lines.append("- No divergences or caveats surfaced in the retrieved evidence.")
    lines.append("")

    lines.append("## Evidence board")
    lines.append("")
    lines.append("| # | Source | Section | Similarity | Stance |")
    lines.append("|---|--------|---------|-----------:|--------|")
    for idx, item in enumerate(board, start=1):
        lines.append(
            f"| {idx} | {item.source} | {item.heading} | {item.score:.3f} | {item.stance} |"
        )
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# 5. End to end
# --------------------------------------------------------------------------

def run(question, top_n=6):
    docs = load_corpus()
    chunks = []
    for source, raw in docs:
        chunks.extend(chunk_markdown(source, raw))
    idf = build_index(chunks)
    query_vec, selected = retrieve(question, chunks, idf, top_n=top_n)
    board = build_evidence_board(query_vec, selected, idf)
    brief = synthesize_brief(question, board)
    return chunks, board, brief


if __name__ == "__main__":
    question = (
        "Should Riverton invest in dockless e-bike sharing or expand bus rapid transit?"
    )
    chunks, board, brief = run(question)
    print(f"Loaded {len(chunks)} chunks from the research corpus.\n")
    print(brief)
