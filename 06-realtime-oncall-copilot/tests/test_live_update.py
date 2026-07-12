"""
test_live_update.py
-------------------
Proves the WHOLE point of the project: an incremental upsert makes a live edit
to an incident note visible to retrieval WITHOUT a full index rebuild.

The test:
  1. Builds the index once (session fixture).
  2. Runs a query; asserts the marker string is absent from retrieval.
  3. Applies a live update (via live_updater.apply_update) that adds the marker.
  4. Runs the SAME query; asserts the marker now appears in retrieval.
  5. Guards the "no full rebuild" claim by monkeypatching build_vectorstore to
     blow up if it's ever called during the update path.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import vectorstore
import live_updater
from rag_chain import retrieve
from cost_router import classify

MARKER = "LIVEUPDATE-MARKER-9F3A"
DEMO_NOTE = vectorstore.INCIDENT_NOTES_DIR / "test_live_update_note.md"
# Phrased to naturally route to the "complex" path (k=6, rerank=True) via the
# "why" keyword - on this small a corpus, the simple path's k=3 with no rerank
# is too narrow to reliably surface a single new document's chunk alongside 64
# pre-existing ones; that is a retrieval-breadth tradeoff of the router, not a
# property of the incremental-upsert path this test exists to prove.
QUERY = "Why is the search indexer stalling, and what is the confirmed mitigation command?"


@pytest.fixture(scope="module", autouse=True)
def built_index():
    """Build the index once for this test module, then clean up the demo note."""
    vectorstore.build_vectorstore(rebuild=True)
    yield
    if DEMO_NOTE.exists():
        DEMO_NOTE.unlink()
    # Drop the note's chunks from the collection too, so the on-disk index is
    # left as it was before the test.
    try:
        vectorstore.upsert_document(DEMO_NOTE)
    except Exception:
        pass


def _retrieve(query):
    return retrieve(query, decision=classify(query))


def test_live_update_changes_retrieval_without_rebuild(monkeypatch):
    initial = f"""# Incident TEST: search indexer stall

**Incident ID:** INC-TEST-0001
**Status:** investigating

## Current Mitigation
No mitigation confirmed yet - still diagnosing the search indexer stall.
"""

    updated = f"""# Incident TEST: search indexer stall

**Incident ID:** INC-TEST-0001
**Status:** mitigating

## Current Mitigation
Confirmed mitigation {MARKER}: restart the indexer workers with
`kubectl rollout restart deployment/search-indexer -n prod` and warm the cache.
This is the authoritative mitigation for the search indexer stall.
"""

    # Seed the initial note through the incremental path.
    live_updater.apply_update(DEMO_NOTE, initial, mode="write")

    before = _retrieve(QUERY)
    assert before, "expected some retrieval results before the update"
    assert not any(MARKER in c.text for c in before), (
        "marker should NOT be present before the live update"
    )

    # From here on, a full rebuild is forbidden: if the update path secretly
    # rebuilds, this makes the test fail loudly instead of passing dishonestly.
    def _boom(*args, **kwargs):
        raise AssertionError("build_vectorstore() must NOT be called on the live-update path")

    monkeypatch.setattr(vectorstore, "build_vectorstore", _boom)
    monkeypatch.setattr(live_updater, "upsert_document", vectorstore.upsert_document)

    summary = live_updater.apply_update(DEMO_NOTE, updated, mode="write")
    assert summary["chunks_added"] >= 1
    assert summary["source_file"] == DEMO_NOTE.name
    assert summary["doc_type"] == "incident_note"

    after = _retrieve(QUERY)
    assert any(MARKER in c.text for c in after), (
        "marker MUST be present after the live update - retrieval did not refresh"
    )
    # The updated file's chunk should be SOMEWHERE in the result set for this
    # targeted query - not necessarily ranked #1, since exact ranking on a
    # ~65-chunk corpus with a low-dimensional TF-IDF/SVD embedder is a
    # separate concern (embedding/ranking quality) from what this test proves
    # (a live edit becomes visible to retrieval without a full rebuild).
    assert any(c.source_file == DEMO_NOTE.name for c in after)


def test_upsert_removes_old_chunks_on_shrink():
    """Editing a file to fewer chunks must remove the orphaned old chunks."""
    big = "# Incident TEST shrink\n\n"
    big += "\n\n".join(f"## Section {i}\n" + ("word " * 120) for i in range(6))
    small = "# Incident TEST shrink\n\n## Only Section\nA single short section now."

    live_updater.apply_update(DEMO_NOTE, big, mode="write")
    collection, _ = vectorstore.load_vectorstore()
    count_big = len(collection.get(where={"source_file": DEMO_NOTE.name})["ids"])

    live_updater.apply_update(DEMO_NOTE, small, mode="write")
    collection, _ = vectorstore.load_vectorstore()
    count_small = len(collection.get(where={"source_file": DEMO_NOTE.name})["ids"])

    assert count_big > count_small, "shrinking a file should leave fewer chunks"
    assert count_small >= 1
