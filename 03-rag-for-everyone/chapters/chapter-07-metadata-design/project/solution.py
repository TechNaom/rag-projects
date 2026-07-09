RECORDS = [
    {
        "chunk_id": "sec-policy:p4:s2:c1",
        "source_id": "customer_data_access_policy",
        "source_uri": "policies/customer-data-access.md",
        "document_type": "policy",
        "section": "Emergency access",
        "authority": "approved",
        "owner": "Security Governance",
        "access_level": "restricted",
        "allowed_roles": ["security", "incident_commander"],
        "region": "EU",
        "version": "2026.1",
        "effective_from": "2026-01-15",
        "expires_at": "2027-01-15",
        "source_position": "page:4 section:2",
        "schema_version": "rag-metadata-v1",
    },
    {
        "chunk_id": "hr-policy:draft:c2",
        "source_id": "remote_work_notes",
        "source_uri": "drafts/remote-work.docx",
        "document_type": "policy",
        "section": "Remote work",
        "authority": "draft",
        "owner": "HR",
        "access_level": "internal",
        "allowed_roles": ["employee"],
        "region": "GLOBAL",
        "version": "draft",
        "effective_from": "",
        "expires_at": "",
        "source_position": "page:2",
        "schema_version": "rag-metadata-v1",
    },
    {
        "chunk_id": "price-table:r9",
        "source_id": "enterprise_pricing_matrix",
        "source_uri": "tables/pricing.csv",
        "document_type": "table",
        "section": "Enterprise tiers",
        "authority": "approved",
        "owner": "Finance",
        "access_level": "restricted",
        "allowed_roles": [],
        "region": "GLOBAL",
        "version": "2026.1",
        "effective_from": "2026-01-01",
        "expires_at": "",
        "source_position": "row:9",
        "schema_version": "rag-metadata-v1",
    },
]

REQUIRED = [
    "chunk_id",
    "source_id",
    "source_uri",
    "document_type",
    "section",
    "authority",
    "owner",
    "access_level",
    "region",
    "version",
    "effective_from",
    "source_position",
    "schema_version",
]

ALLOWED = {
    "document_type": {"policy", "runbook", "table", "docs", "api_record"},
    "authority": {"approved", "supporting", "historical", "draft", "retired"},
    "access_level": {"public", "internal", "restricted"},
    "region": {"GLOBAL", "EU", "US", "APAC"},
    "schema_version": {"rag-metadata-v1"},
}


def missing_fields(record):
    return [field for field in REQUIRED if not record.get(field)]


def invalid_fields(record):
    invalid = []
    for field, allowed_values in ALLOWED.items():
        if record.get(field) not in allowed_values:
            invalid.append(field)
    if record.get("access_level") == "restricted" and not record.get("allowed_roles"):
        invalid.append("allowed_roles")
    return invalid


def first_issue(record):
    missing = missing_fields(record)
    invalid = invalid_fields(record)
    if missing:
        return "missing_fields:" + ",".join(missing)
    if invalid:
        return "invalid_fields:" + ",".join(invalid)
    if record["authority"] == "retired":
        return "retired_source"
    if record["authority"] == "draft":
        return "draft_source"
    if record["access_level"] == "restricted":
        return "permission_filter_required"
    return "none"


def indexing_decision(issue):
    if issue == "none":
        return "publish"
    if issue == "permission_filter_required":
        return "publish_with_permission_filter"
    if issue in {"draft_source"}:
        return "review"
    if issue in {"retired_source"}:
        return "block"
    if issue.startswith("missing_fields") or issue.startswith("invalid_fields"):
        return "review"
    return "review"


def next_action(issue):
    if issue == "none":
        return "index record and include in retrieval evals"
    if issue == "permission_filter_required":
        return "index only with role-aware retrieval filters enabled"
    if issue == "draft_source":
        return "route to owner for approval before production use"
    if issue == "retired_source":
        return "exclude from current-answer retrieval"
    if issue.startswith("missing_fields"):
        return "complete required metadata before indexing"
    if issue.startswith("invalid_fields"):
        if "allowed_roles" in issue:
            return "add allowed roles before enabling restricted-source retrieval"
        return "normalize values using controlled vocabulary"
    return "route to metadata owner"


def first_metric(issue):
    if issue == "none":
        return "metadata_validity_rate"
    if issue == "permission_filter_required":
        return "blocked_source_rate_by_role"
    if issue in {"draft_source", "retired_source"}:
        return "non_authoritative_retrieval_rate"
    if issue.startswith("missing_fields"):
        return "metadata_completeness_rate"
    if issue.startswith("invalid_fields"):
        return "controlled_value_error_rate"
    return "metadata_review_rate"


def validate_record(record):
    issue = first_issue(record)
    return {
        "chunk_id": record["chunk_id"],
        "decision": indexing_decision(issue),
        "first_issue": issue,
        "next_action": next_action(issue),
        "first_metric_to_inspect": first_metric(issue),
    }


if __name__ == "__main__":
    for record in RECORDS:
        print(validate_record(record))
