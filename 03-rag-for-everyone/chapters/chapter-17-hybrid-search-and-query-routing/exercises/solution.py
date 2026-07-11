import re

QUERIES = [
    {"id": "q1", "text": "How do I regenerate credentials?", "risk": "low"},
    {"id": "q2", "text": "AZ-4032-B after key rotation", "risk": "medium"},
    {"id": "q3", "text": "Policy 7.3 termination clause for EU employees", "risk": "high"},
]

EXACT_PATTERNS = [r"\b[A-Z]{2,}-\d{3,}-[A-Z]\b", r"\bSKU-\d+\b", r"\bPolicy\s+\d+(\.\d+)?\b"]


def has_exact_signal(text):
    return any(re.search(pattern, text) for pattern in EXACT_PATTERNS)


def route_query(query):
    text = query["text"]
    exact = has_exact_signal(text)
    semantic = len(text.split()) >= 4
    if query["risk"] == "high":
        route = "high_risk_hybrid"
        reason = "high-risk domain needs exact protection, semantic coverage, strict filters, and citations"
        metric = "high_risk_route_accuracy"
    elif exact and semantic:
        route = "hybrid"
        reason = "query has exact term plus semantic troubleshooting intent"
        metric = "exact_term_recall"
    elif exact:
        route = "sparse"
        reason = "query depends on exact lexical signal"
        metric = "exact_term_recall"
    else:
        route = "dense"
        reason = "query is paraphrase or concept oriented"
        metric = "Recall@k"
    return {"id": query["id"], "route": route, "reason": reason, "metric": metric}


if __name__ == "__main__":
    for query in QUERIES:
        print(route_query(query))
