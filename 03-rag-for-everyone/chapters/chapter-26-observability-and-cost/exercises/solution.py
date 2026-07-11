"""Chapter 26 exercise solution: build a RAG trace cost report."""

TRACE = {
    "trace_id": "tr-1042",
    "route": "policy_lookup",
    "events": [
        {"stage": "rewrite", "latency_ms": 42, "prompt_tokens": 120, "completion_tokens": 20},
        {"stage": "retrieve", "latency_ms": 88, "prompt_tokens": 0, "completion_tokens": 0, "results": 8},
        {"stage": "rerank", "latency_ms": 130, "prompt_tokens": 520, "completion_tokens": 4},
        {"stage": "answer", "latency_ms": 920, "prompt_tokens": 1700, "completion_tokens": 260},
    ],
    "quality": {"citations": 3, "unsupported_claims": 1, "user_rating": 3},
}

TOKEN_PRICES = {"prompt": 0.000002, "completion": 0.000006}


def event_cost(event, prices):
    return (
        event.get("prompt_tokens", 0) * prices["prompt"]
        + event.get("completion_tokens", 0) * prices["completion"]
    )


def build_report(trace, prices):
    stage_rows = []
    total_latency = 0
    total_cost = 0.0
    for event in trace["events"]:
        cost = event_cost(event, prices)
        total_latency += event["latency_ms"]
        total_cost += cost
        stage_rows.append(
            {
                "stage": event["stage"],
                "latency_ms": event["latency_ms"],
                "cost_usd": round(cost, 6),
            }
        )

    slowest = max(stage_rows, key=lambda row: row["latency_ms"])
    expensive = max(stage_rows, key=lambda row: row["cost_usd"])
    quality = trace["quality"]
    risks = []
    if quality["unsupported_claims"]:
        risks.append("unsupported_claims")
    if quality["citations"] == 0:
        risks.append("missing_citations")
    if any(event.get("results") == 0 for event in trace["events"]):
        risks.append("empty_retrieval")

    if slowest["stage"] == "answer" and expensive["stage"] == "answer":
        recommendation = "Trim context, cache stable policy answers, and route simple lookups to a cheaper model."
    elif "unsupported_claims" in risks:
        recommendation = "Tighten citation checks before optimizing spend."
    else:
        recommendation = "Track this route against the baseline and watch tail latency."

    return {
        "trace_id": trace["trace_id"],
        "route": trace["route"],
        "total_latency_ms": total_latency,
        "total_cost_usd": round(total_cost, 6),
        "slowest_stage": slowest["stage"],
        "most_expensive_stage": expensive["stage"],
        "risks": risks,
        "recommendation": recommendation,
        "stages": stage_rows,
    }


if __name__ == "__main__":
    print(build_report(TRACE, TOKEN_PRICES))
