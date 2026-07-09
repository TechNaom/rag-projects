DOCUMENTS = [
    {
        "id": "refund_policy_pdf",
        "format": "pdf",
        "parse_score": 0.91,
        "ocr_confidence": 0.94,
        "table_confidence": 0.58,
        "metadata": {"owner": "Support Ops", "version": "2026.2", "access": "internal"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.06,
        "has_comments": False,
    },
    {
        "id": "developer_docs_html",
        "format": "html",
        "parse_score": 0.9,
        "ocr_confidence": None,
        "table_confidence": None,
        "metadata": {"owner": "DevRel", "version": "live", "access": "public"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.33,
        "has_comments": False,
    },
    {
        "id": "pricing_matrix_csv",
        "format": "csv",
        "parse_score": 0.96,
        "ocr_confidence": None,
        "table_confidence": 0.99,
        "metadata": {"owner": "Finance", "version": "2026.1", "access": "restricted"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.0,
        "has_comments": False,
    },
    {
        "id": "incident_scan",
        "format": "ocr",
        "parse_score": 0.8,
        "ocr_confidence": 0.69,
        "table_confidence": None,
        "metadata": {"owner": "Security", "version": "scan", "access": "restricted"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.02,
        "has_comments": False,
    },
    {
        "id": "hr_policy_docx",
        "format": "docx",
        "parse_score": 0.92,
        "ocr_confidence": None,
        "table_confidence": 0.86,
        "metadata": {"owner": "HR", "version": "2026.1", "access": "internal"},
        "positions_preserved": True,
        "boilerplate_ratio": 0.03,
        "has_comments": True,
    },
]

REQUIRED_METADATA = ("owner", "version", "access")


def missing_metadata(document):
    return [key for key in REQUIRED_METADATA if not document.get("metadata", {}).get(key)]


def first_issue(document):
    if document["parse_score"] < 0.75:
        return "parse_score_below_threshold"
    if missing_metadata(document):
        return "missing_required_metadata"
    if not document["positions_preserved"]:
        return "source_positions_missing"
    if document.get("ocr_confidence") is not None and document["ocr_confidence"] < 0.85:
        return "low_ocr_confidence"
    if document.get("table_confidence") is not None and document["table_confidence"] < 0.75:
        return "low_table_confidence"
    if document.get("has_comments"):
        return "comments_or_tracked_changes_present"
    if document["boilerplate_ratio"] > 0.25:
        return "high_boilerplate_ratio"
    return "none"


def readiness(issue):
    if issue == "none":
        return "publish"
    if issue == "high_boilerplate_ratio":
        return "clean_then_publish"
    if issue in {"parse_score_below_threshold", "source_positions_missing"}:
        return "reject"
    return "review"


def next_action(issue):
    actions = {
        "none": "send parsed contract to chunking",
        "high_boilerplate_ratio": "remove boilerplate, rerun parser diff, then publish",
        "parse_score_below_threshold": "quarantine source and improve parser configuration",
        "missing_required_metadata": "request owner/version/access metadata before indexing",
        "source_positions_missing": "reject until page, row, anchor, or region positions are preserved",
        "low_ocr_confidence": "route low-confidence regions to human review",
        "low_table_confidence": "review table extraction before chunking",
        "comments_or_tracked_changes_present": "separate approved text from comments and revisions",
    }
    return actions[issue]


def first_metric(issue):
    metrics = {
        "none": "parsed_contract_publish_rate",
        "high_boilerplate_ratio": "boilerplate_ratio_after_cleaning",
        "parse_score_below_threshold": "parse_success_rate",
        "missing_required_metadata": "metadata_completeness_rate",
        "source_positions_missing": "source_position_coverage",
        "low_ocr_confidence": "ocr_confidence_by_page_region",
        "low_table_confidence": "table_extraction_accuracy",
        "comments_or_tracked_changes_present": "approved_text_separation_rate",
    }
    return metrics[issue]


def audit_document(document):
    issue = first_issue(document)
    return {
        "id": document["id"],
        "format": document["format"],
        "readiness": readiness(issue),
        "first_issue": issue,
        "next_action": next_action(issue),
        "first_metric_to_inspect": first_metric(issue),
    }


if __name__ == "__main__":
    for document in DOCUMENTS:
        print(audit_document(document))
