from math import sqrt

DOCUMENTS = [
    {"id": "doc-1", "text": "Rotate API credentials", "vector": [0.82, 0.10, 0.44], "active": True, "restricted": False},
    {"id": "doc-2", "text": "Quarterly revenue analysis", "vector": [0.05, 0.91, 0.22], "active": True, "restricted": False},
    {"id": "doc-3", "text": "Legacy password reset policy", "vector": [0.79, 0.13, 0.41], "active": False, "restricted": False},
    {"id": "doc-4", "text": "Private HR credential procedure", "vector": [0.80, 0.12, 0.43], "active": True, "restricted": True},
]


def cosine_similarity(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_length = sqrt(sum(a * a for a in left))
    right_length = sqrt(sum(b * b for b in right))
    if left_length == 0 or right_length == 0:
        return 0.0
    return dot / (left_length * right_length)


def warning_for(document):
    warnings = []
    if not document["active"]:
        warnings.append("inactive source")
    if document["restricted"]:
        warnings.append("restricted source")
    return warnings


def search(query_vector, documents, top_k=3):
    ranked = []
    for document in documents:
        score = cosine_similarity(query_vector, document["vector"])
        warnings = warning_for(document)
        ranked.append({
            "id": document["id"],
            "text": document["text"],
            "score": round(score, 4),
            "warnings": warnings,
            "report": (
                f"{document['id']} scored {score:.4f}. "
                f"{'Warnings: ' + ', '.join(warnings) if warnings else 'No metadata warnings.'}"
            ),
        })
    return sorted(ranked, key=lambda item: item["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    query = [0.81, 0.11, 0.42]
    for result in search(query, DOCUMENTS):
        print(result)
