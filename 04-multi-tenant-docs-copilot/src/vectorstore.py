"""
vectorstore.py
--------------
Builds the per-tenant vector databases. For EACH tenant this:
  1. fits a fresh embedding model on only that tenant's corpus,
  2. embeds only that tenant's chunks, and
  3. stores them in a Chroma collection that lives in its own directory.

This is the heart of the isolation model. Instead of one shared collection with
a `tenant_id` filter on every query (a "soft" boundary that a forgotten WHERE
clause can breach), each tenant gets:

    collection name:  tenant_{slug}
    chroma directory: data/chroma_db/{slug}/
    fitted embedder:  data/chroma_db/{slug}/embedder.pkl

Because the data physically lives in separate collections in separate
directories, there is no query you can write against tenant A's collection that
returns tenant B's chunks — the rows simply aren't there. Isolation is
structural, not a filter you have to remember to apply.

This is the "index time" half of RAG (as opposed to "query time" — see
rag_chain.py and tenant_gateway.py). Index time is where most of the
engineering work in a real RAG system actually lives.
"""

import shutil
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document

from ingest import list_tenants, load_and_chunk_tenant
from embeddings import LocalTfidfEmbeddings

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_ROOT = PROJECT_ROOT / "data" / "chroma_db"


def _tenant_chroma_dir(tenant_id: str) -> Path:
    return CHROMA_ROOT / tenant_id


def _tenant_embedder_path(tenant_id: str) -> Path:
    return _tenant_chroma_dir(tenant_id) / "embedder.pkl"


def _collection_name(tenant_id: str) -> str:
    # Chroma collection names must be 3-63 chars, so slugs map to tenant_<slug>.
    return f"tenant_{tenant_id.replace('-', '_')}"


def build_tenant_vectorstore(tenant_id: str, rebuild: bool = True) -> Tuple[object, LocalTfidfEmbeddings]:
    """Build (or rebuild) a single tenant's isolated collection + embedder."""
    clear_vectorstore_cache()
    chroma_dir = _tenant_chroma_dir(tenant_id)
    if rebuild and chroma_dir.exists():
        shutil.rmtree(chroma_dir)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{tenant_id}] 1. Loading and chunking this tenant's documents...")
    chunks: List[Document] = load_and_chunk_tenant(tenant_id)
    texts = [c.page_content for c in chunks]
    print(f"[{tenant_id}]    -> {len(chunks)} chunks")

    print(f"[{tenant_id}] 2. Fitting a per-tenant embedder (TF-IDF + SVD) on this tenant only...")
    embedder = LocalTfidfEmbeddings(n_components=128)
    embedder.fit(texts)
    embedder.save(str(_tenant_embedder_path(tenant_id)))

    print(f"[{tenant_id}] 3. Embedding this tenant's chunks...")
    vectors = embedder.embed_documents(texts)

    print(f"[{tenant_id}] 4. Writing to an isolated Chroma collection...")
    client = chromadb.PersistentClient(path=str(chroma_dir), settings=Settings(anonymized_telemetry=False))
    collection = client.create_collection(
        name=_collection_name(tenant_id),
        metadata={"hnsw:space": "cosine", "tenant_id": tenant_id},
    )

    ids = [f"{tenant_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = []
    for c in chunks:
        # Chroma metadata values must be primitives
        metadatas.append({
            "tenant_id": c.metadata.get("tenant_id", tenant_id),
            "source_file": c.metadata.get("source_file", ""),
            "section": str(c.metadata.get("section", "")),
            "doc_title": str(c.metadata.get("doc_title", "")),
        })

    collection.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    print(f"[{tenant_id}]    -> {collection.count()} chunks in collection "
          f"'{_collection_name(tenant_id)}' at {chroma_dir}\n")

    return collection, embedder


def build_all_vectorstores(rebuild: bool = True) -> None:
    tenants = list_tenants()
    print(f"Building isolated vector stores for {len(tenants)} tenants: {tenants}\n")
    for tenant_id in tenants:
        build_tenant_vectorstore(tenant_id, rebuild=rebuild)
    print("All tenant vector stores built. Each lives in its own collection + directory.")


@lru_cache(maxsize=None)
def _load_tenant_vectorstore_cached(tenant_id: str):
    chroma_dir = _tenant_chroma_dir(tenant_id)
    embedder_path = _tenant_embedder_path(tenant_id)
    if not chroma_dir.exists() or not embedder_path.exists():
        raise FileNotFoundError(
            f"No vector store found for tenant '{tenant_id}'. "
            f"Run `python src/vectorstore.py` to build all tenants first."
        )
    client = chromadb.PersistentClient(path=str(chroma_dir), settings=Settings(anonymized_telemetry=False))
    collection = client.get_collection(name=_collection_name(tenant_id))
    embedder = LocalTfidfEmbeddings.load(str(embedder_path))
    return collection, embedder


def load_tenant_vectorstore(tenant_id: str):
    """Load one tenant's already-built collection + its matching fitted embedder.

    This is the ONLY function that resolves a tenant to its data, and it resolves
    strictly by the tenant_id passed in — there is no code path that mixes two
    tenants' collections.
    """
    return _load_tenant_vectorstore_cached(tenant_id)


def clear_vectorstore_cache():
    _load_tenant_vectorstore_cached.cache_clear()


if __name__ == "__main__":
    build_all_vectorstores(rebuild=True)
