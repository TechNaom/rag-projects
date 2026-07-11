REQUESTS = [
    {"id": "faq", "risk": "low", "gold_in_candidates": True, "gold_rank": 2},
    {"id": "policy", "risk": "high", "gold_in_candidates": True, "gold_rank": 22},
    {"id": "missing", "risk": "medium", "gold_in_candidates": False, "gold_rank": None},
]


def plan_reranking(request):
    # TODO: return reranking policy.
    raise NotImplementedError


if __name__ == "__main__":
    for request in REQUESTS:
        print(plan_reranking(request))
