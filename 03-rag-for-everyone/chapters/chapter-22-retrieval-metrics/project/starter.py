"""Project starter: retrieval metrics dashboard seed.

Your task:
1. Compute per-case Recall@K, Precision@K, MRR, stale hits, and filtered gold.
2. Summarize metrics by slice and query type.
3. Block release for high-risk retrieval regressions.
"""

CASES = [
    {
        "id": "q_policy_refund",
        "slice": "policy",
        "query_type": "policy_lookup",
        "risk": "high",
        "gold": {"P4_REFUND_EXCEPTION"},
        "retrieved": ["P4_REFUND_EXCEPTION", "P4_REFUND_OVERVIEW", "FAQ_REFUND"],
        "stale": set(),
        "filtered_gold": set(),
    },
    {
        "id": "q_access_filter",
        "slice": "legal",
        "query_type": "restricted_policy",
        "risk": "high",
        "gold": {"LEGAL_ADDENDUM_12"},
        "retrieved": ["LEGAL_PUBLIC_SUMMARY", "POLICY_GENERAL"],
        "stale": set(),
        "filtered_gold": {"LEGAL_ADDENDUM_12"},
    },
]


def evaluate_case(case, k=3):
    # TODO: calculate recall_at_k, precision_at_k, mrr, and diagnosis.
    return {"id": case["id"]}


def evaluate(cases, k=3):
    # TODO: return release_gate, overall metrics, slice summaries, and failures.
    return {"results": [evaluate_case(case, k) for case in cases]}


if __name__ == "__main__":
    print(evaluate(CASES))
