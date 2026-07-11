"""Project starter: grounded prompt policy builder."""

POLICY = {"domain": "enterprise refund policies", "risk": "high", "format": "bullets"}


def build_system_prompt(policy):
    # TODO: generate a grounded system prompt and regression checklist.
    return {"prompt": "", "tests": []}


if __name__ == "__main__":
    result = build_system_prompt(POLICY)
    print(result["prompt"])
    print(result["tests"])
