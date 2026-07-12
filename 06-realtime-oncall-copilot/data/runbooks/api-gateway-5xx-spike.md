# API Gateway 5xx Spike Runbook

**Runbook ID:** RB-GW-002
**Service:** Edge API Gateway (`gw-edge`, Envoy-based)
**Owner:** Edge / Traffic
**Severity mapping:** Sustained 5xx rate > 5% = SEV2, > 20% = SEV1

## 1. Summary
Use this runbook when the edge API gateway shows an elevated rate of 5xx responses (500, 502, 503, 504) across one or more routes. The gateway itself is rarely the root cause — it is usually surfacing a failure in an upstream service, but it is where the alert fires.

## 2. Diagnosis Steps
- Break down 5xx by status code in the `gw-edge` dashboard. 502/503 point at unhealthy upstreams; 504 points at upstream timeouts; a pure 500 spike points at an application bug.
- Break down 5xx by route. If one route is hot (e.g. `/v2/checkout`) the blast radius is one service; if all routes are affected, suspect the gateway itself or a shared dependency.
- Check upstream health: `kubectl get pods -n prod -l tier=backend` and look for `CrashLoopBackOff` or failing readiness probes.
- Check the gateway's own saturation: CPU, file descriptors, and active connection count on the `gw-edge` pods.

## 3. Common Causes
- An upstream deploy that shipped a bug — correlate the spike start time with the deploy timeline in the release channel.
- Upstream connection pool or thread pool exhaustion returning 503.
- A downstream dependency (database, cache) slow enough that upstream requests time out, surfacing as 504 at the gateway.
- Gateway config reload that dropped or misrouted a route.

## 4. Mitigation Commands
- If a specific bad deploy is implicated, roll it back first: `kubectl rollout undo deployment/<service> -n prod`.
- If one upstream is unhealthy and non-critical, shed its traffic by enabling the circuit breaker: `gwctl route disable <route> --reason "5xx mitigation"`.
- If the gateway pods are saturated, scale out: `kubectl scale deployment/gw-edge -n prod --replicas=<current*2>`.
- Force-drain unhealthy upstream pods: `kubectl delete pod <pod> -n prod` to let the scheduler replace them.

## 5. Escalation Criteria
- Page the owning service team if a single upstream is the confirmed root cause and you cannot roll it back safely.
- Escalate to SEV1 and page the incident commander if the 5xx rate crosses 20% or checkout is affected.
- Loop in the Edge on-call lead if the gateway itself (not an upstream) is the root cause.

## 6. Verification
- Confirm the 5xx rate returns below 1% for 5 continuous minutes before downgrading severity.
- Confirm no route remains in a disabled/circuit-broken state that was not intended.
