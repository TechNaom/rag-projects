"""
ingest.py
---------
Loads the runbooks and incident notes and splits them into overlapping chunks.

Two document types live in this corpus and they behave differently:
- runbooks/       change rarely, are authored carefully, and describe the
                  standard procedure for a class of incident.
- incident_notes/ change FREQUENTLY — they're edited/added mid-incident as an
                  engineer writes up what's happening. These are the documents
                  that make a live-updating index worth building.

Every chunk is tagged with `doc_type` (runbook | incident_note) and
`source_file` so retrieval can tell the two apart and so a single file's
chunks can be found and replaced during a live upsert (see vectorstore.py).

Chunking matters more than people expect: too large and retrieval pulls in
irrelevant text alongside the relevant sentence; too small and you lose the
surrounding context a step needs to make sense. For header-structured
markdown, splitting on headers first, then on size within each section, keeps
each chunk topically coherent.
"""

from pathlib import Path
from typing import List

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RUNBOOKS_DIR = DATA_DIR / "runbooks"
INCIDENT_NOTES_DIR = DATA_DIR / "incident_notes"

HEADERS_TO_SPLIT_ON = [
    ("#", "doc_title"),
    ("##", "section"),
]

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Which directory maps to which doc_type, so ingest is the single source of truth.
DOC_SOURCES = [
    (RUNBOOKS_DIR, "runbook"),
    (INCIDENT_NOTES_DIR, "incident_note"),
]


def _splitters(chunk_size: int, chunk_overlap: int):
    md_header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return md_header_splitter, char_splitter


def chunk_file(
    file_path: Path,
    doc_type: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Chunk a SINGLE markdown file into Documents tagged with doc_type/source_file.

    This is factored out of load_and_chunk_documents so the live updater can
    re-chunk exactly one file without touching the rest of the corpus.
    """
    md_header_splitter, char_splitter = _splitters(chunk_size, chunk_overlap)
    raw_text = file_path.read_text(encoding="utf-8")

    # Step 1: split by markdown section headers, so each piece stays within
    # one section (e.g. never spans "Diagnosis Steps" into "Common Causes").
    section_docs = md_header_splitter.split_text(raw_text)

    chunks: List[Document] = []
    chunk_index = 0  # runs across the WHOLE file, not reset per section, so
    # `<source_file>::<chunk_index>` (see vectorstore._chunk_id) stays unique
    # even when a file has multiple ## sections producing multiple chunk 0s.
    for section_doc in section_docs:
        # Step 2: within each section, further split by size if still too long.
        sub_chunks = char_splitter.split_text(section_doc.page_content)
        for chunk_text in sub_chunks:
            metadata = dict(section_doc.metadata)
            metadata["source_file"] = file_path.name
            metadata["doc_type"] = doc_type
            metadata["chunk_index"] = chunk_index
            chunks.append(Document(page_content=chunk_text, metadata=metadata))
            chunk_index += 1
    return chunks


def load_and_chunk_documents(
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Load every .md file across runbooks/ and incident_notes/ and return
    a flat list of chunked Documents."""
    all_chunks: List[Document] = []
    for source_dir, doc_type in DOC_SOURCES:
        if not source_dir.exists():
            continue
        for file_path in sorted(source_dir.glob("*.md")):
            all_chunks.extend(
                chunk_file(file_path, doc_type, chunk_size, chunk_overlap)
            )
    return all_chunks


def doc_type_for_path(file_path: Path) -> str:
    """Infer doc_type from which data directory a file lives in."""
    file_path = Path(file_path).resolve()
    for source_dir, doc_type in DOC_SOURCES:
        try:
            file_path.relative_to(source_dir.resolve())
            return doc_type
        except ValueError:
            continue
    # Default new files that aren't under a known dir to incident_note, since
    # that's the live-authored type.
    return "incident_note"


if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    n_runbooks = len(list(RUNBOOKS_DIR.glob("*.md")))
    n_incidents = len(list(INCIDENT_NOTES_DIR.glob("*.md")))
    print(f"Loaded {n_runbooks} runbooks + {n_incidents} incident notes "
          f"into {len(chunks)} chunks.\n")
    print("--- Sample chunk ---")
    sample = chunks[len(chunks) // 2]
    print(f"Source:   {sample.metadata.get('source_file')}")
    print(f"DocType:  {sample.metadata.get('doc_type')}")
    print(f"Section:  {sample.metadata.get('section')}")
    print(f"Length:   {len(sample.page_content)} chars")
    print(f"Text:\n{sample.page_content[:400]}")
