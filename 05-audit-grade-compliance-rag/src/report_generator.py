"""
report_generator.py
-------------------
Renders a human-readable Markdown "audit report" for a single answered query —
the artifact a compliance reviewer actually reads to decide whether they trust
an answer. Given a trace record (or a live query, which it re-runs), it lays
out:

  * the question and the generated answer
  * every piece of evidence used (doc_id, version, effective_date, status, and
    the exact excerpt), with a per-chunk currency proof
  * the L1-L4 citation-support check results
  * a plain-English verdict a non-engineer can act on

The report is deterministic given a trace record, so re-rendering an archived
trace always produces the same document — which is what makes it usable as
audit evidence rather than a one-off print-out.
"""

from typing import Dict, Optional

from citation_auditor import CitationAuditResult, LevelResult
from currency_filter import RetrievedChunk, verify_currency


def _plain_english_verdict(record: Dict) -> str:
    audit = record["citation_audit"]
    level = audit["highest_level"]
    chunks = record["retrieved_chunks"]
    current_sources = sorted({
        f"{c['doc_id']} v{c['version']}" for c in chunks if c["status"] == "current"
    })
    superseded_sources = sorted({
        f"{c['doc_id']} v{c['version']}" for c in chunks if c["status"] == "superseded"
    })

    if level >= 4:
        src = ", ".join(current_sources) or "the retrieved policy"
        return (
            f"TRUSTED (L4). This answer is grounded in currently-effective policy "
            f"{src}, every claim is cited, and each citation's key facts were found "
            f"in the cited excerpt. No superseded material was used."
        )
    if level == 3:
        src = ", ".join(current_sources) or "the retrieved policy"
        return (
            f"SUPPORTED (L3). Every claim is cited and the citations' key terms match "
            f"the evidence ({src}), but at least one cited source was not confirmed "
            f"current — review the currency proofs below before relying on it."
        )
    if level == 2:
        return (
            "PARTIALLY VERIFIED (L2). Every claim carries a citation, but the "
            "keyword-overlap check could not confirm that each cited excerpt "
            "actually supports its claim. A human should read the excerpts below."
        )
    if level == 1:
        return (
            "WEAK (L1). The answer cites at least one source, but not every claim is "
            "cited. Do not treat this as audit-grade without manual review."
        )
    warn = ""
    if superseded_sources:
        warn = f" Note: retrieval surfaced SUPERSEDED material ({', '.join(superseded_sources)})."
    return (
        "UNCITED (L0). The answer contains no resolvable citation to the evidence. "
        "It must not be used for a compliance decision." + warn
    )


def render_report(record: Dict) -> str:
    """Render a trace record into a Markdown audit report string."""
    audit = record["citation_audit"]
    chunks = record["retrieved_chunks"]

    lines = []
    lines.append("# Audit-Grade Answer Report")
    lines.append("")
    lines.append(f"- **Generated (UTC):** {record['timestamp']}")
    lines.append(f"- **Provider:** {record.get('provider') or 'n/a'}")
    lines.append(f"- **Currency scope:** "
                 + ("all versions (include_superseded=True)" if record.get("include_superseded")
                    else "current versions only"))
    lines.append(f"- **Citation grade:** **{audit['summary']}**")
    lines.append(f"- **Trace signature:** `{record.get('signature', 'n/a')}`")
    lines.append("")

    lines.append("## Question")
    lines.append("")
    lines.append(f"> {record['query']}")
    lines.append("")

    lines.append("## Answer")
    lines.append("")
    lines.append(record["answer"].strip() or "_(no answer text)_")
    lines.append("")

    lines.append("## Evidence used")
    lines.append("")
    if not chunks:
        lines.append("_No evidence chunks were retrieved._")
        lines.append("")
    for i, c in enumerate(chunks, 1):
        status_badge = "CURRENT" if c["status"] == "current" else c["status"].upper()
        lines.append(f"### [{i}] {c['doc_id']} v{c['version']} — {status_badge}")
        lines.append("")
        lines.append(f"- **Title:** {c['title'] or c.get('source_file', '')}")
        lines.append(f"- **Section:** {c['section'] or 'n/a'}")
        lines.append(f"- **Effective date:** {c['effective_date'] or 'n/a'}")
        lines.append(f"- **Retrieval score (cosine sim):** {c['score']}")
        if c["status"] == "current":
            lines.append(f"- **Currency proof:** {c['doc_id']} v{c['version']} is the CURRENT "
                         f"authoritative version (effective {c['effective_date']}, not superseded).")
        else:
            repl = c["superseded_by"] or "an unspecified newer version"
            lines.append(f"- **Currency proof:** SUPERSEDED — replaced by {repl}. "
                         f"Must not ground a current-state answer.")
        lines.append("")
        lines.append("> " + c["excerpt"].strip().replace("\n", "\n> "))
        lines.append("")

    lines.append("## Citation-support checks (L1-L4)")
    lines.append("")
    lines.append("| Level | Check | Result | Detail |")
    lines.append("|-------|-------|--------|--------|")
    for lvl in audit["levels"]:
        mark = "PASS" if lvl["passed"] else "FAIL"
        detail = lvl["detail"].replace("|", "\\|")
        lines.append(f"| {lvl['level']} | {lvl['name']} | {mark} | {detail} |")
    lines.append("")
    lines.append("> L3 is a keyword/number-overlap **heuristic**, not semantic entailment. "
                 "See `citation_auditor.py`.")
    lines.append("")

    lines.append("## Reviewer verdict")
    lines.append("")
    lines.append(_plain_english_verdict(record))
    lines.append("")

    return "\n".join(lines)


def generate_report_for_query(
    query: str,
    k: int = 4,
    include_superseded: bool = False,
    provider: Optional[str] = None,
) -> str:
    """Re-run a query end-to-end (retrieve -> generate -> audit -> trace) and
    render its audit report. Imported lazily to avoid a circular import."""
    from rag_chain import answer_question

    result = answer_question(
        query, k=k, verbose=False, provider=provider,
        include_superseded=include_superseded, write_trace=True,
    )
    return render_report(result["trace"])


if __name__ == "__main__":
    import sys
    question = " ".join(sys.argv[1:]) or "How long must adult patient medical records be retained?"
    print(generate_report_for_query(question))
