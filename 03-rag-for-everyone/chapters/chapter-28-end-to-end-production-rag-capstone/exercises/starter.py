"""Chapter 28 exercise starter: generate a capstone roadmap."""

GOALS = {
    "audience": "SRE team",
    "workflow": "incident response",
    "risk": "high",
    "corpus": ["runbooks", "postmortems", "service catalog"],
}


def generate_roadmap(goals):
    """Return track, mvp_steps, hardening_steps, and evidence_artifacts."""
    # TODO: map the goals to a capstone track and roadmap.
    raise NotImplementedError("Generate the capstone roadmap")


if __name__ == "__main__":
    print(generate_roadmap(GOALS))
