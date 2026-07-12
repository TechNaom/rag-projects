"""
cost_router.py
--------------
A simple, transparent heuristic router that classifies each incoming question
as "simple" or "complex" and picks a cheaper or fuller retrieval path
accordingly.

WHY THIS EXISTS:
Not every on-call question needs the full pipeline. "What's the failover
command for orders-prod?" is a lookup — a small k and no extra work will
answer it. "Why did checkout start returning 504s and how does that compare to
the May incident?" is a reasoning question that benefits from retrieving more
context. Running the heavy path for every query wastes latency and, with a
paid LLM, money. Routing simple queries to a cheaper path is a standard
cost/latency optimization in production RAG.

IMPORTANT — this is a HEURISTIC, not ML:
The classifier below is a documented starting point: length thresholds plus a
keyword list. It is deliberately simple and auditable, NOT a claim of
ML-grade intent classification. In production you'd likely replace it with a
tiny trained classifier or a fast small-model call (see the README). The value
here is the ROUTING SEAM — the pipeline asks the router which path to take, so
the classifier can be upgraded without touching the pipeline.
"""

from dataclasses import dataclass

# Words/phrases that signal a reasoning/analytical question rather than a lookup.
COMPLEX_KEYWORDS = (
    "root cause",
    "why",
    "compare",
    "difference between",
    "versus",
    " vs ",
    "explain",
    "how does",
    "what caused",
    "correlate",
    "trade-off",
    "tradeoff",
    "walk me through",
    "step by step",
    "post-incident",
    "postmortem",
)

# A question longer than this many words is treated as complex regardless of
# keywords — long questions usually carry multiple constraints.
COMPLEX_WORD_COUNT = 18


@dataclass
class RouteDecision:
    route: str          # "simple" or "complex"
    k: int              # how many chunks to retrieve
    rerank: bool        # whether to run the extra reranking-style step
    reason: str         # human-readable explanation (for logs / the CLI)


# Path parameters per route. The "simple" path retrieves fewer chunks and skips
# the extra rerank pass; the "complex" path retrieves more and reranks.
SIMPLE_ROUTE = dict(k=3, rerank=False)
COMPLEX_ROUTE = dict(k=6, rerank=True)


def classify(query: str) -> RouteDecision:
    """Classify a query and return the routing decision.

    Rules, in order:
      1. Any complex keyword present            -> complex
      2. Word count > COMPLEX_WORD_COUNT        -> complex
      3. Otherwise                              -> simple
    """
    text = query.lower().strip()
    word_count = len(text.split())

    matched = next((kw for kw in COMPLEX_KEYWORDS if kw in text), None)
    if matched:
        return RouteDecision(
            route="complex",
            reason=f"matched complex keyword '{matched.strip()}'",
            **COMPLEX_ROUTE,
        )

    if word_count > COMPLEX_WORD_COUNT:
        return RouteDecision(
            route="complex",
            reason=f"long query ({word_count} words > {COMPLEX_WORD_COUNT})",
            **COMPLEX_ROUTE,
        )

    return RouteDecision(
        route="simple",
        reason=f"short lookup-style query ({word_count} words, no complex keywords)",
        **SIMPLE_ROUTE,
    )


if __name__ == "__main__":
    examples = [
        "What's the failover command for orders-prod?",
        "Why did checkout start returning 504s and how does it compare to the May incident?",
        "certificate expiry mitigation",
        "Walk me through the root cause analysis for the queue backlog on June 21",
    ]
    for q in examples:
        d = classify(q)
        print(f"[{d.route:7s}] k={d.k} rerank={d.rerank}  <- {d.reason}\n           {q}")
