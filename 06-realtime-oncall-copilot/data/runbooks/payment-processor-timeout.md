# Payment Processor Timeout Runbook

**Runbook ID:** RB-PAY-003
**Service:** Payments service (`payments-svc`) and external processor Stripewire
**Owner:** Payments
**Severity mapping:** Checkout success rate < 95% = SEV1

## 1. Summary
Use this runbook when checkout is failing or slow because calls from `payments-svc` to the external processor Stripewire are timing out. Symptoms include rising `payment_timeout_total`, falling checkout success rate, and customer reports of "payment stuck / charged but no confirmation."

## 2. Diagnosis Steps
- Check the Stripewire status page and the `payments-svc` outbound latency panel. A processor-side outage shows high latency across ALL payment methods at once.
- Check `payment_timeout_total` broken down by payment method. If only one method (e.g. ACH) is affected, it is a processor partial outage, not a full one.
- Check for duplicate-charge risk: query the idempotency-key store for keys with a `charged` processor state but no local `confirmed` record — these are the "charged but no confirmation" cases.
- Confirm our outbound egress is healthy: a DNS or NAT gateway failure on our side can look identical to a processor outage.

## 3. Common Causes
- Stripewire-side degradation or regional outage (check their status page first, always).
- Our outbound timeout set too aggressively during a processor slow period, converting slow-but-successful charges into timeouts and retries.
- NAT gateway or egress firewall change dropping outbound HTTPS to the processor.
- A retry storm: our own retries amplifying load during a slowdown and making it worse.

## 4. Mitigation Commands
- If the processor is degraded but not down, raise the outbound timeout to ride out the slowness instead of timing out: `payctl set-timeout --service payments-svc --ms 15000`.
- Enable safe-retry mode which keys every attempt on the idempotency key to prevent double charges: `payctl retry-mode safe --service payments-svc`.
- If one payment method is down, disable just that method at checkout: `payctl method disable ach --reason "processor timeout"`.
- Reconcile duplicate-charge candidates: run `payctl reconcile --since <incident-start>` to auto-refund confirmed double charges.

## 5. Escalation Criteria
- Page the Payments on-call lead immediately if checkout success rate drops below 95%.
- Open a Sev-1 ticket with Stripewire support if their status page does not already show the incident.
- Escalate to Finance / Fraud on-call if the reconciliation finds more than 50 duplicate charges.

## 6. Verification
- Confirm checkout success rate is back above 99% for 10 minutes.
- Confirm the idempotency reconciliation queue is drained and no customer remains double-charged.
