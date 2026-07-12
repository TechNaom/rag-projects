"""
ingest.py
---------
Loads one tenant's documents and splits them into overlapping chunks, tagging
every chunk with the owning `tenant_id`.

Chunking matters more than people expect: too large and retrieval pulls in
irrelevant text alongside the relevant sentence; too small and you lose the
surrounding context a clause needs to make sense (e.g. a numbered list item
without the header explaining what it's a list OF). For header-structured docs,
splitting on markdown headers first, then on size within each section, keeps
each chunk topically coherent.

Multi-tenant note: ingestion is always scoped to a single tenant. There is no
function here that loads "all documents" into one undifferentiated pile — you
load a tenant's docs, and every resulting chunk carries `tenant_id` in its
metadata. The vector store then builds a separate collection per tenant from
these chunks (see vectorstore.py), which is what makes cross-tenant retrieval
structurally impossible rather than merely filtered.
"""

from pathlib import Path
from typing import List

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TENANTS_DIR = PROJECT_ROOT / "data" / "tenants"

HEADERS_TO_SPLIT_ON = [
    ("#", "doc_title"),
    ("##", "section"),
]

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100


def list_tenants() -> List[str]:
    """Return the sorted slugs of every tenant that has a document directory."""
    if not TENANTS_DIR.exists():
        return []
    return sorted(p.name for p in TENANTS_DIR.iterdir() if p.is_dir())


def tenant_docs_dir(tenant_id: str) -> Path:
    return TENANTS_DIR / tenant_id


def load_and_chunk_tenant(
    tenant_id: str,
    tenants_dir: Path = TENANTS_DIR,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Load every .md file for one tenant and return a flat list of chunked Documents.

    Every returned chunk has `tenant_id` in its metadata; this is the tag the
    rest of the system uses to guarantee a chunk is only ever served back to the
    tenant that owns it.
    """
    docs_dir = tenants_dir / tenant_id
    if not docs_dir.exists():
        raise FileNotFoundError(f"No document directory for tenant '{tenant_id}' at {docs_dir}")

    md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks: List[Document] = []

    for file_path in sorted(docs_dir.glob("*.md")):
        raw_text = file_path.read_text(encoding="utf-8")

        # Step 1: split by markdown section headers, so each piece stays
        # within one document section (never spans "Section 3" into "Section 4")
        section_docs = md_header_splitter.split_text(raw_text)

        # Step 2: within each section, further split by size if it's still too long
        for section_doc in section_docs:
            sub_chunks = char_splitter.split_text(section_doc.page_content)
            for i, chunk_text in enumerate(sub_chunks):
                metadata = dict(section_doc.metadata)
                metadata["tenant_id"] = tenant_id
                metadata["source_file"] = file_path.name
                metadata["chunk_index"] = i
                all_chunks.append(Document(page_content=chunk_text, metadata=metadata))

    return all_chunks


if __name__ == "__main__":
    for slug in list_tenants():
        chunks = load_and_chunk_tenant(slug)
        n_docs = len(list((TENANTS_DIR / slug).glob("*.md")))
        print(f"{slug:20s} {n_docs} docs -> {len(chunks):3d} chunks")

    tenants = list_tenants()
    if tenants:
        print("\n--- Sample chunk ---")
        sample = load_and_chunk_tenant(tenants[0])[3]
        print(f"Tenant:  {sample.metadata.get('tenant_id')}")
        print(f"Source:  {sample.metadata.get('source_file')}")
        print(f"Section: {sample.metadata.get('section')}")
        print(f"Length:  {len(sample.page_content)} chars")
        print(f"Text:\n{sample.page_content[:300]}")
