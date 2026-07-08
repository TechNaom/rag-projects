questions = [
    {
        "question": "What is Retrieval-Augmented Generation?",
        "classification": "",  # TODO: model_memory, web_search, or rag
        "reason": "",
    },
    {
        "question": "How many vacation days do I get after 5 years at Northkeep?",
        "classification": "",  # TODO
        "reason": "",
    },
    {
        "question": "What is the weather in Mumbai today?",
        "classification": "",  # TODO
        "reason": "",
    },
    {
        "question": "Can I report fraud directly to the SEC under our whistleblower policy?",
        "classification": "",  # TODO
        "reason": "",
    },
]

# TODO: Add one more Northkeep-style policy question.

for item in questions:
    print(f"Question: {item['question']}")
    print(f"Classification: {item['classification'] or '[fill this in]'}")
    print(f"Reason: {item['reason'] or '[fill this in]'}")
    print()

