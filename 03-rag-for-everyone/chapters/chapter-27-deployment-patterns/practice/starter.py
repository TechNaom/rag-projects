"""Chapter 27 practice starter: check release readiness."""

DEPLOYMENT = {
    "auth": True,
    "secrets_managed": True,
    "health_check": True,
    "trace_logging": False,
    "eval_gate": True,
    "rollback": False,
}


def readiness(deployment):
    """Return ready, missing, and next_action."""
    # TODO: inspect the required controls.
    raise NotImplementedError("Check release readiness")


if __name__ == "__main__":
    print(readiness(DEPLOYMENT))
