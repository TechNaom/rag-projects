SOURCES = [
    {"id": "hr_policy_v3.pdf", "format": "pdf", "authority": "approved", "access": "internal", "age_days": 12, "owner": "HR"},
    {"id": "refund_notes.docx", "format": "docx", "authority": "draft", "access": "internal", "age_days": 4, "owner": "Support"},
    {"id": "pricing_2024_deck.pdf", "format": "pdf", "authority": "retired", "access": "sales", "age_days": 240, "owner": "Sales"},
]


def format_risk(source):
    risks = {
        "pdf": "validate reading order, OCR, tables, page citations",
        "docx": "decide whether comments, tracked changes, and embedded tables are source or noise",
        "csv": "preserve schema, units, and column meanings",
        "json": "preserve nested relationships and object ids",
        "html": "remove navigation and boilerplate while preserving canonical URL",
    }
    return risks.get(source["format"], "define parser and metadata contract")


def classify_source(source):
    if source["authority"] == "retired":
        readiness = "reject"
        risk = "retired source could produce outdated answers"
    elif source["authority"] == "draft":
        readiness = "quarantine"
        risk = "draft source should not compete with approved sources"
    elif source["age_days"] > 30:
        readiness = "requires_review"
        risk = "source freshness must be checked before ingestion"
    else:
        readiness = "approved_for_ingestion"
        risk = format_risk(source)

    return {
        "id": source["id"],
        "readiness": readiness,
        "owner": source["owner"],
        "access": source["access"],
        "first_production_risk": risk,
    }


if __name__ == "__main__":
    for source in SOURCES:
        print(classify_source(source))
