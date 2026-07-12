"""
main.py
-------
Interactive CLI for the Real-Time On-Call Ops Copilot.

Usage:
    python3 src/vectorstore.py     # one-time: build the index
    python3 src/main.py            # interactive session

Commands inside the session:
    <any question>                 ask the copilot (routed + timed)
    ask groq <question>            force the Groq provider for this question
    ask ollama <question>          force the Ollama provider for this question
    simulate-update                run the live-update demo (proves live re-index)
    latency report                 print the p50/p95 latency breakdown so far
    quit                           exit

Set GROQ_API_KEY in your environment (or run a local Ollama server) to get
full generated answers; without either, you'll still see retrieval, routing,
and latency working — which is most of the engineering anyway.
"""

from latency_budget import GLOBAL_TIMER
from live_updater import demo as live_update_demo
from rag_chain import answer_question, get_default_provider, get_provider_status

BANNER = """
==========================================================
 Real-Time On-Call Ops Copilot  (live-updating RAG)
==========================================================
Ask about runbooks or live incident notes.
Commands:
  simulate-update      prove the index updates live (no rebuild)
  latency report       show p50/p95 latency per stage
  ask groq <q> / ask ollama <q>   pick a provider for one question
  quit                 exit
"""


def main():
    print(BANNER)
    provider = get_default_provider()
    print(f"Default provider: {provider}")
    print(get_provider_status(provider))
    print()

    while True:
        query = input("oncall> ").strip()
        if not query:
            continue

        lowered = query.lower()
        if lowered in ("quit", "exit", "q"):
            break

        if lowered in ("simulate-update", "simulate update"):
            live_update_demo()
            continue

        if lowered in ("latency report", "latency-report"):
            GLOBAL_TIMER.report()
            continue

        provider = None
        if lowered.startswith("ask groq"):
            provider = "groq"
        elif lowered.startswith("ask ollama"):
            provider = "ollama"

        answer_question(query, verbose=True, provider=provider)


if __name__ == "__main__":
    main()
