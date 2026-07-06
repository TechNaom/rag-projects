# Module 1 — Foundation

## Overview

**"Before you build, understand why RAG exists."**

This module covers the foundational concepts that justify every architectural decision in a RAG system:

1. **Why RAG Exists** — The problem statement
2. **Why LLMs Hallucinate** — The root cause
3. **Context Windows & Limits** — The constraint
4. **Types of RAG** — The solutions
5. **Complete Query Lifecycle** — The flow

## What You'll Learn

✅ Why LLMs need external knowledge  
✅ How hallucinations happen and why they're hard to prevent  
✅ How to design systems around context limits  
✅ When to use naive vs. advanced RAG  
✅ The complete end-to-end flow of a RAG query  

## Topics

### Topic 1.1: Why RAG Exists
- **What**: Problem statement for RAG
- **Why**: Knowledge cutoff, hallucinations, long-tail facts
- **Example**: ChatGPT vs. RAG on current events
- **Time**: 20-30 minutes
- **Files**: `topics/topic-01-why-rag/`

### Topic 1.2: Why LLMs Hallucinate
- **What**: Root cause analysis of hallucinations
- **Why**: Design better systems and prompts
- **Example**: Why Claude can't remember your birthday
- **Time**: 25-35 minutes
- **Files**: `topics/topic-02-hallucinations/`

### Topic 1.3: Context Windows & Their Limits
- **What**: Understanding attention, token counting, compression
- **Why**: Design retrieval to fit constraints
- **Example**: GPT-4 Turbo vs. Claude 3 vs. open models
- **Time**: 20-30 minutes
- **Files**: `topics/topic-03-context-windows/`

### Topic 1.4: Types of RAG
- **What**: Naive, Advanced, Agentic, Graph, Corrective, Adaptive RAG
- **Why**: Choose the right architecture
- **Example**: When to use each type
- **Time**: 30-40 minutes
- **Files**: `topics/topic-04-rag-types/`

### Topic 1.5: Complete Query Lifecycle
- **What**: End-to-end flow from query to answer
- **Why**: See how all pieces fit
- **Example**: A real query flowing through a system
- **Time**: 25-35 minutes
- **Files**: `topics/topic-05-query-lifecycle/`

## Module Project

**Build a Naive RAG System Over Synthetic Banking Data**

You'll ingest a synthetic banking policy corpus and build a system that:
- Chunks documents
- Creates embeddings
- Stores in a vector database
- Retrieves relevant policies
- Generates answers with citations

**Time**: 4-6 hours  
**Skills**: Everything from Module 1  
**Files**: `project/`

## Module Exam

**Written Assessment** (45 minutes)
- 5 short-answer questions
- 2 design questions
- Covers all 5 topics
- Mark module as "Completed" in local storage

**Files**: `exam/`

## Learning Path

### Path A: Foundations First (Recommended for beginners)
1. Read master chapter for each topic
2. Watch YouTube script (mentally or on video)
3. Run notebook examples
4. Complete exercises
5. Answer interview questions
6. Build project
7. Take exam

### Path B: Hands-On First (For experienced engineers)
1. Run notebook examples
2. Complete hands-on lab
3. Read cheat sheet
4. Review interview questions
5. Deep-dive with blog post if needed
6. Build project
7. Take exam

### Path C: System Design Focus (For architects)
1. Review architecture diagrams
2. Study comparison matrices
3. Answer interview questions
4. Read speaker notes
5. Design your own system
6. Build project
7. Take exam

## Time Estimate

- **Reading all master chapters**: 2-2.5 hours
- **Running all notebooks**: 2-2.5 hours
- **Completing exercises & labs**: 3-4 hours
- **Building project**: 4-6 hours
- **Taking exam**: 1 hour
- **Total module time**: 12-16 hours

## Resources

### Within This Module
- 5 interactive lesson.html files
- 5 fill-in-the-blank quizzes
- 5 sets of interview questions
- 5 master chapters (written guides)
- 5 YouTube scripts
- 5 blog posts
- 5 cheat sheets
- 5 Python notebooks with live code
- 5 hands-on labs
- 5 exercise/practice sets
- Architecture diagrams (Mermaid + ASCII)
- Comparison matrices
- Workshop guides
- LinkedIn carousel templates
- 1 capstone project
- 1 written exam

### External Resources
- LangChain documentation
- Chroma DB documentation
- OpenAI Embeddings API
- Papers: "Attention Is All You Need", "Language Models are Unsupervised Multitask Learners"

## Quick Navigation

**Start here:**
- 👉 [Topic 1.1: Why RAG Exists](topics/topic-01-why-rag/)

**Skip to:**
- [Topic 1.2: Why LLMs Hallucinate](topics/topic-02-hallucinations/)
- [Topic 1.3: Context Windows](topics/topic-03-context-windows/)
- [Topic 1.4: Types of RAG](topics/topic-04-rag-types/)
- [Topic 1.5: Query Lifecycle](topics/topic-05-query-lifecycle/)

**Jump to project:**
- [Module 1 Project](project/)

**Assessment:**
- [Module 1 Exam](exam/)

## What's Next?

After completing Module 1, you'll have a solid foundation. Module 2 dives into **Documents & Data Ingestion** — the first step in building a real RAG system.

---

**Estimated completion**: 12-16 hours  
**Difficulty**: Beginner-friendly  
**Prerequisites**: Basic Python, understanding of LLMs  
