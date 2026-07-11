"""Chapter 20 practice solution: diagnose prompt failures."""

CASES = [
    {"id": "no_evidence_answer", "empty_context": True, "bad_citation": False, "injection_obeyed": False},
    {"id": "bad_citation", "empty_context": False, "bad_citation": True, "injection_obeyed": False},
    {"id": "prompt_injection", "empty_context": False, "bad_citation": False, "injection_obeyed": True},
]


def diagnose(case):
    if case["empty_context"]:
        return {"fix": "add_refusal_rule", "test": "empty context should produce insufficiency answer"}
    if case["bad_citation"]:
        return {"fix": "claim_level_citation_rule", "test": "each claim citation must support the sentence"}
    if case["injection_obeyed"]:
        return {"fix": "evidence_as_data_boundary", "test": "retrieved instruction must not override system rules"}
    return {"fix": "monitor", "test": "standard groundedness check"}


if __name__ == "__main__":
    for case in CASES:
        print(case["id"], diagnose(case))
