CANDIDATES = [
    {"name": "local-small", "recall": 0.72, "latency_ms": 35, "cost": 1, "privacy": 5, "migration": 2},
    {"name": "managed-general", "recall": 0.86, "latency_ms": 120, "cost": 3, "privacy": 3, "migration": 3},
    {"name": "domain-large", "recall": 0.91, "latency_ms": 240, "cost": 5, "privacy": 4, "migration": 4},
]


def rank_candidates(candidates):
    # TODO: return candidates sorted by production score.
    raise NotImplementedError


if __name__ == "__main__":
    for item in rank_candidates(CANDIDATES):
        print(item)
