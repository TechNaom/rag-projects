REQUESTS = [
    {"id": "faq", "risk": "low", "gold_in_candidates": True, "gold_rank": 2},
    {"id": "policy", "risk": "high", "gold_in_candidates": True, "gold_rank": 22},
    {"id": "missing", "risk": "medium", "gold_in_candidates": False, "gold_rank": None},
]


def plan_reranking(request):
    if not request["gold_in_candidates"]:
        return {
            "id": request["id"],
            "use_reranker": False,
            "candidate_k": 50,
            "final_k": 6,
            "fix": "improve first-stage retrieval before reranking",
            "metric": "candidate Recall@k",
        }
    if request["risk"] == "high" or request["gold_rank"] > 5:
        return {
            "id": request["id"],
            "use_reranker": True,
            "candidate_k": 50,
            "final_k": 6,
            "fix": "rerank candidates, dedupe, and citation-check",
            "metric": "MRR and citation support",
        }
    return {
        "id": request["id"],
        "use_reranker": False,
        "candidate_k": 10,
        "final_k": 4,
        "fix": "skip reranker unless evals show quality gap",
        "metric": "latency and answer quality",
    }


if __name__ == "__main__":
    for request in REQUESTS:
        print(plan_reranking(request))
