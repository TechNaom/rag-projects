DOCUMENTS = [
    {"id": "refund_policy", "type": "policy", "has_headings": True, "avg_section_tokens": 380, "table_count": 1},
    {"id": "plain_notes", "type": "notes", "has_headings": False, "avg_section_tokens": 120, "table_count": 0},
    {"id": "runbook", "type": "procedure", "has_headings": True, "avg_section_tokens": 900, "table_count": 0},
]


def recommend_chunker(document):
    if document["table_count"] > 0:
        return {
            "strategy": "recursive_with_table_handling",
            "reason": "tables need headers, rows, and captions preserved",
            "chunk_size": 450,
            "overlap": 80,
        }
    if document["has_headings"]:
        return {
            "strategy": "recursive",
            "reason": "document structure carries meaning",
            "chunk_size": 500,
            "overlap": 75,
        }
    return {
        "strategy": "fixed",
        "reason": "plain notes have weak structure and can start with a simple baseline",
        "chunk_size": 350,
        "overlap": 50,
    }


def first_risk(plan):
    if plan["overlap"] / plan["chunk_size"] > 0.25:
        return "overlap may create duplicate retrieval"
    if plan["chunk_size"] < 250:
        return "chunks may be too small to preserve context"
    if plan["chunk_size"] > 800:
        return "chunks may be too large and noisy"
    return "no obvious chunking risk"


if __name__ == "__main__":
    for doc in DOCUMENTS:
        plan = recommend_chunker(doc)
        plan["first_risk"] = first_risk(plan)
        print(doc["id"], plan)
