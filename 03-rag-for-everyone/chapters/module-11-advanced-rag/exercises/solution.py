"""Module 11 exercise solution for Advanced RAG."""

TOPICS = ['Agentic RAG', 'Graph RAG', 'Knowledge Graph RAG', 'Multi-modal RAG', 'SQL RAG', 'Code RAG', 'Long-context RAG', 'Recursive retrieval', 'Adaptive retrieval', 'Multi-agent RAG']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Advanced RAG\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 11: Advanced RAG')
    print('1. Agentic RAG')
    print('2. Graph RAG')
    print('3. Knowledge Graph RAG')
    print('4. Multi-modal RAG')
    print('5. SQL RAG')
    print('6. Code RAG')
    print('7. Long-context RAG')
    print('8. Recursive retrieval')
    print('9. Adaptive retrieval')
    print('10. Multi-agent RAG')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
