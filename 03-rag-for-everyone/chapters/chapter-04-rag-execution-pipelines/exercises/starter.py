SCENARIO = {
    "request_id": "req_1042",
    "question": "Can a contractor access EU customer logs during Sev1?",
    "risk": "high",
    "role": "contractor",
    "region": "EU",
    "index_age_days": 9,
    "retrieved_sources": ["sev1_runbook_v2"],
    "required_source_families": ["incident_runbook", "access_policy"],
}


def choose_route(item):
    # TODO: high-risk policy/access questions should use a corrective policy route.
    return "todo"


def build_filters(item):
    # TODO: return role and region filters.
    return {}


def evaluate_gates(item):
    # TODO: detect stale index, missing source family, and high-risk escalation.
    return []


def build_trace(item):
    return {
        "request_id": item["request_id"],
        "route": choose_route(item),
        "filters": build_filters(item),
        "failed_gates": evaluate_gates(item),
    }


if __name__ == "__main__":
    print(build_trace(SCENARIO))
