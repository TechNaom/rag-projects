from math import sqrt


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_length = sqrt(sum(a * a for a in left))
    right_length = sqrt(sum(b * b for b in right))
    if left_length == 0 or right_length == 0:
        return 0.0
    return dot / (left_length * right_length)


def rank_chunks(query_vector, chunks):
    ranked = []
    for chunk in chunks:
        score = cosine_similarity(query_vector, chunk["vector"])
        warning = "stale candidate" if score > 0.9 and not chunk.get("active", True) else None
        ranked.append({**chunk, "score": round(score, 4), "warning": warning})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


if __name__ == "__main__":
    query = [0.80, 0.12, 0.40]
    chunks = [
        {"id": "api-key", "text": "Rotate access keys safely", "vector": [0.78, 0.11, 0.42], "active": True},
        {"id": "revenue", "text": "Quarterly revenue review", "vector": [0.05, 0.91, 0.22], "active": True},
        {"id": "old-key", "text": "Legacy key rotation policy", "vector": [0.81, 0.10, 0.39], "active": False},
    ]
    for item in rank_chunks(query, chunks):
        print(item)
