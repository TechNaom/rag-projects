"""Chapter 20 exercise: generate grounded prompt rules."""

PROFILE = {"domain": "enterprise policy", "risk": "high", "requires_citations": True}


def build_rules(profile):
    # TODO: return a list of grounded prompt rules based on the profile.
    return []


if __name__ == "__main__":
    for rule in build_rules(PROFILE):
        print("-", rule)
