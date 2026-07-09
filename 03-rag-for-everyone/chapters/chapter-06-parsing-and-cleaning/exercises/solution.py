PARSED_DOCS = [
    {
        "source_id": "refund_policy_pdf",
        "format": "pdf",
        "parse_score": 0.88,
        "ocr_confidence": 0.93,
        "table_confidence": 0.62,
        "metadata": {"owner": "Support", "version": "2026.2", "access": "internal"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.08,
    },
    {
        "source_id": "pricing_table_csv",
        "format": "csv",
        "parse_score": 0.95,
        "ocr_confidence": None,
        "table_confidence": 0.98,
        "metadata": {"owner": "Finance", "version": "2026.1", "access": "restricted"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.01,
    },
    {
        "source_id": "old_runbook_html",
        "format": "html",
        "parse_score": 0.71,
        "ocr_confidence": None,
        "table_confidence": None,
        "metadata": {"owner": "Security", "version": "", "access": ""},
        "positions_preserved": False,
        "boilerplate_ratio": 0.41,
    },
]

REQUIRED_METADATA = ["owner", "version", "access"]


def missing_metadata(parsed_doc):
    metadata = parsed_doc.get("metadata", {})
    return [field for field in REQUIRED_METADATA if not metadata.get(field)]


def readiness(parsed_doc):
    if parsed_doc["parse_score"] < 0.75:
        return "rejected"
    if missing_metadata(parsed_doc):
        return "needs_review"
    if not parsed_doc["positions_preserved"]:
        return "needs_review"
    if parsed_doc.get("table_confidence") is not None and parsed_doc["table_confidence"] < 0.75:
        return "needs_review"
    if parsed_doc.get("ocr_confidence") is not None and parsed_doc["ocr_confidence"] < 0.85:
        return "needs_review"
    if parsed_doc["boilerplate_ratio"] > 0.25:
        return "ready_with_warnings"
    return "ready"


def first_risk(parsed_doc):
    if parsed_doc["parse_score"] < 0.75:
        return "overall extraction quality is too low"
    missing = missing_metadata(parsed_doc)
    if missing:
        return "missing required metadata: " + ", ".join(missing)
    if not parsed_doc["positions_preserved"]:
        return "source positions were lost, so citations will be weak"
    if parsed_doc.get("table_confidence") is not None and parsed_doc["table_confidence"] < 0.75:
        return "table extraction confidence is low"
    if parsed_doc.get("ocr_confidence") is not None and parsed_doc["ocr_confidence"] < 0.85:
        return "OCR confidence is low"
    if parsed_doc["boilerplate_ratio"] > 0.25:
        return "boilerplate noise may pollute retrieval"
    return "no blocking parser risk found"


def next_action(parsed_doc):
    status = readiness(parsed_doc)
    actions = {
        "ready": "publish parsed contract to chunking",
        "ready_with_warnings": "publish only after boilerplate cleaning review",
        "needs_review": "route to ingestion reviewer with parser warnings",
        "rejected": "quarantine source and fix parser before retry",
    }
    return actions[status]


def audit(parsed_doc):
    return {
        "source_id": parsed_doc["source_id"],
        "readiness": readiness(parsed_doc),
        "first_risk": first_risk(parsed_doc),
        "next_action": next_action(parsed_doc),
    }


if __name__ == "__main__":
    for doc in PARSED_DOCS:
        print(audit(doc))
