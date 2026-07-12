"""
trace_store.py
--------------
An append-only audit trail. Every answered query is written as one JSON line to
data/traces.jsonl: when it was asked, the exact question, which chunks were
retrieved (with their doc_id / version / status), the citation-auditor verdict,
and the answer text.

Why append-only JSON Lines: it is the simplest thing that is genuinely
tamper-evident-friendly and replayable. Each record stands alone, the file only
ever grows, and a reviewer (or the report generator) can reconstruct exactly
what evidence produced a given answer at a given time. A production system would
put this in an append-only/WORM database with real integrity protection (see the
README's "What would change for production"); the data shape here is the same.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from citation_auditor import CitationAuditResult
from currency_filter import RetrievedChunk

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_PATH = PROJECT_ROOT / "data" / "traces.jsonl"


def _sign(record: Dict) -> str:
    """A lightweight content signature over the trace record.

    This is a SHA-256 digest, NOT a cryptographic signature — there is no
    private key, so it proves integrity (the record wasn't altered after
    logging) but not authenticity. The README's production section describes
    swapping this for a real digital signature (e.g. Ed25519 / an HSM-backed
    key). The field exists here so the trace and report formats already carry
    a signature slot.
    """
    payload = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def build_trace_record(
    query: str,
    chunks: List[RetrievedChunk],
    audit_result: CitationAuditResult,
    answer: str,
    provider: Optional[str] = None,
    include_superseded: bool = False,
) -> Dict:
    """Assemble (but do not yet write) the structured trace record for a query."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "provider": provider or "",
        "include_superseded": include_superseded,
        "retrieved_chunks": [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "title": c.title,
                "version": c.version,
                "status": c.status,
                "effective_date": c.effective_date,
                "superseded_by": c.superseded_by,
                "section": c.section,
                "source_file": c.source_file,
                "score": c.score,
                "excerpt": c.text,
            }
            for c in chunks
        ],
        "citation_audit": audit_result.as_dict(),
        "answer": answer,
    }
    record["signature"] = _sign(record)
    return record


def log_trace(
    query: str,
    chunks: List[RetrievedChunk],
    audit_result: CitationAuditResult,
    answer: str,
    provider: Optional[str] = None,
    include_superseded: bool = False,
    trace_path: Path = TRACE_PATH,
) -> Dict:
    """Append a trace record for a single answered query and return it."""
    record = build_trace_record(
        query, chunks, audit_result, answer,
        provider=provider, include_superseded=include_superseded,
    )
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def read_traces(trace_path: Path = TRACE_PATH) -> List[Dict]:
    """Read all trace records (oldest first)."""
    if not trace_path.exists():
        return []
    records = []
    with open(trace_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def latest_trace_for_query(query: str, trace_path: Path = TRACE_PATH) -> Optional[Dict]:
    """Return the most recent trace whose query matches, or None."""
    match = None
    for record in read_traces(trace_path):
        if record.get("query") == query:
            match = record
    return match


def verify_signature(record: Dict) -> bool:
    """Recompute the integrity signature and confirm the record is unaltered."""
    stored = record.get("signature", "")
    payload = {k: v for k, v in record.items() if k != "signature"}
    return _sign(payload) == stored


if __name__ == "__main__":
    for rec in read_traces():
        ok = "OK" if verify_signature(rec) else "TAMPERED"
        print(f"[{ok}] {rec['timestamp']}  {rec['citation_audit']['summary']:>3}  {rec['query']}")
