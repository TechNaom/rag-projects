"""Solution: classify a failure trace."""
TRACE = {"source_exists": True, "parser_ok": True, "gold_in_candidates": False, "answer_unsupported": True}
def classify(trace):
    if not trace["source_exists"]:
        return {"root": "corpus_gap", "owner": "content"}
    if not trace["parser_ok"]:
        return {"root": "parsing_failure", "owner": "ingestion"}
    if not trace["gold_in_candidates"]:
        return {"root": "retrieval_recall_failure", "owner": "retrieval"}
    if trace["answer_unsupported"]:
        return {"root": "generation_grounding_failure", "owner": "prompting"}
    return {"root": "healthy", "owner": "none"}
if __name__ == "__main__":
    print(classify(TRACE))
