"""Module 9 exercise starter for Evaluation."""

TOPICS = ['Recall@K', 'Precision@K', 'MRR', 'NDCG', 'Faithfulness', 'Context Precision', 'Answer Relevancy', 'Groundedness', 'Latency', 'Cost', 'Evaluation frameworks: Ragas and DeepEval']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Evaluation\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 9: Evaluation')
    print('1. Recall@K')
    print('2. Precision@K')
    print('3. MRR')
    print('4. NDCG')
    print('5. Faithfulness')
    print('6. Context Precision')
    print('7. Answer Relevancy')
    print('8. Groundedness')
    print('9. Latency')
    print('10. Cost')
    print('11. Evaluation frameworks: Ragas and DeepEval')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
