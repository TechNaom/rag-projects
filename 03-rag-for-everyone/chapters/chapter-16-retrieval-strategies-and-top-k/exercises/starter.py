QUERIES = [
    {"id": "faq", "type": "simple_faq", "risk": "low"},
    {"id": "refund", "type": "policy_exception", "risk": "high"},
    {"id": "sev1", "type": "troubleshooting", "risk": "high"},
]


def recommend_policy(query):
    # TODO: return top_k and retrieval controls.
    raise NotImplementedError


if __name__ == "__main__":
    for query in QUERIES:
        print(recommend_policy(query))
