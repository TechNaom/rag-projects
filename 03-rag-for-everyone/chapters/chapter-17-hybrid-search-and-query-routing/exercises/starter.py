QUERIES = [
    {"id": "q1", "text": "How do I regenerate credentials?", "risk": "low"},
    {"id": "q2", "text": "AZ-4032-B after key rotation", "risk": "medium"},
    {"id": "q3", "text": "Policy 7.3 termination clause for EU employees", "risk": "high"},
]


def route_query(query):
    # TODO: return retrieval route and reason.
    raise NotImplementedError


if __name__ == "__main__":
    for query in QUERIES:
        print(route_query(query))
