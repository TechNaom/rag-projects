"""Solution: classify answer-quality failure patterns."""

FAILURES = [
    {"id": "unsupported_claim", "unsupported": True, "off_topic": False, "bad_citation": False, "false_refusal": False, "missed_refusal": False, "incomplete": False, "risk": "high"},
    {"id": "wrong_citation", "unsupported": False, "off_topic": False, "bad_citation": True, "false_refusal": False, "missed_refusal": False, "incomplete": False, "risk": "high"},
    {"id": "false_refusal", "unsupported": False, "off_topic": False, "bad_citation": False, "false_refusal": True, "missed_refusal": False, "incomplete": False, "risk": "medium"},
    {"id": "incomplete_policy", "unsupported": False, "off_topic": False, "bad_citation": False, "false_refusal": False, "missed_refusal": False, "incomplete": True, "risk": "high"},
    {"id": "missed_refusal", "unsupported": True, "off_topic": False, "bad_citation": True, "false_refusal": False, "missed_refusal": True, "incomplete": False, "risk": "high"},
]


def release_decision(risk, severity):
    if severity == "critical":
        return "block"
    if risk == "high" and severity == "major":
        return "block"
    if severity in {"major", "moderate"}:
        return "review"
    return "monitor"


def classify(failure):
    labels = []
    actions = []

    if failure["unsupported"]:
        labels.append("faithfulness_failure")
        actions.append("inspect grounding prompt, context packaging, and unsupported claim patterns")
    if failure["off_topic"]:
        labels.append("relevance_failure")
        actions.append("tighten task intent extraction and answer structure")
    if failure["bad_citation"]:
        labels.append("citation_correctness_failure")
        actions.append("evaluate claim-to-citation support instead of citation presence")
    if failure["false_refusal"]:
        labels.append("false_refusal")
        actions.append("lower refusal threshold when evidence is sufficient")
    if failure["missed_refusal"]:
        labels.append("missed_refusal")
        actions.append("strengthen insufficient-evidence and escalation policy")
    if failure["incomplete"]:
        labels.append("completeness_failure")
        actions.append("add required conditions and exception checks to the rubric")

    if failure["missed_refusal"] or (failure["unsupported"] and failure["risk"] == "high"):
        severity = "critical"
    elif failure["bad_citation"] or failure["false_refusal"] or failure["incomplete"]:
        severity = "major"
    elif labels:
        severity = "moderate"
    else:
        severity = "none"

    return {
        "id": failure["id"],
        "labels": labels or ["no_failure_detected"],
        "severity": severity,
        "first_action": actions[0] if actions else "continue monitoring",
        "release_decision": release_decision(failure["risk"], severity),
    }


if __name__ == "__main__":
    from pprint import pprint

    for failure in FAILURES:
        pprint(classify(failure))
