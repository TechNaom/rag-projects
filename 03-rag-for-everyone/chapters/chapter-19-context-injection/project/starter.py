"""Project starter: production-style context pack builder."""

EVIDENCE = [
    {"id": "A1", "source": "policy-v4", "text": "Refunds after 30 days need VP approval.", "tokens": 9, "authority": 3, "fresh": True, "access": True, "score": 0.95},
    {"id": "A2", "source": "policy-v3", "text": "Refunds after 30 days need manager approval.", "tokens": 9, "authority": 2, "fresh": False, "access": True, "score": 0.88},
    {"id": "A3", "source": "addendum", "text": "Enterprise addendum requires written exception reason.", "tokens": 8, "authority": 3, "fresh": True, "access": True, "score": 0.89},
    {"id": "A4", "source": "private-note", "text": "Internal margin target is confidential.", "tokens": 7, "authority": 1, "fresh": True, "access": False, "score": 0.80},
]


def build_prompt(question, evidence, max_tokens=18):
    # TODO: build a context pack and render a prompt with evidence boundaries.
    return ""


if __name__ == "__main__":
    print(build_prompt("What approval is needed for enterprise refunds after 30 days?", EVIDENCE))
