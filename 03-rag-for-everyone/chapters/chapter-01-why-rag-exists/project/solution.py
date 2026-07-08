architecture_brief = """
Production RAG Architecture Brief

Scenario:
Northkeep HR & Compliance Policy Assistant.

User and risk profile:
Employees ask about leave, benefits, expense, privacy, whistleblower, and
compliance policies. Risk is medium to high because wrong answers can create
HR, legal, compliance, or trust issues.

Trusted source documents:
The assistant uses synthetic banking HR and compliance Markdown policies.

Metadata and access control:
Each chunk should preserve source file, section, policy ID, policy title,
version, and any role-based access rules. A real system would filter retrieval
by employee role and policy visibility.

Retrieval flow:
The ingestion code splits policies into retrievable chunks while preserving
source file and section metadata. The project embeds chunks with local TF-IDF +
SVD vectors and stores them in ChromaDB. At question time, it retrieves the top
matching chunks.

Prompt rules and refusal behavior:
The prompt tells the model to answer only from retrieved context and cite policy
sources. If the answer is missing, role-restricted, or ambiguous, the assistant
should say so and route the user to HR/compliance.

Evaluation cases and metrics:
The eval script uses a golden set of questions and expected source documents.
It reports Recall@K and MRR, exposing weak spots such as training-policy misses.
Additional evals should check citation correctness and refusal behavior.

Human escalation path:
Questions involving legal interpretation, retaliation, customer privacy, or
regulatory reporting should include a human escalation path.

Next engineering decision:
Add a reranking experiment and compare eval results before changing the rest of
the system.
"""

print(architecture_brief)
