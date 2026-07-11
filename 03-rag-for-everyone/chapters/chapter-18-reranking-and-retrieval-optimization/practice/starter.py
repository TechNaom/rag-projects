CASES = [
    {"id": "rank-low", "gold_in_candidates": True, "gold_rank": 18, "latency_sensitive": False},
    {"id": "missing", "gold_in_candidates": False, "gold_rank": None, "latency_sensitive": False},
    {"id": "faq", "gold_in_candidates": True, "gold_rank": 2, "latency_sensitive": True},
]


def choose_fix(case):
    # TODO: return rerank, retrieval_tuning, or skip.
    raise NotImplementedError


if __name__ == "__main__":
    for case in CASES:
        print(choose_fix(case))
