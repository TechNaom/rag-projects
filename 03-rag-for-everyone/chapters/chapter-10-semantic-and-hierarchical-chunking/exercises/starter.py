CORPORA = [
    {"name": "security_runbook", "topic_shifts": "medium", "needs_parent_context": True, "recursive_pass_rate": 0.81}
]


def recommend_strategy(corpus):
    return "todo"


if __name__ == "__main__":
    for corpus in CORPORA:
        print(recommend_strategy(corpus))
