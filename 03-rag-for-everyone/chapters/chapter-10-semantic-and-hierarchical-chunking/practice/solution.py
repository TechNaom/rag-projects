SCENARIOS = [
    {"name": "Security runbook", "needs_parent": True, "topic_shifts": "medium", "simple_passes": False},
    {"name": "Short FAQ", "needs_parent": False, "topic_shifts": "low", "simple_passes": True},
    {"name": "Research report", "needs_parent": True, "topic_shifts": "high", "simple_passes": False},
    {"name": "Developer docs", "needs_parent": True, "topic_shifts": "medium", "simple_passes": False},
    {"name": "Policy handbook", "needs_parent": True, "topic_shifts": "high", "simple_passes": False},
]


def choose_strategy(scenario):
    if scenario["simple_passes"]:
        return "keep recursive baseline: advanced chunking is not justified yet"
    if scenario["needs_parent"] and scenario["topic_shifts"] == "high":
        return "semantic + hierarchical: split by topic and preserve parent sections"
    if scenario["needs_parent"]:
        return "hierarchical: retrieve child evidence and expand parent context"
    return "semantic: topic boundaries matter more than parent expansion"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], choose_strategy(scenario))
