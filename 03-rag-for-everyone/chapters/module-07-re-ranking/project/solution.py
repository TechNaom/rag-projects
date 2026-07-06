"""Module 7 project solution for Re-ranking."""

TOPICS = ['Cross-encoders', 'Bi-encoders', 'Late interaction', 'Why re-ranking improves quality', 'Trade-offs between speed and accuracy']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Re-ranking\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 7: Re-ranking')
    print('1. Cross-encoders')
    print('2. Bi-encoders')
    print('3. Late interaction')
    print('4. Why re-ranking improves quality')
    print('5. Trade-offs between speed and accuracy')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
