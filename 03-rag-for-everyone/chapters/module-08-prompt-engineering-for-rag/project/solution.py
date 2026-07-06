"""Module 8 project solution for Prompt Engineering for RAG."""

TOPICS = ['Context injection', 'System prompts', 'Citation prompts', 'Grounding', 'Structured output', 'Guardrails', 'Hallucination prevention']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Prompt Engineering for RAG\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 8: Prompt Engineering for RAG')
    print('1. Context injection')
    print('2. System prompts')
    print('3. Citation prompts')
    print('4. Grounding')
    print('5. Structured output')
    print('6. Guardrails')
    print('7. Hallucination prevention')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
