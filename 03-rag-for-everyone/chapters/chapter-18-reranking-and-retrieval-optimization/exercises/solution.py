CANDIDATES = [
    {"id": "c1", "parent": "p1", "first_rank": 1, "term_match": 1, "direct_answer": 0},
    {"id": "c2", "parent": "p2", "first_rank": 2, "term_match": 2, "direct_answer": 1},
    {"id": "c3", "parent": "p2", "first_rank": 3, "term_match": 2, "direct_answer": 0},
]


def relevance(candidate):
    return candidate["term_match"] + candidate["direct_answer"] * 3 - candidate["first_rank"] * 0.05


def rerank(candidates, final_k=2):
    ranked = sorted(candidates, key=relevance, reverse=True)
    seen_parents = set()
    selected = []
    for item in ranked:
        if item["parent"] in seen_parents:
            continue
        seen_parents.add(item["parent"])
        selected.append({**item, "rerank_score": round(relevance(item), 3), "after_rank": len(selected) + 1})
        if len(selected) == final_k:
            break
    return selected


if __name__ == "__main__":
    print(rerank(CANDIDATES))
