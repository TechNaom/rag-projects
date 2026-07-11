"""Chapter 22 practice: diagnose metric symptoms."""

SYMPTOMS = [
    {
        "id": "exact_ids",
        "slice": "exact_terms",
        "recall": 0.2,
        "mrr": 0.2,
        "precision": 0.7,
        "filtered_gold": 0,
        "stale_hits": 0,
        "risk": "high",
    },
    {
        "id": "buried_gold",
        "slice": "policy",
        "recall": 0.9,
        "mrr": 0.18,
        "precision": 0.35,
        "filtered_gold": 0,
        "stale_hits": 0,
        "risk": "high",
    },
    {
        "id": "filter_issue",
        "slice": "access_filter",
        "recall": 0.1,
        "mrr": 0.0,
        "precision": 0.1,
        "filtered_gold": 5,
        "stale_hits": 0,
        "risk": "high",
    },
    {
        "id": "stale_policy",
        "slice": "policy",
        "recall": 0.8,
        "mrr": 0.72,
        "precision": 0.6,
        "filtered_gold": 0,
        "stale_hits": 3,
        "risk": "medium",
    },
]


def recommend(symptom):
    # TODO: return root_cause, watch_metric, first_action, and release_decision.
    return {"id": symptom["id"]}


if __name__ == "__main__":
    for symptom in SYMPTOMS:
        print(symptom["id"], recommend(symptom))
