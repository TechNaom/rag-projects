"""
test_citation_levels.py
-----------------------
Real assertions that citation_auditor correctly identifies pass/fail at each of
L1-L4 for constructed (answer, chunks) pairs — including one example that must
fail L3 (cites a chunk that doesn't support the claim) and one that must fail L4
(cites a superseded chunk).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from citation_auditor import audit_answer  # noqa: E402
from currency_filter import RetrievedChunk  # noqa: E402


def make_chunk(chunk_id, text, doc_id, version, status, superseded_by=""):
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=text,
        source_file=f"{doc_id}.md",
        section="Standard Retention Period",
        doc_id=doc_id,
        title="Patient Records Data Retention Policy",
        version=version,
        status=status,
        effective_date="2025-01-01",
        superseded_by=superseded_by,
        score=0.9,
    )


CURRENT_RETENTION = make_chunk(
    "chunk_0",
    "Adult patient medical records must be retained for a minimum of ten (10) "
    "years from the date of the patient's last treatment or discharge.",
    "RETEN-002", "2.0", "current",
)

SUPERSEDED_RETENTION = make_chunk(
    "chunk_9",
    "Adult patient medical records must be retained for a minimum of six (6) "
    "years from the date of the patient's last treatment or discharge.",
    "RETEN-001", "1.0", "superseded", superseded_by="RETEN-002",
)

UNRELATED_CHUNK = make_chunk(
    "chunk_20",
    "Vendor access is time-bound and automatically expires at the end of the "
    "contract term unless formally renewed.",
    "VEND-001", "1.0", "current",
)


def _levels(result):
    return {lvl.level: lvl.passed for lvl in result.levels}


def test_l0_uncited_answer_fails_l1():
    answer = "Records are retained for ten years."  # no marker, no doc_id
    result = audit_answer(answer, [CURRENT_RETENTION])
    assert result.highest_level == 0
    assert _levels(result)["L1"] is False


def test_l1_passes_when_some_citation_present():
    # Two sentences, only one carries a citation -> L1 passes, L2 fails.
    answer = ("Adult patient records must be retained for ten (10) years [1]. "
              "This also applies to imaging studies.")
    result = audit_answer(answer, [CURRENT_RETENTION])
    levels = _levels(result)
    assert levels["L1"] is True
    assert levels["L2"] is False
    assert result.highest_level == 1


def test_l4_full_pass_on_current_supported_answer():
    answer = ("Adult patient medical records must be retained for ten (10) years "
              "from the date of last treatment [1] (per RETEN-002).")
    result = audit_answer(answer, [CURRENT_RETENTION])
    levels = _levels(result)
    assert levels["L1"] and levels["L2"] and levels["L3"] and levels["L4"]
    assert result.highest_level == 4


def test_fails_l3_when_citation_does_not_support_claim():
    # Claim is about retention periods; the cited chunk [1] is about vendor access.
    answer = ("Adult patient medical records must be retained for ten (10) years "
              "from the date of last treatment [1].")
    result = audit_answer(answer, [UNRELATED_CHUNK])
    levels = _levels(result)
    assert levels["L1"] is True
    assert levels["L2"] is True          # every sentence has a marker
    assert levels["L3"] is False         # ...but the chunk doesn't support it
    assert levels["L4"] is False         # L4 cannot pass once L3 fails
    assert result.highest_level == 2


def test_fails_l4_when_citing_superseded_source():
    # The claim IS supported by the cited chunk (keyword overlap high), but the
    # cited chunk is a SUPERSEDED version -> passes L1-L3, fails L4.
    answer = ("Adult patient medical records must be retained for a minimum of "
              "six (6) years from the date of last treatment [1] (per RETEN-001).")
    result = audit_answer(answer, [SUPERSEDED_RETENTION])
    levels = _levels(result)
    assert levels["L1"] and levels["L2"] and levels["L3"]
    assert levels["L4"] is False
    assert result.highest_level == 3


def test_result_serializes_to_dict():
    result = audit_answer("Records kept ten years [1] (per RETEN-002).", [CURRENT_RETENTION])
    data = result.as_dict()
    assert data["highest_level"] == result.highest_level
    assert len(data["levels"]) == 4
    assert {lvl["level"] for lvl in data["levels"]} == {"L1", "L2", "L3", "L4"}
