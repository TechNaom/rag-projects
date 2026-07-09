SCENARIOS = [
    {
        "name": "Employee handbook FAQ",
        "risk": "low",
        "corpus_complexity": "simple",
        "workflow": "answer",
        "source_formats": ["markdown"],
    },
    {
        "name": "Security runbook assistant",
        "risk": "high",
        "corpus_complexity": "medium",
        "workflow": "answer_or_escalate",
        "source_formats": ["markdown"],
    },
    {
        "name": "Company relationship research assistant",
        "risk": "medium",
        "corpus_complexity": "connected",
        "workflow": "answer",
        "source_formats": ["html", "pdf"],
    },
    {
        "name": "Support ticket assistant",
        "risk": "medium",
        "corpus_complexity": "medium",
        "workflow": "action",
        "source_formats": ["markdown", "api"],
    },
    {
        "name": "Product knowledge assistant",
        "risk": "medium",
        "corpus_complexity": "multimodal",
        "workflow": "answer",
        "source_formats": ["pdf", "slides", "images", "tables"],
    },
]


def recommend_rag_type(item):
    if item["corpus_complexity"] == "multimodal":
        return "multimodal RAG"
    if item["corpus_complexity"] == "connected":
        return "graph RAG"
    if item["workflow"] == "action":
        return "agentic RAG with approval gates"
    if item["risk"] == "high":
        return "corrective RAG"
    if item["corpus_complexity"] == "medium":
        return "advanced RAG"
    return "naive RAG"


def risks_for(rag_type):
    risks = {
        "naive RAG": ["stale source", "missing citation"],
        "advanced RAG": ["metadata errors", "reranking latency"],
        "corrective RAG": ["false confidence signal", "over-refusal"],
        "graph RAG": ["wrong entity resolution", "missing relationship"],
        "agentic RAG with approval gates": ["tool misuse", "approval bypass"],
        "multimodal RAG": ["format extraction error", "table/image grounding failure"],
    }
    return risks.get(rag_type, ["unknown architecture risk"])


def evals_for(rag_type):
    evals = {
        "naive RAG": ["Recall@5", "citation precision"],
        "advanced RAG": ["filter accuracy", "reranked source recall"],
        "corrective RAG": ["unsafe-answer rejection rate", "escalation correctness"],
        "graph RAG": ["entity resolution accuracy", "relationship recall"],
        "agentic RAG with approval gates": ["tool-call precision", "approval-gate pass rate"],
        "multimodal RAG": ["format-specific grounding", "cross-modal citation accuracy"],
    }
    return evals.get(rag_type, ["manual review"])


def decision_record(item):
    rag_type = recommend_rag_type(item)
    return {
        "scenario": item["name"],
        "selected_rag_type": rag_type,
        "why": f"Risk={item['risk']}, corpus={item['corpus_complexity']}, workflow={item['workflow']}.",
        "production_risks": risks_for(rag_type),
        "evals": evals_for(rag_type),
        "observability": ["selected_path", "retrieved_sources", "answer_status", "latency_ms", "cost_estimate"],
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(decision_record(scenario))
