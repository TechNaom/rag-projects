questions = [
    {
        "question": "What is Retrieval-Augmented Generation?",
        "classification": "",  # TODO: model_memory, web_search, or rag
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "How many vacation days do I get after 5 years at Northkeep?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "What is the weather in Mumbai today?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "Can I report fraud directly to the SEC under our whistleblower policy?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "Can a contractor access customer logs during a Sev1 incident?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "What changed in Northkeep's expense policy after the April update?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "Who won the latest Formula 1 race?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "Explain cosine similarity in simple terms.",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "Can the assistant summarize this customer's contract renewal clause?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
    {
        "question": "What is our approved incident communication template for EU customers?",
        "classification": "",  # TODO
        "reason": "",
        "expected_source": "",
        "citation_rule": "",
        "metadata_filters": [],
        "refusal_rule": "",
    },
]

# TODO: Add two more Northkeep-style policy questions:
# 1. One low-risk policy question.
# 2. One high-risk policy question.

golden_eval = {
    "question": "",  # TODO: write one test question that proves RAG is needed
    "expected_source": "",
    "expected_behavior": "",
    "bad_answer_to_catch": "",
    "first_metric_to_inspect": "",
}

product_manager_explanation = """
TODO: In five sentences, explain why this product needs RAG instead of only a
better prompt. Keep it simple, but mention trust, freshness, citations, and risk.
"""

for item in questions:
    print(f"Question: {item['question']}")
    print(f"Classification: {item['classification'] or '[fill this in]'}")
    print(f"Reason: {item['reason'] or '[fill this in]'}")
    print(f"Expected source: {item['expected_source'] or '[fill this in when RAG]'}")
    print(f"Citation rule: {item['citation_rule'] or '[fill this in when RAG]'}")
    print(f"Metadata filters: {item['metadata_filters'] or '[fill this in when useful]'}")
    print(f"Refusal rule: {item['refusal_rule'] or '[fill this in when useful]'}")
    print()

print("Golden eval:")
for key, value in golden_eval.items():
    print(f"- {key}: {value or '[fill this in]'}")

print("\nProduct manager explanation:")
print(product_manager_explanation.strip())
