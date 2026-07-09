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
]


def audit_source(source):
    # TODO: return readiness, production risk, required metadata, and next action.
    return {"id": source["id"]}


if __name__ == "__main__":
    for source in SOURCES:
        print(audit_source(source))
