SCENARIOS = [
    {"name": "HR policy", "shape": "rules_and_exceptions"},
    {"name": "Troubleshooting runbook", "shape": "procedure_steps"},
    {"name": "Developer tutorial", "shape": "explanation_plus_code"},
    {"name": "Pricing table", "shape": "table"},
    {"name": "Long FAQ", "shape": "short_qna"},
]


def choose_strategy(scenario):
    shape = scenario["shape"]
    if shape == "rules_and_exceptions":
        return "recursive: keep headings, rule paragraphs, and exception notes together"
    if shape == "procedure_steps":
        return "recursive: split by procedure step and keep warning blocks attached"
    if shape == "explanation_plus_code":
        return "recursive: keep code blocks with the explanation that introduces them"
    if shape == "table":
        return "table-aware recursive: preserve headers, row ids, units, and captions"
    if shape == "short_qna":
        return "fixed or question-answer boundary: keep each FAQ pair together"
    return "review"


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(scenario["name"], choose_strategy(scenario))
