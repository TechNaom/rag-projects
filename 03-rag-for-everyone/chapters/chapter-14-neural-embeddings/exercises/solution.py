CANDIDATES = [
    {"name": "local-small", "recall": 0.72, "latency_ms": 35, "cost": 1, "privacy": 5, "migration": 2},
    {"name": "managed-general", "recall": 0.86, "latency_ms": 120, "cost": 3, "privacy": 3, "migration": 3},
    {"name": "domain-large", "recall": 0.91, "latency_ms": 240, "cost": 5, "privacy": 4, "migration": 4},
]


def score(candidate):
    latency_penalty = candidate["latency_ms"] / 250
    return (
        candidate["recall"] * 60
        + candidate["privacy"] * 6
        - candidate["cost"] * 4
        - candidate["migration"] * 3
        - latency_penalty * 8
    )


def rank_candidates(candidates):
    ranked = []
    for candidate in candidates:
        production_score = score(candidate)
        ranked.append({
            **candidate,
            "production_score": round(production_score, 2),
            "release_note": (
                f"{candidate['name']} scored {production_score:.2f}. "
                "Validate Recall@k, citation support, privacy approval, and re-indexing plan."
            ),
        })
    return sorted(ranked, key=lambda item: item["production_score"], reverse=True)


if __name__ == "__main__":
    for item in rank_candidates(CANDIDATES):
        print(item)
