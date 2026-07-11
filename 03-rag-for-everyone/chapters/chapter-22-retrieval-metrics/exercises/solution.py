"""Chapter 22 exercise solution: calculate retrieval metrics."""

CASE = {"gold": {"S2", "S4"}, "retrieved": ["S1", "S2", "S3", "S4", "S8"]}


def metric_report(case, k=3):
    gold = set(case["gold"])
    top_k = case["retrieved"][:k]
    hits = [doc_id for doc_id in top_k if doc_id in gold]
    first_rank = next(
        (rank for rank, doc_id in enumerate(case["retrieved"], start=1) if doc_id in gold),
        None,
    )
    return {
        "recall_at_k": len(hits) / len(gold) if gold else 0.0,
        "precision_at_k": len(hits) / k if k else 0.0,
        "reciprocal_rank": 1 / first_rank if first_rank else 0.0,
        "hits": hits,
        "first_relevant_rank": first_rank,
    }


if __name__ == "__main__":
    print(metric_report(CASE, k=3))
