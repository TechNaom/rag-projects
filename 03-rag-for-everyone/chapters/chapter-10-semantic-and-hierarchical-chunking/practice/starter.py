SCENARIOS = [{"name": "Security runbook", "needs_parent": True}]


def choose_strategy(scenario):
    return "todo"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(choose_strategy(scenario))
