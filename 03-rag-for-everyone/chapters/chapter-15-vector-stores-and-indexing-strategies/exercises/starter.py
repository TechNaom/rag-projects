REQUIRED_METADATA = {"source_id", "status", "access", "embedding_model", "index_version"}


def validate_record(record, expected_dimension):
    # TODO: return validation status and problems.
    raise NotImplementedError


if __name__ == "__main__":
    sample = {
        "id": "policy:v1:chunk-01",
        "embedding": [0.1, 0.2, 0.3],
        "metadata": {"source_id": "policy", "status": "active", "access": "support"},
    }
    print(validate_record(sample, 3))
