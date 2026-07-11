"""Solution: deployment planner."""
REQ = {"sensitive": True, "traffic": "medium", "risk": "high", "team": "small"}
def plan(req):
    if req["sensitive"] or req["risk"] == "high":
        pattern = "authenticated_api_service_with_private_index"
        controls = ["auth", "rbac_filters", "trace_store", "eval_gate", "rollback", "rate_limits"]
    elif req["traffic"] == "low":
        pattern = "static_demo_or_local_cli"
        controls = ["mock_data", "no_secrets", "basic_eval"]
    else:
        pattern = "hosted_frontend_plus_rag_api"
        controls = ["observability", "cache", "feedback", "cost_monitor"]
    return {"pattern": pattern, "controls": controls, "day2": ["monitor", "reindex", "review_failures", "rotate_keys"]}
if __name__ == "__main__":
    print(plan(REQ))
