"""Solution: answer quality scorer."""
CASE = {"evidence": "VP approval is required after 30 days.", "answer": "VP approval is required after 30 days [S1].", "citations": ["S1"], "risk": "high"}
def score_answer(case):
    answer = case["answer"].lower()
    evidence = case["evidence"].lower()
    citation_ok = all(f"[{c.lower()}]" in answer for c in case["citations"])
    faithful = "vp approval" in answer and "vp approval" in evidence and "manager approval" not in answer
    relevant = "approval" in answer and "30 days" in answer
    score = sum([citation_ok, faithful, relevant])
    gate = "pass" if score == 3 else ("block" if case["risk"] == "high" else "warn")
    return {"citation_ok": citation_ok, "faithful": faithful, "relevant": relevant, "score": score, "release_gate": gate}
if __name__ == "__main__":
    print(score_answer(CASE))
