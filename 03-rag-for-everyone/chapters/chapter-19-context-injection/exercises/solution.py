"""Chapter 19 exercise solution: build a small context pack."""

CHUNKS = [
    {"id": "S1", "text": "Enterprise refunds require VP approval after 30 days.", "authority": 3, "fresh": True, "access": True, "score": 0.92},
    {"id": "S2", "text": "Old refund rules allowed manager approval after 30 days.", "authority": 2, "fresh": False, "access": True, "score": 0.88},
    {"id": "S3", "text": "Internal finance note: do not disclose private margin targets.", "authority": 1, "fresh": True, "access": False, "score": 0.79},
    {"id": "S4", "text": "Enterprise plan exceptions must be cited from the addendum.", "authority": 3, "fresh": True, "access": True, "score": 0.84},
]


def drop_reason(chunk):
    if not chunk["access"]:
        return "access_denied"
    if not chunk["fresh"]:
        return "stale_version"
    return None


def build_context_pack(question, chunks, max_items=2):
    usable = []
    dropped = []
    for chunk in chunks:
        reason = drop_reason(chunk)
        if reason:
            dropped.append({"id": chunk["id"], "reason": reason})
        else:
            usable.append(chunk)

    ordered = sorted(usable, key=lambda c: (c["authority"], c["score"]), reverse=True)
    evidence = [
        {"citation": chunk["id"], "text": chunk["text"], "authority": chunk["authority"]}
        for chunk in ordered[:max_items]
    ]
    for chunk in ordered[max_items:]:
        dropped.append({"id": chunk["id"], "reason": "token_budget"})

    return {
        "question": question,
        "evidence": evidence,
        "rules": ["answer only from evidence", "cite every claim", "state if evidence is insufficient"],
        "dropped": dropped,
    }


if __name__ == "__main__":
    print(build_context_pack("What is the enterprise refund exception?", CHUNKS))
