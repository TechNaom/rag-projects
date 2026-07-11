"""Chapter 19 practice: diagnose context injection failures."""

CASES = [
    {"id": "conflict", "fresh_conflict": True, "document_instruction": False, "over_budget": False},
    {"id": "injection", "fresh_conflict": False, "document_instruction": True, "over_budget": False},
    {"id": "budget", "fresh_conflict": False, "document_instruction": False, "over_budget": True},
]


def recommend_fix(case):
    # TODO: return a production fix for each case.
    return "todo"


if __name__ == "__main__":
    for case in CASES:
        print(case["id"], recommend_fix(case))
