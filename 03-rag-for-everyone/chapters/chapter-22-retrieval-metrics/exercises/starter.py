"""Chapter 22 exercise: calculate retrieval metrics.

You are preparing a tiny offline evaluator for a RAG release review.
Fill the TODOs so each case becomes a metric report that an engineer can act on.
"""

CASES = [
    {
        "id": "policy_refund",
        "domain": "policy",
        "query_type": "policy_lookup",
        "risk": "high",
        "gold": {"S2", "S4"},
        "retrieved": ["S1", "S2", "S3", "S4", "S8"],
        "stale": set(),
        "filtered_gold": set(),
    },
    {
        "id": "support_error_code",
        "domain": "support",
        "query_type": "exact_term",
        "risk": "high",
        "gold": {"ERR_8842"},
        "retrieved": ["RUNBOOK_TIMEOUT", "SUPPORT_FAQ", "ERR_8842"],
        "stale": set(),
        "filtered_gold": set(),
    },
    {
        "id": "finance_limits",
        "domain": "finance",
        "query_type": "table_lookup",
        "risk": "medium",
        "gold": {"LIMIT_ROW_7"},
        "retrieved": ["LIMITS_OLD", "FINANCE_FAQ", "EXPENSE_POLICY"],
        "stale": {"LIMITS_OLD"},
        "filtered_gold": set(),
    },
]


def metric_report(case, k=3):
    # TODO: calculate top_k, hits, first relevant rank, recall, precision, and MRR.
    # TODO: include stale_hit_count and filtered_gold_count.
    # TODO: add a diagnosis string that explains the likely engineering problem.
    # Hint: partial recall is not healthy for a high-risk multi-evidence answer.
    return {"id": case["id"]}


def summarize(cases, k=3):
    # TODO: return per-case reports and simple overall averages.
    return {"results": [metric_report(case, k) for case in cases]}


if __name__ == "__main__":
    print(summarize(CASES, k=3))
