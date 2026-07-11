"""Solution: score answer quality."""
ANSWER = {"claim_supported": True, "answers_question": True, "citation_supports_claim": False}
def score(item):
    checks = {
        "faithfulness": item["claim_supported"],
        "relevance": item["answers_question"],
        "citation_correctness": item["citation_supports_claim"],
    }
    return {"checks": checks, "score": sum(checks.values()), "gate": "pass" if all(checks.values()) else "review"}
if __name__ == "__main__":
    print(score(ANSWER))
