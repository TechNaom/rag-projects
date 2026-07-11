"""Starter: RAG cost and trace monitor."""
TRACE = {"tokens_in": 3000, "tokens_out": 600, "latency_ms": {"retrieval": 80, "rerank": 240, "model": 2200}}
def summarize(trace):
    return {}
if __name__ == "__main__":
    print(summarize(TRACE))
