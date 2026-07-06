"""Module 1 hands on lab solution for Foundation."""

TOPICS = ['Why LLMs hallucinate', 'Why context windows are limited', 'Why RAG exists', 'Different types of RAG', 'Naive RAG', 'Advanced RAG', 'Agentic RAG', 'Graph RAG', 'Corrective RAG', 'Adaptive RAG', 'Complete lifecycle of a query']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Foundation\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 1: Foundation')
    print('1. Why LLMs hallucinate')
    print('2. Why context windows are limited')
    print('3. Why RAG exists')
    print('4. Different types of RAG')
    print('5. Naive RAG')
    print('6. Advanced RAG')
    print('7. Agentic RAG')
    print('8. Graph RAG')
    print('9. Corrective RAG')
    print('10. Adaptive RAG')
    print('11. Complete lifecycle of a query')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
