"""
cost_tracker.py
---------------
Per-tenant cost and latency accounting for the copilot.

In RAG-as-a-service you are running shared infrastructure for many tenants, so
"what did each tenant cost us and how fast were they served?" is a first-class
operational question — it drives billing, capacity planning, and SLA reporting.
This module wraps each query with a timer and a token estimate, accumulates
per-tenant totals in a small local JSON file, and can print a dashboard.

TOKEN ESTIMATE IS AN APPROXIMATION. We do not call a real tokenizer here; we
estimate tokens as words * 1.3, a common rule of thumb (English text averages
roughly 1.3 tokens per word for GPT/Llama-family tokenizers). For real billing
you would count tokens with the actual model's tokenizer, or read the usage
figures the provider returns in its API response. The structure — measure per
call, attribute to a tenant, accumulate — is exactly what a production meter
does; only the token source changes.
"""

import json
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COST_LOG_PATH = PROJECT_ROOT / "data" / "cost_log.json"

# Illustrative price, in US dollars per 1,000 tokens, for the dashboard's cost
# column. Set to a representative hosted-inference figure; change it to match
# whatever provider/model you actually bill against.
USD_PER_1K_TOKENS = 0.0006

TOKENS_PER_WORD = 1.3  # rough approximation; see module docstring


def estimate_tokens(text: str) -> int:
    """Approximate token count from word count (words * 1.3). Not a real tokenizer."""
    if not text:
        return 0
    return int(round(len(text.split()) * TOKENS_PER_WORD))


def _empty_tenant_record() -> Dict:
    return {
        "queries": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "total_latency_s": 0.0,
    }


def _load_log(path: Path = COST_LOG_PATH) -> Dict[str, Dict]:
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_log(log: Dict[str, Dict], path: Path = COST_LOG_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, sort_keys=True)


def record_query(
    tenant_id: str,
    prompt_text: str,
    completion_text: str,
    latency_s: float,
    path: Path = COST_LOG_PATH,
) -> Dict:
    """Attribute one query's tokens + latency to a tenant and persist the running total."""
    log = _load_log(path)
    rec = log.get(tenant_id, _empty_tenant_record())

    prompt_tokens = estimate_tokens(prompt_text)
    completion_tokens = estimate_tokens(completion_text)

    rec["queries"] += 1
    rec["prompt_tokens"] += prompt_tokens
    rec["completion_tokens"] += completion_tokens
    rec["total_tokens"] += prompt_tokens + completion_tokens
    rec["total_latency_s"] = round(rec["total_latency_s"] + latency_s, 4)

    log[tenant_id] = rec
    _save_log(log, path)
    return rec


@contextmanager
def track(tenant_id: str, prompt_text: str, path: Path = COST_LOG_PATH):
    """Context manager that times a block and records the tenant's usage.

    Usage:
        with track(tenant_id, prompt_text) as result:
            answer = do_work()
            result["completion_text"] = answer

    The block sets `result["completion_text"]` so the tracker can estimate the
    completion tokens; latency is measured automatically around the block.
    """
    start = time.perf_counter()
    result: Dict = {"completion_text": ""}
    try:
        yield result
    finally:
        latency_s = time.perf_counter() - start
        record_query(
            tenant_id=tenant_id,
            prompt_text=prompt_text,
            completion_text=result.get("completion_text", ""),
            latency_s=latency_s,
            path=path,
        )


def reset(path: Path = COST_LOG_PATH) -> None:
    """Clear the accumulated cost log (used by tests and for a fresh dashboard)."""
    if path.exists():
        path.unlink()


def summary(path: Path = COST_LOG_PATH) -> Dict[str, Dict]:
    return _load_log(path)


def format_dashboard(path: Path = COST_LOG_PATH) -> str:
    """Return a printable per-tenant cost/latency table."""
    log = _load_log(path)
    lines = []
    header = (
        f"{'tenant':22s} {'queries':>8s} {'tokens':>10s} "
        f"{'avg latency':>12s} {'est. cost':>11s}"
    )
    bar = "=" * len(header)
    lines.append(bar)
    lines.append("PER-TENANT COST & LATENCY DASHBOARD")
    lines.append(bar)
    lines.append(header)
    lines.append("-" * len(header))

    if not log:
        lines.append("(no queries recorded yet)")
        lines.append(bar)
        return "\n".join(lines)

    tot_q = tot_tok = 0
    tot_lat = 0.0
    tot_cost = 0.0
    for tenant_id in sorted(log):
        rec = log[tenant_id]
        q = rec["queries"]
        tok = rec["total_tokens"]
        avg_lat = (rec["total_latency_s"] / q) if q else 0.0
        cost = tok / 1000.0 * USD_PER_1K_TOKENS
        tot_q += q
        tot_tok += tok
        tot_lat += rec["total_latency_s"]
        tot_cost += cost
        lines.append(
            f"{tenant_id:22s} {q:8d} {tok:10d} {avg_lat:11.4f}s ${cost:10.5f}"
        )

    lines.append("-" * len(header))
    overall_avg_lat = (tot_lat / tot_q) if tot_q else 0.0
    lines.append(
        f"{'TOTAL':22s} {tot_q:8d} {tot_tok:10d} {overall_avg_lat:11.4f}s ${tot_cost:10.5f}"
    )
    lines.append(bar)
    lines.append(
        f"note: token counts are approximate (words * {TOKENS_PER_WORD}); "
        f"cost assumes ${USD_PER_1K_TOKENS}/1K tokens."
    )
    return "\n".join(lines)


def print_dashboard(path: Path = COST_LOG_PATH) -> None:
    print(format_dashboard(path))


if __name__ == "__main__":
    print_dashboard()
