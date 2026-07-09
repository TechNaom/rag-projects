questions = [
    {
        "user_question": "Can a contractor access customer logs during a Sev1 incident?",
        "intent": "Check emergency access rules for contractor log access.",
        "retrieval_query": "contractor customer log access Sev1 incident approval",
        "metadata_filters": ["incident_severity:sev1", "role:contractor", "data:customer_logs"],
        "expected_source": "customer_data_access_policy.md + sev1_incident_runbook.md",
        "context_rule": "Require both access policy and incident exception runbook.",
        "answer_rule": "Answer only with approval owner, allowed scope, and citation.",
        "refusal_rule": "If either source is missing, escalate to incident commander.",
        "metric_to_inspect": "Recall@5 for both required sources.",
    },
    {
        "user_question": "What changed in the April expense policy update?",
        "intent": "Compare current and previous policy versions.",
        "retrieval_query": "expense policy April update changes previous version",
        "metadata_filters": ["policy:expense", "version:april", "status:approved"],
        "expected_source": "expense_policy_2026_april.pdf + expense_policy_2026_march.pdf",
        "context_rule": "Require both versions before summarizing changes.",
        "answer_rule": "List verified changes with both version citations.",
        "refusal_rule": "If one version is missing, say comparison is not reliable.",
        "metric_to_inspect": "Paired-source recall.",
    },
    {
        "user_question": "Why did deployment fail after the new environment variable?",
        "intent": "Troubleshoot deployment with docs and possibly logs.",
        "retrieval_query": "deployment failed new environment variable runbook",
        "metadata_filters": ["system:deployment", "artifact:runbook"],
        "expected_source": "deployment_runbook.md + environment_variables.md",
        "context_rule": "Retrieve docs first; ask for logs if docs are insufficient.",
        "answer_rule": "Give likely checks, not a fake root cause.",
        "refusal_rule": "If no logs are available, avoid claiming certainty.",
        "metric_to_inspect": "Source coverage and follow-up question rate.",
    },
]

failure_scenarios = [
    {
        "symptom": "The assistant retrieved the global policy instead of the EU policy.",
        "first_failure_point": "metadata filtering",
        "first_debug_action": "Inspect region filter and document metadata.",
    },
    {
        "symptom": "The answer cites a document that was not shown in the context block.",
        "first_failure_point": "citation",
        "first_debug_action": "Check citation grounding and source id constraints.",
    },
    {
        "symptom": "The right chunk is ranked 9th, but the system only sends top 5.",
        "first_failure_point": "retrieval",
        "first_debug_action": "Inspect top-k, reranking, and query rewrite options.",
    },
]

trace_log_fields = [
    "request_id",
    "user_question",
    "user_role",
    "retrieval_query",
    "metadata_filters",
    "retrieved_source_ids",
    "retrieval_scores",
    "prompt_template_version",
    "answer_status",
    "citation_source_ids",
    "refusal_reason",
    "latency_ms",
    "estimated_cost",
]

golden_test = {
    "question": "Can a contractor in Germany access customer logs during Sev1?",
    "expected_source": "customer_data_access_policy.md + sev1_incident_runbook.md",
    "expected_behavior": "Answer only if contractor role, EU region, and Sev1 exception are all supported.",
    "metric": "Recall@5 plus citation precision.",
}

for item in questions:
    print(item)

print("Failure scenarios:")
for item in failure_scenarios:
    print(item)

print("Trace fields:", trace_log_fields)
print("Golden test:", golden_test)
