SCENARIOS = [
    {"id": "support", "paraphrase": True, "exact_terms": False, "sensitive": False, "latency_critical": False},
    {"id": "ops", "paraphrase": True, "exact_terms": True, "sensitive": False, "latency_critical": True},
    {"id": "hr", "paraphrase": True, "exact_terms": False, "sensitive": True, "latency_critical": False},
]


def recommend_strategy(scenario):
    # TODO: return embedding strategy and release concern.
    raise NotImplementedError


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_strategy(scenario))
