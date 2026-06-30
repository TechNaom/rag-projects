"""
vectorstore.py
--------------
Builds the vector database: fits the embedding model on the corpus, embeds
every chunk, and stores the vectors + text + metadata in a persisted Chroma
collection on disk.

This is the "index time" half of RAG (as opposed to "query time" — see
rag_chain.py). Index time is where most of the engineering work in a real
RAG system actually lives: re-running this whenever source documents change,
versioning the index, and deciding chunking/embedding parameters.
"""

import shutil
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.config import Settings

from ingest import load_and_chunk_documents
from embeddings import LocalTfidfEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
EMBEDDER_PATH = PROJECT_ROOT / "data" / "embedder.pkl"
COLLECTION_NAME = "northkeep_policies"


def build_vectorstore(rebuild: bool = True):
    clear_vectorstore_cache()
    if rebuild and CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Loading and chunking documents...")
    chunks = load_and_chunk_documents()
    texts = [c.page_content for c in chunks]
    print(f"   -> {len(chunks)} chunks from the policy corpus")

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

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = []
    for c in chunks:
        # Chroma metadata values must be primitives
        metadatas.append({
            "source_file": c.metadata.get("source_file", ""),
            "section": str(c.metadata.get("section", "")),
            "doc_title": str(c.metadata.get("doc_title", "")),
        })

    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    print(f"   -> {collection.count()} chunks stored in Chroma collection '{COLLECTION_NAME}'")
    print(f"   -> persisted at {CHROMA_DIR}")

    return collection, embedder


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
