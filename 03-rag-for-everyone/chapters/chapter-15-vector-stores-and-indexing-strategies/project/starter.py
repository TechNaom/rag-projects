RELEASE = {
    "name": "policy-index-v4",
    "expected_dimension": 3,
    "strategy": "blue_green",
    "eval_recall_at_5": 0.91,
    "stale_hit_rate": 0.01,
    "records": [
        {"id": "policy:v4:c1", "embedding": [0.1, 0.2, 0.3], "metadata": {"source_id": "policy", "status": "active", "access": "support", "embedding_model": "model-a", "index_version": "v4"}},
        {"id": "policy:v4:c2", "embedding": [0.1, 0.2], "metadata": {"source_id": "policy", "status": "active", "access": "support", "embedding_model": "model-a", "index_version": "v4"}},
    ],
}


def build_release_report(release):
    # TODO: return release decision, blockers, and monitoring checklist.
    raise NotImplementedError


if __name__ == "__main__":
    print(build_release_report(RELEASE))
