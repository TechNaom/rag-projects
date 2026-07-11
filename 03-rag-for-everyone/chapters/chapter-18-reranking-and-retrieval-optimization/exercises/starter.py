CANDIDATES = [
    {"id": "c1", "parent": "p1", "first_rank": 1, "term_match": 1, "direct_answer": 0},
    {"id": "c2", "parent": "p2", "first_rank": 2, "term_match": 2, "direct_answer": 1},
    {"id": "c3", "parent": "p2", "first_rank": 3, "term_match": 2, "direct_answer": 0},
]


def rerank(candidates, final_k=2):
    # TODO: score, sort, dedupe by parent, and return final_k.
    raise NotImplementedError


if __name__ == "__main__":
    print(rerank(CANDIDATES))
