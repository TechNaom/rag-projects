"""Module 2 project starter for Documents and Data Ingestion."""

TOPICS = ['PDFs', 'DOCX', 'HTML', 'Markdown', 'JSON', 'APIs', 'Databases', 'Incremental ingestion', 'Metadata', 'Data cleaning', 'OCR', 'Parsing', 'Unstructured vs structured data', 'Why preprocessing matters', 'What production pipelines look like']

def summarize_module(question: str) -> str:
    return f"Question: {question}\nRecommended focus: Documents and Data Ingestion\nKey subtopics: {', '.join(TOPICS[:4])}"

def main() -> None:
    print('Module 2: Documents and Data Ingestion')
    print('1. PDFs')
    print('2. DOCX')
    print('3. HTML')
    print('4. Markdown')
    print('5. JSON')
    print('6. APIs')
    print('7. Databases')
    print('8. Incremental ingestion')
    print('9. Metadata')
    print('10. Data cleaning')
    print('11. OCR')
    print('12. Parsing')
    print('13. Unstructured vs structured data')
    print('14. Why preprocessing matters')
    print('15. What production pipelines look like')
    question = 'How should I study this module?'
    print() 
    print(summarize_module(question))

if __name__ == '__main__':
    main()
