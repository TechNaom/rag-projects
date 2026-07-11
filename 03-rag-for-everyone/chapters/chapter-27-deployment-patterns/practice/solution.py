"""Chapter 27 practice solution: check release readiness."""

DEPLOYMENT = {
    "auth": True,
    "secrets_managed": True,
    "health_check": True,
    "trace_logging": False,
    "eval_gate": True,
    "rollback": False,
}

REQUIRED = ["auth", "secrets_managed", "health_check", "trace_logging", "eval_gate", "rollback"]


def readiness(deployment):
    missing = [control for control in REQUIRED if not deployment.get(control)]
    ready = not missing
    if ready:
        next_action = "Release to canary and monitor latency, quality, and cost slices."
    elif "rollback" in missing:
        next_action = "Add rollback for code, prompt, config, and index versions before launch."
    else:
        next_action = f"Close missing control: {missing[0]}"
    return {"ready": ready, "missing": missing, "next_action": next_action}


if __name__ == "__main__":
    print(readiness(DEPLOYMENT))
