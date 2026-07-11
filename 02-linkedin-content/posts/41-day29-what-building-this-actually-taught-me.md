📘 RAG for Everyone | Day 29/30 — BONUS

🎙️ No chapter today. Just me, being honest about what 28 chapters and one working RAG system actually taught me — including the parts that didn't make it into any of the polished posts.

Today you'll learn:
✅ What surprised me most while building this
✅ Where I was wrong, and had to backtrack
✅ The trade-offs I'd make differently if I started over

What I thought this project would be 🤔
I thought the hard part would be the LLM — prompting, generation, getting the model to sound right. It wasn't. The hard part was everywhere upstream of it: what documents to include, how to chunk them without slicing a policy clause in half, what metadata to attach before I even knew what I'd need to filter by later. By the time I got to writing prompts, most of the outcome was already decided.

Where I was wrong, out loud 🙃
I assumed "grounded RAG" meant the model would just... stop hallucinating, structurally, once retrieval was in place. It doesn't work that way automatically. A grounded system prompt has to actively fight for that behavior — refusal rules, citation discipline, conflict handling — and even then, it's tested, not assumed. I also assumed accuracy numbers would tell the whole story. They don't. "86.7% retrieval accuracy" sounds like a grade. What actually mattered was being able to explain both of the misses — training-policy retrieval, specifically — instead of shrugging at a number.

The trade-off I keep coming back to 📊
Building 28 chapters teaching this stuff and building one real system side by side taught me the same lesson twice: the unglamorous steps — document scoping, metadata design, failure categorization — decide the ceiling on everything else. Chunking and embeddings get the attention. Metadata design and evaluation discipline are what actually determine whether a system can be trusted.

What I'd do differently 💭
I'd write the evaluation set before writing the retrieval code, not after. Building test questions in parallel with the pipeline — instead of once it "felt done" — would have caught the training-policy gap weeks earlier, and cheaper.

The bottom line 💡
None of this is a failure story. It's closer to: the honest version of building in public is admitting the polished 28-chapter course exists because of a much messier process of getting things wrong first, in a repo nobody was watching yet.

🔗 The full course and the working system it's grounded in:
https://github.com/TechNaom/rag-projects

If you find it useful:

⭐ Star the repository
🍴 Fork it
📥 Clone it
💬 Tell me what you'd have done differently — genuinely curious
🔁 Share it with your network

Every contribution and every star helps the project reach more developers.

#AI #RAG #GenerativeAI #LLM #BuildInPublic #OpenSource #ArtificialIntelligence #LessonsLearned #MachineLearning
