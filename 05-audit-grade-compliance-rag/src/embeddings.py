"""
embeddings.py
-------------
A locally-computed embedding model, implementing LangChain's `Embeddings`
interface (embed_documents / embed_query), with NO external network calls.

WHY THIS EXISTS (read this before judging the design):
In a normal environment you'd use a neural embedding model — sentence-transformers
(local), OpenAI text-embedding-3, or Voyage AI (Anthropic's recommended partner).
This sandbox's egress proxy blocks huggingface.co, so model weights can't be
downloaded at runtime. Rather than fake it, this module uses a classic,
fully-local technique: TF-IDF vectorization + Truncated SVD (a form of Latent
Semantic Analysis) to produce fixed-size dense vectors from pure scikit-learn,
which only needs PyPI (allowed).

This is a legitimate, pre-deep-learning embedding technique — it captures
lexical/topical similarity well (good enough to demonstrate retrieval over
clearly-distinct policy documents) but won't capture deep semantic paraphrase
the way a neural embedding would (e.g. it won't strongly connect "time off"
and "vacation" unless both words co-occur enough in the corpus).

>>> SWAP-IN POINT FOR PRODUCTION <<<
To upgrade this to a real neural embedding model once you have full network
access (e.g. running locally, in Claude Code, or in any unrestricted
environment), replace this class with:

    from langchain_huggingface import HuggingFaceEmbeddings
    embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

or for a hosted API:

    from langchain_voyageai import VoyageAIEmbeddings
    embedder = VoyageAIEmbeddings(model="voyage-3", api_key=...)

Everything downstream (vectorstore.py, rag_chain.py) talks to this class only
through the standard `embed_documents`/`embed_query` interface, so swapping
the implementation requires no other code changes. That interface contract
IS the actual lesson here — production RAG systems are built so the
embedding model is a pluggable component, not the application's core
abstraction.
"""

import pickle
from pathlib import Path
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize


class LocalTfidfEmbeddings:
    """LangChain-compatible embedding class backed by TF-IDF + SVD.

    Must be `fit()` once on the full corpus before use (this mirrors how a
    neural embedding model is "pretrained" — except here we're fitting our
    own tiny model on this specific document set, which is also a real
    pattern for domain-specific retrieval in low-resource settings).
    """

    def __init__(self, n_components: int = 128, random_state: int = 42):
        self.n_components = n_components
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),     # unigrams + bigrams capture phrases like "sick leave"
            max_df=0.9,
            min_df=1,
        )
        self.svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        self._fitted = False

    def fit(self, texts: List[str]) -> "LocalTfidfEmbeddings":
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        # SVD component count can't exceed min(n_samples, n_features) - 1
        max_components = min(tfidf_matrix.shape) - 1
        if self.n_components > max_components:
            self.svd = TruncatedSVD(n_components=max_components, random_state=42)
        self.svd.fit(tfidf_matrix)
        self._fitted = True
        return self

    def _embed(self, texts: List[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("Embedder must be fit() on the corpus before embedding.")
        tfidf_matrix = self.vectorizer.transform(texts)
        dense = self.svd.transform(tfidf_matrix)
        return normalize(dense)  # cosine similarity == dot product after L2 normalization

    # --- LangChain Embeddings interface ---
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0].tolist()

    # --- persistence so query-time embedding uses the exact same fitted model ---
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(
                {"vectorizer": self.vectorizer, "svd": self.svd, "n_components": self.n_components},
                f,
            )

    @classmethod
    def load(cls, path: str) -> "LocalTfidfEmbeddings":
        with open(path, "rb") as f:
            state = pickle.load(f)
        obj = cls(n_components=state["n_components"])
        obj.vectorizer = state["vectorizer"]
        obj.svd = state["svd"]
        obj._fitted = True
        return obj
