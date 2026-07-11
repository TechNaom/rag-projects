DOCUMENTS = {
    "doc-1": "rotate api key and update dependent services",
    "doc-2": "quarterly revenue forecast and finance review",
    "doc-3": "reset password and regenerate access credential",
}


def tokenize(text):
    # TODO: return lowercase tokens.
    raise NotImplementedError


def build_idf(documents):
    # TODO: compute IDF for each token.
    raise NotImplementedError


def rank(query, documents):
    # TODO: rank documents by TF-IDF cosine similarity.
    raise NotImplementedError


if __name__ == "__main__":
    print(rank("api key rotation", DOCUMENTS))
