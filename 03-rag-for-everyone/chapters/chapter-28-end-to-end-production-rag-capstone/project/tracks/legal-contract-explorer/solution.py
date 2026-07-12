"""Legal Contract Explorer — reference solution (pure Python standard library).

Capstone track: clause-level retrieval and side-by-side contract comparison for
legal ops / procurement. Given a clause topic (e.g. "termination for
convenience" or "liability cap"), retrieve the single best-matching clause from
EVERY contract in the corpus, then render an apples-to-apples comparison table.
Contracts that have no clause relevant to the topic are not silently dropped —
they are flagged as a review-queue item.

Zero dependencies. TF-IDF and cosine similarity are hand-rolled with `re`,
`math`, and `collections` so any learner can run this with no `pip install`.

Run it:

    python solution.py

Two design choices worth calling out (both are the point of the track):

1. Hierarchical / clause-level chunking (Ch.10). Each chunk is one numbered
   clause, but it never floats free of its context: every chunk carries its
   parent contract name and its section heading as metadata. "60 days notice"
   is meaningless until you know it is Brightwater's Term and Termination
   clause, so we keep that link on the chunk itself.

2. One-result-per-contract retrieval. A naive top-k search would return the
   five best clauses globally, which might all come from two contracts. For a
   side-by-side comparison we instead retrieve the best clause from each
   contract independently, then apply a relevance threshold so a contract that
   genuinely lacks the clause type gets flagged instead of matched to noise.
"""

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# A clause scoring below this cosine similarity is treated as "this contract has
# no clause on this topic" rather than a weak match. Tuned against the bundled
# corpus so that a genuinely missing clause (e.g. Cloudspire has no
# indemnification section) falls below it while real clauses stay above it.
RELEVANCE_THRESHOLD = 0.06

DATA_DIR = Path(__file__).parent / "contracts"

# A small, boring stopword list. Legal text is full of "shall", "party",
# "agreement" etc. — down-weighting them keeps retrieval focused on the words
# that actually distinguish one clause type from another.
STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "at", "by",
    "with", "as", "is", "are", "be", "been", "this", "that", "such", "any",
    "all", "shall", "will", "may", "not", "no", "if", "it", "its", "which",
    "from", "under", "into", "upon", "than", "then", "each", "other", "party",
    "parties", "agreement", "client", "services", "service",
}


@dataclass
class Clause:
    """One clause-level chunk that stays linked to its parent contract.

    This is the hierarchical-chunking payload: `text` is the small, precise
    child chunk, while `contract` + `section_heading` are the parent context
    that make the child safe to quote and compare.
    """

    contract: str            # parent contract name (from the "# Contract:" line)
    source_file: str         # provenance, for citations
    section_number: str      # e.g. "2"
    section_heading: str     # e.g. "Limitation of Liability"
    text: str                # the clause body
    vector: dict = field(default_factory=dict)  # sparse TF-IDF weights, filled later

    @property
    def clause_type(self):
        return self.section_heading


# --------------------------------------------------------------------------- #
# 1. Parsing + hierarchical clause-level chunking
# --------------------------------------------------------------------------- #

def parse_contract(path):
    """Split one markdown contract into clause-level chunks with parent context.

    The contract title comes from the `# Contract: ...` line; each `## N. Head`
    starts a new clause. Everything until the next `##` is that clause's body.
    """
    lines = path.read_text(encoding="utf-8").splitlines()

    contract_name = path.stem  # fallback
    for line in lines:
        if line.startswith("# "):
            contract_name = line[2:].strip()
            if contract_name.lower().startswith("contract:"):
                contract_name = contract_name.split(":", 1)[1].strip()
            break

    clauses = []
    current = None
    body_lines = []
    heading_re = re.compile(r"^##\s+(\d+)\.\s+(.*)$")

    def flush():
        if current is not None:
            clauses.append(
                Clause(
                    contract=contract_name,
                    source_file=path.name,
                    section_number=current[0],
                    section_heading=current[1],
                    text=" ".join(body_lines).strip(),
                )
            )

    for line in lines:
        match = heading_re.match(line)
        if match:
            flush()
            current = (match.group(1), match.group(2).strip())
            body_lines = []
        elif current is not None and not line.startswith("# "):
            if line.strip():
                body_lines.append(line.strip())
    flush()
    return clauses


def load_corpus(data_dir=DATA_DIR):
    """Load every contract in the data dir into a flat list of clause chunks."""
    clauses = []
    for path in sorted(data_dir.glob("*.md")):
        clauses.extend(parse_contract(path))
    return clauses


# --------------------------------------------------------------------------- #
# 2. Hand-rolled TF-IDF + cosine similarity (no numpy / sklearn)
# --------------------------------------------------------------------------- #

def tokenize(text):
    """Lowercase word tokens, stopwords removed. Deliberately simple."""
    tokens = re.findall(r"[a-z]+", text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def compute_idf(clauses):
    """Inverse document frequency across all clause chunks.

    idf(term) = log(N / df(term)). Rare, distinguishing terms get a high
    weight; terms that appear in almost every clause get a low one.
    """
    n_docs = len(clauses)
    doc_freq = defaultdict(int)
    for clause in clauses:
        for term in set(tokenize(clause.text)):
            doc_freq[term] += 1
    # +1 smoothing on the denominator so a term in every doc still gets a small
    # positive weight rather than exactly zero.
    return {term: math.log(n_docs / (1 + df)) + 1 for term, df in doc_freq.items()}


def tfidf_vector(text, idf):
    """Turn text into a sparse {term: weight} TF-IDF vector.

    Term frequency is normalized by the token count so long clauses don't win
    just for being long. Unknown query terms (idf lookup misses) are skipped.
    """
    tokens = tokenize(text)
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    vector = {}
    for term, count in counts.items():
        weight = (count / total) * idf.get(term, 0.0)
        if weight > 0:
            vector[term] = weight
    return vector


def cosine_similarity(a, b):
    """Cosine similarity between two sparse dict vectors."""
    if not a or not b:
        return 0.0
    # Iterate over the smaller vector for the dot product.
    if len(a) > len(b):
        a, b = b, a
    dot = sum(weight * b.get(term, 0.0) for term, weight in a.items())
    if dot == 0.0:
        return 0.0
    norm_a = math.sqrt(sum(w * w for w in a.values()))
    norm_b = math.sqrt(sum(w * w for w in b.values()))
    return dot / (norm_a * norm_b)


def build_index(clauses):
    """Fit TF-IDF on the corpus and attach a vector to every clause chunk."""
    idf = compute_idf(clauses)
    for clause in clauses:
        clause.vector = tfidf_vector(clause.text, idf)
    return idf


# --------------------------------------------------------------------------- #
# 3. One-result-per-contract retrieval + review-queue flagging
# --------------------------------------------------------------------------- #

@dataclass
class ContractMatch:
    contract: str
    source_file: str
    clause: Clause = None   # None => no relevant clause found
    score: float = 0.0

    @property
    def flagged_for_review(self):
        return self.clause is None


def compare_clause_across_contracts(query, clauses, idf, threshold=RELEVANCE_THRESHOLD):
    """For a clause-topic query, return the best clause from EACH contract.

    Retrieval is per-contract, not global top-k, so the comparison is
    apples-to-apples: exactly one row per contract. A contract whose best clause
    scores below `threshold` is returned as a flagged review item, not dropped.
    """
    query_vec = tfidf_vector(query, idf)

    # Group clauses by their parent contract, preserving corpus order.
    by_contract = defaultdict(list)
    order = []
    for clause in clauses:
        if clause.contract not in by_contract:
            order.append((clause.contract, clause.source_file))
        by_contract[clause.contract].append(clause)

    results = []
    for contract, source_file in order:
        best_clause = None
        best_score = 0.0
        for clause in by_contract[contract]:
            score = cosine_similarity(query_vec, clause.vector)
            if score > best_score:
                best_score = score
                best_clause = clause
        if best_clause is not None and best_score >= threshold:
            results.append(ContractMatch(contract, source_file, best_clause, best_score))
        else:
            results.append(ContractMatch(contract, source_file, None, best_score))

    # Matched contracts first (highest score at top), flagged ones after.
    results.sort(key=lambda r: (r.flagged_for_review, -r.score))
    return results


# --------------------------------------------------------------------------- #
# 4. Rendering
# --------------------------------------------------------------------------- #

def _excerpt(text, max_chars=180):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return cut + " ..."


def render_comparison(query, results):
    """Render a readable Markdown side-by-side comparison + review queue."""
    lines = []
    lines.append(f"## Clause comparison: \"{query}\"")
    lines.append("")
    lines.append("| Contract | Matched clause | Score | Excerpt |")
    lines.append("| --- | --- | --- | --- |")

    review_queue = []
    for r in results:
        if r.flagged_for_review:
            review_queue.append(r)
            lines.append(
                f"| {r.contract} | NO CLAUSE FOUND | {r.score:.3f} "
                f"| _flagged for review_ |"
            )
        else:
            clause = r.clause
            label = f"§{clause.section_number} {clause.section_heading}"
            lines.append(
                f"| {r.contract} | {label} | {r.score:.3f} "
                f"| {_excerpt(clause.text)} |"
            )

    lines.append("")
    matched = [r for r in results if not r.flagged_for_review]
    lines.append(
        f"**Coverage:** {len(matched)} of {len(results)} contracts have a clause "
        f"on this topic."
    )
    if review_queue:
        lines.append("")
        lines.append("**Review queue (missing clause — do not assume silence = agreement):**")
        for r in review_queue:
            lines.append(
                f"- {r.contract} ({r.source_file}) — no clause matched "
                f"\"{query}\" above threshold {RELEVANCE_THRESHOLD:.2f} "
                f"(best score {r.score:.3f}). A human should confirm whether this "
                f"protection is truly absent."
            )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #

DEMO_QUERIES = [
    "limitation of liability cap on damages",
    "indemnification hold harmless third-party claims",
    "termination for convenience notice period",
]


def main():
    clauses = load_corpus()
    idf = build_index(clauses)

    contracts = sorted({c.contract for c in clauses})
    print(f"Loaded {len(clauses)} clause chunks from {len(contracts)} contracts.")
    print("Contracts:")
    for name in contracts:
        print(f"  - {name}")
    print()

    for query in DEMO_QUERIES:
        results = compare_clause_across_contracts(query, clauses, idf)
        print(render_comparison(query, results))
        print()
        print("-" * 78)
        print()


if __name__ == "__main__":
    main()
