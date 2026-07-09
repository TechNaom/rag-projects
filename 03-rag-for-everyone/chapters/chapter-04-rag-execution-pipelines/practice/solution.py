SCENARIOS = [
    {"name": "HR parental leave", "risk": "medium", "issue": "old_policy_cited"},
    {"name": "Support refund", "risk": "medium", "issue": "missing_metadata_filter"},
    {"name": "Security runbook", "risk": "high", "issue": "missing_required_source"},
    {"name": "Developer docs v2", "risk": "low", "issue": "wrong_version"},
    {"name": "Sales competitive deck", "risk": "medium", "issue": "retired_source"},
]

PLAYBOOK = {
    "old_policy_cited": {
        "offline_risk": "index freshness failure",
        "online_risk": "stale source entered prompt",
        "gate": "block stale effective-date source",
        "next_action": "rebuild index and compare old/new policy retrieval",
    },
    "missing_metadata_filter": {
        "offline_risk": "metadata schema incomplete",
        "online_risk": "refund policy retrieved without country/tier/date filter",
        "gate": "require country, product tier, and purchase date",
        "next_action": "ask clarification or apply filters before retrieval",
    },
    "missing_required_source": {
        "offline_risk": "source family coverage not validated",
        "online_risk": "answer from runbook without access policy",
        "gate": "paired-source recall required",
        "next_action": "escalate and retrieve missing access policy",
    },
    "wrong_version": {
        "offline_risk": "API version metadata weak",
        "online_risk": "v1 docs outrank v2 docs",
        "gate": "version filter required",
        "next_action": "apply version=v2 filter and rerun retrieval",
    },
    "retired_source": {
        "offline_risk": "retired deck still indexed",
        "online_risk": "retired pricing enters context",
        "gate": "approved-source-only retrieval",
        "next_action": "remove retired deck from published index",
    },
}


def analyze(item):
    return {"name": item["name"], "risk": item["risk"], **PLAYBOOK[item["issue"]]}


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(analyze(scenario))
