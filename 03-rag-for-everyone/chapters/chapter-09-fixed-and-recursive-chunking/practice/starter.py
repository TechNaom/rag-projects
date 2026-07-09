SCENARIOS = [{"name": "HR policy", "shape": "rules_and_exceptions"}]


def choose_strategy(scenario):
    return "todo"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(choose_strategy(scenario))
