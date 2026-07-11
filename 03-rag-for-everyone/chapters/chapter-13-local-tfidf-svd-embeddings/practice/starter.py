SCENARIOS = [
    {"id": "p1", "exact_terms": True, "paraphrase": False, "sensitive": False},
    {"id": "p2", "exact_terms": False, "paraphrase": True, "sensitive": False},
    {"id": "p3", "exact_terms": True, "paraphrase": True, "sensitive": True},
]


def choose_strategy(scenario):
    # TODO: return tfidf, neural, local_hybrid, or governed_hybrid.
    raise NotImplementedError


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(choose_strategy(scenario))
