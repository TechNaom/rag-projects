# Message Queue Backlog Runbook

**Runbook ID:** RB-QUE-006
**Service:** Async worker fleet consuming from `events` queue (SQS)
**Owner:** Platform / Async
**Severity mapping:** Backlog age > 15 min = SEV2, > 1 hr = SEV1

## 1. Summary
Use this runbook when the `events` message queue is building a backlog: producers are enqueueing faster than the worker fleet can consume, so message age and queue depth are climbing. Downstream effects include delayed emails, delayed order fulfillment, and stale search indexes.

## 2. Diagnosis Steps
- Check queue depth and oldest-message age in the SQS dashboard (`ApproximateNumberOfMessagesVisible`, `ApproximateAgeOfOldestMessage`).
- Determine whether depth is rising because consumers slowed down or producers sped up. Compare enqueue rate vs dequeue rate over the last hour.
- Check worker health: `kubectl get pods -n prod -l app=events-worker`. Look for crashed workers, or workers stuck processing (no progress in logs).
- Check the dead-letter queue (DLQ). A flood into the DLQ means a poison message is failing every worker that touches it.

## 3. Common Causes
- A poison message that repeatedly fails and gets retried, blocking a worker or the whole partition until it hits max-receives and moves to the DLQ.
- Workers scaled down (or crashed) so effective consumer capacity dropped.
- A downstream dependency the workers call (e.g. the email provider) is slow, so each message takes longer and throughput falls.
- A producer-side spike (e.g. a bulk import) enqueueing far more than usual.

## 4. Mitigation Commands
- If workers are simply under-scaled, scale out: `kubectl scale deployment/events-worker -n prod --replicas=<higher>`.
- If a poison message is blocking progress, redrive it to the DLQ so healthy messages flow: `queuectl dlq-redrive --queue events --max-receives 1`.
- If a downstream dependency is the bottleneck, that is the real incident — follow the elevated-latency checklist for that dependency, and consider temporarily pausing non-critical producers.
- To drain a large healthy backlog faster, temporarily raise worker concurrency: `queuectl set-concurrency --worker events-worker --value <higher>`.

## 5. Escalation Criteria
- Escalate to SEV1 if the oldest message age exceeds 1 hour or if order-fulfillment messages are affected.
- Page the owning team for whichever downstream dependency is the bottleneck.
- Escalate to the Async on-call lead if the DLQ is filling faster than it can be triaged.

## 6. Verification
- Confirm oldest-message age is falling and returns under 60 seconds.
- Confirm the DLQ is triaged: every message there has a ticket or has been safely replayed.
