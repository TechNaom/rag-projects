"""Chapter 26 practice starter: detect cost regressions."""

BASELINE = {"cost_usd": 0.006, "latency_ms": 900, "groundedness": 0.91}
CURRENT = {"cost_usd": 0.010, "latency_ms": 1260, "groundedness": 0.90}


def guardrail_report(baseline, current):
    """Return a status, flags, and recommendation."""
    # TODO: compare cost, latency, and groundedness.
    raise NotImplementedError("Build the guardrail report")


if __name__ == "__main__":
    print(guardrail_report(BASELINE, CURRENT))
