📘 RAG for Everyone | Day 10/30

🧩 Not every document is a flat wall of text. Contracts have clauses inside sections inside articles. Fixed-size and recursive chunking (Day 9) don't know that structure exists. Today's techniques do.

Today you'll learn:
✅ What semantic chunking actually preserves
✅ What hierarchical chunking adds on top of it
✅ When "advanced" chunking is worth the extra complexity

Two upgrades, two different problems 🔍
Semantic chunking splits by meaning, not by character count — it tries to keep a chunk boundary at a genuine topic shift instead of an arbitrary cut-off. The goal: preserve topic boundaries, so a chunk doesn't start mid-idea.

Hierarchical chunking goes further — it keeps parent-child context. A clause chunk still knows which section it belongs to, and that section still knows which document it's part of. Retrieval can return the specific clause and still carry the surrounding structure that gives it meaning.

Why this is worth the extra engineering 🎯
A flat chunk of "employees must provide 30 days' notice" is ambiguous on its own — notice of what? Resignation? Leave? Termination? With hierarchical context attached, that same chunk carries its section header along with it, and the ambiguity disappears without needing a bigger chunk (and more noise) to resolve it.

Where the trade-off shows up 📊
This is genuinely harder to build than Day 9's approaches — it requires either a semantic similarity signal to detect topic shifts, or a structure-aware parser that understands headings and nesting in the first place. For a 12-document policy set like Northkeep's, simpler chunking was enough to hit 86.7% accuracy. For a system ingesting hundreds of long, deeply nested legal or compliance documents, this is often where the next accuracy gains actually live.

The bottom line 💡
Semantic and hierarchical chunking aren't "better" by default — they're what you reach for when document structure carries meaning that flat chunking throws away. Match the technique to how structured your source documents actually are.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-10-semantic-and-hierarchical-chunking
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #Chunking #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
