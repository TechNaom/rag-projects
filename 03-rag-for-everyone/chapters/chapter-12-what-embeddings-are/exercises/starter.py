from math import sqrt


def cosine_similarity(left, right):
    # TODO: return cosine similarity between two vectors.
    raise NotImplementedError


def rank_chunks(query_vector, chunks):
    # TODO: return chunks sorted by similarity descending.
    raise NotImplementedError


if __name__ == "__main__":
    query = [0.80, 0.12, 0.40]
    chunks = [
        {"id": "api-key", "text": "Rotate access keys safely", "vector": [0.78, 0.11, 0.42], "active": True},
        {"id": "revenue", "text": "Quarterly revenue review", "vector": [0.05, 0.91, 0.22], "active": True},
        {"id": "old-key", "text": "Legacy key rotation policy", "vector": [0.81, 0.10, 0.39], "active": False},
    ]
    print(rank_chunks(query, chunks))
