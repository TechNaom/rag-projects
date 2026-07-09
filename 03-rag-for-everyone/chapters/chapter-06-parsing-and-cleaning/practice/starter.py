SCENARIOS = [
    {"name": "Refund PDF", "format": "pdf", "table_confidence": 0.55, "ocr_confidence": 0.94, "boilerplate_ratio": 0.05},
    {"name": "Docs HTML", "format": "html", "table_confidence": None, "ocr_confidence": None, "boilerplate_ratio": 0.37},
]


def classify_scenario(scenario):
    # TODO: return a production decision for each scenario
    return "todo"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], classify_scenario(scenario))
