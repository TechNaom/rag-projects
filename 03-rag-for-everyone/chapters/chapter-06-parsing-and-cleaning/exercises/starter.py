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
]


def readiness(parsed_doc):
    # TODO: return ready, ready_with_warnings, needs_review, or rejected
    return "todo"


def first_risk(parsed_doc):
    # TODO: explain the first production risk
    return "todo"


def next_action(parsed_doc):
    # TODO: recommend the next action
    return "todo"


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
