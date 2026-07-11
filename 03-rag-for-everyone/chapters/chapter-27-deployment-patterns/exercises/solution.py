"""Chapter 27 exercise solution: recommend a RAG deployment pattern."""

SCENARIO = {
    "name": "Internal benefits assistant",
    "data_sensitivity": "private",
    "daily_queries": 2500,
    "latency_slo_ms": 2500,
    "team_maturity": "medium",
    "needs_user_feedback": True,
}


def recommend_pattern(scenario):
    private = scenario["data_sensitivity"] in {"private", "regulated"}
    meaningful_traffic = scenario["daily_queries"] > 1000
    has_slo = scenario["latency_slo_ms"] is not None

    if not private and scenario["daily_queries"] < 100:
        pattern = "static_demo"
        controls = ["mock_data", "no_secrets", "public_readme"]
        rollout = "publish static site after link and content review"
    elif private or meaningful_traffic or has_slo:
        pattern = "hosted_api_rag_service"
        controls = [
            "auth_before_retrieval",
            "managed_secret_store",
            "trace_logging",
            "eval_release_gate",
            "health_checks",
            "index_versioning",
            "rollback_plan",
        ]
        rollout = "deploy canary to internal cohort, compare traces and evals, then expand"
    else:
        pattern = "local_cli_or_single_user_api"
        controls = ["env_file_template", "local_index_snapshot", "manual_eval_report"]
        rollout = "ship as reproducible developer workflow"

    if scenario.get("needs_user_feedback") and "feedback_capture" not in controls:
        controls.append("feedback_capture")

    return {
        "scenario": scenario["name"],
        "pattern": pattern,
        "required_controls": controls,
        "rollout": rollout,
    }


if __name__ == "__main__":
    print(recommend_pattern(SCENARIO))
