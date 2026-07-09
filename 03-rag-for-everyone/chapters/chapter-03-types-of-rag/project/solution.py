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


def advantages_for(rag_type):
    advantages = {
        "naive RAG": ["fast to build", "low cost", "easy to debug"],
        "advanced RAG": ["better precision", "metadata-aware", "stronger grounding"],
        "corrective RAG": ["safer under weak evidence", "supports refusal and escalation"],
        "graph RAG": ["relationship-aware", "good for multi-hop entity questions"],
        "agentic RAG with approval gates": ["handles workflows", "can use tools with control"],
        "multimodal RAG": ["works across images, tables, slides, and text"],
    }
    return advantages.get(rag_type, ["depends on implementation"])


def disadvantages_for(rag_type):
    disadvantages = {
        "naive RAG": ["weak for multi-hop", "sensitive to chunk quality"],
        "advanced RAG": ["more tuning", "more latency"],
        "corrective RAG": ["can over-refuse", "thresholds are hard to tune"],
        "graph RAG": ["entity resolution complexity", "graph freshness burden"],
        "agentic RAG with approval gates": ["tool risk", "harder to test", "higher cost"],
        "multimodal RAG": ["harder extraction", "harder citation and evaluation"],
    }
    return disadvantages.get(rag_type, ["depends on implementation"])


def engineering_profile_for(rag_type):
    profiles = {
        "naive RAG": {
            "scale": "low to medium",
            "accuracy": "good when the right chunk is retrieved",
            "consistency": "medium; drops with conflicting chunks",
            "latency_cost": "low",
        },
        "advanced RAG": {
            "scale": "medium to high",
            "accuracy": "high with strong metadata and reranking",
            "consistency": "high when filters and index versions are stable",
            "latency_cost": "medium",
        },
        "corrective RAG": {
            "scale": "medium",
            "accuracy": "high safety; lower unsupported-answer rate",
            "consistency": "depends on confidence thresholds",
            "latency_cost": "medium to high",
        },
        "graph RAG": {
            "scale": "high if graph pipeline is maintained",
            "accuracy": "high for connected knowledge when entity links are correct",
            "consistency": "depends on graph freshness and entity resolution",
            "latency_cost": "high",
        },
        "agentic RAG with approval gates": {
            "scale": "medium; requires workflow controls",
            "accuracy": "task-oriented, not just answer-oriented",
            "consistency": "harder because plans can vary",
            "latency_cost": "high",
        },
        "multimodal RAG": {
            "scale": "high pipeline complexity",
            "accuracy": "depends on extraction and multimodal grounding",
            "consistency": "harder across formats",
            "latency_cost": "high",
        },
    }
    return profiles.get(
        rag_type,
        {"scale": "unknown", "accuracy": "unknown", "consistency": "unknown", "latency_cost": "unknown"},
    )


def client_fit_for(rag_type):
    fit = {
        "naive RAG": ["internal FAQ", "small docs portal", "training assistant"],
        "advanced RAG": ["customer support", "HR policy", "developer docs", "finance policy"],
        "corrective RAG": ["security", "legal triage", "compliance", "healthcare policy"],
        "graph RAG": ["research intelligence", "fraud", "supply-chain risk", "legal discovery"],
        "agentic RAG with approval gates": ["support operations", "DevOps", "ticketing", "workflow copilots"],
        "multimodal RAG": ["product support", "healthcare", "manufacturing", "education"],
    }
    return fit.get(rag_type, ["custom client fit"])


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
        "what_it_is": f"{rag_type} selected for this scenario shape.",
        "client_fit": client_fit_for(rag_type),
        "advantages": advantages_for(rag_type),
        "disadvantages": disadvantages_for(rag_type),
        "production_risks": risks_for(rag_type),
        "engineering_profile": engineering_profile_for(rag_type),
        "evals": evals_for(rag_type),
        "observability": ["selected_path", "retrieved_sources", "answer_status", "latency_ms", "cost_estimate"],
    }


if __name__ == "__main__":
    for scenario in SCENARIOS:
        print(decision_record(scenario))
