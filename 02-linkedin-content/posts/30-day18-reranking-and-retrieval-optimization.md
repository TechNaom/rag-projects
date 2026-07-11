📘 RAG for Everyone | Day 18/30

🎚️ Before: retrieve 5 chunks, hope they're the right 5. After: retrieve 30 chunks cheaply, then spend real compute figuring out which 5 actually deserve to be in the prompt.

Today you'll learn:
✅ The "retrieve-many-return-few" pattern
✅ What a cross-encoder does that embedding search can't
✅ The latency trade-off you're accepting when you add this step

Why your first-pass ranking isn't your best ranking 📉
Vector search ranks chunks by how close their embedding is to the query's embedding — computed independently, one comparison at a time. That's fast enough to search millions of chunks. It's also a coarser signal than it feels like: it never actually reads the query and the chunk together.

What reranking adds 🔬
A cross-encoder does exactly that — it takes the query and a candidate chunk together as one input and scores their relevance jointly, catching relationships a distance-based comparison misses. It's far more accurate. It's also far more expensive per comparison, which is why nobody runs it against the whole corpus.

The pattern that makes it affordable ⚙️
→ Retrieve many — pull, say, 30–50 candidates cheaply with vector or hybrid search
→ Rerank — run the expensive cross-encoder only on that shortlist, not the full index
→ Return few — keep the top handful after reranking, the ones that actually deserve prompt space

The trade-off, honestly 📊
This step adds latency — you're now paying for an extra scoring pass on every query, not just at index time. Whether that's worth it depends entirely on your accuracy bar and your latency budget. For a compliance-sensitive system where a wrong retrieved chunk means a wrong cited policy, the extra hundreds of milliseconds are usually a easy trade. For a chat feature where users expect instant replies, it might not be.

The bottom line 💡
Reranking isn't about replacing your retriever — it's about not fully trusting its first pass. Retrieve broad and cheap, then spend your compute budget where it counts: getting the final shortlist right.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-18-reranking-and-retrieval-optimization
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #Reranking #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
