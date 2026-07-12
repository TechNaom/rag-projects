# Elevated Latency Checklist Runbook

**Runbook ID:** RB-LAT-004
**Service:** Cross-service (any service breaching its latency SLO)
**Owner:** Platform / SRE
**Severity mapping:** p99 > 2x SLO for 10 min = SEV2

## 1. Summary
A general-purpose checklist for when a service's request latency (usually p95 or p99) breaches its SLO but error rate is still low — requests are succeeding, just slowly. This is the most common and most ambiguous class of incident, so work the checklist top to bottom rather than guessing.

## 2. Diagnosis Steps
Work these in order, cheapest checks first:
- Confirm which percentile moved. p50 rising means a broad systemic slowdown; only p99 rising means tail latency (a subset of slow requests, often GC pauses, a slow shard, or one bad node).
- Check whether latency correlates with a traffic increase. If yes, this may be a capacity problem, not a bug.
- Check downstream dependency latency (database, cache, downstream services). Elevated latency almost always propagates upward from a slow dependency.
- Check for a recent deploy on the affected service or its dependencies.
- Check host-level saturation: CPU throttling, memory pressure / swap, and network saturation on the pods.

## 3. Common Causes
- A slow database query, often from a missing index after a data-volume increase.
- Cache hit rate dropping (cold cache after a deploy or eviction), pushing load to the slow path.
- CPU throttling from Kubernetes CPU limits set too low for current traffic.
- Garbage collection pauses on JVM/Go services under memory pressure (shows as p99-only spikes).
- A single slow node or shard dragging the tail.

## 4. Mitigation Commands
- If a cold cache is the cause, let it warm and consider pre-warming: `cachectl warm --service <svc> --keys top-1000`.
- If CPU throttling, raise the limit and roll: `kubectl set resources deployment/<svc> -n prod --limits=cpu=2 && kubectl rollout restart deployment/<svc> -n prod`.
- If capacity-driven, scale out: `kubectl scale deployment/<svc> -n prod --replicas=<higher>`.
- If one node is slow, cordon and drain it: `kubectl cordon <node> && kubectl drain <node> --ignore-daemonsets`.

## 5. Escalation Criteria
- Escalate to the owning service team if a specific slow query or code path is identified and needs a code fix.
- Escalate to SEV1 if the latency starts producing timeouts and the error rate climbs above 2%.
- Page the SRE lead if latency is systemic across many unrelated services (suspect a shared dependency: DNS, service mesh, or the network).

## 6. Verification
- Confirm the breaching percentile returns under SLO for 15 continuous minutes.
- Record which mitigation actually moved the metric, for the post-incident review.
