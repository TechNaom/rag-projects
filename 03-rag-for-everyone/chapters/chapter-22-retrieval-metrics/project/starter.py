"""Project starter: retrieval metrics dashboard seed."""

CASES = [
    {"id": "q1", "slice": "policy", "risk": "high", "gold": {"S2"}, "retrieved": ["S2", "S4", "S8"]},
    {"id": "q2", "slice": "exact_terms", "risk": "high", "gold": {"E7"}, "retrieved": ["S1", "S3", "E7"]},
    {"id": "q3", "slice": "support", "risk": "low", "gold": {"H1"}, "retrieved": ["H2", "H3", "H4"]},
]


def evaluate(cases, k=3):
    # TODO: compute per-case metrics, slice summary, and release gate.
    return {}


if __name__ == "__main__":
    print(evaluate(CASES))
