📘 RAG for Everyone | Day 24/30

🕵️ "It got 2 questions wrong out of 15." That sentence is where most people stop. It's where the actually useful work starts.

Today you'll learn:
✅ Why a raw failure count is close to meaningless on its own
✅ The three-step discipline for turning failures into fixes
✅ Why "replay testing" is what stops a fixed bug from coming back

Stopping at the number is the mistake 🛑
"86.7% accuracy" or "2 failures out of 15" sounds like a conclusion. It's actually just the starting point for the real question: what do those failures have in common, and is it one root cause or three unrelated ones wearing the same symptom?

The three-part discipline 🔧
1. Root-cause categorization — take every failed output and sort it into a real category (bad chunk boundary, missing metadata filter, ambiguous query, model over-generalizing) instead of one generic bucket labeled "wrong"
2. Ownership assignment — decide who's actually responsible for fixing that category: a chunking fix, a prompt fix, and a source-document fix are different people's problems even on a small team
3. Replay testing — after a fix ships, re-run the exact failing cases (plus your full regression set) to confirm the fix worked and didn't quietly break something else

What this looked like on Northkeep 📊
Both of Northkeep's 2 failed questions traced back to the same root cause: retrieval gaps around training-policy content specifically, not a random spread of unrelated issues. That's the payoff of categorization — "2 failures" became "one specific, addressable gap in how training-policy documents were chunked and indexed," which is a problem you can actually go fix, instead of a vague accuracy ceiling you just have to accept.

The bottom line 💡
A failure count without root-cause analysis is just a scoreboard. Categorize failures, assign clear ownership, and replay-test every fix — that's the difference between a system that slowly improves and one that just re-fails the same way every few months.

🔗 Full open-source lesson:
https://github.com/TechNaom/rag-projects/tree/main/03-rag-for-everyone/chapters/chapter-24-failure-analysis
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Share your feedback
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #FailureAnalysis #BuildInPublic #OpenSource #ArtificialIntelligence #BankingTech
