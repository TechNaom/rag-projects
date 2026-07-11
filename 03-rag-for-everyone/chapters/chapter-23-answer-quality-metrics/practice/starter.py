"""Practice: classify answer-quality failure patterns."""

FAILURES = [
    {"id": "unsupported_claim", "unsupported": True, "off_topic": False, "bad_citation": False, "false_refusal": False, "missed_refusal": False, "incomplete": False, "risk": "high"},
    {"id": "wrong_citation", "unsupported": False, "off_topic": False, "bad_citation": True, "false_refusal": False, "missed_refusal": False, "incomplete": False, "risk": "high"},
    {"id": "false_refusal", "unsupported": False, "off_topic": False, "bad_citation": False, "false_refusal": True, "missed_refusal": False, "incomplete": False, "risk": "medium"},
    {"id": "incomplete_policy", "unsupported": False, "off_topic": False, "bad_citation": False, "false_refusal": False, "missed_refusal": False, "incomplete": True, "risk": "high"},
]


def classify(failure):
    # TODO: return labels, severity, first_action, and release_decision.
    return {"id": failure["id"]}


if __name__ == "__main__":
    for failure in FAILURES:
        print(classify(failure))
