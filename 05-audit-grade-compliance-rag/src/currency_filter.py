"""
currency_filter.py
-------------------
The core audit-grade module: retrieval that is *version-aware*.

A naive RAG system will happily cite whatever chunk is most textually similar
to the question — including a clause from a policy that was superseded three
years ago. In a compliance setting that is not a small error: answering with
"records are kept for six years" when the currently-effective policy says ten
years is a defensible-audit failure, even though the six-year sentence really
does exist verbatim in the corpus.

This module enforces one rule: **by default, retrieval only returns chunks
whose status == "current".** Superseded chunks are excluded unless the caller
explicitly opts in with `include_superseded=True` (needed for historical or
"what did the policy used to say?" audit questions). It also exposes
`verify_currency(chunk)`, which returns a structured proof — drawn straight
from the chunk's own indexed metadata — that a chunk is (or is not) the current
authoritative version.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

from vectorstore import load_vectorstore


@dataclass
class RetrievedChunk:
    """A chunk returned from retrieval, carrying its full provenance record."""
    chunk_id: str
    text: str
    source_file: str
    section: str
    doc_id: str
    title: str
    version: str
    status: str
    effective_date: str
    superseded_by: str
    score: float  # cosine similarity, higher = more relevant

    def as_dict(self) -> Dict:
        return asdict(self)


def _to_chunk(chunk_id: str, doc: str, meta: Dict, distance: float) -> RetrievedChunk:
    # Chroma returns cosine *distance*; similarity = 1 - distance
    similarity = 1 - distance
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=doc,
        source_file=meta.get("source_file", "unknown"),
        section=meta.get("section", ""),
        doc_id=meta.get("doc_id", ""),
        title=meta.get("title", "") or meta.get("doc_title", ""),
        version=meta.get("version", ""),
        status=meta.get("status", ""),
        effective_date=meta.get("effective_date", ""),
        superseded_by=meta.get("superseded_by", ""),
        score=round(similarity, 3),
    )


def retrieve(
    query: str,
    k: int = 4,
    include_superseded: bool = False,
) -> List[RetrievedChunk]:
    """Version-aware retrieval.

    By default (`include_superseded=False`) this filters the vector query so
    that ONLY chunks with status == "current" can be returned — a superseded
    clause can never leak into an answer. Set `include_superseded=True` to
    retrieve across all versions, which is what audit/historical questions
    ("what was the old retention period?") legitimately need.
    """
    collection, embedder = load_vectorstore()
    query_vector = embedder.embed_query(query)

    where = None if include_superseded else {"status": "current"}

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    ids = results.get("ids", [[]])[0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    return [_to_chunk(cid, doc, meta, dist) for cid, doc, meta, dist in zip(ids, docs, metas, dists)]


def verify_currency(chunk: RetrievedChunk) -> Dict:
    """Return structured proof that a chunk is / is not the current version.

    The proof is drawn entirely from the chunk's own indexed metadata — the
    same fields that were parsed from the source document's frontmatter at
    ingest time. This is deliberately auditable: a reviewer can trace the
    verdict back to a concrete field on a concrete versioned document.
    """
    is_current = chunk.status == "current"
    proof = {
        "doc_id": chunk.doc_id,
        "version": chunk.version,
        "status": chunk.status,
        "effective_date": chunk.effective_date,
        "superseded_by": chunk.superseded_by,
        "is_current": is_current,
    }
    if is_current:
        proof["verdict"] = (
            f"{chunk.doc_id} v{chunk.version} is the CURRENT authoritative version "
            f"(effective {chunk.effective_date}, not superseded)."
        )
    else:
        replacement = chunk.superseded_by or "an unspecified newer version"
        proof["verdict"] = (
            f"{chunk.doc_id} v{chunk.version} is SUPERSEDED "
            f"(replaced by {replacement}); it must not be used to answer a "
            f"current-state compliance question."
        )
    return proof


if __name__ == "__main__":
    # Demonstrate the currency filter on the retention-period question.
    q = "How long must adult patient medical records be retained?"
    print(f"QUERY: {q}\n")

    print("--- default retrieval (current only) ---")
    for c in retrieve(q, k=3):
        print(f"  {c.doc_id} v{c.version} [{c.status}] score={c.score}  ({c.section})")

    print("\n--- include_superseded=True (audit/historical) ---")
    for c in retrieve(q, k=3, include_superseded=True):
        print(f"  {c.doc_id} v{c.version} [{c.status}] score={c.score}  ({c.section})")
