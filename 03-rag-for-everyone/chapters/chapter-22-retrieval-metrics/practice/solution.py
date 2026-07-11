"""Chapter 22 practice solution: diagnose metric symptoms."""

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


def release_decision(symptom, severity):
    if symptom["risk"] == "high" and severity in {"critical", "major"}:
        return "block"
    if severity in {"major", "moderate"}:
        return "warn"
    return "monitor"


def recommend(symptom):
    if symptom["filtered_gold"]:
        severity = "critical"
        response = {
            "root_cause": "metadata_or_access_filter_failure",
            "watch_metric": "filtered-out gold rate",
            "first_action": "audit tenant, access, freshness, and metadata filter traces",
        }
    elif symptom["stale_hits"]:
        severity = "major"
        response = {
            "root_cause": "freshness_or_index_version_failure",
            "watch_metric": "stale hit rate and source version correctness",
            "first_action": "repair index refresh, deletion handling, and source version metadata",
        }
    elif symptom["slice"] == "exact_terms" and symptom["recall"] < 0.6:
        severity = "major"
        response = {
            "root_cause": "exact_term_candidate_discovery_failure",
            "watch_metric": "exact-term Recall@10 and exact-term hit rate",
            "first_action": "add BM25 or hybrid retrieval and protect ids, codes, and clause names",
        }
    elif symptom["recall"] >= 0.8 and symptom["mrr"] < 0.3:
        severity = "major"
        response = {
            "root_cause": "ranking_or_reranking_failure",
            "watch_metric": "MRR and first relevant rank",
            "first_action": "inspect fusion weights, reranker input, dedupe, and final-k cutoff",
        }
    elif symptom["precision"] < 0.4:
        severity = "moderate"
        response = {
            "root_cause": "final_context_noise",
            "watch_metric": "Precision@K and citation support",
            "first_action": "tighten reranking, context packing, and source diversity controls",
        }
    else:
        severity = "low"
        response = {
            "root_cause": "no_clear_regression",
            "watch_metric": "slice-level trend",
            "first_action": "keep this slice in nightly regression tests",
        }

    response["release_decision"] = release_decision(symptom, severity)
    response["severity"] = severity
    return response


if __name__ == "__main__":
    from pprint import pprint

    for symptom in SYMPTOMS:
        print(symptom["id"])
        pprint(recommend(symptom))
