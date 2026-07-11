📘 RAG for Everyone | Day 17/30

⚔️ Keyword search vs. semantic search isn't actually a competition you need to win. It's a false choice — the best production systems run both, at the same time, on purpose.

Today you'll learn:
✅ Why dense and sparse search fail differently
✅ How Reciprocal Rank Fusion merges them into one ranking
✅ What query routing adds on top

Two searches, two different blind spots 🔍
→ Dense search (embeddings) — finds meaning even with zero shared words. Its blind spot: exact identifiers. Ask for "policy HR-2024-011" and a purely semantic search may not treat that code as special — it's just more text to embed.
→ Sparse search (keyword-based, e.g. BM25) — nails exact terms, codes, and names with precision. Its blind spot: synonyms and paraphrasing, exactly what dense search is good at.

Run both, then merge with Reciprocal Rank Fusion ➕
Instead of picking one, hybrid search runs both retrieval methods and combines their rankings. Reciprocal Rank Fusion (RRF) converts each method's ranked list into normalized scores and merges them — so a chunk that ranks well in either search (or both) surfaces near the top, without needing to hand-tune how much to "trust" each method.

Query routing — the layer above both 🚦
Not every question needs both engines run at full cost. Query routing looks at a query's characteristics and decides where to send it — a document-code lookup might route straight to sparse search; a "what's our policy on..." question might route to dense, or to both with RRF merging the result. This is also where risk routing lives: flagging queries that need extra scrutiny before they're answered at all.

The bottom line 💡
Dense and sparse search aren't rivals — they're complementary error correctors for each other's weak spots. Hybrid search plus RRF isn't an "advanced" feature to bolt on later; it's often the single highest-leverage upgrade over a single-method retriever.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-17-hybrid-search-and-query-routing
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #HybridSearch #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
