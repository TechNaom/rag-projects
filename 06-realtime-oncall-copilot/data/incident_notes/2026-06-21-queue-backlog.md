# Incident 2026-06-21: events queue backlog from poison message

**Incident ID:** INC-2026-0621
**Severity:** SEV2
**Duration:** 55 minutes
**Services:** events queue (SQS), events-worker fleet
**Author:** on-call (async rotation)

## Summary
Starting around 09:40 UTC the `events` queue backlog climbed to over 40,000 messages with oldest-message age passing 20 minutes. A single malformed message was failing every worker that received it and being retried, stalling throughput. Redriving it to the DLQ restored normal consumption.

## Timeline
- 09:40 — Backlog-age alert fired (`ApproximateAgeOfOldestMessage > 15m`).
- 09:48 — Confirmed enqueue rate was normal; dequeue rate had collapsed, so this was a consumer-side problem.
- 09:55 — Worker logs showed repeated `KeyError: 'order_id'` on the same message id, retried on a loop.
- 10:07 — Redrove the poison message per RB-QUE-006: `queuectl dlq-redrive --queue events --max-receives 1`.
- 10:20 — Dequeue rate recovered; backlog began draining.
- 10:35 — Oldest-message age back under 60s.

## Root Cause
A producer shipped a message schema change that omitted `order_id` for a subset of events. The worker did not defensively handle the missing key, so it crashed on every attempt instead of dead-lettering the bad message.

## What Worked
- RB-QUE-006's DLQ diagnosis step pointed straight at the poison-message pattern.

## Follow-ups
- Make the worker dead-letter unparseable messages immediately instead of crash-looping.
- Add producer-side schema validation before enqueue.
