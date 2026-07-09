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
        "source_position": "page:4",
    },
    {
        "chunk_id": "policy:hr:002",
        "source_id": "remote_work_draft",
        "source_uri": "policies/hr-draft.docx",
        "section": "",
        "authority": "draft",
        "access_level": "internal",
        "allowed_roles": ["employee"],
        "region": "Europe",
        "version": "",
        "effective_from": "",
        "schema_version": "rag-metadata-v1",
        "source_position": "",
    },
]

REQUIRED_FIELDS = [
    "chunk_id",
    "source_id",
    "source_uri",
    "section",
    "authority",
    "access_level",
    "allowed_roles",
    "region",
    "version",
    "effective_from",
    "schema_version",
    "source_position",
]

ALLOWED = {
    "authority": {"approved", "supporting", "historical", "draft", "retired"},
    "access_level": {"public", "internal", "restricted"},
    "region": {"GLOBAL", "EU", "US", "APAC"},
    "schema_version": {"rag-metadata-v1"},
}

NORMALIZE_REGION = {"Europe": "EU", "European Union": "EU", "global": "GLOBAL", "usa": "US"}


def normalized(chunk):
    copy = dict(chunk)
    copy["region"] = NORMALIZE_REGION.get(copy.get("region"), copy.get("region"))
    return copy


def missing_fields(chunk):
    return [field for field in REQUIRED_FIELDS if not chunk.get(field)]


def invalid_fields(chunk):
    invalid = []
    for field, allowed_values in ALLOWED.items():
        if chunk.get(field) and chunk[field] not in allowed_values:
            invalid.append(field)
    if chunk.get("access_level") == "restricted" and not chunk.get("allowed_roles"):
        invalid.append("allowed_roles")
    return invalid


def first_risk(chunk):
    missing = missing_fields(chunk)
    invalid = invalid_fields(chunk)
    if missing:
        return "missing required metadata: " + ", ".join(missing)
    if invalid:
        return "invalid controlled values: " + ", ".join(invalid)
    if chunk["authority"] in {"draft", "retired"}:
        return "non-authoritative source should not answer production questions"
    if chunk["access_level"] == "restricted":
        return "restricted source requires permission-aware retrieval"
    return "no blocking metadata risk found"


def indexing_decision(chunk):
    if missing_fields(chunk) or invalid_fields(chunk):
        return "review"
    if chunk["schema_version"] != "rag-metadata-v1":
        return "migrate_schema"
    if chunk["authority"] == "retired":
        return "block"
    if chunk["authority"] == "draft":
        return "review"
    return "publish"


def validate_metadata(chunk):
    checked = normalized(chunk)
    return {
        "chunk_id": checked["chunk_id"],
        "normalized_region": checked.get("region"),
        "missing_fields": missing_fields(checked),
        "invalid_fields": invalid_fields(checked),
        "first_risk": first_risk(checked),
        "indexing_decision": indexing_decision(checked),
    }


if __name__ == "__main__":
    for chunk in CHUNKS:
        print(validate_metadata(chunk))
