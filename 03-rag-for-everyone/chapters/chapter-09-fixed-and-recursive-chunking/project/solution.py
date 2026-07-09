CORPORA = [
    {
        "name": "refund_policy",
        "document_type": "policy",
        "has_headings": True,
        "has_tables": True,
        "avg_chunk_tokens": 520,
        "overlap_tokens": 80,
        "boundary_break_rate": 0.04,
        "metadata_complete": True,
    },
    {
        "name": "support_notes",
        "document_type": "notes",
        "has_headings": False,
        "has_tables": False,
        "avg_chunk_tokens": 160,
        "overlap_tokens": 90,
        "boundary_break_rate": 0.18,
        "metadata_complete": True,
    },
    {
        "name": "runbook",
        "document_type": "procedure",
        "has_headings": True,
        "has_tables": False,
        "avg_chunk_tokens": 920,
        "overlap_tokens": 120,
        "boundary_break_rate": 0.22,
        "metadata_complete": False,
    },
]


def strategy(corpus):
    if corpus["has_tables"]:
        return "table-aware recursive"
    if corpus["has_headings"]:
        return "recursive"
    return "fixed baseline"


def first_risk(corpus):
    overlap_ratio = corpus["overlap_tokens"] / max(corpus["avg_chunk_tokens"], 1)
    if not corpus["metadata_complete"]:
        return "missing chunk metadata"
    if corpus["avg_chunk_tokens"] < 220:
        return "chunks may be too small"
    if corpus["avg_chunk_tokens"] > 800:
        return "chunks may be too large"
    if overlap_ratio > 0.35:
        return "overlap may cause duplicate retrieval"
    if corpus["boundary_break_rate"] > 0.15:
        return "boundary break rate is high"
    return "no blocking chunking risk"


def next_action(risk):
    actions = {
        "missing chunk metadata": "add source id, chunk id, heading path, position, access, and chunker version",
        "chunks may be too small": "increase chunk size or prepend heading and local context",
        "chunks may be too large": "split by headings, procedure steps, or paragraphs",
        "overlap may cause duplicate retrieval": "reduce overlap and deduplicate near-identical retrieved chunks",
        "boundary break rate is high": "switch to recursive splitting and test golden queries",
        "no blocking chunking risk": "run retrieval evals and compare against baseline",
    }
    return actions[risk]


def first_metric(risk):
    metrics = {
        "missing chunk metadata": "metadata_completeness",
        "chunks may be too small": "lost_context_rate",
        "chunks may be too large": "chunk_noise_score",
        "overlap may cause duplicate retrieval": "duplicate_retrieval_rate",
        "boundary break rate is high": "boundary_break_rate",
        "no blocking chunking risk": "Recall@5",
    }
    return metrics[risk]


def evaluate_corpus(corpus):
    risk = first_risk(corpus)
    return {
        "name": corpus["name"],
        "recommended_strategy": strategy(corpus),
        "first_risk": risk,
        "next_action": next_action(risk),
        "first_metric_to_inspect": first_metric(risk),
    }


if __name__ == "__main__":
    for corpus in CORPORA:
        print(evaluate_corpus(corpus))
