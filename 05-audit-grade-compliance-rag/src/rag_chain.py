"""
rag_chain.py
------------
The "query time" half of RAG, made audit-grade. Given a user question it:

  1. retrieves through `currency_filter` (current versions ONLY by default),
  2. builds a grounded, citation-instructed prompt,
  3. generates an answer via Ollama (default) or Groq (if GROQ_API_KEY set),
     falling back to a deterministic **extractive** answerer when no LLM
     provider is reachable,
  4. runs the `citation_auditor` (L1-L4) over the answer + evidence,
  5. writes the whole thing to the append-only `trace_store`,
  6. can optionally render a full `report_generator` audit report.

The extractive fallback is not a mock: it composes the answer out of the actual
retrieved sentences and attaches genuine citation markers, so the L1-L4 audit
and currency proofs are real even in an offline sandbox with no model server.
When you run this somewhere with Ollama or a Groq key, the LLM answer is used
instead and the exact same audit pipeline grades it.
"""

import json
import os
import re
import urllib.request
from typing import Dict, List, Optional, Tuple

from config import get_api_settings
from currency_filter import retrieve, verify_currency, RetrievedChunk
from citation_auditor import audit_answer
from trace_store import log_trace

SYSTEM_PROMPT = """You are an audit-grade compliance assistant for Aventine Health Network (AHN), a fictional healthcare provider.
Answer the reviewer's question using ONLY the policy excerpts provided in <context> below.

Rules:
- If the answer isn't in the provided context, say so explicitly. Do not guess or use outside knowledge.
- Cite EVERY factual claim. Attach a bracketed marker like [1] pointing to the numbered context excerpt you used, AND name the policy by its doc_id (e.g. "per RETEN-002").
- Put a citation on every sentence that states a fact.
- Be exact with numbers (retention periods, deadlines, day counts) - copy them precisely from the context.
- The excerpts provided are already filtered to the CURRENTLY-EFFECTIVE version of each policy. Do not invent older values.
- Keep the answer concise and direct.
"""

CODE_API_KEYS = {
    "groq": "",
}

GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL", get_api_settings()["groq_model"])

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


# --------------------------------------------------------------------------- #
# Retrieval + context
# --------------------------------------------------------------------------- #
def get_top_k(k: Optional[int]) -> int:
    if k is not None:
        return k
    try:
        return max(1, int(os.environ.get("RAG_TOP_K", "4")))
    except ValueError:
        return 4


def build_context_block(chunks: List[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(
            f"[{i}] (doc_id: {c.doc_id} v{c.version} | status: {c.status} | "
            f"section: {c.section})\n{c.text}"
        )
    return "\n\n".join(parts)


# --------------------------------------------------------------------------- #
# Providers
# --------------------------------------------------------------------------- #
def get_api_key(provider: str) -> str:
    env_key = os.environ.get(f"{provider.upper()}_API_KEY")
    if env_key:
        return env_key
    if provider == "groq":
        settings = get_api_settings()
        return settings.get("groq_api_key", CODE_API_KEYS.get("groq", ""))
    return ""


def get_default_provider() -> str:
    return get_api_settings()["default_provider"]


def get_provider_status(provider: Optional[str] = None) -> str:
    provider_name = (provider or get_default_provider()).lower()
    if provider_name == "groq":
        if get_api_key("groq"):
            return "Groq status: ready"
        return "Groq status: missing GROQ_API_KEY. Falls back to extractive answerer."
    if provider_name == "ollama":
        try:
            with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5):
                return "Ollama status: ready"
        except Exception:
            return "Ollama status: not reachable at http://localhost:11434 (extractive fallback will be used)"
    return f"Provider status: {provider_name}"


def parse_provider(query: str, default_provider: Optional[str] = None) -> Tuple[str, str]:
    cleaned_query = query.strip()
    if cleaned_query.startswith('"') and cleaned_query.endswith('"') and len(cleaned_query) >= 2:
        cleaned_query = cleaned_query[1:-1].strip()

    lowered = cleaned_query.lower()
    for name in ("ask groq", "ask ollama", "ask extractive"):
        if lowered.startswith(name):
            remainder = cleaned_query[len(name):].strip()
            if remainder.startswith((":", "-")):
                remainder = remainder[1:].strip()
            return name.split()[1], remainder

    provider = (default_provider or get_default_provider()).lower()
    return provider, cleaned_query


def generate_with_ollama(prompt: str, model_name: str) -> str:
    timeout_seconds = int(os.environ.get("OLLAMA_TIMEOUT", get_api_settings()["ollama_timeout"]))
    payload = {"model": model_name, "prompt": prompt[:3000], "stream": False}
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            return response_data.get("response", "")
    except Exception as exc:
        return f"[Ollama request failed: {exc}]"


def generate_with_groq(prompt: str, model_name: str) -> str:
    groq_api_key = get_api_key("groq")
    if not groq_api_key:
        return "[No GROQ_API_KEY found in environment or code config - skipping generation.]"

    groq_api_base = os.environ.get("GROQ_API_BASE", get_api_settings()["groq_api_base"])
    try:
        max_tokens = int(os.environ.get("GROQ_MAX_TOKENS", get_api_settings()["groq_max_tokens"]))
    except ValueError:
        max_tokens = 1024

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        groq_api_base,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {groq_api_key}",
            "User-Agent": "audit-rag/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            choices = response_data.get("choices", [])
            if not choices:
                return "[Groq returned no choices.]"
            return choices[0].get("message", {}).get("content", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        if exc.code == 401:
            return "[Groq authentication failed: check your API key and permissions.]"
        if exc.code == 403:
            return "[Groq access denied: the API key may be invalid, expired, or not authorized.]"
        return f"[Groq request failed with HTTP {exc.code}: {detail}]"
    except Exception as exc:
        return f"[Groq request failed: {exc}]"


def _query_terms(query: str) -> set:
    return {t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) >= 4}


def generate_extractive(query: str, chunks: List[RetrievedChunk], max_sentences: int = 2) -> str:
    """Deterministic, offline answerer used when no LLM provider is reachable.

    It selects the retrieved sentences most relevant to the question and emits
    them verbatim, each stamped with a citation marker [i] and the source
    doc_id. Because the answer is literally the supporting text, the citation
    auditor's L1-L4 checks and currency proofs are genuine, not simulated.
    """
    if not chunks:
        return "The provided policy excerpts do not contain an answer to this question."

    q_terms = _query_terms(query)
    scored = []
    for idx, c in enumerate(chunks, 1):
        for sent in _SENTENCE_SPLIT_RE.split(c.text):
            sent = sent.strip()
            if len(sent) < 25:
                continue
            s_terms = {t for t in re.findall(r"[a-z0-9]+", sent.lower()) if len(t) >= 4}
            overlap = len(q_terms & s_terms)
            scored.append((overlap, idx, c, sent))

    # Highest overlap first; stable on retrieval order for ties.
    scored.sort(key=lambda x: (-x[0], x[1]))
    picked = [s for s in scored if s[0] > 0][:max_sentences]
    if not picked:
        # No lexical overlap - fall back to the single most relevant chunk's first sentence.
        c = chunks[0]
        first = _SENTENCE_SPLIT_RE.split(c.text)[0].strip()
        return f"{first} [1] (per {c.doc_id} v{c.version})."

    sentences = []
    for _, idx, c, sent in picked:
        sent = sent.rstrip(".")
        sentences.append(f"{sent} [{idx}] (per {c.doc_id} v{c.version}).")
    return " ".join(sentences)


def generate_answer(
    question_text: str,
    chunks: List[RetrievedChunk],
    provider: str,
) -> Tuple[str, str]:
    """Return (answer_text, effective_provider_label)."""
    context_block = build_context_block(chunks)
    user_message = f"<context>\n{context_block}\n</context>\n\nReviewer question: {question_text}"

    if provider == "extractive":
        return generate_extractive(question_text, chunks), "extractive"

    if provider == "groq":
        answer = generate_with_groq(user_message, os.environ.get("GROQ_MODEL", GROQ_MODEL_NAME))
        if answer.startswith("[") and answer.endswith("]"):
            return generate_extractive(question_text, chunks), "extractive-fallback"
        return answer, "groq"

    if provider == "ollama":
        model_name = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
        answer = generate_with_ollama(f"{SYSTEM_PROMPT}\n\n{user_message}", model_name)
        if answer.startswith("[") and answer.endswith("]"):
            return generate_extractive(question_text, chunks), "extractive-fallback"
        return answer, "ollama"

    return generate_extractive(question_text, chunks), "extractive"


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def answer_question(
    query: str,
    k: Optional[int] = None,
    verbose: bool = True,
    provider: Optional[str] = None,
    include_superseded: bool = False,
    write_trace: bool = True,
) -> Dict:
    """Full audit-grade answer pipeline. Returns a dict with keys:
    answer, provider, chunks, audit (CitationAuditResult), trace (dict)."""
    resolved_provider, question_text = parse_provider(query, default_provider=provider)
    k = get_top_k(k)

    chunks = retrieve(question_text, k=k, include_superseded=include_superseded)

    if verbose:
        print(f"\n{'='*70}\nQUERY: {question_text}\n{'='*70}")
        scope = "ALL versions" if include_superseded else "current only"
        print(f"\n--- Retrieved {len(chunks)} chunks ({scope}) ---")
        for i, c in enumerate(chunks, 1):
            print(f"  [{i}] score={c.score}  {c.doc_id} v{c.version} [{c.status}]  ({c.section})")

    answer, effective_provider = generate_answer(question_text, chunks, resolved_provider)

    if verbose:
        print(f"\n--- Provider: {effective_provider} ---")
        print(f"\n--- Answer ---\n{answer}\n")

    audit = audit_answer(answer, chunks)
    if verbose:
        print(f"--- Citation audit: {audit.summary} ---")
        for lvl in audit.levels:
            print(f"  {lvl.level} {lvl.name}: {'PASS' if lvl.passed else 'FAIL'}")

    trace = None
    if write_trace:
        trace = log_trace(
            question_text, chunks, audit, answer,
            provider=effective_provider, include_superseded=include_superseded,
        )

    return {
        "answer": answer,
        "provider": effective_provider,
        "chunks": chunks,
        "audit": audit,
        "trace": trace,
    }


if __name__ == "__main__":
    answer_question("How long must adult patient medical records be retained?")
