questions = [
    {
        "question": "What is Retrieval-Augmented Generation?",
        "classification": "model_memory",
        "reason": "A general definition can usually come from model knowledge.",
    },
    {
        "question": "How many vacation days do I get after 5 years at Northkeep?",
        "classification": "rag",
        "reason": "The answer must come from Northkeep's private policy document.",
    },
    {
        "question": "What is the weather in Mumbai today?",
        "classification": "web_search",
        "reason": "The answer is current public information, not a private corpus question.",
    },
    {
        "question": "Can I report fraud directly to the SEC under our whistleblower policy?",
        "classification": "rag",
        "reason": "The assistant needs the exact internal policy and should cite it.",
    },
    {
        "question": "What is the client dinner approval threshold in our expense policy?",
        "classification": "rag",
        "reason": "The threshold must be retrieved from the approved expense policy.",
    },
]

for item in questions:
    print(f"Question: {item['question']}")
    print(f"Classification: {item['classification']}")
    print(f"Reason: {item['reason']}")
    print()

