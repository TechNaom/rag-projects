"""Solution: failure triage."""
TRACE = {"gold_present": False, "source_exists": True, "parser_ok": True, "answer_unsupported": True}
def classify(trace):
    if not trace["source_exists"]:
        return {"root_cause": "corpus_gap", "owner": "content", "fix": "add authoritative source"}
    if not trace["parser_ok"]:
        return {"root_cause": "parsing_failure", "owner": "ingestion", "fix": "repair parser and replay"}
    if not trace["gold_present"]:
        return {"root_cause": "retrieval_recall_failure", "owner": "retrieval", "fix": "tune search, filters, chunking"}
    if trace["answer_unsupported"]:
        return {"root_cause": "generation_grounding_failure", "owner": "prompting", "fix": "strengthen grounded prompt and eval"}
    return {"root_cause": "no_failure", "owner": "none", "fix": "monitor"}
if __name__ == "__main__":
    print(classify(TRACE))
