SCENARIOS = [
    {"id": "tenant", "multi_tenant": True, "major_rebuild": False, "model_change": False},
    {"id": "model-v2", "multi_tenant": False, "major_rebuild": True, "model_change": True},
    {"id": "policy-delete", "multi_tenant": False, "major_rebuild": False, "model_change": False, "delete_required": True},
]


def recommend_index_plan(scenario):
    if scenario.get("model_change") or scenario.get("major_rebuild"):
        return {
            "id": scenario["id"],
            "collection_strategy": "new index collection/version",
            "release_strategy": "blue-green with golden-query eval gate",
            "risk": "high",
        }
    if scenario.get("multi_tenant"):
        return {
            "id": scenario["id"],
            "collection_strategy": "tenant-aware collections or strict tenant metadata filters",
            "release_strategy": "staging validation before prod promotion",
            "risk": "high if filters are weak",
        }
    if scenario.get("delete_required"):
        return {
            "id": scenario["id"],
            "collection_strategy": "same collection with deterministic ids",
            "release_strategy": "delete/upsert audit plus stale-hit eval",
            "risk": "critical if retired content remains active",
        }
    return {
        "id": scenario["id"],
        "collection_strategy": "same collection",
        "release_strategy": "controlled refresh",
        "risk": "medium",
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(recommend_index_plan(scenario))
