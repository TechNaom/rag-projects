"""Project solution: retrieval metrics dashboard seed.

This script is intentionally small enough for learners to read, but it models
real production ideas: gold labels, slice-level metrics, stale hits, filtered
gold, release gates, and diagnostic recommendations.
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
        "id": "q_exact_error",
        "slice": "support",
        "query_type": "exact_term",
        "risk": "high",
        "gold": {"ERR_8842_RUNBOOK"},
        "retrieved": ["RUNBOOK_TIMEOUT", "ERR_8842_RUNBOOK", "SUPPORT_OVERVIEW"],
        "stale": set(),
        "filtered_gold": set(),
    },
    {
        "id": "q_pdf_table",
        "slice": "finance",
        "query_type": "table_lookup",
        "risk": "medium",
        "gold": {"FIN_LIMITS_TABLE_ROW_7"},
        "retrieved": ["FIN_LIMITS_OLD", "FIN_POLICY_OVERVIEW", "EXPENSE_FAQ"],
        "stale": {"FIN_LIMITS_OLD"},
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
    top_k = case["retrieved"][:k]
    hits = [doc_id for doc_id in top_k if doc_id in case["gold"]]
    first_rank = next(
        (rank for rank, doc_id in enumerate(case["retrieved"], start=1) if doc_id in case["gold"]),
        None,
    )
    stale_hits = [doc_id for doc_id in top_k if doc_id in case["stale"]]
    recall = len(hits) / len(case["gold"]) if case["gold"] else 0.0
    precision = len(hits) / k if k else 0.0
    mrr = 1 / first_rank if first_rank else 0.0

    if case["filtered_gold"]:
        diagnosis = "filtered_gold"
        recommendation = "Inspect metadata, tenant, access, and freshness filters before tuning search."
    elif stale_hits and recall < 1.0:
        diagnosis = "stale_and_missing_gold"
        recommendation = "Fix index freshness and then inspect parsing, chunking, and table retrieval coverage."
    elif recall == 0:
        diagnosis = "candidate_discovery_failure"
        recommendation = "Inspect corpus coverage, parsing, chunking, query rewrite, and hybrid retrieval."
    elif recall < 1.0:
        diagnosis = "partial_evidence_failure"
        recommendation = "Gold evidence is incomplete; inspect multi-hop retrieval, source coverage, and final-k cutoff."
    elif mrr < 0.5:
        diagnosis = "ranking_or_reranking_failure"
        recommendation = "Gold exists but ranks too low; inspect fusion, reranking, and final-k policy."
    elif stale_hits:
        diagnosis = "freshness_risk"
        recommendation = "Update index freshness, source version metadata, and stale-hit gates."
    else:
        diagnosis = "healthy"
        recommendation = "Keep monitoring this slice against future releases."

    return {
        "id": case["id"],
        "slice": case["slice"],
        "query_type": case["query_type"],
        "risk": case["risk"],
        "recall_at_k": round(recall, 3),
        "precision_at_k": round(precision, 3),
        "mrr": round(mrr, 3),
        "first_relevant_rank": first_rank,
        "stale_hit_count": len(stale_hits),
        "filtered_gold_count": len(case["filtered_gold"]),
        "diagnosis": diagnosis,
        "recommendation": recommendation,
    }


def average(values):
    return round(sum(values) / len(values), 3) if values else 0.0


def summarize_by(results, key):
    groups = {}
    for result in results:
        groups.setdefault(result[key], []).append(result)
    return {
        name: {
            "count": len(items),
            "recall_at_k": average([item["recall_at_k"] for item in items]),
            "precision_at_k": average([item["precision_at_k"] for item in items]),
            "mrr": average([item["mrr"] for item in items]),
            "filtered_gold_count": sum(item["filtered_gold_count"] for item in items),
            "stale_hit_count": sum(item["stale_hit_count"] for item in items),
        }
        for name, items in sorted(groups.items())
    }


def evaluate(cases, k=3):
    results = [evaluate_case(case, k) for case in cases]
    blocking_failures = [
        result for result in results
        if result["risk"] == "high"
        and (
            result["recall_at_k"] < 1.0
            or result["filtered_gold_count"] > 0
            or result["stale_hit_count"] > 0
        )
    ]
    warnings = [
        result for result in results
        if result["risk"] != "high" and result["recall_at_k"] < 1.0
    ]
    return {
        "release_gate": "block" if blocking_failures else ("warn" if warnings else "pass"),
        "overall": {
            "recall_at_k": average([result["recall_at_k"] for result in results]),
            "precision_at_k": average([result["precision_at_k"] for result in results]),
            "mrr": average([result["mrr"] for result in results]),
        },
        "by_slice": summarize_by(results, "slice"),
        "by_query_type": summarize_by(results, "query_type"),
        "blocking_failures": blocking_failures,
        "warnings": warnings,
        "results": results,
    }


if __name__ == "__main__":
    from pprint import pprint

    pprint(evaluate(CASES))
