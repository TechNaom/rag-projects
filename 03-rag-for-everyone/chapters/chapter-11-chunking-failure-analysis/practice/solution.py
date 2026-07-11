SCENARIOS = [
    {"id": "hr-001", "symptom": "missing_exception", "gold_rank": 1, "duplicate_rate": 0.04, "stale_hit_rate": 0.0},
    {"id": "docs-002", "symptom": "repeated_neighbors", "gold_rank": 2, "duplicate_rate": 0.61, "stale_hit_rate": 0.0},
    {"id": "legal-003", "symptom": "old_policy", "gold_rank": 1, "duplicate_rate": 0.03, "stale_hit_rate": 0.42},
]

LABELS = {
    "missing_exception": ("lost_context", "high", "add bounded parent or neighbor expansion", "citation_support"),
    "repeated_neighbors": ("overlap_noise", "medium", "reduce overlap and add dedupe", "duplicate_rate"),
    "old_policy": ("stale_chunk", "critical", "filter active versions and rebuild index", "stale_hit_rate"),
}


def create_failure_report(scenarios):
    reports = []
    for scenario in scenarios:
        label, risk, fix, metric = LABELS.get(
            scenario["symptom"],
            ("unknown", "unknown", "collect richer trace", "trace_completeness"),
        )
        reports.append({
            "id": scenario["id"],
            "label": label,
            "risk": risk,
            "fix": fix,
            "metric": metric,
            "release_note": f"{scenario['id']}: {label} risk is {risk}; prove fix using {metric}.",
        })
    return reports


if __name__ == "__main__":
    for report in create_failure_report(SCENARIOS):
        print(report)
