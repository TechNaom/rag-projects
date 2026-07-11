TRACES = [
    {"id": "hr-001", "symptom": "missing_exception", "source": "hr-policy", "user_impact": "wrong eligibility"},
    {"id": "docs-002", "symptom": "repeated_neighbors", "source": "api-docs", "user_impact": "confusing answer"},
    {"id": "legal-003", "symptom": "old_policy", "source": "legal-faq", "user_impact": "wrong compliance advice"},
]


def build_review_board(traces):
    # TODO: produce release-ready reports.
    raise NotImplementedError


if __name__ == "__main__":
    for item in build_review_board(TRACES):
        print(item)
