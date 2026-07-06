"""Module 3 project starter for Chunking Deep Dive."""

TOPICS = [
    'Fixed-size chunking',
    'Recursive chunking',
    'Sentence chunking',
    'Paragraph chunking',
    'Semantic chunking',
    'Sliding window chunking',
    'Parent-child chunking',
    'Hierarchical chunking',
    'Agentic chunking',
    'LLM-based chunking',
]


def summarize_module(question: str) -> str:
    return (
        f"Question: {question}\n"
        "Recommended focus: Chunking Deep Dive\n"
        f"Key subtopics: {', '.join(TOPICS[:4])}"
    )


def main() -> None:
    print('Module 3: Chunking Deep Dive')
    for index, topic in enumerate(TOPICS, start=1):
        print(f"{index}. {topic}")
    question = 'How should I study this module?'
    print('\n' + summarize_module(question))


if __name__ == '__main__':
    main()
