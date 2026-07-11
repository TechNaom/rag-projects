"""Chapter 22 practice: diagnose metric symptoms."""

SYMPTOMS = [
    {"id": "exact_ids", "recall": 0.2, "mrr": 0.2, "slice": "exact_terms"},
    {"id": "buried_gold", "recall": 0.9, "mrr": 0.18, "slice": "policy"},
    {"id": "filter_issue", "recall": 0.1, "mrr": 0.0, "slice": "access_filter"},
]


def recommend(symptom):
    # TODO: map symptom to likely fix.
    return {}


if __name__ == "__main__":
    for symptom in SYMPTOMS:
        print(symptom["id"], recommend(symptom))
