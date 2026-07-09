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
    Document(
        "security_runbook_sev1",
        "Sev1 Security Runbook",
        "Customer log access during Sev1 requires incident commander approval.",
        {"region": "global", "topic": "security", "status": "approved"},
    ),
]


def classify_intent(question):
    q = question.lower()
    if "refund" in q:
        return "refund_policy"
    if "log" in q or "sev1" in q:
        return "security_access"
    return "unknown"


def build_retrieval_query(question, intent):
    if intent == "refund_policy":
        return "refund annual plan regional policy"
    if intent == "security_access":
        return "customer log access sev1 incident approval"
    return question


def build_filters(question, intent):
    q = question.lower()
    filters = {"status": "approved"}
    if intent == "refund_policy":
        filters["topic"] = "refund"
        filters["region"] = "EU" if "germany" in q or "eu" in q else "US"
    if intent == "security_access":
        filters["topic"] = "security"
    return filters


def retrieve(query, filters):
    matches = []
    for doc in DOCUMENTS:
        if all(doc.metadata.get(key) == value for key, value in filters.items()):
            matches.append(doc)
    return matches


def answer(question, docs):
    if not docs:
        return (
            "refused",
            "I cannot answer from the approved sources I retrieved.",
            [],
            "No approved supporting source was retrieved.",
        )

    doc = docs[0]
    if doc.metadata["topic"] == "refund":
        return (
            "answered",
            f"Based on {doc.title}, {doc.text}",
            [doc.source_id],
            "",
        )
    if doc.metadata["topic"] == "security":
        return (
            "escalated",
            f"{doc.text} Escalate to the incident commander before granting access.",
            [doc.source_id],
            "",
        )
    return "refused", "The retrieved source does not support a safe answer.", [], "Unsupported topic."


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


def golden_eval():
    answer_text, trace = run_pipeline("Can I get a refund for my annual plan in Germany?")
    assert trace.intent == "refund_policy"
    assert trace.filters["region"] == "EU"
    assert "refund_policy_eu_2026" in trace.retrieved_sources
    assert trace.answer_status == "answered"
    assert trace.citations == ["refund_policy_eu_2026"]
    return answer_text, trace


if __name__ == "__main__":
    result, trace = golden_eval()
    print(result)
    print(trace)
