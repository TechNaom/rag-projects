"""Project solution: retrieval metrics dashboard seed."""

CASES = [
    {"id": "q1", "slice": "policy", "risk": "high", "gold": {"S2"}, "retrieved": ["S2", "S4", "S8"]},
    {"id": "q2", "slice": "exact_terms", "risk": "high", "gold": {"E7"}, "retrieved": ["S1", "S3", "E7"]},
    {"id": "q3", "slice": "support", "risk": "low", "gold": {"H1"}, "retrieved": ["H2", "H3", "H4"]},
]


def evaluate_case(case, k):
    top_k = case["retrieved"][:k]
    hits = [doc_id for doc_id in top_k if doc_id in case["gold"]]
    first_rank = next(
        (rank for rank, doc_id in enumerate(case["retrieved"], start=1) if doc_id in case["gold"]),
        None,
    )
    return {
        "id": case["id"],
        "slice": case["slice"],
        "risk": case["risk"],
        "recall_at_k": len(hits) / len(case["gold"]),
        "precision_at_k": len(hits) / k,
        "mrr": 1 / first_rank if first_rank else 0.0,
    }


def average(values):
    return sum(values) / len(values) if values else 0.0


def evaluate(cases, k=3):
    results = [evaluate_case(case, k) for case in cases]
    slices = {}
    for result in results:
        slices.setdefault(result["slice"], []).append(result)
    slice_summary = {
        name: {
            "recall_at_k": average([item["recall_at_k"] for item in items]),
            "mrr": average([item["mrr"] for item in items]),
            "count": len(items),
        }
        for name, items in slices.items()
    }
    high_risk_failures = [
        result for result in results
        if result["risk"] == "high" and result["recall_at_k"] < 1.0
    ]
    return {
        "results": results,
        "slice_summary": slice_summary,
        "release_gate": "block" if high_risk_failures else "pass",
        "high_risk_failures": high_risk_failures,
    }


if __name__ == "__main__":
    print(evaluate(CASES))
