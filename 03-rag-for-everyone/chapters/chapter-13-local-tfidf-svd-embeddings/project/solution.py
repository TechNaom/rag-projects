from collections import Counter
from math import log, sqrt
import re

DOCUMENTS = {
    "security": "rotate api key regenerate credential update dependent service",
    "finance": "quarterly revenue forecast budget finance review",
    "support": "reset password recover account login credential",
    "policy": "paid time off probation employee eligibility policy",
}

TOPIC_AXES = {
    "security": {"api", "key", "credential", "password", "login"},
    "finance": {"revenue", "forecast", "budget", "finance"},
    "hr": {"paid", "time", "off", "probation", "employee", "eligibility"},
}


def tokenize(text):
    return re.findall(r"[a-z0-9-]+", text.lower())


def build_idf(documents):
    total = len(documents)
    df = Counter()
    for text in documents.values():
        df.update(set(tokenize(text)))
    return {token: log((1 + total) / (1 + count)) + 1 for token, count in df.items()}


def vectorize(text, vocabulary, idf):
    counts = Counter(tokenize(text))
    total = sum(counts.values()) or 1
    return [(counts[token] / total) * idf.get(token, 0.0) for token in vocabulary]


def cosine(left, right):
    dot = sum(a * b for a, b in zip(left, right))
    left_len = sqrt(sum(a * a for a in left))
    right_len = sqrt(sum(b * b for b in right))
    if left_len == 0 or right_len == 0:
        return 0.0
    return dot / (left_len * right_len)


def project_topics(tokens):
    token_set = set(tokens)
    return {
        topic: len(token_set.intersection(words))
        for topic, words in TOPIC_AXES.items()
    }


def local_search(query, documents, top_k=3):
    idf = build_idf(documents)
    vocabulary = sorted(idf)
    query_tokens = tokenize(query)
    query_vector = vectorize(query, vocabulary, idf)
    query_topic = project_topics(query_tokens)
    results = []
    for doc_id, text in documents.items():
        doc_tokens = tokenize(text)
        doc_vector = vectorize(text, vocabulary, idf)
        matched_terms = sorted(set(query_tokens).intersection(doc_tokens))
        missing_terms = sorted(set(query_tokens).difference(doc_tokens))
        score = cosine(query_vector, doc_vector)
        warning = None
        if not matched_terms:
            warning = "lexical gap: consider neural or hybrid retrieval"
        elif missing_terms:
            warning = "partial lexical match: inspect paraphrase risk"
        results.append({
            "id": doc_id,
            "score": round(score, 4),
            "matched_terms": matched_terms,
            "missing_terms": missing_terms,
            "topic_projection": project_topics(doc_tokens),
            "query_projection": query_topic,
            "warning": warning,
            "trace": f"{doc_id}: matched={matched_terms}, missing={missing_terms}, score={score:.4f}",
        })
    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    for result in local_search("api credential rotation", DOCUMENTS):
        print(result)
