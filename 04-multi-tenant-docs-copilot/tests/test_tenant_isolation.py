"""
test_tenant_isolation.py
------------------------
THE key proof point of this project.

We build all three tenants' isolated vector stores, then for each tenant fire a
handful of queries — deliberately including queries phrased to sound like ANOTHER
tenant's content — and assert that every retrieved chunk belongs to a document
the querying tenant actually owns. If a single foreign chunk ever came back, the
isolation claim would be false and this test would fail.

Because each tenant is a separate Chroma collection in a separate directory,
there is no query that can return another tenant's rows — this test verifies
that structural guarantee holds end to end, through the real gateway code path.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import ingest
import vectorstore
from tenant_gateway import UnknownTenantError, get_gateway


@pytest.fixture(scope="module", autouse=True)
def built_stores():
    """Build every tenant's vector store once for this test module."""
    vectorstore.build_all_vectorstores(rebuild=True)
    yield
    vectorstore.clear_vectorstore_cache()


def _owned_source_files(tenant_id: str):
    """The set of .md filenames that genuinely belong to a tenant."""
    docs_dir = ingest.TENANTS_DIR / tenant_id
    return {p.name for p in docs_dir.glob("*.md")}


# Cross-tenant "bait" queries: each is worded to resemble a DIFFERENT tenant's
# content, to make sure retrieval can't be lured across the boundary.
BAIT_QUERIES = [
    "How long does the drone fly on one battery and how do I launch a survey mission?",
    "What are the consultant day rates and the discount approval thresholds?",
    "Who is eligible for a grant and what is the disbursement schedule?",
    "How do I rotate an API bearer token and handle a 429 rate limit?",
    "What is the escalation path when a client sponsor is unhappy?",
    "What counts as an ineligible cost and how much overhead is allowed?",
]


def test_all_tenants_built():
    tenants = ingest.list_tenants()
    assert set(tenants) == {"starlight-robotics", "aldergate-partners", "riverbend-trust"}


def test_no_cross_tenant_leakage():
    tenants = ingest.list_tenants()
    for tenant_id in tenants:
        owned = _owned_source_files(tenant_id)
        gateway = get_gateway(tenant_id)
        for query in BAIT_QUERIES:
            chunks = gateway.retrieve(query, k=5)
            assert chunks, f"expected retrieval to return something for '{tenant_id}'"
            for c in chunks:
                # 1. Every chunk is stamped with the querying tenant's id.
                assert c.tenant_id == tenant_id, (
                    f"tenant '{tenant_id}' retrieved a chunk owned by '{c.tenant_id}'"
                )
                # 2. Every retrieved source file is one this tenant actually owns.
                assert c.source_file in owned, (
                    f"tenant '{tenant_id}' retrieved foreign source '{c.source_file}'; "
                    f"owned files are {sorted(owned)}"
                )


def test_source_file_sets_are_disjoint():
    """Sanity check: the three tenants share no filenames, so a leak is detectable."""
    tenants = ingest.list_tenants()
    seen = {}
    for tenant_id in tenants:
        for name in _owned_source_files(tenant_id):
            seen.setdefault(name, set()).add(tenant_id)
    # No filename should be claimed by more than one tenant.
    shared = {name: owners for name, owners in seen.items() if len(owners) > 1}
    assert not shared, f"tenants share filenames, weakening the test: {shared}"


def test_unknown_tenant_fails_closed():
    with pytest.raises(UnknownTenantError):
        get_gateway("acme-that-does-not-exist")
