"""Solution: access filter."""
USER = {"tenant": "t1", "roles": {"support"}}
CHUNK = {"tenant": "t1", "roles": {"legal"}}
def allowed(user, chunk):
    return user["tenant"] == chunk["tenant"] and bool(user["roles"] & chunk["roles"])
if __name__ == "__main__":
    print(allowed(USER, CHUNK))
