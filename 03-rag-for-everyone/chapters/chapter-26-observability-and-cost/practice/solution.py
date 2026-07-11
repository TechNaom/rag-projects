"""Chapter 26 practice solution: detect cost regressions."""

BASELINE = {"cost_usd": 0.006, "latency_ms": 900, "groundedness": 0.91}
CURRENT = {"cost_usd": 0.010, "latency_ms": 1260, "groundedness": 0.90}


def percent_change(old, new):
    return (new - old) / old if old else 0.0


def guardrail_report(baseline, current):
    cost_change = percent_change(baseline["cost_usd"], current["cost_usd"])
    latency_change = percent_change(baseline["latency_ms"], current["latency_ms"])
    groundedness_change = current["groundedness"] - baseline["groundedness"]
    flags = []
    if cost_change > 0.25:
        flags.append("cost_regression")
    if latency_change > 0.20:
        flags.append("latency_regression")
    if groundedness_change < -0.02:
        flags.append("quality_regression")

    status = "block_release" if "quality_regression" in flags or len(flags) >= 2 else "watch"
    recommendation = (
        "Block release and inspect context size, rerank pool, retries, and model route."
        if status == "block_release"
        else "Ship behind monitoring and compare tenant-level slices."
    )
    return {
        "status": status,
        "flags": flags,
        "cost_change_pct": round(cost_change * 100, 1),
        "latency_change_pct": round(latency_change * 100, 1),
        "groundedness_delta": round(groundedness_change, 3),
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    print(guardrail_report(BASELINE, CURRENT))
