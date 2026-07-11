"""Starter: answer quality scorer."""
CASE = {"evidence": "VP approval is required after 30 days.", "answer": "VP approval is required after 30 days [S1].", "citations": ["S1"], "risk": "high"}
def score_answer(case):
    return {}
if __name__ == "__main__":
    print(score_answer(CASE))
