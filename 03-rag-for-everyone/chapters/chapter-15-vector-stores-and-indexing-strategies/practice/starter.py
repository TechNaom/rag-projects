SCENARIOS = [
    {"id": "tenant", "multi_tenant": True, "major_rebuild": False, "model_change": False},
    {"id": "model-v2", "multi_tenant": False, "major_rebuild": True, "model_change": True},
    {"id": "policy-delete", "multi_tenant": False, "major_rebuild": False, "model_change": False, "delete_required": True},
]


def recommend_index_plan(scenario):
    # TODO: recommend collection and release strategy.
    raise NotImplementedError


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_index_plan(scenario))
