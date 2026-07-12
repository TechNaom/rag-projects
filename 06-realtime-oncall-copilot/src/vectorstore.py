"""
vectorstore.py
--------------
Builds the vector database: fits the embedding model on the corpus, embeds
every chunk, and stores the vectors + text + metadata in a persisted Chroma
collection on disk.

This is the "index time" half of RAG (as opposed to "query time" — see
rag_chain.py). For an on-call copilot the interesting part of index time is
NOT the initial build — it's keeping the index fresh while incident notes are
being edited mid-incident. That's what `upsert_document()` is for: it
re-chunks and re-embeds ONE file and swaps just that file's chunks in place,
WITHOUT a full rebuild. A full rebuild would refit the embedder, re-embed the
whole corpus, and take seconds-to-minutes — unacceptable when an engineer just
appended two lines to an incident note and immediately asks a question about it.

Chunk IDs are deterministic and namespaced by source file
(`<source_file>::<chunk_index>`), which is what makes a targeted delete +
re-add of a single file's chunks possible.
"""

import shutil
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.config import Settings

from ingest import (
    load_and_chunk_documents,
    chunk_file,
    doc_type_for_path,
    INCIDENT_NOTES_DIR,  # re-exported: live_updater/tests reference it via this module too
)
from embeddings import LocalTfidfEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
EMBEDDER_PATH = PROJECT_ROOT / "data" / "embedder.pkl"
COLLECTION_NAME = "oncall_copilot"


def _chunk_id(source_file: str, chunk_index: int) -> str:
    return f"{source_file}::{chunk_index}"


def _metadata_for(chunk) -> dict:
    # Chroma metadata values must be primitives.
    return {
        "source_file": chunk.metadata.get("source_file", ""),
        "doc_type": str(chunk.metadata.get("doc_type", "")),
        "section": str(chunk.metadata.get("section", "")),
        "doc_title": str(chunk.metadata.get("doc_title", "")),
        "chunk_index": int(chunk.metadata.get("chunk_index", 0)),
    }


def build_vectorstore(rebuild: bool = True):
    clear_vectorstore_cache()
    if rebuild and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Loading and chunking documents (runbooks + incident notes)...")
    chunks = load_and_chunk_documents()
    texts = [c.page_content for c in chunks]
    print(f"   -> {len(chunks)} chunks from the on-call corpus")

    print("2. Fitting local embedding model (TF-IDF + SVD) on corpus...")
    embedder = LocalTfidfEmbeddings(n_components=128)
    embedder.fit(texts)
    embedder.save(str(EMBEDDER_PATH))
    print(f"   -> embedder fitted and saved to {EMBEDDER_PATH}")

    print("3. Embedding all chunks...")
    vectors = embedder.embed_documents(texts)
    print(f"   -> {len(vectors)} vectors of dimension {len(vectors[0])}")

    print("4. Writing to Chroma (persisted to disk)...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    collection = client.create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    ids = [_chunk_id(c.metadata["source_file"], c.metadata["chunk_index"]) for c in chunks]
    metadatas = [_metadata_for(c) for c in chunks]

    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    print(f"   -> {collection.count()} chunks stored in Chroma collection '{COLLECTION_NAME}'")
    print(f"   -> persisted at {CHROMA_DIR}")

    return collection, embedder


def upsert_document(file_path) -> dict:
    """Incrementally re-index a SINGLE document without a full rebuild.

    Steps:
      1. Load the frozen embedder (fit once at build time — NOT refit here).
      2. Re-chunk just this one file.
      3. Delete this file's existing chunks from the collection (by source_file).
      4. Embed the new chunks with the frozen embedder and add them.

    Returns a small summary dict (useful for logging / tests).

    This is deliberately O(size of one file), not O(size of corpus). It is the
    whole point of the project: the index reflects a live edit in milliseconds,
    with no rebuild.
    """
    file_path = Path(file_path)
    collection, embedder = load_vectorstore()

    source_file = file_path.name
    doc_type = doc_type_for_path(file_path)

    # 1. Remove any existing chunks for this file (handles edits AND shrinking
    #    documents, where the new version has fewer chunks than the old one).
    existing = collection.get(where={"source_file": source_file})
    removed = len(existing.get("ids", []))
    if removed:
        collection.delete(where={"source_file": source_file})

    # 2. Re-chunk + embed just this file with the frozen embedder.
    new_chunks = chunk_file(file_path, doc_type)
    added = 0
    if new_chunks:
        texts = [c.page_content for c in new_chunks]
        vectors = embedder.embed_documents(texts)
        ids = [_chunk_id(source_file, c.metadata["chunk_index"]) for c in new_chunks]
        metadatas = [_metadata_for(c) for c in new_chunks]
        collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
        added = len(new_chunks)

    return {
        "source_file": source_file,
        "doc_type": doc_type,
        "chunks_removed": removed,
        "chunks_added": added,
        "collection_count": collection.count(),
    }


@lru_cache(maxsize=1)
def _load_vectorstore_cached():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    collection = client.get_collection(name=COLLECTION_NAME)
    embedder = LocalTfidfEmbeddings.load(str(EMBEDDER_PATH))
    return collection, embedder


def load_vectorstore():
    """Load an already-built collection + the matching fitted embedder."""
    return _load_vectorstore_cached()


def clear_vectorstore_cache():
    _load_vectorstore_cached.cache_clear()


if __name__ == "__main__":
    build_vectorstore(rebuild=True)
