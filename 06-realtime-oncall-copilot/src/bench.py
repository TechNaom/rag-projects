"""
bench.py
--------
Runs a batch of real on-call queries through the routed, timed retrieval
pipeline and prints:
  1. how the cost router classified each query, and
  2. a p50/p95 latency breakdown per stage vs the documented budget.

Generation is skipped (no LLM required) so this exercises the retrieval hot
path deterministically. Run it after building the index:

    python src/vectorstore.py   # once
    python src/bench.py
"""

from cost_router import classify
from latency_budget import StageTimer
from rag_chain import retrieve

# A realistic mix of simple lookups and complex/analytical questions.
QUERIES = [
    "What's the command to manually fail over orders-prod?",
    "certificate expiry mitigation command",
    "how do I redrive a poison message on the events queue?",
    "gateway 5xx rollback command",
    "raise the payments outbound timeout",
    "Why did checkout start returning 504s after the payments deploy?",
    "What is the root cause of the June 21 queue backlog incident?",
    "Compare the database storage-full incident to the standard failover runbook",
    "Walk me through diagnosing elevated p99 latency step by step",
    "explain how a duplicate charge happens during a payment processor timeout",
]

# Repeat the batch a few times so p50/p95 have enough samples to be meaningful.
REPEATS = 3


def run_router_preview():
    print(f"\n{'='*74}\nCOST ROUTER CLASSIFICATION\n{'='*74}")
    for q in QUERIES:
        d = classify(q)
        print(f"[{d.route:7s}] k={d.k} rerank={str(d.rerank):5s}  {q}")
        print(f"            reason: {d.reason}")


def run_bench():
    timer = StageTimer()
    for _ in range(REPEATS):
        for q in QUERIES:
            retrieve(q, decision=classify(q), timer=timer)
    n = len(QUERIES) * REPEATS
    print(f"\nRan {n} queries ({len(QUERIES)} unique x {REPEATS} repeats) through the pipeline.")
    timer.report()


if __name__ == "__main__":
    run_router_preview()
    run_bench()
