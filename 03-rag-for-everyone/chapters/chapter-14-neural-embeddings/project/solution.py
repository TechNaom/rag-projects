CANDIDATES = [
    {"name": "local-open", "recall_at_5": 0.76, "citation": 0.70, "latency": 40, "cost": 1, "privacy": "approved", "migration": "medium"},
    {"name": "managed-api", "recall_at_5": 0.88, "citation": 0.82, "latency": 135, "cost": 3, "privacy": "review", "migration": "medium"},
    {"name": "domain-private", "recall_at_5": 0.92, "citation": 0.86, "latency": 210, "cost": 5, "privacy": "approved", "migration": "high"},
]

MIGRATION_PENALTY = {"low": 2, "medium": 6, "high": 11}
PRIVACY_PENALTY = {"approved": 0, "review": 9, "blocked": 100}


def production_score(candidate):
    quality = candidate["recall_at_5"] * 50 + candidate["citation"] * 30
    latency_penalty = candidate["latency"] / 60
    cost_penalty = candidate["cost"] * 4
    return quality - latency_penalty - cost_penalty - MIGRATION_PENALTY[candidate["migration"]] - PRIVACY_PENALTY[candidate["privacy"]]


def release_decision(candidate):
    if candidate["privacy"] == "blocked":
        return "blocked"
    if candidate["privacy"] == "review":
        return "conditional: privacy approval required"
    if candidate["migration"] == "high":
        return "conditional: parallel index and rollback required"
    return "ready for controlled rollout"


def build_selection_board(candidates):
    board = []
    for candidate in candidates:
        score = production_score(candidate)
        decision = release_decision(candidate)
        board.append({
            **candidate,
            "score": round(score, 2),
            "release_decision": decision,
            "migration_note": "build a new index version, shadow test, then roll out gradually",
            "review_sentence": (
                f"{candidate['name']} scored {score:.2f}. "
                f"Decision: {decision}. Validate Recall@5, citation support, privacy, and rollback."
            ),
        })
    return sorted(board, key=lambda item: item["score"], reverse=True)


if __name__ == "__main__":
    for item in build_selection_board(CANDIDATES):
        print(item)
