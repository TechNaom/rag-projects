SOURCES = [
    {
        "id": "policy_hr_2026_v1",
        "format": "pdf",
        "authority": "approved",
        "owner": "HR",
        "access": "internal",
        "freshness_days": 10,
        "version": "2026.1",
    },
    {
        "id": "refund_playbook_draft",
        "format": "docx",
        "authority": "draft",
        "owner": "Support",
        "access": "internal",
        "freshness_days": 2,
        "version": "draft",
    },
    {
        "id": "customer_records",
        "format": "database",
        "authority": "approved",
        "owner": "Data Platform",
        "access": "restricted",
        "freshness_days": 0,
        "version": "live",
    },
]

FORMAT_RISKS = {
    "pdf": "validate OCR, tables, page numbers, reading order",
    "docx": "resolve comments, tracked changes, and draft status",
    "database": "enforce row-level permissions and schema versioning",
    "json": "preserve nested object relationships",
    "csv": "preserve schema, units, and column descriptions",
}

BASE_METADATA = ["id", "format", "authority", "owner", "access", "version", "source_uri", "freshness_rule"]


def readiness(source):
    if source["authority"] == "retired":
        return "reject"
    if source["authority"] == "draft":
        return "quarantine"
    if source["freshness_days"] > 30:
        return "requires_review"
    if source["access"] == "restricted":
        return "approved_with_permission_filter"
    return "approved"


def first_risk(source):
    status = readiness(source)
    if status == "reject":
        return "retired source can cause outdated answers"
    if status == "quarantine":
        return "draft source is not authoritative"
    if status == "requires_review":
        return "freshness expired"
    if status == "approved_with_permission_filter":
        return "restricted source requires permission-aware retrieval"
    return FORMAT_RISKS.get(source["format"], "parser contract must be defined")


def next_action(source):
    status = readiness(source)
    actions = {
        "reject": "remove from ingestion candidate set",
        "quarantine": "send to owner for approval workflow",
        "requires_review": "request owner freshness confirmation",
        "approved_with_permission_filter": "add access policy before indexing",
        "approved": "run format-specific parser validation",
    }
    return actions[status]


def audit_source(source):
    return {
        "id": source["id"],
        "readiness": readiness(source),
        "production_risk": first_risk(source),
        "required_metadata": BASE_METADATA,
        "next_action": next_action(source),
    }


if __name__ == "__main__":
    for source in SOURCES:
        print(audit_source(source))
