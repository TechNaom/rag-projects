REQUIRED_METADATA = {"source_id", "status", "access", "embedding_model", "index_version"}

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


def record_problems(record, expected_dimension):
    problems = []
    if not record.get("id"):
        problems.append("missing id")
    if len(record.get("embedding", [])) != expected_dimension:
        problems.append("dimension mismatch")
    missing = REQUIRED_METADATA.difference(record.get("metadata", {}))
    if missing:
        problems.append("missing metadata: " + ", ".join(sorted(missing)))
    return problems


def build_release_report(release):
    blockers = []
    for record in release["records"]:
        problems = record_problems(record, release["expected_dimension"])
        if problems:
            blockers.append({"id": record.get("id", "unknown"), "problems": problems})
    if release["eval_recall_at_5"] < 0.85:
        blockers.append({"id": "eval", "problems": ["Recall@5 below release threshold"]})
    if release["stale_hit_rate"] > 0.02:
        blockers.append({"id": "eval", "problems": ["stale-hit rate too high"]})
    decision = "blocked" if blockers else "ready for controlled rollout"
    return {
        "release": release["name"],
        "decision": decision,
        "strategy": release["strategy"],
        "blockers": blockers,
        "monitoring": ["Recall@5", "latency", "empty result rate", "stale-hit rate", "delete lag"],
        "rollback": "keep previous index version online until new index is stable",
    }


if __name__ == "__main__":
    print(build_release_report(RELEASE))
