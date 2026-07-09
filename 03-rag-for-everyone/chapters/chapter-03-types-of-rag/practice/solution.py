decision = {
    "scenario": "Security runbook assistant",
    "selected_rag_type": "corrective RAG",
    "why_not_simpler": "Naive RAG may confidently answer from weak or partial evidence.",
    "required_capability": "detect weak retrieval and retry, refuse, or escalate",
    "production_risk": "unsafe incident response guidance",
    "eval": "unsafe-answer rejection rate plus paired-source recall",
    "observability_signal": "retrieval confidence, refusal reason, escalation rate",
}

print(decision)
