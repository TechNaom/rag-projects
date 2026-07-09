SOURCES = [
    {"id": "hr_policy_v3.pdf", "format": "pdf", "authority": "approved", "access": "internal", "age_days": 12, "owner": "HR"},
    {"id": "refund_notes.docx", "format": "docx", "authority": "draft", "access": "internal", "age_days": 4, "owner": "Support"},
    {"id": "pricing_2024_deck.pdf", "format": "pdf", "authority": "retired", "access": "sales", "age_days": 240, "owner": "Sales"},
]


def classify_source(source):
    # TODO: return readiness and first production risk.
    return {"id": source["id"]}


if __name__ == "__main__":
    for source in SOURCES:
        print(classify_source(source))
