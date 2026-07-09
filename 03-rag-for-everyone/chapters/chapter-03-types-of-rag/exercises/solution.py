scenarios = [
    {
        "name": "Employee handbook FAQ",
        "rag_type": "naive or lightly advanced RAG",
        "reason": "One clean corpus and low-risk answers do not justify agents or graph logic.",
        "risk": "stale policy or missing citation",
        "eval": "source recall plus citation precision",
    },
    {
        "name": "Refund bot with country-specific policy",
        "rag_type": "advanced RAG",
        "reason": "Needs metadata filters, policy versioning, and possibly hybrid retrieval.",
        "risk": "wrong country or outdated policy",
        "eval": "region-filter accuracy and policy-version recall",
    },
    {
        "name": "Security runbook with weak retrieval retry",
        "rag_type": "corrective RAG",
        "reason": "Weak retrieval can create dangerous advice, so the system needs retry/refusal/escalation.",
        "risk": "unsupported security action",
        "eval": "unsafe-answer rejection rate",
    },
    {
        "name": "Research assistant over connected companies and people",
        "rag_type": "graph RAG",
        "reason": "The answer depends on relationships between entities, not isolated chunks only.",
        "risk": "missing relationship or wrong entity link",
        "eval": "entity relationship recall",
    },
    {
        "name": "Support assistant that can open tickets after retrieving docs",
        "rag_type": "agentic RAG",
        "reason": "The system retrieves knowledge and then performs a controlled workflow action.",
        "risk": "tool misuse or incorrect ticket creation",
        "eval": "tool-call precision and approval gate pass rate",
    },
]

for scenario in scenarios:
    print(scenario)
