"""Module 3 project starter for Chunking Deep Dive."""

TOPICS = ['Fixed-size chunking', 'Recursive chunking', 'Sentence chunking', 'Paragraph chunking', 'Semantic chunking', 'Sliding window chunking', 'Parent-child chunking', 'Hierarchical chunking', 'Agentic chunking', 'LLM-based chunking']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Chunking Deep Dive\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 3: Chunking Deep Dive')
    print('1. Fixed-size chunking')
    print('2. Recursive chunking')
    print('3. Sentence chunking')
    print('4. Paragraph chunking')
    print('5. Semantic chunking')
    print('6. Sliding window chunking')
    print('7. Parent-child chunking')
    print('8. Hierarchical chunking')
    print('9. Agentic chunking')
    print('10. LLM-based chunking')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
