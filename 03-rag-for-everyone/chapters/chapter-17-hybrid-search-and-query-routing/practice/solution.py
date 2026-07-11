DENSE = ["A", "C", "D", "F"]
SPARSE = ["B", "A", "E", "C"]


def reciprocal_rank_fusion(dense, sparse, k=60):
    scores = {}
    for results in (dense, sparse):
        for rank, doc_id in enumerate(results, start=1):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return [
        {"id": doc_id, "rrf_score": round(score, 6)}
        for doc_id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
    ]


if __name__ == "__main__":
    print(reciprocal_rank_fusion(DENSE, SPARSE))
