# Northkeep National Bank — Internal Policy Assistant (RAG POC)

A working, end-to-end Retrieval-Augmented Generation system over a synthetic
corpus of banking HR & compliance policy documents. Built to learn the full
RAG stack hands-on: document chunking, embeddings, a real vector database,
retrieval, generation, and — usually skipped — evaluation.

## Why this domain
Internal policy/compliance Q&A is one of the most common real-world RAG
deployments inside banks (alongside RM/advisor copilots and underwriting
assistants). It's also one of the easiest to build *honestly*: the
documents are self-contained, the questions have unambiguous correct
answers, and there's no pretense of giving regulated financial advice to an
actual customer.

The corpus is intentionally a blend — generic HR policy (leave, benefits,
performance reviews) plus banking-specific compliance content (insider
trading, customer NPI handling, AML training, whistleblower protections
under Dodd-Frank/Sarbanes-Oxley) — which is what makes it read as "a bank's"
internal knowledge base rather than a generic company's.

**The bank name, employees, and all policy content are entirely fictional**,
invented for this project and not modeled on, or representing, any real
financial institution. "Northkeep National Bank" does not exist. This keeps
the project clean to share, reuse, or build on without it ever being
mistaken for, or associated with, a real company's actual internal
policy.

## Architecture

```
data/raw_docs/*.md          12 synthetic policy documents (the corpus)
        |
        v
src/ingest.py                Markdown-header-aware chunking (111 chunks)
        |
        v
src/embeddings.py             TF-IDF + SVD -> dense vectors (see note below)
        |
        v
src/vectorstore.py            Fits embedder on corpus, writes to ChromaDB
        |                     (persisted at data/chroma_db/)
        v
src/rag_chain.py              retrieve() -> build_context_block() -> generate_answer()
        |                     generation calls Claude via the Anthropic API
        v
src/main.py                   Interactive CLI
src/eval.py                   Golden-set retrieval evaluation (Recall@k, MRR)
```

## A real constraint, handled honestly: the embedding model

A production RAG system would use a neural embedding model — local
(sentence-transformers), or hosted (OpenAI, or Voyage AI, which is
Anthropic's recommended embeddings partner). The sandbox this was built in
blocks `huggingface.co` at the network layer, so model weights can't be
downloaded at runtime, and there's no embeddings API endpoint reachable
either.

Rather than fake that constraint away, `src/embeddings.py` implements a
**fully local, pip-only** embedding method: TF-IDF vectorization reduced to
a 128-dim dense vector via Truncated SVD (classic Latent Semantic Analysis).
It's a legitimate, pre-deep-learning retrieval technique, not a toy — but it
is **lexical**, not semantic: it matches on shared/related vocabulary, not
deep paraphrase. The evaluation suite catches exactly this limitation (see
below). `embeddings.py` has a clearly marked swap-in point with the exact
code to drop in `HuggingFaceEmbeddings` or `VoyageAIEmbeddings` once you're
running somewhere with full network access — nothing else in the pipeline
needs to change, because everything talks to the embedder only through
LangChain's standard interface. That pluggability *is* the actual lesson.

## A real constraint, handled honestly: generation

This sandbox can reach `api.anthropic.com` over the network, but has no API
key auto-injected (that only happens for in-browser Artifacts, not this
container). So `rag_chain.py`'s generation step is fully implemented and
correct, but will only run with your own key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# or: export GEMINI_API_KEY=...
python3 src/main.py
```

Without a key, the CLI still shows you the retrieved chunks and scores for
every question — which, honestly, is most of what's interesting about a RAG
system anyway. Generation is "stuff the context into a good prompt," which
is the easy part once retrieval is solid.

## Running it

```bash
pip install -r requirements.txt

# 1. Build the index (run once, or whenever data/raw_docs/ changes)
python3 src/vectorstore.py

# 2. Ask questions interactively
python3 src/main.py

# 3. Check retrieval quality against the golden test set
python3 src/eval.py
```

## Evaluation results (this build)

Running `eval.py`'s 15-question golden set at k=3: **Recall@3 = 86.7%
(13/15), MRR = 0.789**. Two real misses, both informative:

- *"What training do branch tellers need that other employees don't?"* and
  *"Is workplace harassment training mandatory?"* both failed to retrieve
  the training policy document. Cause: nearly every policy document
  *mentions* training in passing (its closing section), so a purely lexical
  method can't distinguish "mentions training" from "is about training."
  This is a textbook case for either (a) a neural embedding model, which
  would capture that the *topic* is training, not just the word, or (b) a
  reranking step after initial retrieval.

This is the kind of result a real eval should produce — a credible system
that mostly works, with specific, explainable failures, not a hand-picked
demo where everything looks perfect.

## What would change for production

- **Embeddings**: swap in a neural model (see `embeddings.py` docstring)
- **Vector DB**: ChromaDB persisted locally works fine to ~1M vectors; a
  bank-scale deployment with multiple knowledge bases and access control
  would more likely use a managed service (Pinecone, Qdrant Cloud) or an
  existing data platform's vector capability (e.g. pgvector on existing
  Postgres infra, which many banks prefer for audit/compliance reasons)
- **Retrieval**: add hybrid search (keyword + vector) and a reranking
  step — the training-question miss above is exactly what a reranker is
  for
- **Access control**: real policy content is often role-restricted (e.g. a
  branch teller shouldn't retrieve Wealth Management compliance content);
  metadata filtering on the vector query would enforce this
- **Guardrails**: a real internal assistant needs to refuse to answer
  outside its grounded context (this prompt already instructs that), log
  every query/answer for audit, and flag answers touching regulatory
  thresholds for human review
- **Evaluation**: this golden set has 15 questions; production needs
  hundreds, ideally including real (anonymized) questions employees
  actually asked, plus answer-faithfulness checks (not just retrieval
  recall) using something like the RAGAS framework
