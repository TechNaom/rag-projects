"""
main.py
-------
Interactive CLI for the Multi-Tenant Documentation Copilot.

Usage:
    python src/vectorstore.py     # one-time: build every tenant's isolated index
    python src/main.py            # pick a tenant, then ask questions scoped to it

The CLI first asks which tenant you are, then answers questions using ONLY that
tenant's documents. Type 'cost report' to print the per-tenant cost/latency
dashboard, 'switch' to change tenant, or 'quit' to exit.

Set GROQ_API_KEY in your environment (or run a local Ollama server) to get full
generated answers; without either, you'll still see retrieval working (which is
most of the engineering anyway).
"""

import cost_tracker
from ingest import list_tenants
from rag_chain import answer_question, get_default_provider, get_provider_status
from tenant_gateway import UnknownTenantError, get_gateway

BANNER = """
==========================================================
 Multi-Tenant Documentation Copilot (RAG-as-a-service)
==========================================================
Each tenant has its own private knowledge base with HARD
retrieval isolation (one Chroma collection per tenant).
Type 'cost report' for the dashboard, 'switch' to change
tenant, or 'quit' to exit.
"""


def choose_tenant() -> str:
    tenants = list_tenants()
    options = " / ".join(tenants)
    while True:
        choice = input(f"Which tenant? ({options})\n> ").strip()
        if choice.lower() in ("quit", "exit", "q"):
            raise SystemExit(0)
        if choice in tenants:
            # Constructing the gateway here validates the tenant + warms its store.
            try:
                get_gateway(choice)
            except UnknownTenantError as exc:
                print(f"  {exc}\n")
                continue
            return choice
        print(f"  Unknown tenant '{choice}'. Choose one of: {options}\n")


def main():
    print(BANNER)
    if not list_tenants():
        print("No tenants found. Run `python src/vectorstore.py` to build the indexes first.")
        return

    provider = get_default_provider()
    print(f"Default provider: {provider}")
    print(get_provider_status(provider))

    tenant_id = choose_tenant()
    print(f"\nNow answering as tenant: {tenant_id}\n")

    while True:
        query = input(f"[{tenant_id}] question> ").strip()
        lowered = query.lower()

        if lowered in ("quit", "exit", "q"):
            break
        if not query:
            continue
        if lowered in ("cost report", "cost", "report"):
            print()
            cost_tracker.print_dashboard()
            print()
            continue
        if lowered in ("switch", "switch tenant"):
            tenant_id = choose_tenant()
            print(f"\nNow answering as tenant: {tenant_id}\n")
            continue

        provider = None
        if lowered.startswith("ask groq"):
            provider = "groq"
        elif lowered.startswith("ask ollama"):
            provider = "ollama"

        answer_question(tenant_id, query, k=4, verbose=True, provider=provider)


if __name__ == "__main__":
    main()
