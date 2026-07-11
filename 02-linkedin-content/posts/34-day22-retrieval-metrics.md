📘 RAG for Everyone | Day 22/30

📊 "It seems to work pretty well" is not a metric. Today's chapter is about replacing that sentence with actual numbers.

Today you'll learn:
✅ The four core retrieval metrics and what each one actually tells you
✅ Why you need gold-standard labels before any of them mean anything
✅ How "failure slicing" turns one accuracy number into a diagnosis

The four metrics, in plain terms 🔢
→ Recall@K — of all the chunks that should have been retrieved, what fraction actually showed up in your top K results? This is the one Northkeep's 86.7% figure comes from.
→ Precision@K — of the chunks you did retrieve, what fraction were actually relevant? High recall with low precision means you're burying the right answer in noise.
→ MRR (Mean Reciprocal Rank) — how high did the first genuinely relevant chunk rank? A relevant chunk at position 1 scores far better than the same chunk at position 8.
→ nDCG — a graduated version of the above: it rewards ranking the most relevant chunks highest, not just getting relevant chunks in the list somewhere.

The step before any of these matter 🏷️
None of these numbers mean anything without gold-standard labels — a human-verified answer key for "given this question, which chunks should the system retrieve." Building that label set, honestly, is more work than computing the metrics themselves. It's also the part that makes the metrics trustworthy instead of self-serving.

Real numbers, and the harder truth in them 📈
Northkeep's system hit 86.7% recall across 15 evaluation questions — 13 answered correctly, 2 missed. Failure slicing means not stopping at "86.7%," but asking: which 2 failed, and what do they have in common? Both misses turned out to cluster around training-policy retrieval — a specific, explainable pattern, not random noise. That's what makes the number actionable instead of just a grade.

The bottom line 💡
A single accuracy percentage tells you almost nothing on its own. Recall, precision, MRR, and nDCG together — measured against real gold labels, and sliced by failure pattern — tell you where the system is actually weak, which is the only version of "measuring RAG" that leads anywhere useful.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-22-retrieval-metrics
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #Metrics #BuildInPublic #OpenSource #ArtificialIntelligence #BankingTech
