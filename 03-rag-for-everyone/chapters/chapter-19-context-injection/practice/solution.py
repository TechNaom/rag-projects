"""Chapter 19 practice solution: diagnose context injection failures."""

CASES = [
    {"id": "conflict", "fresh_conflict": True, "document_instruction": False, "over_budget": False},
    {"id": "injection", "fresh_conflict": False, "document_instruction": True, "over_budget": False},
    {"id": "budget", "fresh_conflict": False, "document_instruction": False, "over_budget": True},
]


def recommend_fix(case):
    if case["fresh_conflict"]:
        return {
            "fix": "conflict_policy",
            "action": "prefer authoritative fresh source or refuse with conflict note",
            "metric": "citation support and conflict rate",
        }
    if case["document_instruction"]:
        return {
            "fix": "prompt_boundary",
            "action": "quote document text as evidence and ignore embedded commands",
            "metric": "prompt injection pass rate",
        }
    if case["over_budget"]:
        return {
            "fix": "budgeted_packing",
            "action": "drop duplicates and low-authority chunks with logged reasons",
            "metric": "context precision and truncation rate",
        }
    return {"fix": "monitor", "action": "no immediate issue", "metric": "answer quality"}


if __name__ == "__main__":
    for case in CASES:
        print(case["id"], recommend_fix(case))
