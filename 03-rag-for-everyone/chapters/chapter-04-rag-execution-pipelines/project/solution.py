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

REQUIRED_FAMILIES_BY_ROUTE = {
    "corrective_access_policy_rag": {"incident_runbook", "access_policy"},
    "advanced_docs_rag": {"documentation"},
}


def route_request(request):
    question = request["question"].lower()
    if request["risk"] == "high" and ("access" in question or "customer logs" in question):
        return {
            "route": "corrective_access_policy_rag",
            "reason": "High-risk access question requires paired policy evidence.",
        }
    return {"route": "advanced_docs_rag", "reason": "Default documentation flow."}


def build_filters(request):
    return {
        "role": request["role"],
        "region": request["region"],
        "status": "approved",
        "authorization": "enforced_before_context",
    }


def run_gates(request):
    route = route_request(request)["route"]
    required_families = REQUIRED_FAMILIES_BY_ROUTE[route]
    retrieved_families = {source["family"] for source in request["retrieved_sources"]}
    failed = []

    if request["index_age_days"] > 7:
        failed.append({"gate": "freshness", "reason": "Index is older than 7 days."})

    missing = sorted(required_families - retrieved_families)
    if missing:
        failed.append({"gate": "required_source_family", "reason": f"Missing {', '.join(missing)}."})

    unauthorized = [source["id"] for source in request["retrieved_sources"] if not source["authorized"]]
    if unauthorized:
        failed.append({"gate": "authorization", "reason": f"Unauthorized sources: {', '.join(unauthorized)}."})

    if request["risk"] == "high" and missing:
        failed.append({"gate": "high_risk_incomplete_evidence", "reason": "High-risk answer cannot proceed with incomplete source families."})

    return failed


def answer_policy(failed_gates):
    gate_names = {item["gate"] for item in failed_gates}
    if "authorization" in gate_names:
        return "refuse"
    if "required_source_family" in gate_names or "high_risk_incomplete_evidence" in gate_names:
        return "escalate"
    if "freshness" in gate_names:
        return "needs_review"
    return "answer_allowed"


def build_trace(request):
    route = route_request(request)
    failed_gates = run_gates(request)
    return {
        "request_id": request["request_id"],
        "index_version": request["index_version"],
        "route": route["route"],
        "route_reason": route["reason"],
        "filters": build_filters(request),
        "retrieved_sources": [source["id"] for source in request["retrieved_sources"]],
        "failed_gates": failed_gates,
        "answer_status": answer_policy(failed_gates),
        "recommended_next_action": "Retrieve access_policy source family, rebuild stale index if needed, then rerun gates.",
        "observability": ["request_id", "index_version", "route", "filters", "retrieved_sources", "failed_gates", "answer_status"],
    }


if __name__ == "__main__":
    print(build_trace(REQUEST))
