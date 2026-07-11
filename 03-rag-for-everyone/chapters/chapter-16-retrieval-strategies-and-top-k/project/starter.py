REQUESTS = [
    {"id": "faq-001", "intent": "simple_faq", "risk": "low", "gold_rank": 2, "duplicates": 0},
    {"id": "policy-002", "intent": "policy_exception", "risk": "high", "gold_rank": 9, "duplicates": 1},
    {"id": "runbook-003", "intent": "troubleshooting", "risk": "high", "gold_rank": 4, "duplicates": 4},
]


def build_retrieval_policy(request):
    # TODO: return top_k, controls, metric, and trace note.
    raise NotImplementedError


if __name__ == "__main__":
    for request in REQUESTS:
        print(build_retrieval_policy(request))
