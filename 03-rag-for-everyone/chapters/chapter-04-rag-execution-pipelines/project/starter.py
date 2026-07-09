REQUEST = {
    "request_id": "req_prod_001",
    "question": "Can a contractor access EU customer logs during Sev1?",
    "risk": "high",
    "role": "contractor",
    "region": "EU",
    "index_version": "policies_2026_07_01",
    "index_age_days": 8,
    "retrieved_sources": [
        {"id": "sev1_runbook_v2", "family": "incident_runbook", "score": 0.86, "authorized": True},
    ],
}


def route_request(request):
    # TODO: choose route and explain why.
    return "todo"


def build_filters(request):
    # TODO: return role, region, and status filters.
    return {}


def run_gates(request):
    # TODO: check stale index, required sources, authorization, and risk.
    return []


def build_trace(request):
    return {
        "request_id": request["request_id"],
        "route": route_request(request),
        "filters": build_filters(request),
        "failed_gates": run_gates(request),
    }


if __name__ == "__main__":
    print(build_trace(REQUEST))
