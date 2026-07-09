SCENARIOS = [
    {"name": "EU security policy", "authority": "approved", "access_level": "restricted", "region": "EU"},
    {"name": "Draft HR policy", "authority": "draft", "access_level": "internal", "region": "GLOBAL"},
]


def recommend_metadata_action(scenario):
    # TODO: return metadata action for each scenario
    return "todo"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], recommend_metadata_action(scenario))
