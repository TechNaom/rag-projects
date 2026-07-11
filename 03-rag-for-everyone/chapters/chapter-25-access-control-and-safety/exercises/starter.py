"""Exercise: access filter."""
USER = {"tenant": "t1", "roles": {"support"}}
CHUNK = {"tenant": "t1", "roles": {"legal"}}
def allowed(user, chunk):
    return False
if __name__ == "__main__":
    print(allowed(USER, CHUNK))
