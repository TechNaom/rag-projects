SCENARIOS = [
    {"id": "p1", "exact_terms": True, "paraphrase": False, "sensitive": False},
    {"id": "p2", "exact_terms": False, "paraphrase": True, "sensitive": False},
    {"id": "p3", "exact_terms": True, "paraphrase": True, "sensitive": True},
]


def choose_strategy(scenario):
    if scenario["sensitive"] and scenario["exact_terms"] and scenario["paraphrase"]:
        return {
            "id": scenario["id"],
            "strategy": "governed_hybrid",
            "reason": "combine local lexical matching with an approved semantic option",
        }
    if scenario["exact_terms"] and not scenario["paraphrase"]:
        return {
            "id": scenario["id"],
            "strategy": "tfidf",
            "reason": "exact terms are the main signal and local explainability is enough",
        }
    if scenario["paraphrase"]:
        return {
            "id": scenario["id"],
            "strategy": "neural",
            "reason": "paraphrase-heavy queries need stronger semantic matching",
        }
    return {
        "id": scenario["id"],
        "strategy": "tfidf_baseline",
        "reason": "start with a local baseline and measure misses",
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(choose_strategy(scenario))
