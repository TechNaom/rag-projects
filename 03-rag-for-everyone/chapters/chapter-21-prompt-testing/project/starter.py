"""Project starter: prompt regression harness."""

CASES = [
    {"id": "happy", "answer": "VP approval is required [S1]. Evidence used: [S1]", "must_cite": True, "must_refuse": False, "high_risk": True},
    {"id": "missing", "answer": "I do not have enough evidence to answer.", "must_cite": False, "must_refuse": True, "high_risk": True},
    {"id": "bad", "answer": "Manager approval is enough.", "must_cite": True, "must_refuse": False, "high_risk": True},
]


def run_suite(cases):
    # TODO: return per-case results and release gate status.
    return {"passed": False, "results": []}


if __name__ == "__main__":
    print(run_suite(CASES))
