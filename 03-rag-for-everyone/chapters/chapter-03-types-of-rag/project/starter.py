scenario = {
    "name": "Security runbook assistant",
    "risk": "high",  # low, medium, high
    "corpus_complexity": "medium",  # simple, medium, connected, multimodal
    "workflow": "answer_or_escalate",  # answer, answer_or_escalate, action
    "source_formats": ["markdown"],
}


def recommend_rag_type(item):
    # TODO: return selected RAG type
    return ""


def decision_record(item):
    return {
        "scenario": item["name"],
        "selected_rag_type": recommend_rag_type(item),
        "why": "",
        "production_risks": [],
        "evals": [],
        "observability": [],
    }


print(decision_record(scenario))
