# Primary Database Failover Runbook

**Runbook ID:** RB-DB-001
**Service:** Aurora PostgreSQL (primary cluster `orders-prod`)
**Owner:** Platform / Data Reliability
**Severity mapping:** Primary unreachable = SEV1

## 1. Summary
This runbook covers a failover of the primary `orders-prod` PostgreSQL cluster to a standby replica when the writer node is unhealthy, unreachable, or showing sustained replication or storage failure. Follow it when writes are failing but reads may still be served from replicas.

## 2. Diagnosis Steps
Confirm the writer is actually unhealthy before failing over — an unnecessary failover causes a 30-90 second write outage of its own.
- Check the writer endpoint: `psql -h orders-prod.writer.internal -c "SELECT 1"`. A timeout or connection refused for more than 60 seconds confirms the writer is down.
- Check replica lag: `SELECT now() - pg_last_xact_replay_timestamp() AS lag;` on each replica. A healthy failover target has lag under 5 seconds.
- Check the AWS RDS event log for `failover`, `storage-full`, or `hardware` events on the cluster.
- Confirm application-side symptoms: rising `db_write_errors_total` and 5xx on any write endpoint (checkout, cart update).

## 3. Common Causes
- Storage volume full on the writer (most common). Check `FreeStorageSpace` CloudWatch metric.
- Underlying host hardware failure (AWS will usually auto-failover within 120s; only intervene if it does not).
- A long-running migration holding `ACCESS EXCLUSIVE` locks, starving all writes. This is NOT a failover case — kill the migration instead.
- Connection pool exhaustion on the app side masquerading as a DB outage. Check pool saturation before failing over.

## 4. Mitigation Commands
If AWS auto-failover has not triggered within 120 seconds and the writer is confirmed down:
- Trigger a manual failover: `aws rds failover-db-cluster --db-cluster-identifier orders-prod`.
- Watch the promotion: `watch -n2 'aws rds describe-db-clusters --db-cluster-identifier orders-prod --query "DBClusters[0].Members"'`.
- Once a new writer is promoted, force application pods to drop stale connections: `kubectl rollout restart deployment/orders-api -n prod`.
- Verify writes recover: hit the checkout health probe and confirm `db_write_errors_total` stops climbing.

## 5. Escalation Criteria
- Escalate to the Data Reliability on-call lead if failover does not complete within 5 minutes.
- Escalate to AWS Enterprise Support (Sev A case) if the promotion is stuck or replicas are also unreachable.
- Declare a SEV1 and page the incident commander if writes are down for more than 10 minutes.

## 6. Post-Failover
- Confirm the old writer is quarantined and will not rejoin as a writer.
- Open a follow-up ticket to rebuild the failed node as a fresh replica.
- Capture the `FreeStorageSpace` and replication lag graphs for the post-incident review.
