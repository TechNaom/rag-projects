CORPORA = [
    {"name": "security_runbook", "topic_shifts": "medium", "needs_parent_context": True, "recursive_pass_rate": 0.81},
    {"name": "short_faq", "topic_shifts": "low", "needs_parent_context": False, "recursive_pass_rate": 0.96},
    {"name": "research_report", "topic_shifts": "high", "needs_parent_context": True, "recursive_pass_rate": 0.72},
]


def recommend_strategy(corpus):
    if corpus["recursive_pass_rate"] >= 0.92 and not corpus["needs_parent_context"]:
        return "recursive_baseline"
    if corpus["topic_shifts"] == "high" and corpus["needs_parent_context"]:
        return "semantic_plus_hierarchical"
    if corpus["needs_parent_context"]:
        return "hierarchical"
    if corpus["topic_shifts"] == "high":
        return "semantic"
    return "recursive_baseline"


def first_risk(strategy):
    risks = {
        "recursive_baseline": "over-engineering risk if advanced chunking is added without eval proof",
        "semantic": "topic detector quality can create unstable boundaries",
        "hierarchical": "parent expansion can flood the prompt if not capped",
        "semantic_plus_hierarchical": "topic boundaries and parent expansion both need separate evaluation",
    }
    return risks[strategy]


def first_metric(strategy):
    metrics = {
        "recursive_baseline": "recursive_baseline_recall",
        "semantic": "topic_boundary_precision",
        "hierarchical": "parent_expansion_precision",
        "semantic_plus_hierarchical": "child_recall_and_parent_expansion_precision",
    }
    return metrics[strategy]


if __name__ == "__main__":
    for corpus in CORPORA:
        strategy = recommend_strategy(corpus)
        print({"name": corpus["name"], "strategy": strategy, "first_risk": first_risk(strategy), "metric": first_metric(strategy)})
