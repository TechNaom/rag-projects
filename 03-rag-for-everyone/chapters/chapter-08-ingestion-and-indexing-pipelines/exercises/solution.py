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
    },
    {
        "run_id": "ingest_002",
        "mode": "hotfix",
        "sources_changed": 1,
        "failed_sources": 0,
        "metadata_completeness": 1.0,
        "golden_query_pass_rate": 0.72,
        "access_tests_passed": True,
        "stale_chunks": 0,
    },
    {
        "run_id": "ingest_003",
        "mode": "batch",
        "sources_changed": 830,
        "failed_sources": 14,
        "metadata_completeness": 0.91,
        "golden_query_pass_rate": 0.94,
        "access_tests_passed": False,
        "stale_chunks": 23,
    },
]


def first_issue(run):
    if not run["access_tests_passed"]:
        return "access-control regression"
    if run["golden_query_pass_rate"] < 0.9:
        return "golden retrieval tests failed"
    if run["metadata_completeness"] < 0.98:
        return "metadata completeness below release threshold"
    if run["stale_chunks"] > 0:
        return "stale chunks remain in candidate index"
    if run["failed_sources"] > 0:
        return "some sources failed and need owner review"
    return "none"


def publish_decision(run):
    issue = first_issue(run)
    if issue == "none":
        return "publish"
    if "access-control" in issue or "golden" in issue:
        return "rollback"
    if "metadata" in issue or "stale" in issue:
        return "hold"
    return "review"


def recovery_action(run):
    issue = first_issue(run)
    actions = {
        "none": "publish candidate index and monitor online retrieval metrics",
        "access-control regression": "hold publish and rollback to previous known-good index",
        "golden retrieval tests failed": "hold publish, inspect failed queries, and use rollback index",
        "metadata completeness below release threshold": "route missing records to metadata owner before publish",
        "stale chunks remain in candidate index": "fix delete/replacement logic and rerun incremental indexing",
        "some sources failed and need owner review": "quarantine failed sources and continue only if they are non-critical",
    }
    return actions[issue]


if __name__ == "__main__":
    for run in RUNS:
        print(run["run_id"], publish_decision(run), recovery_action(run))
