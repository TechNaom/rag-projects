"""Chapter 22 practice solution: diagnose metric symptoms."""

SYMPTOMS = [
    {"id": "exact_ids", "recall": 0.2, "mrr": 0.2, "slice": "exact_terms"},
    {"id": "buried_gold", "recall": 0.9, "mrr": 0.18, "slice": "policy"},
    {"id": "filter_issue", "recall": 0.1, "mrr": 0.0, "slice": "access_filter"},
]


def recommend(symptom):
    if symptom["slice"] == "exact_terms":
        return {"fix": "hybrid_or_sparse_search", "metric": "exact-term hit rate and Recall@10"}
    if symptom["recall"] >= 0.8 and symptom["mrr"] < 0.3:
        return {"fix": "reranking_or_ranking_tuning", "metric": "MRR and first relevant rank"}
    if symptom["slice"] == "access_filter":
        return {"fix": "filter_trace_audit", "metric": "filtered-out gold rate"}
    return {"fix": "failure_analysis", "metric": "slice-level recall"}


if __name__ == "__main__":
    for symptom in SYMPTOMS:
        print(symptom["id"], recommend(symptom))
