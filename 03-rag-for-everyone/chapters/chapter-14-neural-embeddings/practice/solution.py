SCENARIOS = [
    {"id": "support", "paraphrase": True, "exact_terms": False, "sensitive": False, "latency_critical": False},
    {"id": "ops", "paraphrase": True, "exact_terms": True, "sensitive": False, "latency_critical": True},
    {"id": "hr", "paraphrase": True, "exact_terms": False, "sensitive": True, "latency_critical": False},
]


def recommend_strategy(scenario):
    if scenario["sensitive"]:
        return {
            "id": scenario["id"],
            "strategy": "approved local or private hosted neural embeddings",
            "release_concern": "privacy review, data residency, and access filters",
        }
    if scenario["exact_terms"] and scenario["paraphrase"]:
        return {
            "id": scenario["id"],
            "strategy": "hybrid dense + sparse retrieval",
            "release_concern": "latency budget, fallback behavior, and exact-term Recall@k",
        }
    if scenario["paraphrase"]:
        return {
            "id": scenario["id"],
            "strategy": "managed general neural embeddings",
            "release_concern": "retrieval evals, cost estimate, and re-index plan",
        }
    return {
        "id": scenario["id"],
        "strategy": "local lexical baseline",
        "release_concern": "watch paraphrase misses",
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_strategy(scenario))
