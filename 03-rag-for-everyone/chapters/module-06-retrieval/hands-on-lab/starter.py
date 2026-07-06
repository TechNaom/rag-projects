"""Module 6 hands on lab for Retrieval."""

TOPICS = ['Similarity search', 'Hybrid search', 'BM25', 'Sparse retrieval', 'Dense retrieval', 'Reciprocal Rank Fusion (RRF)', 'Multi-query retrieval', 'Multi-vector retrieval', 'Parent-document retrieval', 'Self-query retrieval', 'Metadata filtering', 'Context compression', 'Query rewriting', 'Query expansion']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Retrieval\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 6: Retrieval')
    print('1. Similarity search')
    print('2. Hybrid search')
    print('3. BM25')
    print('4. Sparse retrieval')
    print('5. Dense retrieval')
    print('6. Reciprocal Rank Fusion (RRF)')
    print('7. Multi-query retrieval')
    print('8. Multi-vector retrieval')
    print('9. Parent-document retrieval')
    print('10. Self-query retrieval')
    print('11. Metadata filtering')
    print('12. Context compression')
    print('13. Query rewriting')
    print('14. Query expansion')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
