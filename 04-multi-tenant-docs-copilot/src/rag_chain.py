"""
rag_chain.py
------------
The "query time" half of RAG, scoped to a single tenant: given a tenant_id and
a user question, retrieve that tenant's most relevant chunks THROUGH the tenant
gateway, build a grounded prompt, and call an LLM provider to generate an answer
that cites its sources.

Two differences from a single-tenant RAG chain:
  1. Retrieval goes through `tenant_gateway`, never a global vector store, so a
     query for one tenant can only ever see that tenant's documents.
  2. Every query is wrapped in `cost_tracker.track(...)`, so latency and an
     approximate token count are attributed to the calling tenant.

The app supports Ollama locally by default and Groq when a GROQ_API_KEY is
provided. Without a provider configured, retrieval still runs and the retrieved
chunks are shown — which is most of what's interesting about a RAG system.
"""

import json
import os
import urllib.error
import urllib.request
from typing import List, Optional, Tuple

from config import get_api_settings
import cost_tracker
from tenant_gateway import RetrievedChunk, get_gateway

SYSTEM_PROMPT = """You are a documentation copilot answering questions for a single organization's users.
Answer the user's question using ONLY the documentation excerpts provided in <context> below.

Rules:
- If the answer isn't in the provided context, say so explicitly. Do not guess or use outside knowledge.
- Always cite which document(s) you used, by their source file or Doc ID.
- Be precise with numbers (amounts, day counts, limits, deadlines) - get them exactly right from the context.
- Keep answers concise and direct, the way a knowledgeable colleague would answer in chat.
"""

# Optional fallback keys that can be set directly in code when you do not want to use environment variables.
CODE_API_KEYS = {
    "groq": "",
}

GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL", get_api_settings()["groq_model"])


def retrieve(tenant_id: str, query: str, k: Optional[int] = None) -> List[RetrievedChunk]:
    if k is None:
        try:
            k = max(1, int(os.environ.get("RAG_TOP_K", "4")))
        except ValueError:
            k = 4
    # All retrieval is mediated by the tenant gateway — there is no global store.
    return get_gateway(tenant_id).retrieve(query, k=k)


def build_context_block(chunks: List[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] (source: {c.source_file} | section: {c.section})\n{c.text}")
    return "\n\n".join(parts)


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
        groq_api_key = get_api_key("groq")
        if groq_api_key:
            return "Groq status: ready"
        return "Groq status: missing GROQ_API_KEY. Use 'ask ollama' or set GROQ_API_KEY."
    if provider_name == "ollama":
        try:
            with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5):
                return "Ollama status: ready"
        except Exception:
            return "Ollama status: not reachable at http://localhost:11434"
    return f"Provider status: {provider_name}"


def parse_provider(query: str, default_provider: Optional[str] = None) -> Tuple[str, str]:
    cleaned_query = query.strip()
    if cleaned_query.startswith('"') and cleaned_query.endswith('"') and len(cleaned_query) >= 2:
        cleaned_query = cleaned_query[1:-1].strip()

    lowered = cleaned_query.lower()

    if lowered.startswith("ask groq"):
        remainder = cleaned_query[len("ask groq"):].strip()
        if remainder.startswith(":") or remainder.startswith("-"):
            remainder = remainder[1:].strip()
        return "groq", remainder

    if lowered.startswith("ask ollama"):
        remainder = cleaned_query[len("ask ollama"):].strip()
        if remainder.startswith(":") or remainder.startswith("-"):
            remainder = remainder[1:].strip()
        return "ollama", remainder

    provider = (default_provider or get_default_provider()).lower()
    return provider, cleaned_query


def generate_with_ollama(prompt: str, model_name: str) -> str:
    timeout_seconds = int(os.environ.get("OLLAMA_TIMEOUT", get_api_settings()["ollama_timeout"]))
    payload = {
        "model": model_name,
        "prompt": prompt[:3000],
        "stream": False,
    }
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
            "User-Agent": "multi-tenant-copilot/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            choices = response_data.get("choices", [])
            if not choices:
                return "[Groq returned no choices.]"
            message = choices[0].get("message", {})
            return message.get("content", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        if exc.code == 401:
            return "[Groq authentication failed: check your API key and permissions.]"
        if exc.code == 403:
            return "[Groq access denied: the API key may be invalid, expired, or not authorized for this endpoint.]"
        return f"[Groq request failed with HTTP {exc.code}: {detail}]"
    except Exception as exc:
        return f"[Groq request failed: {exc}]"


def generate_answer(query: str, chunks: List[RetrievedChunk], provider: Optional[str] = None) -> str:
    """Calls Groq or Ollama with the retrieved context."""
    context_block = build_context_block(chunks)
    provider_name, question_text = parse_provider(query, default_provider=provider)
    user_message = f"<context>\n{context_block}\n</context>\n\nUser question: {question_text}"

    if provider_name == "groq":
        return generate_with_groq(user_message, os.environ.get("GROQ_MODEL", GROQ_MODEL_NAME))

    if provider_name == "ollama":
        model_name = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
        return generate_with_ollama(f"{SYSTEM_PROMPT}\n\n{user_message}", model_name)

    return f"[Unsupported provider: {provider_name}]"


def answer_question(
    tenant_id: str,
    query: str,
    k: Optional[int] = None,
    verbose: bool = True,
    provider: Optional[str] = None,
):
    """Answer one question for one tenant, tracking cost/latency for that tenant."""
    resolved_provider, question_text = parse_provider(query, default_provider=provider)

    # Everything inside `track` is attributed to this tenant's cost/latency line.
    with cost_tracker.track(tenant_id, prompt_text=question_text) as usage:
        chunks = retrieve(tenant_id, question_text, k=k)

        if verbose:
            print(f"\n{'='*70}\nTENANT: {tenant_id}\nQUERY:  {query}\n{'='*70}")
            print(f"\n--- Retrieved {len(chunks)} chunks (from '{tenant_id}' collection only) ---")
            for i, c in enumerate(chunks, 1):
                print(f"  [{i}] score={c.score}  {c.source_file}  ({c.section})")
            if resolved_provider == "groq":
                print(f"\n--- Model ---\nProvider: Groq (model: {os.environ.get('GROQ_MODEL', GROQ_MODEL_NAME)})\n")
            elif resolved_provider == "ollama":
                model_name = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
                print(f"\n--- Model ---\nProvider: Ollama (model: {model_name})\n")
            else:
                print(f"\n--- Model ---\nProvider: {resolved_provider}\n")

        answer = generate_answer(question_text, chunks, provider=resolved_provider)
        usage["completion_text"] = answer

    if verbose:
        print(f"\n--- Generated Answer ---\n{answer}\n")

    return answer, chunks


if __name__ == "__main__":
    answer_question(
        "starlight-robotics",
        "How long does the Skylark X2 fly on one battery?",
    )
