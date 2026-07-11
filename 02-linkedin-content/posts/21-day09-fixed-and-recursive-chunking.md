📘 RAG for Everyone | Day 9/30

✂️ "Chunking turns parsed documents into retrieval units." One sentence. It's also where a huge chunk (pun intended) of RAG quality problems actually start.

Today you'll learn:
✅ What chunking is really doing to your documents
✅ Fixed-size vs. recursive chunking, side by side
✅ Why the "simple" default isn't always the safe default

Two ways to cut, side by side 📐
Fixed-size chunking — split every N characters or tokens, regardless of what's on the page.
+ Dead simple, fast, predictable chunk sizes
- Slices straight through sentences, tables, and clauses with zero regard for meaning

Recursive chunking — split along a hierarchy of separators (paragraphs, then sentences, then words), falling back only when a piece is still too big.
+ Respects natural document structure far more often
- More logic to get right, and still imperfect on messy source formatting

Why this isn't a solved problem 🧩
A chunk is the atomic unit your retriever can return. Cut a policy clause in half with fixed-size chunking, and you can retrieve the "if" without the "then" — a technically-correct-looking passage that's actually missing the condition that changes its meaning. Recursive chunking reduces this, but it's still a heuristic, not a guarantee.

Real numbers 📊
Northkeep's 12 policy documents became 111 chunks — a ratio of roughly 9 chunks per document. That number isn't arbitrary; it's a direct consequence of the chunking strategy and size chosen. Chunk too coarse and you retrieve noise along with the answer. Chunk too fine and you lose the surrounding context that makes the answer make sense.

The bottom line 💡
Chunking strategy isn't a preprocessing detail you set once and forget — it's a design decision with a direct line to your retrieval accuracy. Fixed-size gets you moving fast; recursive gets you closer to chunks that actually respect what the document is saying.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-09-fixed-and-recursive-chunking
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #Chunking #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
