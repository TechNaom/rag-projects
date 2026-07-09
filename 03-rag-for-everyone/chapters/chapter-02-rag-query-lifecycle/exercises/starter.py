questions = [
    {
        "user_question": "Can a contractor access customer logs during a Sev1 incident?",
        "intent": "",
        "retrieval_query": "",
        "metadata_filters": [],
        "expected_source": "",
        "context_rule": "",
        "answer_rule": "",
        "refusal_rule": "",
        "metric_to_inspect": "",
    },
    {
        "user_question": "What changed in the April expense policy update?",
        "intent": "",
        "retrieval_query": "",
        "metadata_filters": [],
        "expected_source": "",
        "context_rule": "",
        "answer_rule": "",
        "refusal_rule": "",
        "metric_to_inspect": "",
    },
    {
        "user_question": "Why did deployment fail after the new environment variable?",
        "intent": "",
        "retrieval_query": "",
        "metadata_filters": [],
        "expected_source": "",
        "context_rule": "",
        "answer_rule": "",
        "refusal_rule": "",
        "metric_to_inspect": "",
    },
]

failure_scenarios = [
    {
        "symptom": "The assistant retrieved the global policy instead of the EU policy.",
        "first_failure_point": "",  # TODO
        "first_debug_action": "",
    },
    {
        "symptom": "The answer cites a document that was not shown in the context block.",
        "first_failure_point": "",  # TODO
        "first_debug_action": "",
    },
    {
        "symptom": "The right chunk is ranked 9th, but the system only sends top 5.",
        "first_failure_point": "",  # TODO
        "first_debug_action": "",
    },
]

trace_log_fields = []

golden_test = {
    "question": "",
    "expected_source": "",
    "expected_behavior": "",
    "metric": "",
}

for item in questions:
    print(item)

print("Failure scenarios:")
for item in failure_scenarios:
    print(item)

print("Trace fields:", trace_log_fields)
print("Golden test:", golden_test)
