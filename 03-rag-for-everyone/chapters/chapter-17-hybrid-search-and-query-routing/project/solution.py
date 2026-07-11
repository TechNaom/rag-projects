import re

REQUESTS = [
    {"id": "support", "query": "How do I regenerate credentials?", "risk": "low"},
    {"id": "ops", "query": "AZ-4032-B after key rotation", "risk": "medium"},
    {"id": "legal", "query": "Policy 7.3 termination clause", "risk": "high"},
]


def has_exact_signal(query):
    patterns = [r"\b[A-Z]{2,}-\d{3,}-[A-Z]\b", r"\bPolicy\s+\d+(\.\d+)?\b", r"\bSKU-\d+\b"]
    return any(re.search(pattern, query) for pattern in patterns)


def reciprocal_rank_fusion(*ranked_lists, k=60):
    scores = {}
    for ranked in ranked_lists:
        for rank, item in enumerate(ranked, start=1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)


def build_route_plan(request):
    query = request["query"]
    exact = has_exact_signal(query)
    semantic = len(query.split()) >= 4
    if request["risk"] == "high":
        route = "high_risk_hybrid"
        controls = ["strict_filters", "sparse_exact", "dense_semantic", "rerank", "citation_check"]
        metric = "high_risk_route_accuracy"
        reason = "high-risk query needs exact protection and citation-safe semantic coverage"
    elif exact and semantic:
        route = "hybrid"
        controls = ["sparse_exact", "dense_semantic", "rrf", "dedupe"]
        metric = "exact_term_recall"
        reason = "exact operational token plus semantic troubleshooting intent"
    elif exact:
        route = "sparse"
        controls = ["sparse_exact", "metadata_filters"]
        metric = "exact_term_recall"
        reason = "exact identifier is the primary signal"
    else:
        route = "dense"
        controls = ["dense_semantic", "metadata_filters"]
        metric = "Recall@k"
        reason = "semantic paraphrase query without exact-term dependency"
    return {
        "id": request["id"],
        "route": route,
        "reason": reason,
        "controls": controls,
        "metric": metric,
    }


if __name__ == "__main__":
    for request in REQUESTS:
        print(build_route_plan(request))
    print("rrf_demo", reciprocal_rank_fusion(["A", "C", "D"], ["B", "A", "C"]))
