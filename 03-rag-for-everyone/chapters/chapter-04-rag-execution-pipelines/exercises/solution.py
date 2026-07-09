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

SOURCE_FAMILIES = {
    "sev1_runbook_v2": "incident_runbook",
    "access_policy_v4": "access_policy",
}


def choose_route(item):
    question = item["question"].lower()
    if item["risk"] == "high" and ("access" in question or "logs" in question):
        return "corrective_policy_rag"
    return "advanced_rag"


def build_filters(item):
    return {
        "role": item["role"],
        "region": item["region"],
        "status": "approved",
    }


def evaluate_gates(item):
    failed = []
    if item["index_age_days"] > 7:
        failed.append("stale_index")

    retrieved_families = {SOURCE_FAMILIES.get(source_id, "unknown") for source_id in item["retrieved_sources"]}
    missing = [family for family in item["required_source_families"] if family not in retrieved_families]
    if missing:
        failed.append(f"missing_required_sources:{','.join(missing)}")

    if item["risk"] == "high" and missing:
        failed.append("must_escalate_high_risk_incomplete_evidence")

    return failed


def answer_status(failed_gates):
    if any(gate.startswith("missing_required_sources") for gate in failed_gates):
        return "escalated"
    if "stale_index" in failed_gates:
        return "needs_review"
    return "answer_allowed"


def build_trace(item):
    failed_gates = evaluate_gates(item)
    return {
        "request_id": item["request_id"],
        "route": choose_route(item),
        "filters": build_filters(item),
        "retrieved_sources": item["retrieved_sources"],
        "failed_gates": failed_gates,
        "answer_status": answer_status(failed_gates),
        "recommended_next_action": "retrieve access_policy_v4 or escalate to incident commander",
    }


if __name__ == "__main__":
    print(build_trace(SCENARIO))
