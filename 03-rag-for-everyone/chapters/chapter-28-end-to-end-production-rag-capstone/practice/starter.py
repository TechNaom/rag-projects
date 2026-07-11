"""Chapter 28 practice starter: score capstone readiness."""

PLAN = {
    "saved_workflows": 2,
    "has_eval_set": True,
    "has_tracing": True,
    "has_access_model": False,
    "has_demo_script": True,
    "scope_items": 14,
}


def score_plan(plan):
    """Return score, strengths, risks, and recommendation."""
    # TODO: score revisit value, evidence, and finishability.
    raise NotImplementedError("Score the capstone plan")


if __name__ == "__main__":
    print(score_plan(PLAN))
