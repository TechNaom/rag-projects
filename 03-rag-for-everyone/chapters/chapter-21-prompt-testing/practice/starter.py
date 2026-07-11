"""Chapter 21 practice: choose prompt test type."""

FAILURES = [
    {"id": "empty_context_answered", "type": "unsupported"},
    {"id": "wrong_source_cited", "type": "citation"},
    {"id": "json_broken", "type": "format"},
    {"id": "ignored_system_rules", "type": "injection"},
]


def choose_test(failure):
    # TODO: return the test family to add.
    return "todo"


if __name__ == "__main__":
    for failure in FAILURES:
        print(failure["id"], choose_test(failure))
