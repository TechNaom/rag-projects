"""Chapter 22 exercise solution: calculate retrieval metrics."""

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
    gold = set(case["gold"])
    top_k = case["retrieved"][:k]
    hits = [doc_id for doc_id in top_k if doc_id in gold]
    first_rank = next(
        (rank for rank, doc_id in enumerate(case["retrieved"], start=1) if doc_id in gold),
        None,
    )
    stale_hits = [doc_id for doc_id in top_k if doc_id in case["stale"]]

    recall = len(hits) / len(gold) if gold else 0.0
    precision = len(hits) / k if k else 0.0
    mrr = 1 / first_rank if first_rank else 0.0
    hit_rate = 1.0 if hits else 0.0

    if case["filtered_gold"]:
        diagnosis = "filtered_gold"
        action = "audit metadata, access, tenant, and freshness filters"
    elif stale_hits:
        diagnosis = "stale_evidence_risk"
        action = "fix freshness metadata, deletion handling, or index lag"
    elif recall == 0:
        diagnosis = "candidate_discovery_failure"
        action = "inspect parsing, chunking, embeddings, sparse search, and query rewrite"
    elif recall < 1.0:
        diagnosis = "partial_evidence_failure"
        action = "inspect whether multi-document evidence is being retrieved within the final context budget"
    elif mrr < 0.5:
        diagnosis = "ranking_failure"
        action = "inspect hybrid fusion, reranking, dedupe, and final-k selection"
    else:
        diagnosis = "healthy"
        action = "keep this slice in regression monitoring"

    return {
        "id": case["id"],
        "domain": case["domain"],
        "query_type": case["query_type"],
        "risk": case["risk"],
        "recall_at_k": round(recall, 3),
        "precision_at_k": round(precision, 3),
        "mrr": round(mrr, 3),
        "hit_rate": hit_rate,
        "hits": hits,
        "first_relevant_rank": first_rank,
        "stale_hit_count": len(stale_hits),
        "filtered_gold_count": len(case["filtered_gold"]),
        "diagnosis": diagnosis,
        "next_action": action,
    }


def average(items, key):
    return round(sum(item[key] for item in items) / len(items), 3) if items else 0.0


def summarize(cases, k=3):
    results = [metric_report(case, k) for case in cases]
    high_risk_failures = [
        result for result in results
        if result["risk"] == "high" and result["recall_at_k"] < 1.0
    ]
    return {
        "overall": {
            "recall_at_k": average(results, "recall_at_k"),
            "precision_at_k": average(results, "precision_at_k"),
            "mrr": average(results, "mrr"),
            "hit_rate": average(results, "hit_rate"),
        },
        "release_gate": "block" if high_risk_failures else "review",
        "high_risk_failures": high_risk_failures,
        "results": results,
    }


if __name__ == "__main__":
    from pprint import pprint

    pprint(summarize(CASES, k=3))
