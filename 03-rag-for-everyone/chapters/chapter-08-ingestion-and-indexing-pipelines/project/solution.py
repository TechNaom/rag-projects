RUNS = [
    {
        "run_id": "ingest_2026_07_09_001",
        "mode": "incremental",
        "index_version": "support-index-2026-07-09.1",
        "rollback_index": "support-index-2026-07-08.4",
        "sources_seen": 1240,
        "sources_changed": 18,
        "failed_sources": 0,
        "critical_failed_sources": 0,
        "metadata_completeness": 0.995,
        "parse_success_rate": 0.998,
        "golden_query_pass_rate": 0.97,
        "access_tests_passed": True,
        "stale_chunks": 0,
        "duplicate_chunk_rate": 0.001,
    },
    {
        "run_id": "ingest_2026_07_09_002",
        "mode": "hotfix",
        "index_version": "security-index-2026-07-09.2",
        "rollback_index": "security-index-2026-07-09.1",
        "sources_seen": 420,
        "sources_changed": 1,
        "failed_sources": 0,
        "critical_failed_sources": 0,
        "metadata_completeness": 1.0,
        "parse_success_rate": 1.0,
        "golden_query_pass_rate": 0.82,
        "access_tests_passed": True,
        "stale_chunks": 0,
        "duplicate_chunk_rate": 0.0,
    },
    {
        "run_id": "ingest_2026_07_09_003",
        "mode": "full_reindex",
        "index_version": "hr-index-2026-07-09.1",
        "rollback_index": "hr-index-2026-07-01.3",
        "sources_seen": 980,
        "sources_changed": 980,
        "failed_sources": 9,
        "critical_failed_sources": 2,
        "metadata_completeness": 0.94,
        "parse_success_rate": 0.991,
        "golden_query_pass_rate": 0.93,
        "access_tests_passed": False,
        "stale_chunks": 31,
        "duplicate_chunk_rate": 0.018,
    },
]


def first_issue(run):
    if not run["access_tests_passed"]:
        return "access_tests_failed"
    if run["golden_query_pass_rate"] < 0.9:
        return "golden_queries_failed"
    if run["critical_failed_sources"] > 0:
        return "critical_sources_failed"
    if run["metadata_completeness"] < 0.98:
        return "metadata_incomplete"
    if run["stale_chunks"] > 0:
        return "stale_chunks_present"
    if run["duplicate_chunk_rate"] > 0.01:
        return "duplicate_chunks_high"
    if run["failed_sources"] > 0:
        return "non_critical_sources_failed"
    return "none"


def publish_decision(issue):
    if issue == "none":
        return "publish"
    if issue in {"access_tests_failed", "golden_queries_failed"}:
        return "rollback"
    if issue in {"critical_sources_failed", "metadata_incomplete", "stale_chunks_present"}:
        return "hold"
    return "review"


def next_action(run, issue):
    actions = {
        "none": "publish candidate index and monitor online retrieval quality",
        "access_tests_failed": "block publish and switch to rollback index",
        "golden_queries_failed": "inspect failed golden queries and use rollback index",
        "critical_sources_failed": "repair critical source failures before publish",
        "metadata_incomplete": "route missing metadata to owners and rerun validation",
        "stale_chunks_present": "fix delete or replacement logic, then rerun indexing",
        "duplicate_chunks_high": "repair idempotency or chunk identity logic",
        "non_critical_sources_failed": "quarantine failed records and publish only if owners accept risk",
    }
    return actions[issue]


def first_metric(issue):
    metrics = {
        "none": "online_retrieval_success_rate",
        "access_tests_failed": "permission_filter_regression_count",
        "golden_queries_failed": "golden_query_pass_rate",
        "critical_sources_failed": "critical_failed_source_count",
        "metadata_incomplete": "metadata_completeness",
        "stale_chunks_present": "stale_chunk_count",
        "duplicate_chunks_high": "duplicate_chunk_rate",
        "non_critical_sources_failed": "failed_source_count",
    }
    return metrics[issue]


def audit_run(run):
    issue = first_issue(run)
    return {
        "run_id": run["run_id"],
        "mode": run["mode"],
        "index_version": run["index_version"],
        "decision": publish_decision(issue),
        "first_issue": issue,
        "next_action": next_action(run, issue),
        "first_metric_to_inspect": first_metric(issue),
        "rollback_index": run["rollback_index"],
    }


if __name__ == "__main__":
    for run in RUNS:
        print(audit_run(run))
