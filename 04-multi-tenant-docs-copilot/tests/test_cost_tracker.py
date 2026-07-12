"""
test_cost_tracker.py
--------------------
Verifies that per-tenant cost/latency accounting accumulates correctly and stays
attributed to the right tenant. Uses a temp cost-log file so it never touches the
real data/cost_log.json.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import cost_tracker


@pytest.fixture
def log_path(tmp_path):
    return tmp_path / "cost_log.json"


def test_estimate_tokens_is_word_based():
    # 10 words * 1.3 = 13 tokens (approximation documented in the module).
    text = "one two three four five six seven eight nine ten"
    assert cost_tracker.estimate_tokens(text) == 13
    assert cost_tracker.estimate_tokens("") == 0


def test_record_query_accumulates_per_tenant(log_path):
    cost_tracker.record_query("tenant-a", "a b c", "x y", latency_s=0.5, path=log_path)
    cost_tracker.record_query("tenant-a", "d e", "z", latency_s=0.25, path=log_path)
    cost_tracker.record_query("tenant-b", "one two three four", "answer here", latency_s=1.0, path=log_path)

    log = cost_tracker.summary(log_path)

    assert log["tenant-a"]["queries"] == 2
    assert log["tenant-b"]["queries"] == 1

    # tenant-a prompt tokens: (3 words + 2 words) * 1.3 = round(3.9)+round(2.6)=4+3=7
    assert log["tenant-a"]["prompt_tokens"] == 7
    # latency accumulates
    assert log["tenant-a"]["total_latency_s"] == pytest.approx(0.75)
    # totals are internally consistent
    for rec in log.values():
        assert rec["total_tokens"] == rec["prompt_tokens"] + rec["completion_tokens"]


def test_tenants_do_not_bleed_into_each_other(log_path):
    cost_tracker.record_query("tenant-a", "hello world", "hi", latency_s=0.1, path=log_path)
    cost_tracker.record_query("tenant-b", "foo bar baz", "ok", latency_s=0.2, path=log_path)

    log = cost_tracker.summary(log_path)
    # Each tenant only counts its own queries.
    assert log["tenant-a"]["queries"] == 1
    assert log["tenant-b"]["queries"] == 1
    assert set(log.keys()) == {"tenant-a", "tenant-b"}


def test_track_context_manager_records_latency_and_completion(log_path):
    with cost_tracker.track("tenant-a", prompt_text="what is the flight time", path=log_path) as usage:
        usage["completion_text"] = "about 34 minutes"

    log = cost_tracker.summary(log_path)
    assert log["tenant-a"]["queries"] == 1
    assert log["tenant-a"]["completion_tokens"] > 0
    assert log["tenant-a"]["total_latency_s"] >= 0.0


def test_dashboard_renders_and_reset_clears(log_path):
    cost_tracker.record_query("tenant-a", "a b c", "x", latency_s=0.3, path=log_path)
    table = cost_tracker.format_dashboard(log_path)
    assert "tenant-a" in table
    assert "PER-TENANT COST & LATENCY DASHBOARD" in table

    cost_tracker.reset(log_path)
    assert cost_tracker.summary(log_path) == {}
    empty_table = cost_tracker.format_dashboard(log_path)
    assert "no queries recorded yet" in empty_table
