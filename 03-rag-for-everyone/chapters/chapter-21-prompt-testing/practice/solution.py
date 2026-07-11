"""Chapter 21 practice solution: choose prompt test type."""

FAILURES = [
    {"id": "empty_context_answered", "type": "unsupported"},
    {"id": "wrong_source_cited", "type": "citation"},
    {"id": "json_broken", "type": "format"},
    {"id": "ignored_system_rules", "type": "injection"},
]


TEST_MAP = {
    "unsupported": "groundedness_and_refusal_test",
    "citation": "citation_support_test",
    "format": "schema_or_format_regression_test",
    "injection": "prompt_injection_resistance_test",
}


def choose_test(failure):
    return {
        "test_family": TEST_MAP[failure["type"]],
        "release_gate": "block if high-risk case fails",
    }


if __name__ == "__main__":
    for failure in FAILURES:
        print(failure["id"], choose_test(failure))
