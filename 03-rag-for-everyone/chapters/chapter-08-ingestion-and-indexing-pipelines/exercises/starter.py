RUNS = [
    {
        "run_id": "ingest_001",
        "mode": "incremental",
        "sources_changed": 12,
        "failed_sources": 0,
        "metadata_completeness": 0.99,
        "golden_query_pass_rate": 0.97,
        "access_tests_passed": True,
        "stale_chunks": 0,
    }
]


def publish_decision(run):
    # TODO: return publish, hold, rollback, or review
    return "todo"


def recovery_action(run):
    # TODO: explain next action
    return "todo"


if __name__ == "__main__":
    for run in RUNS:
        print(run["run_id"], publish_decision(run), recovery_action(run))
