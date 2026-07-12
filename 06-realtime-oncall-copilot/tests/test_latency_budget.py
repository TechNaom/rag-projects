"""
test_latency_budget.py
----------------------
Unit tests for the stage timer and its p50/p95 math. These use synthetic
timing data (no real pipeline) so the percentile logic is verified exactly,
independent of machine speed.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from latency_budget import StageTimer, percentile


def test_percentile_nearest_rank_known_values():
    data = list(range(1, 101))  # 1..100
    # Nearest-rank: p50 -> rank 50 -> value 50; p95 -> rank 95 -> value 95.
    assert percentile(data, 50) == 50
    assert percentile(data, 95) == 95
    assert percentile(data, 100) == 100
    assert percentile([], 95) == 0.0
    assert percentile([42.0], 95) == 42.0


def test_percentile_unsorted_input():
    data = [30, 10, 50, 20, 40]  # sorted: [10, 20, 30, 40, 50]
    # p50 rank = int(0.5*5) = 2 -> 2nd smallest = 20
    assert percentile(data, 50) == 20
    # p95 rank = int(0.95*5) = int(4.75) = 4 -> 4th smallest = 40
    assert percentile(data, 95) == 40


def test_timer_records_counts_and_stats():
    timer = StageTimer()
    for ms in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        timer.record("vector_search", ms)

    stats = timer.stage_stats("vector_search")
    assert stats["count"] == 10
    # p50 rank = int(0.5*10)=5 -> 5th smallest = 50
    assert stats["p50"] == 50
    # p95 rank = int(0.95*10)=9 -> 9th smallest = 90
    assert stats["p95"] == 90
    assert stats["max"] == 100


def test_context_manager_accumulates_across_calls():
    timer = StageTimer()
    for _ in range(3):
        with timer.stage("embed_query"):
            time.sleep(0.005)  # 5ms
    stats = timer.stage_stats("embed_query")
    assert stats["count"] == 3
    # Each sleep is at least ~5ms; allow generous headroom for scheduler noise.
    assert stats["p50"] >= 4.0
    assert stats["max"] < 500.0


def test_report_pass_fail_against_budget():
    timer = StageTimer()
    # embed_query well under its 50ms budget -> PASS
    for ms in [5, 6, 7, 8, 9]:
        timer.record("embed_query", ms)
    # vector_search blowing past its 100ms budget -> FAIL
    for ms in [200, 210, 220, 230, 240]:
        timer.record("vector_search", ms)

    budget = {"embed_query": 50.0, "vector_search": 100.0}
    all_pass = timer.report(budget=budget)
    assert all_pass is False

    # With only the passing stage, the overall report should pass.
    timer2 = StageTimer()
    for ms in [5, 6, 7, 8, 9]:
        timer2.record("embed_query", ms)
    assert timer2.report(budget={"embed_query": 50.0}) is True


def test_reset_clears_timings():
    timer = StageTimer()
    timer.record("generation", 123.0)
    assert timer.stage_stats("generation")["count"] == 1
    timer.reset()
    assert timer.stage_stats("generation")["count"] == 0
