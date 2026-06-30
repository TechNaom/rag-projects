"""
ingest.py
---------
Loads the raw policy documents and splits them into overlapping chunks.

Chunking matters more than people expect: too large and retrieval pulls in
irrelevant text alongside the relevant sentence; too small and you lose the
surrounding context a clause needs to make sense (e.g. a numbered list item
without the header explaining what it's a list OF). For policy documents
with numbered sections, splitting on markdown headers first, then on size
within each section, keeps each chunk topically coherent.
"""

from pathlib import Path
from typing import List

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

RAW_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "raw_docs"

HEADERS_TO_SPLIT_ON = [
    ("#", "doc_title"),
    ("##", "section"),
]

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100


def load_and_chunk_documents(
    raw_docs_dir: Path = RAW_DOCS_DIR,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Load every .md file in raw_docs_dir and return a flat list of chunked Documents."""

    md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks: List[Document] = []

    for file_path in sorted(raw_docs_dir.glob("*.md")):
        raw_text = file_path.read_text(encoding="utf-8")

        # Step 1: split by markdown section headers, so each piece stays
        # within one policy section (e.g. never spans "Section 3" into "Section 4")
        section_docs = md_header_splitter.split_text(raw_text)

        # Step 2: within each section, further split by size if it's still too long
        for section_doc in section_docs:
            sub_chunks = char_splitter.split_text(section_doc.page_content)
            for i, chunk_text in enumerate(sub_chunks):
                metadata = dict(section_doc.metadata)
                metadata["source_file"] = file_path.name
                metadata["chunk_index"] = i
                all_chunks.append(Document(page_content=chunk_text, metadata=metadata))

    return all_chunks


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    print(f"Loaded and chunked {len(list(RAW_DOCS_DIR.glob('*.md')))} documents into {len(chunks)} chunks.\n")
    print("--- Sample chunk ---")
    sample = chunks[5]
    print(f"Source: {sample.metadata.get('source_file')}")
    print(f"Section: {sample.metadata.get('section')}")
    print(f"Length: {len(sample.page_content)} chars")
    print(f"Text:\n{sample.page_content[:400]}")
