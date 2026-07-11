DOCUMENTS = [
    {"id": "doc-1", "text": "Rotate API credentials", "vector": [0.82, 0.10, 0.44], "active": True, "restricted": False},
    {"id": "doc-2", "text": "Quarterly revenue analysis", "vector": [0.05, 0.91, 0.22], "active": True, "restricted": False},
    {"id": "doc-3", "text": "Legacy password reset policy", "vector": [0.79, 0.13, 0.41], "active": False, "restricted": False},
    {"id": "doc-4", "text": "Private HR credential procedure", "vector": [0.80, 0.12, 0.43], "active": True, "restricted": True},
]


def search(query_vector, documents, top_k=3):
    # TODO: rank documents and include warnings for inactive or restricted chunks.
    raise NotImplementedError


if __name__ == "__main__":
    query = [0.81, 0.11, 0.42]
    for result in search(query, DOCUMENTS):
        print(result)
