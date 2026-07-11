SCENARIOS = [
    {"id": "s1", "signal": "paraphrase", "exact_terms": False, "sensitive": False},
    {"id": "s2", "signal": "error_code", "exact_terms": True, "sensitive": False},
    {"id": "s3", "signal": "hr_policy", "exact_terms": False, "sensitive": True},
]


def recommend_retrieval(scenario):
    # TODO: return dense, sparse, hybrid, or governed_dense.
    raise NotImplementedError


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_retrieval(scenario))
