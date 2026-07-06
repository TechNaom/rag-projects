"""Module 12 exercise solution for Hands-on Projects."""

TOPICS = ['Basic RAG', 'Production-ready RAG', 'Hybrid Search RAG', 'Parent-Child RAG', 'Multi-query RAG', 'Agentic RAG', 'Graph RAG', 'Enterprise RAG', 'Architecture diagrams', 'Python implementation', 'Performance discussion', 'Interview questions', 'Design trade-offs']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Hands-on Projects\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 12: Hands-on Projects')
    print('1. Basic RAG')
    print('2. Production-ready RAG')
    print('3. Hybrid Search RAG')
    print('4. Parent-Child RAG')
    print('5. Multi-query RAG')
    print('6. Agentic RAG')
    print('7. Graph RAG')
    print('8. Enterprise RAG')
    print('9. Architecture diagrams')
    print('10. Python implementation')
    print('11. Performance discussion')
    print('12. Interview questions')
    print('13. Design trade-offs')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
