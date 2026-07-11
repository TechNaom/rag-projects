📘 RAG for Everyone | Day 5/30

📂 Before you pick a vector database, before you choose an embedding model, before any of the "interesting" decisions — someone has to decide what documents your AI is even allowed to know about. Nobody talks about this part.

Today you'll learn:
✅ Why source document selection is a design decision, not a chore
✅ The questions that matter before a single file gets ingested
✅ What happens when this step gets skipped

The unglamorous first question 🤔
"What documents go into the system?" sounds obvious until you're staring at a shared drive with five versions of the same policy, two of them outdated, one of them marked "DRAFT — do not distribute" in the filename but not in the content. RAG doesn't know that. It'll retrieve and cite whatever you feed it with equal confidence.

What actually has to get decided ✅
→ Scope — which documents are in-bounds for this system, and which are explicitly excluded
→ Ownership — who approves a document before it's ingestable, and who's accountable when it's wrong
→ Currency — how do you know a document is still the current version, not a superseded one sitting in the same folder
→ Format reality — PDFs, scanned images, Word docs, and web pages all need different handling before they're even "text"

Real numbers 📊
Northkeep National Bank's assistant is scoped to exactly 12 policy documents — HR and compliance content that was explicitly approved for this system. Not "everything in the shared drive." That scoping decision, made before a single chunk was created, is what makes 86.7% retrieval accuracy meaningful instead of a number measured against the wrong universe of documents.

The bottom line 💡
Garbage in, confidently-cited garbage out. The most important architectural decision in a RAG system often isn't the model or the vector store — it's the boring, unglamorous work of deciding exactly what the system is and isn't allowed to know.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-05-source-documents
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #DataGovernance #BuildInPublic #OpenSource #ArtificialIntelligence #BankingTech
