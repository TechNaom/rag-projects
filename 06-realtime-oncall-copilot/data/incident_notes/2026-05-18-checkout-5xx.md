# Incident 2026-05-18: Checkout 5xx spike after payments deploy

**Incident ID:** INC-2026-0518
**Severity:** SEV2
**Duration:** 41 minutes
**Services:** gw-edge, payments-svc
**Author:** on-call (edge rotation)

## Summary
At 14:02 UTC the edge gateway began returning 502/504 on `/v2/checkout` at a peak rate of 12%. The spike started 3 minutes after a `payments-svc` deploy (build `payments-svc@4.7.1`). Rolling back the deploy resolved it.

## Timeline
- 14:02 — Alert `gw-edge 5xx > 5%` fired for route `/v2/checkout`.
- 14:06 — On-call correlated the start time with the `payments-svc@4.7.1` deploy in the release channel.
- 14:11 — Confirmed `payments-svc` pods were healthy but returning slow responses (504 at the gateway), not crashing.
- 14:18 — Rolled back: `kubectl rollout undo deployment/payments-svc -n prod`.
- 14:29 — 5xx rate returned under 1%. Monitored to 14:43.

## Root Cause
Build `4.7.1` introduced a synchronous call to the fraud-scoring service inside the checkout path without a timeout, so when fraud-scoring was slow, checkout requests hung and timed out at the gateway as 504s.

## What Worked
- The deploy-timeline correlation in RB-GW-002 pointed straight at the bad deploy.
- Rollback was clean and fast.

## Follow-ups
- Add a timeout and circuit breaker around the fraud-scoring call (owner: payments).
- Add a pre-deploy check that fails a deploy if it adds a synchronous external call to the checkout path.
