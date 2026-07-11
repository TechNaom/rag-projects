"""Chapter 21 exercise: write prompt assertions."""

CASES = [
    {"id": "happy", "answer": "VP approval is required [S1].", "expects_citation": True, "expects_refusal": False},
    {"id": "missing", "answer": "I do not have enough evidence to answer.", "expects_citation": False, "expects_refusal": True},
]


def evaluate(case):
    # TODO: return pass/fail checks for citation and refusal behavior.
    return {"id": case["id"], "passed": False}


if __name__ == "__main__":
    for case in CASES:
        print(evaluate(case))
