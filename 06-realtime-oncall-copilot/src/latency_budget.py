"""
latency_budget.py
-----------------
A small, dependency-free stage timer for a latency-sensitive pipeline.

On-call tooling is used while something is already on fire, so it has a hard
latency budget: a copilot that takes four seconds to answer "what's the
failover command" is useless when the pager is going off. This module lets you
wrap each pipeline stage (embed the query, search the vector store, generate)
in a named timer, accumulate timings across many queries, and print a p50/p95
breakdown per stage against a documented target budget.

Usage:
    timer = StageTimer()
    with timer.stage("embed_query"):
        vec = embedder.embed_query(q)
    with timer.stage("vector_search"):
        results = collection.query(...)
    ...
    timer.report()   # prints p50/p95 per stage and pass/fail vs budget

The design is intentionally boring: plain wall-clock timing with
time.perf_counter(), stored in memory. It is a starting point for real
observability, not a replacement for it (see "What would change for
production" in the README).
"""

import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, List

# Documented per-stage target budget, in milliseconds. These are p95 targets:
# 95% of queries should complete each stage under this bound. Numbers chosen
# for the local TF-IDF + Chroma path on a laptop; generation is measured but
# left generous because it depends on the external LLM provider.
BUDGET_P95_MS: Dict[str, float] = {
    "embed_query": 50.0,
    "vector_search": 100.0,
    "generation": 4000.0,
}


def percentile(values: List[float], pct: float) -> float:
    """Nearest-rank percentile (pct in [0, 100]). Returns 0.0 for empty input.

    Nearest-rank is used (rather than linear interpolation) because it's simple
    and unambiguous to reason about in a test: p95 of 20 samples is the value at
    rank ceil(0.95 * 20) = 19, i.e. the 19th-smallest.
    """
    if not values:
        return 0.0
    ordered = sorted(values)
    if pct <= 0:
        return ordered[0]
    rank = int((pct / 100.0) * len(ordered))
    if rank < 1:
        rank = 1
    if rank > len(ordered):
        rank = len(ordered)
    return ordered[rank - 1]


@dataclass
class StageTimer:
    """Accumulates per-stage timings (in milliseconds) across many queries."""

    timings_ms: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            self.timings_ms[name].append(elapsed_ms)

    def record(self, name: str, elapsed_ms: float):
        """Manually record a timing (used by tests with synthetic data)."""
        self.timings_ms[name].append(elapsed_ms)

    def reset(self):
        self.timings_ms = defaultdict(list)

    def stage_stats(self, name: str) -> dict:
        samples = self.timings_ms.get(name, [])
        return {
            "count": len(samples),
            "p50": percentile(samples, 50),
            "p95": percentile(samples, 95),
            "max": max(samples) if samples else 0.0,
        }

    def report(self, budget: Dict[str, float] = None) -> bool:
        """Print a p50/p95 breakdown per stage and whether each meets its p95
        budget. Returns True iff every stage with a defined budget passes."""
        budget = budget if budget is not None else BUDGET_P95_MS
        # Preserve a sensible stage order: known budget stages first, then any
        # extra stages that were recorded.
        ordered_stages = [s for s in budget if s in self.timings_ms]
        ordered_stages += [s for s in self.timings_ms if s not in budget]

        n_queries = max((len(v) for v in self.timings_ms.values()), default=0)
        print(f"\n{'='*74}")
        print(f"LATENCY REPORT  (per-stage, across {n_queries} recorded call(s))")
        print(f"{'='*74}")
        header = f"{'stage':<18}{'count':>7}{'p50 ms':>11}{'p95 ms':>11}{'budget p95':>13}{'status':>10}"
        print(header)
        print("-" * 74)

        all_pass = True
        for name in ordered_stages:
            stats = self.stage_stats(name)
            budget_ms = budget.get(name)
            if budget_ms is None:
                status = "  (no SLO)"
            else:
                passed = stats["p95"] <= budget_ms
                all_pass = all_pass and passed
                status = "  PASS" if passed else "  FAIL"
            budget_str = f"{budget_ms:.0f}" if budget_ms is not None else "-"
            print(f"{name:<18}{stats['count']:>7}{stats['p50']:>11.2f}"
                  f"{stats['p95']:>11.2f}{budget_str:>13}{status:>10}")

        print("-" * 74)
        overall = "MEETS BUDGET" if all_pass else "OVER BUDGET"
        print(f"Overall (stages with an SLO): {overall}")
        print(f"{'='*74}\n")
        return all_pass


# A module-level default timer so the pipeline can accumulate across queries in
# an interactive session without threading a timer object through every call.
GLOBAL_TIMER = StageTimer()
