"""Chapter 28 practice solution: score capstone readiness."""

PLAN = {
    "saved_workflows": 2,
    "has_eval_set": True,
    "has_tracing": True,
    "has_access_model": False,
    "has_demo_script": True,
    "scope_items": 14,
}


def score_plan(plan):
    score = 0
    strengths = []
    risks = []
    if plan["saved_workflows"] >= 2:
        score += 25
        strengths.append("high_revisit_value")
    else:
        risks.append("single_use_demo")
    for field, label in [
        ("has_eval_set", "evaluation_evidence"),
        ("has_tracing", "operability_evidence"),
        ("has_access_model", "trust_boundary"),
        ("has_demo_script", "reviewer_demo_path"),
    ]:
        if plan[field]:
            score += 15
            strengths.append(label)
        else:
            risks.append(f"missing_{label}")
    if plan["scope_items"] <= 10:
        score += 15
        strengths.append("finishable_scope")
    else:
        risks.append("scope_too_broad")

    recommendation = (
        "Proceed after trimming scope and adding the missing access/trust model."
        if score >= 70
        else "Narrow the track and add evaluation, tracing, and demo evidence before building."
    )
    return {
        "score": score,
        "strengths": strengths,
        "risks": risks,
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    print(score_plan(PLAN))
