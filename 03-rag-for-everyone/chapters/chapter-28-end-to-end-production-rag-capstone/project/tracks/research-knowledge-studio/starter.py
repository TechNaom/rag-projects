"""Project starter: Research Knowledge Studio.

Fill in the TODOs to turn this skeleton into a working multi-source research
assistant. When you are done it should:
  1. chunk the markdown corpus in data/ by section header,
  2. score chunks against a research question with hand-rolled TF-IDF,
  3. retrieve the strongest evidence ACROSS several source documents, and
  4. assemble a cited evidence board + an exportable Markdown brief.

Pure standard library only -- no pip install. Compare with solution.py once you
have taken a real attempt. This file runs today, but only prints a stub.
"""

import math  # noqa: F401  (you will need log/sqrt)
import re
from collections import Counter, defaultdict  # noqa: F401
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {"the", "a", "an", "and", "or", "to", "of", "in", "is", "are", "for"}


def tokenize(text):
    return [tok for tok in TOKEN_RE.findall(text.lower()) if tok not in STOPWORDS]


def load_corpus(data_dir=DATA_DIR):
    """Already done for you: return [(filename, raw_markdown)]."""
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted(data_dir.glob("*.md"))]


def chunk_markdown(source, raw):
    # TODO: split `raw` into chunks at "## " section headers. Return a list of
    # dicts like {"source": source, "heading": ..., "text": ...}. Keep each
    # research finding whole -- do not split mid-section.
    return [{"source": source, "heading": "Whole document", "text": raw}]


def build_index(chunks):
    # TODO: compute term frequency per chunk and inverse document frequency
    # across all chunks, then store a tf-idf vector (dict term -> weight) on
    # each chunk. Return the idf table so the query can reuse it.
    return {}


def embed_query(query, idf):
    # TODO: build a tf-idf vector for the query using the corpus idf table.
    return {}


def cosine(vec_a, vec_b):
    # TODO: cosine similarity between two sparse dict vectors. Return 0.0 when
    # either is empty.
    return 0.0


def retrieve(query, chunks, idf, top_n=6, per_source_cap=1):
    # TODO: rank every chunk by cosine similarity to the query, then enforce
    # source diversity (cap chunks per source) so the board spans MULTIPLE
    # documents, not just the single best-matching one. Return the top items.
    return []


def build_evidence_board(query, selected, idf):
    # TODO: for each retrieved chunk, pull its most query-relevant sentence and
    # tag whether it reinforces or qualifies the emerging picture. Return a list
    # of evidence items carrying source, heading, excerpt, and score.
    return []


def synthesize_brief(question, board):
    # TODO: compose a Markdown brief: a short synthesized answer that cites each
    # source as [filename], a "where sources converge" list, a "where sources
    # diverge or add caveats" list, and an evidence-board table.
    return f"# Research Brief\n\n**Question:** {question}\n\n(TODO: synthesize the board)"


def run(question, top_n=6):
    docs = load_corpus()
    chunks = []
    for source, raw in docs:
        chunks.extend(chunk_markdown(source, raw))
    idf = build_index(chunks)
    selected = retrieve(question, chunks, idf, top_n=top_n)
    board = build_evidence_board(question, selected, idf)
    return chunks, board, synthesize_brief(question, board)


if __name__ == "__main__":
    question = (
        "Should Riverton invest in dockless e-bike sharing or expand bus rapid transit?"
    )
    chunks, board, brief = run(question)
    print(f"Loaded {len(chunks)} chunks (chunking not implemented yet).")
    print(f"Evidence items: {len(board)} (retrieval not implemented yet).\n")
    print(brief)
