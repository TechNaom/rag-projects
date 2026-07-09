CHUNKS = [
    {
        "chunk_id": "policy:sec:001",
        "source_id": "customer_data_access_policy",
        "source_uri": "policies/security.md",
        "section": "Emergency access",
        "authority": "approved",
        "access_level": "restricted",
        "allowed_roles": ["security"],
        "region": "EU",
        "version": "2026.1",
        "effective_from": "2026-01-15",
        "schema_version": "rag-metadata-v1",
    }
]


def validate_metadata(chunk):
    # TODO: return missing fields, invalid fields, and indexing decision
    return {}


if __name__ == "__main__":
    for chunk in CHUNKS:
        print(validate_metadata(chunk))
