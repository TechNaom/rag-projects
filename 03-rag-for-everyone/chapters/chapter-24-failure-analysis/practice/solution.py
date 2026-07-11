"""Solution: choose fix order."""
FAILURE = {"missing_source": False, "gold_rank": 22, "final_k": 5}
def recommend(failure):
    if failure["missing_source"]:
        return "add_authoritative_source"
    if failure["gold_rank"] > failure["final_k"]:
        return "improve_ranking_or_reranking"
    return "inspect_prompt_and_citations"
if __name__ == "__main__":
    print(recommend(FAILURE))
