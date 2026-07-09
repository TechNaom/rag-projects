DOCUMENTS = [
    {"id": "refund_policy", "type": "policy", "has_headings": True, "avg_section_tokens": 380}
]


def recommend_chunker(document):
    # TODO: return fixed or recursive with reason
    return "todo"


if __name__ == "__main__":
    for doc in DOCUMENTS:
        print(recommend_chunker(doc))
