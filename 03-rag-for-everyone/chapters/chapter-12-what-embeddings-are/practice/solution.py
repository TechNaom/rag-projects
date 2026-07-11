SCENARIOS = [
    {"id": "s1", "signal": "paraphrase", "exact_terms": False, "sensitive": False},
    {"id": "s2", "signal": "error_code", "exact_terms": True, "sensitive": False},
    {"id": "s3", "signal": "hr_policy", "exact_terms": False, "sensitive": True},
]


def recommend_retrieval(scenario):
    if scenario.get("sensitive"):
        return {
            "id": scenario["id"],
            "strategy": "governed_dense",
            "reason": "semantic search helps, but provider and privacy controls must be approved",
        }
    if scenario.get("exact_terms"):
        return {
            "id": scenario["id"],
            "strategy": "hybrid",
            "reason": "exact identifiers need sparse matching while dense search can still help with surrounding language",
        }
    return {
        "id": scenario["id"],
        "strategy": "dense",
        "reason": "paraphrase-heavy questions benefit from semantic similarity",
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_retrieval(scenario))
