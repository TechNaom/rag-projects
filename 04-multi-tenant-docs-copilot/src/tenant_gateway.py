"""
tenant_gateway.py
-----------------
The single, narrow doorway between a request and a tenant's data.

Every retrieval in this system goes through `TenantGateway.retrieve()`. Given a
`tenant_id` and a query, the gateway resolves ONLY that tenant's collection and
that tenant's embedder, embeds the query with that tenant's fitted model, and
queries that tenant's collection. There is deliberately no method, argument, or
branch that lets a gateway bound to tenant A read from tenant B's collection.

Why a gateway object at all, instead of a bare function? Two reasons that
matter in real multi-tenant systems:

1. Binding. A `TenantGateway` is constructed for exactly one tenant and holds
   no way to switch. Application code passes around a gateway that is already
   scoped, so the "which tenant?" decision is made once, at the trust boundary,
   not re-derived on every call where it could be gotten wrong.

2. Auditability. Because all retrieval funnels through one place, this is the
   natural spot to add per-tenant authorization, rate limiting, and query
   logging in production (see the README's "What would change for production").

The tenant list is validated against the tenants that actually have a built
vector store, so an unknown or spoofed tenant_id fails closed with a clear
error rather than silently returning nothing.
"""

from dataclasses import dataclass
from typing import List, Optional

from ingest import list_tenants
from vectorstore import load_tenant_vectorstore


@dataclass
class RetrievedChunk:
    text: str
    tenant_id: str
    source_file: str
    section: str
    score: float  # cosine similarity, higher = more relevant


class UnknownTenantError(ValueError):
    """Raised when a tenant_id has no built vector store (fail closed)."""


class TenantGateway:
    """A retrieval handle bound to exactly one tenant. Cannot cross tenants."""

    def __init__(self, tenant_id: str):
        known = set(list_tenants())
        if tenant_id not in known:
            raise UnknownTenantError(
                f"Unknown tenant '{tenant_id}'. Known tenants: {sorted(known)}"
            )
        # Bound once, at construction. There is no setter to change it later.
        self._tenant_id = tenant_id
        # Resolve this tenant's — and only this tenant's — collection + embedder.
        self._collection, self._embedder = load_tenant_vectorstore(tenant_id)

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    def retrieve(self, query: str, k: int = 4) -> List[RetrievedChunk]:
        """Retrieve the top-k chunks for this tenant, from this tenant's collection only."""
        query_vector = self._embedder.embed_query(query)
        results = self._collection.query(
            query_embeddings=[query_vector],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        chunks: List[RetrievedChunk] = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            # Chroma returns cosine *distance*; similarity = 1 - distance
            similarity = 1 - dist
            chunks.append(RetrievedChunk(
                text=doc,
                tenant_id=meta.get("tenant_id", self._tenant_id),
                source_file=meta.get("source_file", "unknown"),
                section=meta.get("section", ""),
                score=round(similarity, 3),
            ))

        # Belt-and-suspenders assertion: a bound gateway must never surface a
        # chunk stamped with another tenant's id. If the invariant is ever
        # violated (e.g. a build bug), fail loudly instead of leaking.
        for c in chunks:
            if c.tenant_id != self._tenant_id:
                raise RuntimeError(
                    f"Tenant isolation violated: gateway for '{self._tenant_id}' "
                    f"retrieved a chunk owned by '{c.tenant_id}'."
                )
        return chunks


def get_gateway(tenant_id: str) -> TenantGateway:
    """Convenience factory: resolve a tenant_id to its bound gateway."""
    return TenantGateway(tenant_id)


def retrieve(tenant_id: str, query: str, k: int = 4) -> List[RetrievedChunk]:
    """One-shot retrieval helper for a tenant. Builds a bound gateway and queries it."""
    return get_gateway(tenant_id).retrieve(query, k=k)


if __name__ == "__main__":
    for slug in list_tenants():
        gw = get_gateway(slug)
        hits = gw.retrieve("How do I get started?", k=3)
        print(f"\n[{slug}] top chunks for 'How do I get started?'")
        for i, c in enumerate(hits, 1):
            print(f"  [{i}] score={c.score}  {c.source_file}  ({c.section})")
