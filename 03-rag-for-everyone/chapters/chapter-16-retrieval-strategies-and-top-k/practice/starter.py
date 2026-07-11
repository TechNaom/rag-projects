MISSES = [
    {"id": "rank", "gold_rank": 7, "top_k": 5, "duplicates": 0, "filtered_gold": False},
    {"id": "dupes", "gold_rank": 2, "top_k": 8, "duplicates": 5, "filtered_gold": False},
    {"id": "filter", "gold_rank": None, "top_k": 8, "duplicates": 0, "filtered_gold": True},
]


def diagnose_miss(miss):
    # TODO: return retrieval failure label and fix.
    raise NotImplementedError


if __name__ == "__main__":
    for miss in MISSES:
        print(diagnose_miss(miss))
