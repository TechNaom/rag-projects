SCENARIOS = [
    {"name": "Nightly support-doc sync", "change": "few_sources_changed"},
    {"name": "Embedding model upgrade", "change": "embedding_model_changed"},
]


def choose_pipeline_mode(scenario):
    # TODO: return mode and release concern
    return "todo"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], choose_pipeline_mode(scenario))
