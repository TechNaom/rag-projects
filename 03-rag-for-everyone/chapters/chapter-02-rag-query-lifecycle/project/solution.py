from dataclasses import dataclass, field
from typing import Iterable


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
    candidate_sources: list[str] = field(default_factory=list)
    reranked_sources: list[str] = field(default_factory=list)
    context_sources: list[str] = field(default_factory=list)
    blocked_sources: list[str] = field(default_factory=list)
    answer_status: str = ""
    citations: list[str] = field(default_factory=list)
    refusal_reason: str = ""
    first_metric_to_inspect: str = ""


DOCUMENTS = [
    Document(
        "refund_policy_eu_2026",
        "EU Refund Policy 2026",
        "Annual plans in Germany are refundable within 14 days of purchase. Refund answers must cite the EU policy version.",
        {"region": "EU", "topic": "refund", "status": "approved", "version": "2026"},
        {"support", "manager", "admin"},
    ),
    Document(
        "refund_policy_us_2026",
        "US Refund Policy 2026",
        "Annual plans in the US are refundable within 7 days of purchase.",
        {"region": "US", "topic": "refund", "status": "approved", "version": "2026"},
        {"support", "manager", "admin"},
    ),
    Document(
        "security_runbook_sev1",
        "Sev1 Security Runbook",
        "Customer log access during Sev1 requires incident commander approval and must be time boxed.",
        {"region": "global", "topic": "security", "status": "approved", "severity": "sev1"},
        {"engineer", "incident_commander", "admin"},
    ),
    Document(
        "customer_data_access_policy",
        "Customer Data Access Policy",
        "Contractors cannot access customer logs unless an approved exception is recorded by the incident commander.",
        {"region": "global", "topic": "security", "status": "approved", "data": "customer_logs"},
        {"engineer", "incident_commander", "admin"},
    ),
    Document(
        "draft_refund_policy_2027",
        "Draft Refund Policy 2027",
        "Draft: annual plans may be refundable within 30 days. This policy is not approved.",
        {"region": "EU", "topic": "refund", "status": "draft", "version": "2027"},
        {"admin"},
    ),
]


SYNONYMS = {
    "refund_policy": ["refund", "refundable", "annual", "plan", "purchase"],
    "security_access": ["customer", "log", "logs", "sev1", "incident", "access", "contractor"],
}


def normalize(text: str) -> list[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return [token for token in cleaned.split() if len(token) > 2]


def classify_intent(question: str) -> str:
    q = question.lower()
    if "refund" in q or "annual plan" in q:
        return "refund_policy"
    if "log" in q or "sev1" in q or "contractor" in q:
        return "security_access"
    return "unknown"


def build_retrieval_query(question: str, intent: str) -> str:
    expansion = " ".join(SYNONYMS.get(intent, []))
    return f"{question} {expansion}".strip()


def build_filters(question: str, intent: str) -> dict:
    q = question.lower()
    filters = {"status": "approved"}
    if intent == "refund_policy":
        filters["topic"] = "refund"
        if "germany" in q or "eu" in q:
            filters["region"] = "EU"
        elif "us" in q or "america" in q:
            filters["region"] = "US"
    elif intent == "security_access":
        filters["topic"] = "security"
    return filters


def passes_metadata(doc: Document, filters: dict) -> bool:
    return all(doc.metadata.get(key) == value for key, value in filters.items())


def apply_access_control(documents: Iterable[Document], user_role: str, trace: Trace) -> list[Document]:
    visible = []
    for doc in documents:
        if user_role in doc.allowed_roles:
            visible.append(doc)
        else:
            trace.blocked_sources.append(doc.source_id)
    return visible


def score_document(query_terms: list[str], doc: Document) -> Candidate:
    doc_terms = set(normalize(f"{doc.title} {doc.text} {' '.join(str(v) for v in doc.metadata.values())}"))
    matched = sorted(set(query_terms).intersection(doc_terms))
    score = len(matched)
    if doc.metadata.get("status") == "approved":
        score += 0.5
    if doc.metadata.get("topic") in query_terms:
        score += 1
    return Candidate(doc, score, matched)


def retrieve(query: str, filters: dict, user_role: str, trace: Trace) -> list[Candidate]:
    filtered = [doc for doc in DOCUMENTS if passes_metadata(doc, filters)]
    visible = apply_access_control(filtered, user_role, trace)
    query_terms = normalize(query)
    candidates = [score_document(query_terms, doc) for doc in visible]
    candidates = [candidate for candidate in candidates if candidate.score > 0]
    trace.candidate_sources = [candidate.document.source_id for candidate in candidates]
    return candidates


def rerank(candidates: list[Candidate], intent: str) -> list[Candidate]:
    def boost(candidate: Candidate) -> float:
        score = candidate.score
        source_id = candidate.document.source_id
        if intent == "security_access" and source_id in {"security_runbook_sev1", "customer_data_access_policy"}:
            score += 2
        if intent == "refund_policy" and "refund_policy" in source_id:
            score += 2
        return score

    return sorted(candidates, key=boost, reverse=True)


def assemble_context(candidates: list[Candidate], max_sources: int = 2) -> list[Document]:
    return [candidate.document for candidate in candidates[:max_sources]]


def generate_answer(question: str, intent: str, context_docs: list[Document]) -> tuple[str, str, list[str], str]:
    if not context_docs:
        return (
            "refused",
            "I cannot answer from the approved sources available to this user.",
            [],
            "No visible approved source matched the request.",
        )

    source_ids = {doc.source_id for doc in context_docs}
    if intent == "refund_policy":
        refund_doc = next((doc for doc in context_docs if doc.metadata.get("topic") == "refund"), None)
        if not refund_doc:
            return "refused", "I could not find the approved refund policy.", [], "Missing refund policy."
        return (
            "answered",
            f"Based on {refund_doc.title}, {refund_doc.text}",
            [refund_doc.source_id],
            "",
        )

    if intent == "security_access":
        required = {"security_runbook_sev1", "customer_data_access_policy"}
        if not required.issubset(source_ids):
            return (
                "escalated",
                "I found partial security guidance, but not enough approved evidence to authorize access. Escalate to the incident commander.",
                sorted(source_ids),
                "Security access requires both runbook and access policy.",
            )
        return (
            "escalated",
            "Customer log access during Sev1 requires incident commander approval, a recorded exception, and a time-boxed scope.",
            sorted(required),
            "",
        )

    return (
        "refused",
        "I do not have enough approved context to answer this request.",
        [],
        "Unknown intent.",
    )


def run_pipeline(question: str, user_role: str = "support", request_id: str = "req_demo") -> tuple[str, Trace]:
    trace = Trace(request_id=request_id, user_question=question, user_role=user_role)
    trace.intent = classify_intent(question)
    trace.retrieval_query = build_retrieval_query(question, trace.intent)
    trace.filters = build_filters(question, trace.intent)
    candidates = retrieve(trace.retrieval_query, trace.filters, user_role, trace)
    reranked = rerank(candidates, trace.intent)
    trace.reranked_sources = [candidate.document.source_id for candidate in reranked]
    context_docs = assemble_context(reranked)
    trace.context_sources = [doc.source_id for doc in context_docs]
    status, answer, citations, refusal = generate_answer(question, trace.intent, context_docs)
    trace.answer_status = status
    trace.citations = citations
    trace.refusal_reason = refusal
    trace.first_metric_to_inspect = choose_metric(trace)
    return answer, trace


def choose_metric(trace: Trace) -> str:
    if not trace.candidate_sources:
        return "filtered_recall"
    if trace.intent == "security_access":
        return "paired_source_recall"
    if trace.citations:
        return "citation_precision"
    return "answer_support_rate"


GOLDEN_EVALS = [
    {
        "name": "EU refund answer",
        "question": "Can I get a refund for my annual plan in Germany?",
        "role": "support",
        "expected_status": "answered",
        "expected_citations": {"refund_policy_eu_2026"},
    },
    {
        "name": "Security access escalation",
        "question": "Can a contractor access customer logs during a Sev1 incident?",
        "role": "engineer",
        "expected_status": "escalated",
        "expected_citations": {"security_runbook_sev1", "customer_data_access_policy"},
    },
    {
        "name": "Access-controlled refusal",
        "question": "Can a contractor access customer logs during a Sev1 incident?",
        "role": "support",
        "expected_status": "refused",
        "expected_citations": set(),
    },
]


def run_evals() -> list[dict]:
    results = []
    for case in GOLDEN_EVALS:
        answer, trace = run_pipeline(case["question"], case["role"], request_id=case["name"])
        citations = set(trace.citations)
        passed = trace.answer_status == case["expected_status"] and case["expected_citations"].issubset(citations)
        results.append(
            {
                "name": case["name"],
                "passed": passed,
                "status": trace.answer_status,
                "citations": trace.citations,
                "metric": trace.first_metric_to_inspect,
                "answer": answer,
                "trace": trace,
            }
        )
    return results


if __name__ == "__main__":
    for result in run_evals():
        print(f"{result['name']}: {'PASS' if result['passed'] else 'FAIL'}")
        print("status:", result["status"])
        print("citations:", result["citations"])
        print("metric:", result["metric"])
        print("answer:", result["answer"])
        print("trace:", result["trace"])
        print()
