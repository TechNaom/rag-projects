"""Chapter 20 practice: diagnose prompt failures."""

CASES = [
    {"id": "no_evidence_answer", "empty_context": True, "bad_citation": False, "injection_obeyed": False},
    {"id": "bad_citation", "empty_context": False, "bad_citation": True, "injection_obeyed": False},
    {"id": "prompt_injection", "empty_context": False, "bad_citation": False, "injection_obeyed": True},
]


def diagnose(case):
    # TODO: return a fix and a regression test.
    return {}


if __name__ == "__main__":
    for case in CASES:
        print(case["id"], diagnose(case))
