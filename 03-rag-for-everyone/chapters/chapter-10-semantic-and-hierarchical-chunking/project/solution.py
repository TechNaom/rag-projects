CORPORA = [
    {
        "name": "short_faq",
        "recursive_pass_rate": 0.96,
        "topic_shift_score": 0.12,
        "parent_context_needed": False,
        "has_parent_ids": False,
        "access_sensitive": False,
    },
    {
        "name": "security_runbook",
        "recursive_pass_rate": 0.78,
        "topic_shift_score": 0.42,
        "parent_context_needed": True,
        "has_parent_ids": True,
        "access_sensitive": True,
    },
    {
        "name": "research_report",
        "recursive_pass_rate": 0.71,
        "topic_shift_score": 0.81,
        "parent_context_needed": True,
        "has_parent_ids": False,
        "access_sensitive": False,
    },
]


def strategy(corpus):
    if corpus["recursive_pass_rate"] >= 0.92 and not corpus["parent_context_needed"]:
        return "keep_recursive_baseline"
    if corpus["topic_shift_score"] >= 0.7 and corpus["parent_context_needed"]:
        return "semantic_plus_hierarchical"
    if corpus["parent_context_needed"]:
        return "hierarchical"
    if corpus["topic_shift_score"] >= 0.7:
        return "semantic"
    return "recursive_baseline_with_eval"


def first_risk(corpus, chosen):
    if chosen == "keep_recursive_baseline":
        return "over_engineering"
    if "hierarchical" in chosen and not corpus["has_parent_ids"]:
        return "missing_parent_ids"
    if corpus["access_sensitive"] and "hierarchical" in chosen:
        return "parent_child_access_filter_required"
    if chosen in {"semantic", "semantic_plus_hierarchical"} and corpus["topic_shift_score"] < 0.75:
        return "unstable_topic_boundaries"
    return "no_blocking_risk"


def next_action(risk):
    actions = {
        "over_engineering": "keep simple chunking and monitor golden-query performance",
        "missing_parent_ids": "add parent ids, child ids, heading path, and source positions before indexing",
        "parent_child_access_filter_required": "enforce access checks on child and expanded parent context",
        "unstable_topic_boundaries": "compare semantic boundaries against recursive baseline",
        "no_blocking_risk": "run child recall and parent expansion evals",
    }
    return actions[risk]


def metric(risk):
    metrics = {
        "over_engineering": "recursive_baseline_recall",
        "missing_parent_ids": "hierarchy_metadata_completeness",
        "parent_child_access_filter_required": "blocked_parent_context_rate",
        "unstable_topic_boundaries": "topic_boundary_precision",
        "no_blocking_risk": "child_recall_and_parent_precision",
    }
    return metrics[risk]


def plan_chunking(corpus):
    chosen = strategy(corpus)
    risk = first_risk(corpus, chosen)
    return {
        "name": corpus["name"],
        "strategy": chosen,
        "first_risk": risk,
        "next_action": next_action(risk),
        "first_metric_to_inspect": metric(risk),
    }


if __name__ == "__main__":
    for corpus in CORPORA:
        print(plan_chunking(corpus))
