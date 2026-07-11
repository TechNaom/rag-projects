CANDIDATES = [
    {"name": "local-open", "recall_at_5": 0.76, "citation": 0.70, "latency": 40, "cost": 1, "privacy": "approved", "migration": "medium"},
    {"name": "managed-api", "recall_at_5": 0.88, "citation": 0.82, "latency": 135, "cost": 3, "privacy": "review", "migration": "medium"},
    {"name": "domain-private", "recall_at_5": 0.92, "citation": 0.86, "latency": 210, "cost": 5, "privacy": "approved", "migration": "high"},
]


def build_selection_board(candidates):
    # TODO: produce ranked release recommendations.
    raise NotImplementedError


if __name__ == "__main__":
    for item in build_selection_board(CANDIDATES):
        print(item)
