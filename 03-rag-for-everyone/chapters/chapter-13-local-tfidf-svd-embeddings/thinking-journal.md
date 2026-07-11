# GenAI Thought Process Journal: Local TF-IDF + SVD Embeddings

## Builder Reflection

Local retrieval teaches humility. It shows exactly what matched, what did not match, and why lexical systems can be both powerful and limited.

Ask yourself:

- Did the query terms exist in the corpus?
- Did cleaning remove important identifiers?
- Did common words dominate the score?
- Did SVD compression blur important details?
- Is this an exact-term problem, a paraphrase problem, or both?

## Prompt Testing Habit

Use this prompt when reviewing local retrieval:

```text
Given a query, top documents, matched terms, missing terms, TF-IDF scores,
and expected evidence, review whether local lexical retrieval is enough.

Return:
1. what matched
2. what important terms were missing
3. whether paraphrase risk exists
4. whether SVD compression may hurt
5. whether neural or hybrid retrieval is recommended
6. one eval case to add
```

## Mentor Reminder

The goal is not to worship old methods or new methods. The goal is to choose the method whose failure mode you can explain and manage.
