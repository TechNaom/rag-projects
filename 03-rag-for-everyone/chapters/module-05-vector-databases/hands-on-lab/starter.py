"""Module 5 hands on lab for Vector Databases."""

TOPICS = ['ANN vs Exact Search', 'HNSW', 'IVF', 'PQ', 'OPQ', 'DiskANN', 'ScaNN', 'Filtering', 'Metadata search', 'Hybrid search', 'Distributed vector databases', 'Sharding', 'Replication', 'Database comparisons: Pinecone, Weaviate, Qdrant, Milvus, and Chroma']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Vector Databases\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 5: Vector Databases')
    print('1. ANN vs Exact Search')
    print('2. HNSW')
    print('3. IVF')
    print('4. PQ')
    print('5. OPQ')
    print('6. DiskANN')
    print('7. ScaNN')
    print('8. Filtering')
    print('9. Metadata search')
    print('10. Hybrid search')
    print('11. Distributed vector databases')
    print('12. Sharding')
    print('13. Replication')
    print('14. Database comparisons: Pinecone, Weaviate, Qdrant, Milvus, and Chroma')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
