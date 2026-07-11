"""Starter: access-aware RAG gateway."""
USER = {"tenant": "acme", "roles": {"finance"}}
CHUNKS = [{"id": "S1", "tenant": "acme", "roles": {"finance"}, "text": "Budget policy"}, {"id": "S2", "tenant": "acme", "roles": {"legal"}, "text": "Legal memo"}]
def filter_chunks(user, chunks):
    return {}
if __name__ == "__main__":
    print(filter_chunks(USER, CHUNKS))
