"""Solution: capstone planner."""
TRACKS = {
    "policy_intelligence_desk": ["corpus", "metadata_rbac", "hybrid_retrieval", "citations", "audit_logs"],
    "incident_runbook_copilot": ["service_catalog", "severity_routing", "runbook_retrieval", "step_answers", "post_incident_evals"],
    "research_knowledge_studio": ["evidence_board", "claim_checks", "source_compare", "brief_export", "citation_review"],
}
def backlog(track):
    core = ["architecture_diagram", "ingestion_pipeline", "chunking", "indexing", "eval_suite", "observability", "deployment_plan"]
    return {"track": track, "milestones": core + TRACKS.get(track, []), "review_gates": ["retrieval_metrics", "answer_quality", "safety", "cost", "demo_readiness"]}
if __name__ == "__main__":
    print(backlog("policy_intelligence_desk"))
