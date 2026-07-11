FAILURE_RULES = {
    "missing_exception": "lost_context",
    "repeated_neighbors": "overlap_noise",
    "old_policy": "stale_chunk",
    "keyword_only": "tiny_chunk",
    "broad_context": "giant_chunk",
    "many_topics": "mixed_topic",
}

FIXES = {
    "lost_context": ("add bounded parent or neighbor expansion", "citation_support"),
    "overlap_noise": ("reduce overlap and deduplicate retrieved chunks", "duplicate_rate"),
    "stale_chunk": ("filter by active version and rebuild the index", "stale_hit_rate"),
    "tiny_chunk": ("merge fragments into complete thought units", "answer_completeness"),
    "giant_chunk": ("split by task or heading and cite smaller evidence", "gold_chunk_rank"),
    "mixed_topic": ("split by semantic or heading boundary", "retrieval_precision"),
    "unknown": ("collect a richer trace before tuning", "trace_completeness"),
}


def diagnose_trace(trace):
    symptom = trace.get("symptom", "")
    label = FAILURE_RULES.get(symptom, "unknown")
    fix, metric = FIXES[label]
    return {
        "trace_id": trace.get("id", "unknown"),
        "failure_label": label,
        "fix_candidate": fix,
        "metric_to_watch": metric,
        "production_note": (
            f"Trace {trace.get('id', 'unknown')} is labeled {label}. "
            f"Try one controlled fix: {fix}. Prove it with {metric}."
        ),
    }


if __name__ == "__main__":
    sample = {
        "id": "refund-001",
        "symptom": "missing_exception",
        "gold_rank": 1,
        "duplicate_rate": 0.12,
        "stale_hit_rate": 0.0,
    }
    print(diagnose_trace(sample))
