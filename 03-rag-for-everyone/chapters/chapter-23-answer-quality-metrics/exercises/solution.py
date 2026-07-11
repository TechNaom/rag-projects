"""Solution: score answer quality with a production rubric."""

CASES = [
    {
        "id": "supported_policy",
        "risk": "high",
        "question": "Who approves enterprise refunds after 30 days?",
        "evidence": "Enterprise refunds after 30 days require VP approval. The request must include a written reason.",
        "answer": "Enterprise refunds after 30 days require VP approval and a written reason [S1].",
        "citations": {"S1": "Enterprise refunds after 30 days require VP approval. The request must include a written reason."},
        "expected_terms": {"vp approval", "written reason"},
        "unsupported_terms": {"manager approval", "automatic approval"},
        "should_refuse": False,
    },
    {
        "id": "unsupported_claim",
        "risk": "high",
        "question": "Who approves enterprise refunds after 30 days?",
        "evidence": "Enterprise refunds after 30 days require VP approval.",
        "answer": "Managers can approve enterprise refunds after 30 days [S1].",
        "citations": {"S1": "Enterprise refunds after 30 days require VP approval."},
        "expected_terms": {"vp approval"},
        "unsupported_terms": {"manager approval", "managers can approve"},
        "should_refuse": False,
    },
    {
        "id": "false_refusal",
        "risk": "medium",
        "question": "What document is needed with the refund request?",
        "evidence": "The request must include a written reason.",
        "answer": "I do not have enough information to answer.",
        "citations": {"S1": "The request must include a written reason."},
        "expected_terms": {"written reason"},
        "unsupported_terms": set(),
        "should_refuse": False,
    },
]


def contains_any(text, terms):
    lowered = text.lower()
    return any(term in lowered for term in terms)


def contains_all(text, terms):
    lowered = text.lower()
    return all(term in lowered for term in terms)


def score_case(case):
    answer = case["answer"].lower()
    evidence = case["evidence"].lower()
    refusal = (
        "not enough information" in answer
        or "do not have enough information" in answer
        or "cannot answer" in answer
    )
    unsupported_hit = contains_any(answer, case["unsupported_terms"])
    expected_in_answer = contains_all(answer, case["expected_terms"])
    expected_in_evidence = contains_all(evidence, case["expected_terms"])
    citation_ids_present = all(f"[{source_id.lower()}]" in answer for source_id in case["citations"])
    citation_support = citation_ids_present and any(
        contains_all(source_text, case["expected_terms"])
        for source_text in case["citations"].values()
    )

    checks = {
        "faithfulness": expected_in_evidence and not unsupported_hit and not refusal,
        "relevance": contains_any(answer, {"approval", "refund", "written reason"}) and not refusal,
        "citation_support": citation_support,
        "completeness": expected_in_answer if not case["should_refuse"] else True,
        "refusal_correctness": refusal == case["should_refuse"],
        "safety": not unsupported_hit,
    }

    failed = [name for name, passed in checks.items() if not passed]
    if unsupported_hit or ("faithfulness" in failed and case["risk"] == "high"):
        severity = "critical"
    elif "citation_support" in failed or "refusal_correctness" in failed:
        severity = "major"
    elif failed:
        severity = "moderate"
    else:
        severity = "none"

    if severity == "critical" or (case["risk"] == "high" and severity == "major"):
        gate = "block"
    elif severity in {"major", "moderate"}:
        gate = "review"
    else:
        gate = "pass"

    return {
        "id": case["id"],
        "risk": case["risk"],
        "checks": checks,
        "score": sum(checks.values()),
        "failed_checks": failed,
        "severity": severity,
        "release_gate": gate,
    }


if __name__ == "__main__":
    from pprint import pprint

    for case in CASES:
        pprint(score_case(case))
