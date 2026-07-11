"""Chapter 26 exercise starter: build a RAG trace cost report."""

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


def build_report(trace, prices):
    """Return latency, cost, risk, and recommendation fields."""
    # TODO: aggregate stage metrics and return a dictionary.
    raise NotImplementedError("Build the trace report")


if __name__ == "__main__":
    print(build_report(TRACE, TOKEN_PRICES))
