"""
main.py
-------
Interactive CLI for the Northkeep Policy Assistant RAG POC.

Usage:
    python3 src/vectorstore.py     # one-time: build the index
    python3 src/main.py            # ask questions interactively

Set ANTHROPIC_API_KEY in your environment to get full generated answers;
without it, you'll still see retrieval working (which is most of the
engineering anyway).
"""

import os
from rag_chain import answer_question

BANNER = """
==========================================================
 Northkeep National Bank — Internal Policy Assistant (RAG)
==========================================================
Ask a question about HR or compliance policy. Type 'quit' to exit.
"""


def main():
    print(BANNER)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("(No ANTHROPIC_API_KEY set - showing retrieval only, no generated answer.\n"
              " export ANTHROPIC_API_KEY=sk-ant-... to enable generation.)\n")

    while True:
        query = input("Your question> ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue
        answer_question(query, k=4, verbose=True)


if __name__ == "__main__":
    main()
