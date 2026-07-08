questions = [
    {
        "question": "What is Retrieval-Augmented Generation?",
        "classification": "model_memory",
        "reason": "A general definition can usually come from model knowledge.",
        "expected_source": "None required for a basic definition.",
        "citation_rule": "Optional citation if this is part of a formal course or docs page.",
        "metadata_filters": [],
        "refusal_rule": "Refuse only if the user asks for a company-specific definition without sources.",
    },
    {
        "question": "How many vacation days do I get after 5 years at Northkeep?",
        "classification": "rag",
        "reason": "The answer must come from Northkeep's private policy document.",
        "expected_source": "northkeep_pto_policy_2026.pdf",
        "citation_rule": "Cite policy version, section, and effective date.",
        "metadata_filters": ["country", "employment_type", "tenure_band", "policy_version"],
        "refusal_rule": "If the policy or employee context is missing, ask for location and employment type instead of guessing.",
    },
    {
        "question": "What is the weather in Mumbai today?",
        "classification": "web_search",
        "reason": "The answer is current public information, not a private corpus question.",
        "expected_source": "Current weather provider or public web source.",
        "citation_rule": "Cite timestamp and source if shown in a customer-facing answer.",
        "metadata_filters": ["location", "date"],
        "refusal_rule": "If no live source is available, say the system cannot verify current weather.",
    },
    {
        "question": "Can I report fraud directly to the SEC under our whistleblower policy?",
        "classification": "rag",
        "reason": "The assistant needs the exact internal policy and should cite it.",
        "expected_source": "whistleblower_policy_2026.pdf",
        "citation_rule": "Cite the reporting-rights section and include escalation contact.",
        "metadata_filters": ["jurisdiction", "employee_type", "policy_version"],
        "refusal_rule": "If the retrieved context does not cover SEC reporting, avoid legal advice and route to compliance.",
    },
    {
        "question": "Can a contractor access customer logs during a Sev1 incident?",
        "classification": "rag",
        "reason": "This depends on internal access policy, incident severity, role, and data classification.",
        "expected_source": "customer_data_access_policy.md and sev1_incident_runbook.md",
        "citation_rule": "Cite access rule, incident exception rule, and approval owner.",
        "metadata_filters": ["role", "incident_severity", "data_classification", "region"],
        "refusal_rule": "If approval or role is unclear, say access cannot be confirmed and escalate to incident commander.",
    },
    {
        "question": "What changed in Northkeep's expense policy after the April update?",
        "classification": "rag",
        "reason": "The answer requires comparing approved policy versions, not model memory.",
        "expected_source": "expense_policy_2026_april.pdf and expense_policy_2026_march.pdf",
        "citation_rule": "Cite both versions and list only verified changes.",
        "metadata_filters": ["policy_name", "effective_date", "region"],
        "refusal_rule": "If only one version is retrieved, explain that a reliable comparison is not possible.",
    },
    {
        "question": "Who won the latest Formula 1 race?",
        "classification": "web_search",
        "reason": "The answer is public and time-sensitive.",
        "expected_source": "Current sports/news source.",
        "citation_rule": "Cite event name and publish timestamp.",
        "metadata_filters": ["sport", "event_date"],
        "refusal_rule": "If live data is unavailable, say the result cannot be verified.",
    },
    {
        "question": "Explain cosine similarity in simple terms.",
        "classification": "model_memory",
        "reason": "This is a stable concept that the model can explain without private context.",
        "expected_source": "None required for a simple explanation.",
        "citation_rule": "Optional for academic or formal material.",
        "metadata_filters": [],
        "refusal_rule": "If the user asks for the company's exact embedding scoring method, switch to RAG.",
    },
    {
        "question": "Can the assistant summarize this customer's contract renewal clause?",
        "classification": "rag",
        "reason": "The answer depends on a private contract and may carry legal risk.",
        "expected_source": "customer_contract.pdf",
        "citation_rule": "Cite clause number and avoid legal conclusions.",
        "metadata_filters": ["customer_id", "contract_version", "confidentiality_level"],
        "refusal_rule": "If the clause is missing or ambiguous, summarize only what is present and route legal interpretation to counsel.",
    },
    {
        "question": "What is our approved incident communication template for EU customers?",
        "classification": "rag",
        "reason": "The assistant needs the approved internal template and region-specific compliance guidance.",
        "expected_source": "eu_incident_comms_template.md and gdpr_incident_policy.pdf",
        "citation_rule": "Cite template version, approval owner, and region.",
        "metadata_filters": ["region", "incident_type", "customer_tier", "template_version"],
        "refusal_rule": "If the EU template is missing, do not reuse another region's template; escalate to communications/legal.",
    },
    {
        "question": "What is the client dinner approval threshold in our expense policy?",
        "classification": "rag",
        "reason": "The threshold must be retrieved from the approved expense policy.",
        "expected_source": "expense_policy_2026.pdf",
        "citation_rule": "Cite spend threshold, approver role, and region-specific exception.",
        "metadata_filters": ["region", "employee_level", "expense_category"],
        "refusal_rule": "If region or amount is missing, ask for those details before answering.",
    },
]

golden_eval = {
    "question": "Can a contractor in Germany access customer logs during a Sev1 incident?",
    "expected_source": "customer_data_access_policy.md and sev1_incident_runbook.md",
    "expected_behavior": "Answer only if both access policy and Sev1 exception rules are retrieved; otherwise escalate.",
    "bad_answer_to_catch": "Yes, Sev1 incidents allow all engineers to access logs.",
    "first_metric_to_inspect": "Recall@k for the access policy and runbook pair.",
}

product_manager_explanation = """
We need RAG because the assistant must answer from Northkeep's approved sources,
not from general model memory. Policies change, and a better prompt cannot know
which version is currently approved. RAG also lets the answer cite the policy so
employees and reviewers can verify it. When the right source is missing, the
assistant can refuse or escalate instead of guessing. That makes the product more
trustworthy, auditable, and safer to ship.
"""

for item in questions:
    print(f"Question: {item['question']}")
    print(f"Classification: {item['classification']}")
    print(f"Reason: {item['reason']}")
    print(f"Expected source: {item['expected_source']}")
    print(f"Citation rule: {item['citation_rule']}")
    print(f"Metadata filters: {item['metadata_filters']}")
    print(f"Refusal rule: {item['refusal_rule']}")
    print()

print("Golden eval:")
for key, value in golden_eval.items():
    print(f"- {key}: {value}")

print("\nProduct manager explanation:")
print(product_manager_explanation.strip())
