SCENARIOS = [
    {"name": "HR parental leave", "risk": "medium", "issue": "old_policy_cited"},
    {"name": "Support refund", "risk": "medium", "issue": "missing_metadata_filter"},
    {"name": "Security runbook", "risk": "high", "issue": "missing_required_source"},
    {"name": "Developer docs v2", "risk": "low", "issue": "wrong_version"},
    {"name": "Sales competitive deck", "risk": "medium", "issue": "retired_source"},
]


def analyze(item):
    # TODO: return offline risk, online risk, gate, and next action.
    return {"name": item["name"]}


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(analyze(scenario))
