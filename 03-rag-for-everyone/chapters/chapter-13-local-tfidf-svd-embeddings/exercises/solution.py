from collections import Counter
from math import log, sqrt
import re

DOCUMENTS = {
    "doc-1": "rotate api key and update dependent services",
    "doc-2": "quarterly revenue forecast and finance review",
    "doc-3": "reset password and regenerate access credential",
}


def tokenize(text):
    return re.findall(r"[a-z0-9-]+", text.lower())


def build_idf(documents):
    total_docs = len(documents)
    document_frequency = Counter()
    for text in documents.values():
        document_frequency.update(set(tokenize(text)))
    return {
        token: log((1 + total_docs) / (1 + count)) + 1
        for token, count in document_frequency.items()
    }


def vectorize(text, vocabulary, idf):
    counts = Counter(tokenize(text))
    total = sum(counts.values()) or 1
    return [
        (counts[token] / total) * idf.get(token, 0.0)
        for token in vocabulary
    ]


def cosine(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_length = sqrt(sum(a * a for a in left))
    right_length = sqrt(sum(b * b for b in right))
    if left_length == 0 or right_length == 0:
        return 0.0
    return dot / (left_length * right_length)


def rank(query, documents):
    idf = build_idf(documents)
    vocabulary = sorted(idf)
    query_vector = vectorize(query, vocabulary, idf)
    query_tokens = set(tokenize(query))
    results = []
    for doc_id, text in documents.items():
        doc_vector = vectorize(text, vocabulary, idf)
        score = cosine(query_vector, doc_vector)
        matched = sorted(query_tokens.intersection(tokenize(text)))
        results.append({
            "id": doc_id,
            "score": round(score, 4),
            "matched_terms": matched,
            "trace": f"{doc_id} matched {matched or 'no query terms'} with score {score:.4f}.",
        })
    return sorted(results, key=lambda item: item["score"], reverse=True)


if __name__ == "__main__":
    for result in rank("api key rotation", DOCUMENTS):
        print(result)
