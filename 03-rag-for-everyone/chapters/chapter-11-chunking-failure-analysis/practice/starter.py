SCENARIOS = [
    {"id": "hr-001", "symptom": "missing_exception", "gold_rank": 1, "duplicate_rate": 0.04, "stale_hit_rate": 0.0},
    {"id": "docs-002", "symptom": "repeated_neighbors", "gold_rank": 2, "duplicate_rate": 0.61, "stale_hit_rate": 0.0},
    {"id": "legal-003", "symptom": "old_policy", "gold_rank": 1, "duplicate_rate": 0.03, "stale_hit_rate": 0.42},
]


def create_failure_report(scenarios):
    # TODO: return one report per scenario with label, risk, fix, and metric.
    raise NotImplementedError


if __name__ == "__main__":
    print(create_failure_report(SCENARIOS))
