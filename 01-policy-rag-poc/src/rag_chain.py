"""
rag_chain.py
------------
The "query time" half of RAG: given a user question, retrieve the most
relevant chunks from the vector store, build a grounded prompt, and call
an LLM (Claude) to generate an answer that cites its sources.

Generation requires a real Anthropic API key (ANTHROPIC_API_KEY env var).
This sandbox doesn't have one pre-configured, so this module degrades
gracefully: retrieval always works; generation runs only if a key is
present. Run this on your own machine with `export ANTHROPIC_API_KEY=...`
to see the full pipeline including the generated answer.
"""

import os
from dataclasses import dataclass
from typing import List

from vectorstore import load_vectorstore

try:
    import anthropic
except ImportError:
    anthropic = None

SYSTEM_PROMPT = """You are an internal HR & Compliance policy assistant for Northkeep National Bank.
Answer the employee's question using ONLY the policy excerpts provided in <context> below.

Rules:
- If the answer isn't in the provided context, say so explicitly. Do not guess or use outside knowledge.
- Always cite which policy document(s) you used, by their Policy ID (e.g. "per HR-LV-003").
- Be precise with numbers (dollar amounts, day counts, deadlines) - get them exactly right from the context.
- Keep answers concise and direct, the way a knowledgeable HR colleague would answer in Slack.
"""


@dataclass
class RetrievedChunk:
    text: str
    source_file: str
    section: str
    score: float  # cosine similarity, higher = more relevant


def retrieve(query: str, k: int = 4) -> List[RetrievedChunk]:
    collection, embedder = load_vectorstore()
    query_vector = embedder.embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        # Chroma returns cosine *distance*; similarity = 1 - distance
        similarity = 1 - dist
        chunks.append(RetrievedChunk(
            text=doc,
            source_file=meta.get("source_file", "unknown"),
            section=meta.get("section", ""),
            score=round(similarity, 3),
        ))
    return chunks


def build_context_block(chunks: List[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] (source: {c.source_file} | section: {c.section})\n{c.text}")
    return "\n\n".join(parts)


def generate_answer(query: str, chunks: List[RetrievedChunk]) -> str:
    """Calls Claude with the retrieved context. Requires ANTHROPIC_API_KEY."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            "[No ANTHROPIC_API_KEY found in environment - skipping generation.]\n"
            "Set it with: export ANTHROPIC_API_KEY=sk-ant-...\n"
            "Retrieval above is what would be fed to the model as context."
        )
    if anthropic is None:
        return "[anthropic package not installed - run: pip install anthropic]"

    client = anthropic.Anthropic(api_key=api_key)
    context_block = build_context_block(chunks)
    user_message = f"<context>\n{context_block}\n</context>\n\nEmployee question: {query}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def answer_question(query: str, k: int = 4, verbose: bool = True):
    chunks = retrieve(query, k=k)

    if verbose:
        print(f"\n{'='*70}\nQUERY: {query}\n{'='*70}")
        print(f"\n--- Retrieved {len(chunks)} chunks ---")
        for i, c in enumerate(chunks, 1):
            print(f"  [{i}] score={c.score}  {c.source_file}  ({c.section})")

    answer = generate_answer(query, chunks)

    if verbose:
        print(f"\n--- Generated Answer ---\n{answer}\n")

    return answer, chunks


if __name__ == "__main__":
    answer_question("How many days of parental leave do I get and does it matter if I'm the primary or secondary caregiver?")
