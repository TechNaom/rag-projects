"""
main.py
-------
Interactive CLI for the Northkeep Policy Assistant RAG POC.

Usage:
    python3 src/vectorstore.py     # one-time: build the index
    python3 src/main.py            # ask questions interactively

Set GROQ_API_KEY in your environment (or run a local Ollama server) to get
full generated answers; without either, you'll still see retrieval working
(which is most of the engineering anyway).
"""

import os
from rag_chain import answer_question, get_default_provider, get_provider_status

BANNER = """
==========================================================
 Northkeep National Bank — Internal Policy Assistant (RAG)
==========================================================
Ask a question about HR or compliance policy.
Prefix your question with 'ask groq' or 'ask ollama' to choose the model.
Type 'quit' to exit.
"""


def main():
    print(BANNER)
    provider = get_default_provider()
    status = get_provider_status(provider)
    print(f"Default provider: {provider}")
    print(status)
    print()

    while True:
        query = input("Your question> ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue
        provider = None
        lowered = query.lower()
        if lowered.startswith("ask groq"):
            provider = "groq"
        elif lowered.startswith("ask ollama"):
            provider = "ollama"

        answer_question(query, k=4, verbose=True, provider=provider)


if __name__ == "__main__":
    main()
