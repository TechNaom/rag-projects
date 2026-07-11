REQUIRED_METADATA = {"source_id", "status", "access", "embedding_model", "index_version"}


def validate_record(record, expected_dimension):
    problems = []
    if not record.get("id"):
        problems.append("missing stable id")
    embedding = record.get("embedding", [])
    if len(embedding) != expected_dimension:
        problems.append(f"dimension mismatch: expected {expected_dimension}, got {len(embedding)}")
    metadata = record.get("metadata", {})
    missing = sorted(REQUIRED_METADATA.difference(metadata))
    if missing:
        problems.append(f"missing metadata: {', '.join(missing)}")
    if metadata.get("status") not in {None, "active", "inactive"}:
        problems.append("invalid status value")
    return {
        "id": record.get("id", "unknown"),
        "ready": not problems,
        "problems": problems,
        "release_note": "ready for staging upsert" if not problems else "blocked: " + "; ".join(problems),
    }


if __name__ == "__main__":
    sample = {
        "id": "policy:v1:chunk-01",
        "embedding": [0.1, 0.2, 0.3],
        "metadata": {"source_id": "policy", "status": "active", "access": "support"},
    }
    print(validate_record(sample, 3))
