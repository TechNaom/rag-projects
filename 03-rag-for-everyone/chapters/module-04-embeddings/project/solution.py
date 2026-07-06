"""Module 4 project solution for Embeddings."""

TOPICS = ['What embeddings are', 'Vector spaces', 'Similarity', 'Dimensionality', 'Distance metrics', 'Cosine similarity', 'Euclidean distance', 'Dot product', 'Embedding models', 'Domain-specific embeddings', 'Fine-tuning', 'Embedding drift', 'Re-indexing', 'Provider comparisons: OpenAI, Cohere, Google, and BAAI']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Embeddings\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 4: Embeddings')
    print('1. What embeddings are')
    print('2. Vector spaces')
    print('3. Similarity')
    print('4. Dimensionality')
    print('5. Distance metrics')
    print('6. Cosine similarity')
    print('7. Euclidean distance')
    print('8. Dot product')
    print('9. Embedding models')
    print('10. Domain-specific embeddings')
    print('11. Fine-tuning')
    print('12. Embedding drift')
    print('13. Re-indexing')
    print('14. Provider comparisons: OpenAI, Cohere, Google, and BAAI')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
