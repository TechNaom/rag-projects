FAILURE_RULES = {
    "missing_exception": "lost_context",
    "repeated_neighbors": "overlap_noise",
    "old_policy": "stale_chunk",
    "keyword_only": "tiny_chunk",
    "broad_context": "giant_chunk",
    "many_topics": "mixed_topic",
}


def diagnose_trace(trace):
    """Return failure label, fix, metric, and short production note."""
    # TODO: inspect trace["symptom"] and return a useful diagnosis dict.
    raise NotImplementedError


if __name__ == "__main__":
    sample = {
        "id": "refund-001",
        "symptom": "missing_exception",
        "gold_rank": 1,
        "duplicate_rate": 0.12,
        "stale_hit_rate": 0.0,
    }
    print(diagnose_trace(sample))
