"""Project solution: prompt regression harness."""

CASES = [
    {"id": "happy", "answer": "VP approval is required [S1]. Evidence used: [S1]", "must_cite": True, "must_refuse": False, "high_risk": True},
    {"id": "missing", "answer": "I do not have enough evidence to answer.", "must_cite": False, "must_refuse": True, "high_risk": True},
    {"id": "bad", "answer": "Manager approval is enough.", "must_cite": True, "must_refuse": False, "high_risk": True},
]


def has_citation(answer):
    return "[" in answer and "]" in answer


def has_refusal(answer):
    lowered = answer.lower()
    return "not have enough evidence" in lowered or "insufficient" in lowered


def evaluate_case(case):
    failures = []
    if case["must_cite"] and not has_citation(case["answer"]):
        failures.append("missing_citation")
    if case["must_refuse"] and not has_refusal(case["answer"]):
        failures.append("missing_refusal")
    if not case["must_refuse"] and has_refusal(case["answer"]):
        failures.append("false_refusal")
    return {
        "id": case["id"],
        "passed": not failures,
        "high_risk": case["high_risk"],
        "failures": failures,
    }


def run_suite(cases):
    results = [evaluate_case(case) for case in cases]
    blocking_failures = [
        result for result in results
        if result["high_risk"] and not result["passed"]
    ]
    return {
        "passed": not blocking_failures,
        "results": results,
        "release_gate": "pass" if not blocking_failures else "block",
        "blocking_failures": blocking_failures,
    }


if __name__ == "__main__":
    print(run_suite(CASES))
