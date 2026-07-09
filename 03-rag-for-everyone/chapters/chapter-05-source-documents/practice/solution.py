SOURCES = [
    {"id": "parental_leave_policy.pdf", "format": "pdf", "authority": "approved", "access": "internal", "fresh": True},
    {"id": "refund_edge_cases.docx", "format": "docx", "authority": "draft", "access": "support", "fresh": True},
    {"id": "pricing_2024.pdf", "format": "pdf", "authority": "retired", "access": "sales", "fresh": False},
    {"id": "product_catalog.json", "format": "json", "authority": "approved", "access": "public", "fresh": True},
    {"id": "customers_table", "format": "database", "authority": "approved", "access": "restricted", "fresh": True},
]


FORMAT_CONTROLS = {
    "pdf": "page number, OCR confidence, table extraction status",
    "docx": "revision status, comments policy, section hierarchy",
    "json": "object id, parent-child path, schema version",
    "database": "query view, row-level access, schema version",
}


def decide(source):
    if source["authority"] == "retired":
        decision = "reject"
        risk = "retired source can create outdated answers"
    elif source["authority"] == "draft":
        decision = "quarantine"
        risk = "draft source is not authoritative"
    elif not source["fresh"]:
        decision = "requires_review"
        risk = "freshness unknown or expired"
    elif source["access"] == "restricted":
        decision = "approved_with_permission_filter"
        risk = "retrieval must enforce row/document-level access"
    else:
        decision = "approved"
        risk = "format-specific extraction must be validated"

    return {
        "id": source["id"],
        "decision": decision,
        "risk": risk,
        "required_metadata": ["owner", "authority", "version", "access", "freshness_rule", FORMAT_CONTROLS.get(source["format"], "parser contract")],
    }


if __name__ == "__main__":
    for source in SOURCES:
        print(decide(source))
