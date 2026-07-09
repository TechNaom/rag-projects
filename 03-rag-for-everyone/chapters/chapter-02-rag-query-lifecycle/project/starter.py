from dataclasses import dataclass, field


@dataclass
class Document:
    source_id: str
    title: str
    text: str
    metadata: dict
    allowed_roles: set[str]


@dataclass
class Candidate:
    document: Document
    score: float
    matched_terms: list[str]


@dataclass
class Trace:
    request_id: str
    user_question: str
    user_role: str
    intent: str = ""
    retrieval_query: str = ""
    filters: dict = field(default_factory=dict)
    candidate_sources: list = field(default_factory=list)
    reranked_sources: list = field(default_factory=list)
    context_sources: list = field(default_factory=list)
    blocked_sources: list = field(default_factory=list)
    answer_status: str = ""
    citations: list = field(default_factory=list)
    refusal_reason: str = ""
    first_metric_to_inspect: str = ""


DOCUMENTS = [
    Document(
        "refund_policy_eu_2026",
        "EU Refund Policy 2026",
        "Annual plans in Germany are refundable within 14 days of purchase.",
        {"region": "EU", "topic": "refund", "status": "approved"},
        {"support", "manager", "admin"},
    ),
    Document(
        "refund_policy_us_2026",
        "US Refund Policy 2026",
        "Annual plans in the US are refundable within 7 days of purchase.",
        {"region": "US", "topic": "refund", "status": "approved"},
        {"support", "manager", "admin"},
    ),
    Document(
        "security_runbook_sev1",
        "Sev1 Security Runbook",
        "Customer log access during Sev1 requires incident commander approval.",
        {"region": "global", "topic": "security", "status": "approved"},
        {"engineer", "incident_commander", "admin"},
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


def retrieve(query, filters, user_role, trace):
    # TODO: apply metadata filters, access control, and simple lexical scoring.
    return []


def rerank(candidates, intent):
    # TODO: reorder candidates so the strongest evidence comes first.
    return candidates


def assemble_context(candidates, max_sources=2):
    # TODO: return the documents that should enter the grounded prompt.
    return []


def answer(question, intent, docs):
    # TODO: return status, answer text, citations, refusal reason
    return "refused", "", [], "No implementation yet."


def choose_metric(trace):
    # TODO: choose the first metric a production engineer should inspect.
    return ""


def run_pipeline(question, user_role="support", request_id="req_demo"):
    trace = Trace(request_id=request_id, user_question=question, user_role=user_role)
    trace.intent = classify_intent(question)
    trace.retrieval_query = build_retrieval_query(question, trace.intent)
    trace.filters = build_filters(question, trace.intent)
    candidates = retrieve(trace.retrieval_query, trace.filters, user_role, trace)
    trace.candidate_sources = [candidate.document.source_id for candidate in candidates]
    reranked = rerank(candidates, trace.intent)
    trace.reranked_sources = [candidate.document.source_id for candidate in reranked]
    docs = assemble_context(reranked)
    trace.context_sources = [doc.source_id for doc in docs]
    status, text, citations, refusal = answer(question, trace.intent, docs)
    trace.answer_status = status
    trace.citations = citations
    trace.refusal_reason = refusal
    trace.first_metric_to_inspect = choose_metric(trace)
    return text, trace


if __name__ == "__main__":
    result, trace = run_pipeline("Can I get a refund for my annual plan in Germany?")
    print(result)
    print(trace)
