"""Chapter 28 exercise solution: generate a capstone roadmap."""

GOALS = {
    "audience": "SRE team",
    "workflow": "incident response",
    "risk": "high",
    "corpus": ["runbooks", "postmortems", "service catalog"],
}

TRACKS = {
    "policy": "Enterprise Policy RAG",
    "incident": "Incident Runbook Copilot",
    "contract": "Legal Contract Explorer",
    "support": "Customer Support Knowledge Hub",
    "research": "Research Briefing Studio",
}


def choose_track(goals):
    text = " ".join([goals["audience"], goals["workflow"], " ".join(goals["corpus"])]).lower()
    if "incident" in text or "runbook" in text or "sre" in text:
        return TRACKS["incident"]
    if "policy" in text or "benefit" in text:
        return TRACKS["policy"]
    if "contract" in text or "legal" in text:
        return TRACKS["contract"]
    if "ticket" in text or "support" in text:
        return TRACKS["support"]
    return TRACKS["research"]


def generate_roadmap(goals):
    track = choose_track(goals)
    mvp_steps = [
        "Define user questions and success criteria",
        "Collect a public-safe or synthetic corpus",
        "Parse documents and attach metadata",
        "Chunk, embed, and build a versioned index",
        "Implement retrieval, reranking, and cited answer generation",
        "Create a small gold eval set for retrieval and answer support",
        "Build a simple UI or CLI demo with feedback capture",
    ]
    hardening_steps = [
        "Add access and freshness checks",
        "Add trace logging with latency, token, and citation fields",
        "Add release gates against baseline quality and cost",
        "Document rollback for prompts, code, config, and index versions",
    ]
    if goals["risk"] == "high":
        hardening_steps.insert(1, "Add refusal behavior for missing, stale, or conflicting evidence")

    evidence_artifacts = [
        "architecture diagram",
        "eval report with failure analysis",
        "trace examples",
        "demo script for happy, edge, and failure paths",
        "cost model",
        "deployment plan",
        "roadmap of next production improvements",
    ]
    return {
        "track": track,
        "mvp_steps": mvp_steps,
        "hardening_steps": hardening_steps,
        "evidence_artifacts": evidence_artifacts,
    }


if __name__ == "__main__":
    print(generate_roadmap(GOALS))
