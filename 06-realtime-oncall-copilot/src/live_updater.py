"""
live_updater.py
---------------
The core new module for this project: apply a live edit to a runbook or
incident note and reflect it in the retrieval index IMMEDIATELY, without a full
rebuild.

Mid-incident, an on-call engineer (or an automated system watching a chat
channel / ticket) is constantly editing the incident note: "we tried X, it
didn't work", "root cause is Y", "mitigation is command Z". The copilot is
useless if it answers from a stale snapshot taken at build time. `apply_update`
closes that loop: it writes the new content to disk and calls
`vectorstore.upsert_document`, which re-chunks and re-embeds ONLY that file and
swaps its chunks in place.

The `demo()` function proves it end to end: it asks a question, applies an
update that changes what the correct answer should be, asks the SAME question
again, and shows retrieval now surfaces the updated content — all without ever
calling build_vectorstore().
"""

from pathlib import Path
from typing import Optional

from vectorstore import upsert_document
from ingest import INCIDENT_NOTES_DIR
from rag_chain import retrieve
from cost_router import RouteDecision


def apply_update(file_path, new_content: str, mode: str = "write") -> dict:
    """Write new content to file_path and incrementally re-index that one file.

    mode:
      "write"  -> replace the file's contents with new_content (an edit).
      "append" -> append new_content to the existing file (a live addendum).

    Returns the upsert summary dict from vectorstore.upsert_document.
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if mode == "append" and file_path.exists():
        existing = file_path.read_text(encoding="utf-8")
        combined = existing.rstrip() + "\n\n" + new_content.lstrip()
        file_path.write_text(combined, encoding="utf-8")
    else:
        file_path.write_text(new_content, encoding="utf-8")

    summary = upsert_document(file_path)
    return summary


def _sources(query: str):
    # Deliberately bypass the cost_router heuristic here: this demo exists to
    # prove the live-update mechanism is visible to retrieval, not to exercise
    # routing. A ~65-chunk corpus needs a wider candidate pool than the
    # "simple" route's k=3 to reliably surface one specific new document
    # alongside everything else, independent of how a given query happens to
    # be phrased.
    decision = RouteDecision(route="demo", k=8, rerank=True, reason="live-update demo: wide retrieval")
    chunks = retrieve(query, decision=decision)
    return chunks


def demo(query: Optional[str] = None, cleanup: bool = True) -> bool:
    """Run the live-update proof end to end and print it.

    Returns True if retrieval genuinely changed to reflect the update.
    """
    query = query or "What is the current mitigation for the payment reconciliation incident?"

    # A fresh incident note that does NOT exist in the built index yet. The
    # marker string is what we assert on: it can only appear if the live upsert
    # actually indexed the new file.
    note_path = INCIDENT_NOTES_DIR / "2026-07-12-live-demo.md"
    marker = "MITIGATION-XYZ-777"

    initial_content = f"""# Incident 2026-07-12: payment reconciliation drift (LIVE)

**Incident ID:** INC-2026-0712
**Severity:** SEV2
**Status:** investigating

## Summary
Nightly payment reconciliation is reporting a small drift between processor
charges and local confirmations. Under investigation. No mitigation confirmed yet.

## Current Mitigation
None yet - still diagnosing whether this is a duplicate-charge issue or a
reporting lag.
"""

    updated_content = f"""# Incident 2026-07-12: payment reconciliation drift (LIVE)

**Incident ID:** INC-2026-0712
**Severity:** SEV2
**Status:** mitigating

## Summary
Nightly payment reconciliation drift was root-caused to a retry storm creating
duplicate charges during a processor slowdown.

## Current Mitigation
Confirmed mitigation {marker}: run `payctl reconcile --since 2026-07-12T00:00Z`
to auto-refund the duplicate charges, and enable `payctl retry-mode safe` to
stop new duplicates. This is the current authoritative mitigation for INC-2026-0712.
"""

    print(f"\n{'#'*74}\n# LIVE-UPDATE DEMO\n{'#'*74}")
    print(f"Query under test:\n  \"{query}\"\n")

    try:
        # --- Stage 1: index the initial note and query it ---
        print("[1] Indexing initial incident note (no mitigation yet) via incremental upsert...")
        s1 = apply_update(note_path, initial_content, mode="write")
        print(f"    upsert: +{s1['chunks_added']} chunks, -{s1['chunks_removed']} removed, "
              f"collection now {s1['collection_count']} chunks\n")

        print("[2] Retrieval BEFORE the live update:")
        before = _sources(query)
        before_has_marker = any(marker in c.text for c in before)
        for i, c in enumerate(before, 1):
            print(f"    [{i}] score={c.score}  {c.source_file}  ({c.section})")
        top_before = before[0].text.strip().splitlines()[-1] if before else "(none)"
        print(f"    top-1 mitigation line: {top_before!r}")
        print(f"    contains marker {marker!r}? {before_has_marker}\n")

        # --- Stage 2: live edit changes the answer, then re-query ---
        print("[3] Applying LIVE update (engineer writes the confirmed mitigation)...")
        s2 = apply_update(note_path, updated_content, mode="write")
        print(f"    upsert: +{s2['chunks_added']} chunks, -{s2['chunks_removed']} removed, "
              f"collection now {s2['collection_count']} chunks")
        print("    NOTE: no build_vectorstore() call - only this one file was re-indexed.\n")

        print("[4] Retrieval AFTER the live update (SAME query):")
        after = _sources(query)
        after_has_marker = any(marker in c.text for c in after)
        for i, c in enumerate(after, 1):
            print(f"    [{i}] score={c.score}  {c.source_file}  ({c.section})")
        top_after = after[0].text.strip().splitlines()[-1] if after else "(none)"
        print(f"    top-1 mitigation line: {top_after!r}")
        print(f"    contains marker {marker!r}? {after_has_marker}\n")

        changed = after_has_marker and not before_has_marker
        print(f"{'='*74}")
        if changed:
            print("RESULT: PASS - retrieval changed live. The updated mitigation "
                  f"(marker {marker}) was\n        absent before the edit and present after, "
                  "with NO full rebuild.")
        else:
            print("RESULT: FAIL - retrieval did not reflect the live update.")
        print(f"{'='*74}\n")
        return changed
    finally:
        if cleanup and note_path.exists():
            # Remove the demo note from disk AND from the index so repeated runs
            # start clean and the demo leaves no artifact behind.
            note_path.unlink()
            try:
                upsert_document(note_path)  # file now gone -> deletes its chunks
            except Exception:
                pass


if __name__ == "__main__":
    demo()
