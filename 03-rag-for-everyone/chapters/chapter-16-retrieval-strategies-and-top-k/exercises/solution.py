QUERIES = [
    {"id": "faq", "type": "simple_faq", "risk": "low"},
    {"id": "refund", "type": "policy_exception", "risk": "high"},
    {"id": "sev1", "type": "troubleshooting", "risk": "high"},
]


def recommend_policy(query):
    if query["type"] == "simple_faq":
        return {
            "id": query["id"],
            "top_k": 3,
            "controls": ["metadata_filters", "dedupe"],
            "trace_note": "simple FAQ: keep k small to reduce noise",
        }
    if query["type"] == "policy_exception":
        return {
            "id": query["id"],
            "top_k": 10,
            "controls": ["metadata_filters", "query_rewrite", "parent_expansion", "rerank"],
            "trace_note": "policy exception: increase recall and preserve exact citations",
        }
    if query["type"] == "troubleshooting":
        return {
            "id": query["id"],
            "top_k": 8,
            "controls": ["metadata_filters", "multi_query", "dedupe", "ordered_context"],
            "trace_note": "troubleshooting: retrieve procedure, warnings, and nearby steps",
        }
    return {
        "id": query["id"],
        "top_k": 5,
        "controls": ["metadata_filters", "trace"],
        "trace_note": "default: use baseline policy and inspect misses",
    }


if __name__ == "__main__":
    for query in QUERIES:
        print(recommend_policy(query))
