"""Chapter 21 exercise solution: write prompt assertions."""

CASES = [
    {"id": "happy", "answer": "VP approval is required [S1].", "expects_citation": True, "expects_refusal": False},
    {"id": "missing", "answer": "I do not have enough evidence to answer.", "expects_citation": False, "expects_refusal": True},
]


def has_citation(answer):
    return "[" in answer and "]" in answer


def has_refusal(answer):
    lowered = answer.lower()
    return "not have enough evidence" in lowered or "insufficient" in lowered


def evaluate(case):
    citation_ok = has_citation(case["answer"]) == case["expects_citation"]
    refusal_ok = has_refusal(case["answer"]) == case["expects_refusal"]
    return {
        "id": case["id"],
        "citation_ok": citation_ok,
        "refusal_ok": refusal_ok,
        "passed": citation_ok and refusal_ok,
    }


if __name__ == "__main__":
    for case in CASES:
        print(evaluate(case))
