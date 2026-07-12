"""
test_version_currency.py
------------------------
Asserts the currency filter's core guarantees against the REAL built vector
store:

  * default retrieval never returns a superseded chunk,
  * include_superseded=True does surface a superseded chunk when relevant,
  * verify_currency correctly flags superseded vs current.

These run against a live ChromaDB collection. If the index hasn't been built,
the module builds it once before the tests run, so `pytest` works from a clean
clone.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import vectorstore  # noqa: E402
from currency_filter import retrieve, verify_currency  # noqa: E402

RETENTION_QUERY = "How long must adult patient medical records be retained?"


@pytest.fixture(scope="module", autouse=True)
def ensure_index_built():
    """Build the vector store once if it isn't present, so tests are self-contained."""
    try:
        vectorstore.clear_vectorstore_cache()
        vectorstore.load_vectorstore()
    except Exception:
        vectorstore.build_vectorstore(rebuild=True)
    yield


def test_default_retrieval_excludes_superseded():
    chunks = retrieve(RETENTION_QUERY, k=5)
    assert chunks, "expected at least one retrieved chunk"
    assert all(c.status == "current" for c in chunks), \
        f"superseded chunk leaked into default retrieval: {[(c.doc_id, c.status) for c in chunks]}"
    # And specifically the superseded retention policy must not appear.
    assert all(c.doc_id != "RETEN-001" for c in chunks)


def test_default_retrieval_surfaces_current_retention_policy():
    chunks = retrieve(RETENTION_QUERY, k=5)
    doc_ids = {c.doc_id for c in chunks}
    assert "RETEN-002" in doc_ids, f"current retention policy not retrieved; got {doc_ids}"


def test_include_superseded_returns_superseded_version():
    chunks = retrieve(RETENTION_QUERY, k=8, include_superseded=True)
    statuses = {c.status for c in chunks}
    doc_ids = {c.doc_id for c in chunks}
    assert "superseded" in statuses, f"expected a superseded chunk; statuses={statuses}"
    assert "RETEN-001" in doc_ids, f"expected superseded RETEN-001; got {doc_ids}"


def test_verify_currency_flags_current_and_superseded():
    all_versions = retrieve(RETENTION_QUERY, k=8, include_superseded=True)
    current = next(c for c in all_versions if c.doc_id == "RETEN-002")
    superseded = next(c for c in all_versions if c.doc_id == "RETEN-001")

    current_proof = verify_currency(current)
    assert current_proof["is_current"] is True
    assert "CURRENT" in current_proof["verdict"]

    superseded_proof = verify_currency(superseded)
    assert superseded_proof["is_current"] is False
    assert superseded_proof["superseded_by"] == "RETEN-002"
    assert "SUPERSEDED" in superseded_proof["verdict"]


def test_current_and_superseded_disagree_on_retention_period():
    """The whole point: the two versions state different retention periods, and
    the default (current-only) retrieval must reflect the NEW value."""
    current_only = retrieve(RETENTION_QUERY, k=5)
    current_text = " ".join(c.text.lower() for c in current_only)
    assert "ten (10) years" in current_text or "10) years" in current_text
    assert "six (6) years" not in current_text
