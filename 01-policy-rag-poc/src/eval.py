"""
eval.py
-------
Retrieval evaluation: a small "golden set" of (question, expected source
document) pairs, used to measure whether the retriever actually surfaces
the right document — independent of whether generation is available.

This is the part of a RAG build that gets skipped most often, and it's the
part that actually tells you whether your system works. A demo where you
manually try five queries and eyeball the results is not evaluation - it's
a sanity check.

Metric used: Recall@k (did the expected source file appear anywhere in the
top-k retrieved chunks?) and MRR (Mean Reciprocal Rank - rewards the
expected source appearing higher, not just present).
"""

from rag_chain import retrieve

# Golden set: (query, expected_source_file). Each question is paraphrased,
# not copy-pasted from the document, since real user questions never match
# document wording exactly - that's the actual point of semantic retrieval.
GOLDEN_SET = [
    ("How many vacation days do I get after 5 years here?", "03_leave_time_off.md"),
    ("What's the cap on a client dinner before I need approval?", "05_expense_travel.md"),
    ("Can my manager see my PTO requests before approving them?", "03_leave_time_off.md"),
    ("Someone offered me a $200 gift card for approving their loan faster. What do I do?", "02_conflicts_insider_trading.md"),
    ("I saw a coworker looking up their ex's account balance for no work reason - is that a problem?", "08_data_privacy_confidentiality.md"),
    ("Is it true I can report fraud straight to the SEC without telling my boss first?", "10_whistleblower_policy.md"),
    ("How many paid weeks do I get if I'm not the primary parent after having a baby?", "03_leave_time_off.md"),
    ("Do I need a doctor's note if I'm out sick for two days?", "03_leave_time_off.md"),
    ("What's the company match if I put 6% of my salary into retirement?", "04_health_wellness_benefits.md"),
    ("Can I retweet a customer complaint to defend the bank?", "11_social_media_external_comms.md"),
    ("If I get a bad performance rating, how soon do I hear about a PIP?", "12_performance_review_promotion.md"),
    ("Do I have to be in the office a set number of days if I'm hybrid?", "06_remote_hybrid_work.md"),
    ("What training do branch tellers need that other employees don't?", "09_compliance_training.md"),
    ("Is workplace harassment training mandatory and how often?", "09_compliance_training.md"),
    ("Can I be punished for reporting my manager if it turns out I was wrong but believed it at the time?", "10_whistleblower_policy.md"),
]


def evaluate(k: int = 3):
    hits = 0
    reciprocal_ranks = []
    print(f"{'='*70}\nRETRIEVAL EVALUATION  (k={k}, n={len(GOLDEN_SET)} questions)\n{'='*70}\n")

    for query, expected_source in GOLDEN_SET:
        chunks = retrieve(query, k=k)
        retrieved_sources = [c.source_file for c in chunks]

        rank = None
        for i, src in enumerate(retrieved_sources, 1):
            if src == expected_source:
                rank = i
                break

        hit = rank is not None
        hits += hit
        reciprocal_ranks.append(1 / rank if hit else 0)

        status = f"HIT  (rank {rank})" if hit else "MISS"
        print(f"[{status:14s}] {query}")
        print(f"                expected: {expected_source}")
        print(f"                got:      {retrieved_sources}\n")

    recall_at_k = hits / len(GOLDEN_SET)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print(f"{'='*70}")
    print(f"Recall@{k}: {recall_at_k:.1%}  ({hits}/{len(GOLDEN_SET)})")
    print(f"MRR:       {mrr:.3f}")
    print(f"{'='*70}")
    return recall_at_k, mrr


if __name__ == "__main__":
    evaluate(k=3)
