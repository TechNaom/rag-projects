"""
main.py
-------
Interactive CLI for the Aventine Health Network Audit-Grade Compliance RAG.

Usage:
    python src/vectorstore.py     # one-time: build the index
    python src/main.py            # interactive

Commands inside the prompt:
    <question>                    ask normally (current-policy answer + audit summary)
    audit <question>              print the FULL Markdown audit report for a question
    history <question>            include superseded versions (for historical/audit queries)
    ask groq <question>           force the Groq provider for this query
    ask ollama <question>         force a local Ollama server for this query
    ask extractive <question>     force the offline extractive answerer
    quit                          exit

Set GROQ_API_KEY (or run a local Ollama server) for LLM-generated answers.
Without either, the offline extractive answerer is used, and the full audit
pipeline still runs end-to-end.
"""

from rag_chain import answer_question, get_default_provider, get_provider_status
from report_generator import render_report

BANNER = """
==============================================================
 Aventine Health Network — Audit-Grade Compliance Assistant
==============================================================
Ask a compliance question. Answers use only currently-effective
policy by default, every answer is traced, and 'audit <question>'
prints a full reviewer report.

Commands: audit <q> | history <q> | ask groq|ollama|extractive <q> | quit
"""


def main():
    print(BANNER)
    provider = get_default_provider()
    print(f"Default provider: {provider}")
    print(get_provider_status(provider))
    print()

    while True:
        try:
            query = input("compliance> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            break

        lowered = query.lower()
        if lowered.startswith("audit "):
            question = query[len("audit "):].strip()
            result = answer_question(question, verbose=False, write_trace=True)
            print()
            print(render_report(result["trace"]))
            print()
            continue

        if lowered.startswith("history "):
            question = query[len("history "):].strip()
            answer_question(question, verbose=True, include_superseded=True)
            continue

        provider = None
        if lowered.startswith("ask groq"):
            provider = "groq"
        elif lowered.startswith("ask ollama"):
            provider = "ollama"
        elif lowered.startswith("ask extractive"):
            provider = "extractive"

        answer_question(query, verbose=True, provider=provider)


if __name__ == "__main__":
    main()
