"""Starter: answer quality scorer.

Build a reusable scorer for RAG answer releases.
"""

CASES = [
    {
        "id": "policy_good",
        "domain": "policy",
        "query_type": "policy_lookup",
        "risk": "high",
        "question": "Who approves enterprise refunds after 30 days?",
        "evidence": {"S1": "Enterprise refunds after 30 days require VP approval and a written reason."},
        "answer": "Enterprise refunds after 30 days require VP approval and a written reason [S1].",
        "expected_terms": {"vp approval", "written reason"},
        "unsupported_terms": {"manager approval", "automatic approval"},
        "should_refuse": False,
        "versions": {"prompt": "p23-a", "model": "gpt-release-candidate", "corpus": "policy-v4"},
    },
    {
        "id": "policy_bad_claim",
        "domain": "policy",
        "query_type": "policy_lookup",
        "risk": "high",
        "question": "Who approves enterprise refunds after 30 days?",
        "evidence": {"S1": "Enterprise refunds after 30 days require VP approval."},
        "answer": "Managers can approve enterprise refunds after 30 days [S1].",
        "expected_terms": {"vp approval"},
        "unsupported_terms": {"managers can approve", "manager approval"},
        "should_refuse": False,
        "versions": {"prompt": "p23-a", "model": "gpt-release-candidate", "corpus": "policy-v4"},
    },
]


def score_answer(case):
    # TODO: return checks, failed_checks, severity, release_gate, and trace.
    return {"id": case["id"]}


def evaluate(cases):
    # TODO: score every case and summarize by domain/risk.
    return {"results": [score_answer(case) for case in cases]}


if __name__ == "__main__":
    print(evaluate(CASES))
