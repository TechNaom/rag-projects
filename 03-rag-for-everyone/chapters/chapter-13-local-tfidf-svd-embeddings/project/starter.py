DOCUMENTS = {
    "security": "rotate api key regenerate credential update dependent service",
    "finance": "quarterly revenue forecast budget finance review",
    "support": "reset password recover account login credential",
    "policy": "paid time off probation employee eligibility policy",
}

TOPIC_AXES = {
    "security": {"api", "key", "credential", "password", "login"},
    "finance": {"revenue", "forecast", "budget", "finance"},
    "hr": {"paid", "time", "off", "probation", "employee", "eligibility"},
}


def local_search(query, documents, top_k=3):
    # TODO: rank documents with TF-IDF and include tiny topic projection.
    raise NotImplementedError


if __name__ == "__main__":
    for result in local_search("api credential rotation", DOCUMENTS):
        print(result)
