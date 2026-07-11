📘 RAG for Everyone | Day 16/30

🔢 "Just set top-k to 5." I've heard that piece of advice given as if it's a universal constant. It isn't. It's a guess dressed up as a default.

Today you'll learn:
✅ Why top-k is a trade-off, not a fixed setting
✅ What query rewriting and multi-query retrieval add on top of a single search
✅ How to actually tune retrieval instead of eyeballing it

The problem with a fixed top-k 🎯
Set k too low, and a genuinely relevant chunk that ranked 6th never makes it into the prompt — the model answers confidently from incomplete evidence. Set k too high, and you drown the truly relevant chunks in noise, pushing up token cost and giving the model more irrelevant material to accidentally get distracted by.

The toolkit beyond "just pick a number" 🧰
→ Scores — don't just take the top k blindly; look at the similarity scores themselves. A steep drop-off after result 3 tells you something different than a gradual decline through result 10.
→ Filters — narrow the candidate pool with metadata (Day 7) before ranking, so top-k is chosen from the right subset, not the whole corpus
→ Query rewriting — reformulate a vague or poorly-phrased user question into something that retrieves better, before it ever hits the vector store
→ Multi-query retrieval — generate several variations of the question, retrieve for each, and merge the results, catching relevant chunks a single phrasing would have missed

Why tracing beats intuition here 📊
The chapter's own framing is blunt about this: retrieval tuning without tracing is guesswork. Log what got retrieved for real queries, look at where the answer-bearing chunk actually ranked, and let that data set k — not a number that felt right in a demo with three test questions.

The bottom line 💡
Top-k isn't a knob you set once at project kickoff. It's a parameter you tune against real query traces, and the right value depends on your chunk size, your corpus, and how noisy your embeddings are. Guess first, measure always.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-16-retrieval-strategies-and-top-k
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #Retrieval #BuildInPublic #OpenSource #ArtificialIntelligence #MachineLearning
