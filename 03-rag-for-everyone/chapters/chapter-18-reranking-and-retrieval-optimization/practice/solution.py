CASES = [
    {"id": "rank-low", "gold_in_candidates": True, "gold_rank": 18, "latency_sensitive": False},
    {"id": "missing", "gold_in_candidates": False, "gold_rank": None, "latency_sensitive": False},
    {"id": "faq", "gold_in_candidates": True, "gold_rank": 2, "latency_sensitive": True},
]


def choose_fix(case):
    if not case["gold_in_candidates"]:
        return {"id": case["id"], "fix": "retrieval_tuning", "reason": "reranker cannot promote missing evidence"}
    if case["gold_rank"] > 5 and not case["latency_sensitive"]:
        return {"id": case["id"], "fix": "rerank", "reason": "gold evidence is present but ranked too low"}
    return {"id": case["id"], "fix": "skip_or_light_rerank", "reason": "baseline rank is acceptable or latency is sensitive"}


if __name__ == "__main__":
    for case in CASES:
        print(choose_fix(case))
