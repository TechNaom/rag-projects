scenario = {
    "name": "Customer Refund Bot",
    "user_question": "Can I get a refund for my annual plan in Germany?",
    "lifecycle": {
        "intent": "Determine refund eligibility for annual plan in Germany.",
        "retrieval_query": "Germany annual plan refund eligibility cancellation policy",
        "metadata_filters": ["country:DE", "product_tier:annual", "policy_status:approved"],
        "expected_sources": ["refund_policy_eu_2026.md", "annual_plan_terms_2026.md"],
        "context_rule": "Require both regional refund policy and annual-plan terms.",
        "answer_rule": "Answer with eligibility, deadline, next step, and citations.",
        "refusal_rule": "If purchase date or source policy is missing, ask for purchase date and avoid promising refund.",
        "logs": ["request_id", "retrieval_query", "filters", "source_ids", "answer_status", "latency_ms"],
        "metric": "Recall@5 for regional policy plus citation precision.",
    },
}

print(scenario)
