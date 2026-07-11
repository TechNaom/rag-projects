📘 RAG for Everyone | Day 4/30

🏗️ Every production RAG system is secretly two systems wearing one name. Most beginners only ever build one of them.

Today you'll learn:
✅ The two-pipeline architecture behind every real RAG system
✅ Why mixing them up is a common (and expensive) mistake
✅ Which pipeline actually needs to be fast

One name, two very different jobs 🔀
"RAG pipeline" sounds like a single thing. In production it's split into two pipelines with completely different constraints:

→ Offline Indexing Pipeline — runs in batches, whenever documents change. Parses, cleans, chunks, embeds, and stores. It can take minutes. Nobody's waiting on it.
→ Online Query Execution Pipeline — runs every single time a user asks a question. It has to be fast, because a person is staring at a loading spinner.

Why the split matters 🧩
Beginners often write one script that does everything — parse, embed, retrieve, generate — top to bottom, every time. It works for a demo. It falls apart the moment you have real document volume, because you end up re-processing documents on every query instead of once, offline, ahead of time.

Real numbers 📊
On the Northkeep POC, the offline pipeline runs once to turn 12 policy documents into 111 indexed chunks in ChromaDB. The online pipeline then only ever touches that already-built index — retrieval and generation, nothing else, on every question. Separating those two meant query latency depended on retrieval and generation only, not on re-parsing PDFs every time someone asked about the leave policy.

The bottom line 💡
If your RAG system re-does indexing work on every query, you haven't built a query pipeline — you've built a very slow indexing pipeline that also answers questions. Split the two, and each one gets to be optimized for what it actually needs: throughput for indexing, latency for querying.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-04-rag-execution-pipelines
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #DataEngineering #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
