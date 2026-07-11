"""Chapter 27 exercise starter: recommend a RAG deployment pattern."""

SCENARIO = {
    "name": "Internal benefits assistant",
    "data_sensitivity": "private",
    "daily_queries": 2500,
    "latency_slo_ms": 2500,
    "team_maturity": "medium",
    "needs_user_feedback": True,
}


def recommend_pattern(scenario):
    """Return pattern, required_controls, and rollout."""
    # TODO: choose a deployment pattern from the scenario constraints.
    raise NotImplementedError("Recommend the deployment pattern")


if __name__ == "__main__":
    print(recommend_pattern(SCENARIO))
