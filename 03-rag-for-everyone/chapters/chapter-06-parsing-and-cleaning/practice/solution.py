SCENARIOS = [
    {"name": "Refund PDF", "format": "pdf", "table_confidence": 0.55, "ocr_confidence": 0.94, "boilerplate_ratio": 0.05},
    {"name": "Docs HTML", "format": "html", "table_confidence": None, "ocr_confidence": None, "boilerplate_ratio": 0.37},
    {"name": "Incident Scan", "format": "ocr", "table_confidence": None, "ocr_confidence": 0.73, "boilerplate_ratio": 0.02},
    {"name": "Pricing CSV", "format": "csv", "table_confidence": 0.98, "ocr_confidence": None, "boilerplate_ratio": 0.01},
    {"name": "Policy DOCX", "format": "docx", "table_confidence": 0.87, "ocr_confidence": None, "boilerplate_ratio": 0.06, "has_comments": True},
]


def classify_scenario(scenario):
    if scenario.get("ocr_confidence") is not None and scenario["ocr_confidence"] < 0.85:
        return "needs_review: OCR confidence is too low for production indexing"
    if scenario.get("table_confidence") is not None and scenario["table_confidence"] < 0.75:
        return "needs_review: table extraction confidence is too low"
    if scenario["boilerplate_ratio"] > 0.25:
        return "clean_then_retest: boilerplate may pollute retrieval"
    if scenario.get("has_comments"):
        return "needs_review: comments or tracked changes must be separated from approved text"
    return "ready: parser output can move to chunking with metadata preserved"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], classify_scenario(scenario))
