TRACES = [
    {"id": "hr-001", "symptom": "missing_exception", "source": "hr-policy", "user_impact": "wrong eligibility"},
    {"id": "docs-002", "symptom": "repeated_neighbors", "source": "api-docs", "user_impact": "confusing answer"},
    {"id": "legal-003", "symptom": "old_policy", "source": "legal-faq", "user_impact": "wrong compliance advice"},
]

PLAYBOOK = {
    "missing_exception": {
        "label": "lost_context",
        "severity": "high",
        "fix": "add bounded parent expansion around the retrieved child chunk",
        "metric": "citation_support",
        "rollback_risk": "medium",
    },
    "repeated_neighbors": {
        "label": "overlap_noise",
        "severity": "medium",
        "fix": "reduce overlap and add near-duplicate collapse after retrieval",
        "metric": "duplicate_rate",
        "rollback_risk": "low",
    },
    "old_policy": {
        "label": "stale_chunk",
        "severity": "critical",
        "fix": "filter active versions, rebuild index, and block retired source ids",
        "metric": "stale_hit_rate",
        "rollback_risk": "high",
    },
}


def build_review_board(traces):
    reports = []
    for trace in traces:
        rule = PLAYBOOK.get(trace["symptom"], {
            "label": "unknown",
            "severity": "needs-triage",
            "fix": "collect retrieved chunks, scores, filters, citations, and index version",
            "metric": "trace_completeness",
            "rollback_risk": "unknown",
        })
        decision = "block release" if rule["severity"] == "critical" else "run controlled experiment"
        reports.append({
            "trace_id": trace["id"],
            "source": trace["source"],
            "failure_label": rule["label"],
            "severity": rule["severity"],
            "user_impact": trace["user_impact"],
            "fix_candidate": rule["fix"],
            "metric_to_prove": rule["metric"],
            "rollback_risk": rule["rollback_risk"],
            "release_decision": decision,
            "review_sentence": (
                f"{trace['id']} is a {rule['severity']} {rule['label']} failure. "
                f"Fix by: {rule['fix']}. Prove with {rule['metric']}."
            ),
        })
    return reports


if __name__ == "__main__":
    for item in build_review_board(TRACES):
        print(item)
