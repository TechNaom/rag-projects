REQUESTS = [
    {"id": "faq-001", "intent": "simple_faq", "risk": "low", "gold_rank": 2, "duplicates": 0},
    {"id": "policy-002", "intent": "policy_exception", "risk": "high", "gold_rank": 9, "duplicates": 1},
    {"id": "runbook-003", "intent": "troubleshooting", "risk": "high", "gold_rank": 4, "duplicates": 4},
]

BASE_POLICIES = {
    "simple_faq": {"top_k": 3, "controls": ["metadata_filters", "dedupe"], "metric": "citation_support"},
    "policy_exception": {"top_k": 10, "controls": ["metadata_filters", "query_rewrite", "parent_expansion", "rerank"], "metric": "Recall@10"},
    "troubleshooting": {"top_k": 8, "controls": ["metadata_filters", "multi_query", "dedupe", "ordered_context"], "metric": "procedure_completeness"},
}


def build_retrieval_policy(request):
    policy = BASE_POLICIES.get(request["intent"], {"top_k": 5, "controls": ["metadata_filters"], "metric": "Recall@5"})
    controls = list(policy["controls"])
    if request["duplicates"] >= 3 and "dedupe" not in controls:
        controls.append("dedupe")
    if request["gold_rank"] > policy["top_k"]:
        controls.append("increase_k_or_rerank")
    if request["risk"] == "high" and "trace_review" not in controls:
        controls.append("trace_review")
    return {
        "id": request["id"],
        "top_k": policy["top_k"],
        "controls": controls,
        "primary_metric": policy["metric"],
        "trace_note": (
            f"{request['id']} uses k={policy['top_k']} for {request['intent']}; "
            f"gold_rank={request['gold_rank']}, duplicates={request['duplicates']}."
        ),
    }


if __name__ == "__main__":
    for request in REQUESTS:
        print(build_retrieval_policy(request))
