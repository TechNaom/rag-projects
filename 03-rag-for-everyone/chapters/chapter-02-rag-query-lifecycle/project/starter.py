from dataclasses import dataclass, field


@dataclass
class Document:
    source_id: str
    title: str
    text: str
    metadata: dict


@dataclass
class Trace:
    user_question: str
    intent: str = ""
    retrieval_query: str = ""
    filters: dict = field(default_factory=dict)
    retrieved_sources: list = field(default_factory=list)
    answer_status: str = ""
    citations: list = field(default_factory=list)
    refusal_reason: str = ""


DOCUMENTS = [
    Document(
        "refund_policy_eu_2026",
        "EU Refund Policy 2026",
        "Annual plans in Germany are refundable within 14 days of purchase.",
        {"region": "EU", "topic": "refund", "status": "approved"},
    ),
    Document(
        "refund_policy_us_2026",
        "US Refund Policy 2026",
        "Annual plans in the US are refundable within 7 days of purchase.",
        {"region": "US", "topic": "refund", "status": "approved"},
    ),
]


def classify_intent(question):
    # TODO: return a simple intent such as "refund_policy"
    return ""


def build_retrieval_query(question, intent):
    # TODO: convert user question into a search-friendly query
    return ""


def build_filters(question, intent):
    # TODO: infer metadata filters such as region and topic
    return {}


def retrieve(query, filters):
    # TODO: return documents matching filters
    return []


def answer(question, docs):
    # TODO: return status, answer text, citations, refusal reason
    return "refused", "", [], "No implementation yet."


def run_pipeline(question):
    trace = Trace(user_question=question)
    trace.intent = classify_intent(question)
    trace.retrieval_query = build_retrieval_query(question, trace.intent)
    trace.filters = build_filters(question, trace.intent)
    docs = retrieve(trace.retrieval_query, trace.filters)
    trace.retrieved_sources = [doc.source_id for doc in docs]
    status, text, citations, refusal = answer(question, docs)
    trace.answer_status = status
    trace.citations = citations
    trace.refusal_reason = refusal
    return text, trace


if __name__ == "__main__":
    result, trace = run_pipeline("Can I get a refund for my annual plan in Germany?")
    print(result)
    print(trace)
