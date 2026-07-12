# Sample Support Questions

Test questions for the Knowledge Hub pipeline. Each line is:

    expected | question text

`expected` is only used to sanity-check the pipeline in the summary. It is NOT
fed into retrieval or the confidence decision. `answerable` means the KB should
cover it; `out-of-scope` means no article covers it and it SHOULD be flagged as a
knowledge gap.

answerable | I forgot my password and the reset link says it is no longer valid, what do I do?
answerable | How do I export all my notes and tasks as a backup?
answerable | I want to cancel my subscription, will I lose my notes and can I get a refund?
answerable | How do I invite a coworker as a read-only viewer?
answerable | My notes are not showing up on my other device, how do I fix syncing?
answerable | The API keeps returning 429, how should my integration handle rate limits?
out-of-scope | How do I connect Notedeck to Slack so new tasks post to a channel?
out-of-scope | Does Notedeck support single sign-on with SAML for my company?
out-of-scope | Can I sync my Notedeck tasks to my Google Calendar automatically?
out-of-scope | How do I record a voice memo and have Notedeck transcribe it into a note?