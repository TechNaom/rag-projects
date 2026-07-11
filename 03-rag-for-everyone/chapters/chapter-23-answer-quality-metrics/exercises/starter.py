"""Exercise: score answer quality with a production rubric."""

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
]


def score_case(case):
    # TODO: calculate faithfulness, relevance, citation_support,
    # completeness, refusal_correctness, score, severity, and release_gate.
    return {"id": case["id"]}


if __name__ == "__main__":
    for case in CASES:
        print(score_case(case))
