architecture_explainer = """
Northkeep Policy Assistant

Documents:
The assistant uses synthetic banking HR and compliance Markdown policies.

Chunking:
The ingestion code splits policies into retrievable chunks while preserving
source file and section metadata.

Retrieval:
The project embeds chunks with local TF-IDF + SVD vectors and stores them in
ChromaDB. At question time, it retrieves the top matching chunks.

Prompting:
The prompt tells the model to answer only from retrieved context and cite policy
sources. If the answer is missing, the assistant should say so.

Evaluation:
The eval script uses a golden set of questions and expected source documents.
It reports Recall@K and MRR, exposing weak spots such as training-policy misses.

Next engineering decision:
Add a reranking experiment and compare eval results before changing the rest of
the system.
"""

print(architecture_explainer)

