"""Module 3 project solution for Chunking Deep Dive."""

from __future__ import annotations

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

SAMPLE_TEXT = (
    'RAG systems improve answer quality by retrieving grounded evidence. '
    'Chunking decides how much of that evidence travels together. '
    'Bad chunk boundaries can hide the exact sentence you need.'
)


def summarize_module(question: str) -> str:
    return (
        f"Question: {question}\n"
        "Recommended focus: Chunking Deep Dive\n"
        f"Key subtopics: {', '.join(TOPICS[:4])}"
    )


def fixed_size_chunks(text: str, size: int = 50) -> list[str]:
    return [text[index:index + size] for index in range(0, len(text), size)]


def overlapping_chunks(text: str, size: int = 50, overlap: int = 10) -> list[str]:
    chunks = []
    step = max(1, size - overlap)
    for index in range(0, len(text), step):
        chunk = text[index:index + size]
        if chunk:
            chunks.append(chunk)
        if index + size >= len(text):
            break
    return chunks


def main() -> None:
    print('Module 3: Chunking Deep Dive')
    for index, topic in enumerate(TOPICS, start=1):
        print(f"{index}. {topic}")

    question = 'How should I study this module?'
    print('\n' + summarize_module(question))

    print('\nFixed-size chunks:')
    for chunk in fixed_size_chunks(SAMPLE_TEXT):
        print('-', chunk)

    print('\nOverlapping chunks:')
    for chunk in overlapping_chunks(SAMPLE_TEXT):
        print('-', chunk)


if __name__ == '__main__':
    main()
