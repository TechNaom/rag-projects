SCENARIOS = [
    {"name": "Nightly support-doc sync", "change": "few_sources_changed"},
    {"name": "Embedding model upgrade", "change": "embedding_model_changed"},
    {"name": "Urgent security runbook fix", "change": "high_risk_hotfix"},
    {"name": "Parser upgrade", "change": "parser_output_changed"},
    {"name": "Retired policy removal", "change": "delete_or_retire_source"},
]


def choose_pipeline_mode(scenario):
    change = scenario["change"]
    if change == "few_sources_changed":
        return "incremental: validate changed-source retrieval and stale chunk removal"
    if change == "embedding_model_changed":
        return "full_reindex: compare old and candidate indexes with golden queries"
    if change == "high_risk_hotfix":
        return "hotfix: require owner approval, access tests, and rollback"
    if change == "parser_output_changed":
        return "targeted_reindex: run parser diff and rebuild affected chunks"
    if change == "delete_or_retire_source":
        return "incremental_delete: verify retired chunks no longer retrieve"
    return "review: unknown pipeline change"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], choose_pipeline_mode(scenario))
