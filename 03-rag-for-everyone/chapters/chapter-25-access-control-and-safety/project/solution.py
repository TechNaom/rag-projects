"""Solution: access-aware RAG gateway."""
USER = {"tenant": "acme", "roles": {"finance"}}
CHUNKS = [{"id": "S1", "tenant": "acme", "roles": {"finance"}, "text": "Budget policy"}, {"id": "S2", "tenant": "acme", "roles": {"legal"}, "text": "Legal memo"}]
def filter_chunks(user, chunks):
    allowed, denied = [], []
    for chunk in chunks:
        if chunk["tenant"] != user["tenant"]:
            denied.append({"id": chunk["id"], "reason": "tenant_mismatch"})
        elif not (chunk["roles"] & user["roles"]):
            denied.append({"id": chunk["id"], "reason": "role_denied"})
        else:
            allowed.append(chunk)
    return {"allowed": allowed, "audit": {"policy": "rbac-v1", "denied": denied, "allowed_count": len(allowed)}}
if __name__ == "__main__":
    print(filter_chunks(USER, CHUNKS))
