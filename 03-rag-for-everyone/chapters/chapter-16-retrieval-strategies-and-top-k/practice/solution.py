MISSES = [
    {"id": "rank", "gold_rank": 7, "top_k": 5, "duplicates": 0, "filtered_gold": False},
    {"id": "dupes", "gold_rank": 2, "top_k": 8, "duplicates": 5, "filtered_gold": False},
    {"id": "filter", "gold_rank": None, "top_k": 8, "duplicates": 0, "filtered_gold": True},
]


def diagnose_miss(miss):
    if miss["filtered_gold"]:
        return {
            "id": miss["id"],
            "label": "filter_error_or_metadata_gap",
            "fix": "audit metadata filters and source labels",
            "metric": "filtered_gold_count",
        }
    if miss["gold_rank"] and miss["gold_rank"] > miss["top_k"]:
        return {
            "id": miss["id"],
            "label": "top_k_too_low",
            "fix": "increase k, rewrite query, or rerank candidates",
            "metric": "Recall@k",
        }
    if miss["duplicates"] >= 3:
        return {
            "id": miss["id"],
            "label": "duplicate_context_noise",
            "fix": "dedupe by source, parent id, or content hash",
            "metric": "duplicate_rate",
        }
    return {
        "id": miss["id"],
        "label": "needs_trace_review",
        "fix": "inspect ranks, scores, filters, and context assembly",
        "metric": "trace_completeness",
    }


if __name__ == "__main__":
    for miss in MISSES:
        print(diagnose_miss(miss))
