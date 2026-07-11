"""Chapter 19 exercise: build a small context pack."""

CHUNKS = [
    {"id": "S1", "text": "Enterprise refunds require VP approval after 30 days.", "authority": 3, "fresh": True, "access": True, "score": 0.92},
    {"id": "S2", "text": "Old refund rules allowed manager approval after 30 days.", "authority": 2, "fresh": False, "access": True, "score": 0.88},
    {"id": "S3", "text": "Internal finance note: do not disclose private margin targets.", "authority": 1, "fresh": True, "access": False, "score": 0.79},
    {"id": "S4", "text": "Enterprise plan exceptions must be cited from the addendum.", "authority": 3, "fresh": True, "access": True, "score": 0.84},
]


def build_context_pack(question, chunks, max_items=2):
    # TODO: drop inaccessible/stale chunks, order useful evidence, and return audit info.
    return {"question": question, "evidence": [], "dropped": []}


if __name__ == "__main__":
    print(build_context_pack("What is the enterprise refund exception?", CHUNKS))
