# Incident 2026-06-02: orders-prod writer storage full

**Incident ID:** INC-2026-0602
**Severity:** SEV1
**Duration:** 18 minutes
**Services:** orders-prod (Aurora PostgreSQL)
**Author:** on-call (data reliability rotation)

## Summary
At 03:14 UTC all writes to `orders-prod` began failing. The writer node's storage volume filled to 100%, so PostgreSQL rejected writes. AWS did not auto-failover because the standby shared the same storage condition risk. A manual failover plus a WAL cleanup restored writes.

## Timeline
- 03:14 — `db_write_errors_total` alert fired; checkout returning 5xx on writes.
- 03:17 — Confirmed writer up but rejecting writes with `could not extend file: No space left on device`.
- 03:19 — `FreeStorageSpace` metric confirmed 0 bytes free.
- 03:24 — Triggered manual failover per RB-DB-001: `aws rds failover-db-cluster --db-cluster-identifier orders-prod`.
- 03:29 — New writer promoted; restarted `orders-api` to drop stale connections.
- 03:32 — Writes recovered.

## Root Cause
A runaway logical-replication slot was retaining WAL segments that could never be reclaimed, consuming all free storage over ~six hours. The inactive replication slot was left behind by a decommissioned analytics consumer.

## What Worked
- RB-DB-001's storage-full diagnosis step identified the cause immediately.

## Follow-ups
- Add an alert on inactive replication slots retaining WAL.
- Add a `FreeStorageSpace < 15%` warning alert (previously only alerted at 5%).
