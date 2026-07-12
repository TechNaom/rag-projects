"""
ingest.py
---------
Loads the raw compliance documents and splits them into overlapping chunks.

This mirrors the chunking pattern from 01-policy-rag-poc (markdown-header
splitter + recursive character splitter), but adds one audit-grade step: each
document carries **YAML frontmatter** describing its version and lifecycle
status (doc_id, version, status, effective_date, superseded_by). We parse that
frontmatter first and stamp it onto EVERY chunk produced from the document, so
that downstream retrieval can filter by currency and every retrieved excerpt
knows exactly which authoritative version it came from.

Chunking matters more than people expect: too large and retrieval pulls in
irrelevant text alongside the relevant sentence; too small and you lose the
surrounding context a clause needs to make sense. For policy documents with
numbered sections, splitting on markdown headers first, then on size within
each section, keeps each chunk topically coherent.
"""

from pathlib import Path
from typing import Dict, List, Tuple

import yaml
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

# The frontmatter fields we require/expect on every compliance document.
FRONTMATTER_FIELDS = ("doc_id", "title", "version", "status", "effective_date", "superseded_by")


def parse_frontmatter(raw_text: str) -> Tuple[Dict[str, str], str]:
    """Split a markdown file into (frontmatter_dict, body_markdown).

    Frontmatter is a YAML block delimited by leading and trailing '---' lines,
    as used by Jekyll/Hugo/Obsidian. If no frontmatter is present we return an
    empty dict and the original text, so plain markdown still ingests cleanly.
    """
    stripped = raw_text.lstrip()
    if not stripped.startswith("---"):
        return {}, raw_text

    # Find the closing '---' that ends the frontmatter block.
    lines = stripped.splitlines()
    closing_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_index = i
            break
    if closing_index is None:
        return {}, raw_text

    yaml_block = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1:])
    parsed = yaml.safe_load(yaml_block) or {}

    # Normalize every value to a string so it is Chroma-metadata safe.
    frontmatter = {}
    for field in FRONTMATTER_FIELDS:
        value = parsed.get(field, "")
        frontmatter[field] = "" if value is None else str(value)
    return frontmatter, body


def load_and_chunk_documents(
    raw_docs_dir: Path = RAW_DOCS_DIR,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Load every .md file in raw_docs_dir and return a flat list of chunked Documents.

    Each returned Document's metadata includes the parsed frontmatter fields
    (doc_id, version, status, effective_date, superseded_by) plus the usual
    source_file / section / chunk_index bookkeeping.
    """

    md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks: List[Document] = []

    for file_path in sorted(raw_docs_dir.glob("*.md")):
        raw_text = file_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(raw_text)

        # Step 1: split by markdown section headers, so each piece stays
        # within one policy section (e.g. never spans "Section 3" into "Section 4")
        section_docs = md_header_splitter.split_text(body)

        # Step 2: within each section, further split by size if it's still too long
        for section_doc in section_docs:
            sub_chunks = char_splitter.split_text(section_doc.page_content)
            for i, chunk_text in enumerate(sub_chunks):
                metadata = dict(section_doc.metadata)
                metadata.update(frontmatter)  # doc_id / version / status / ...
                metadata["source_file"] = file_path.name
                metadata["chunk_index"] = i
                all_chunks.append(Document(page_content=chunk_text, metadata=metadata))

    return all_chunks


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    n_docs = len(list(RAW_DOCS_DIR.glob("*.md")))
    print(f"Loaded and chunked {n_docs} documents into {len(chunks)} chunks.\n")
    print("--- Sample chunk ---")
    sample = chunks[5]
    print(f"Source:  {sample.metadata.get('source_file')}")
    print(f"Doc ID:  {sample.metadata.get('doc_id')}  v{sample.metadata.get('version')}  [{sample.metadata.get('status')}]")
    print(f"Section: {sample.metadata.get('section')}")
    print(f"Length:  {len(sample.page_content)} chars")
    print(f"Text:\n{sample.page_content[:400]}")
