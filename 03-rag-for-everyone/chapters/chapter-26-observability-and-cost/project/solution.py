"""Solution: RAG cost and trace monitor."""
TRACE = {"tokens_in": 3000, "tokens_out": 600, "latency_ms": {"retrieval": 80, "rerank": 240, "model": 2200}}
def summarize(trace):
    cost = trace["tokens_in"] * 0.000001 + trace["tokens_out"] * 0.000003
    slowest = max(trace["latency_ms"], key=trace["latency_ms"].get)
    recommendations = []
    if trace["tokens_in"] > 2500:
        recommendations.append("compress_context_or_reduce_final_k")
    if trace["latency_ms"].get("rerank", 0) > 200:
        recommendations.append("route_reranking_to_high_value_queries")
    return {"estimated_cost": round(cost, 6), "total_latency_ms": sum(trace["latency_ms"].values()), "slowest_stage": slowest, "recommendations": recommendations}
if __name__ == "__main__":
    print(summarize(TRACE))
