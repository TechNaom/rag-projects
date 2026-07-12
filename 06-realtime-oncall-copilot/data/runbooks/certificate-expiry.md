# TLS Certificate Expiry Runbook

**Runbook ID:** RB-CERT-005
**Service:** Cross-service (TLS/SSL certificates on public and internal endpoints)
**Owner:** Security / Platform
**Severity mapping:** Expired cert on a customer-facing endpoint = SEV1

## 1. Summary
Use this runbook when a TLS certificate has expired or is about to expire, causing clients to reject connections with errors like `certificate has expired` or `SEC_ERROR_EXPIRED_CERTIFICATE`. Expired certs are almost always avoidable and almost always caught too late — treat an active expiry as a live outage.

## 2. Diagnosis Steps
- Identify the exact endpoint and cert: `echo | openssl s_client -connect <host>:443 -servername <host> 2>/dev/null | openssl x509 -noout -dates`. Read the `notAfter` date.
- Determine blast radius: is this a public customer-facing endpoint, an internal service-to-service endpoint, or a partner integration? Public expiry is a SEV1.
- Check whether cert renewal automation (cert-manager / ACME) is present and why it failed — look at cert-manager logs for the affected `Certificate` resource.
- Check for a wildcard vs single-host cert; a wildcard expiry has a much larger blast radius.

## 3. Common Causes
- cert-manager renewal failing silently due to a broken ACME HTTP-01/DNS-01 challenge (e.g. a firewall or DNS change blocked the challenge).
- A manually-issued cert that was never added to renewal automation.
- Clock skew on a client or server making a valid cert appear expired.
- A renewed cert that was issued but never rolled out to the load balancer / ingress.

## 4. Mitigation Commands
- If cert-manager has a valid renewed cert but it did not roll out, force a re-sync: `kubectl cert-manager renew <certificate> -n <ns>` then restart the ingress: `kubectl rollout restart deployment/ingress-nginx -n ingress`.
- For an emergency manual issue via ACME: `certbot certonly --standalone -d <host>` and install the resulting fullchain on the load balancer.
- Verify the new cert is live: re-run the `openssl s_client` check and confirm a future `notAfter` date.
- Purge any CDN/edge cache that may be pinning the old cert chain.

## 5. Escalation Criteria
- Page the Security on-call lead immediately for any expired customer-facing cert.
- Escalate to the Platform lead if cert-manager automation is broken cluster-wide (multiple certs at risk).
- Involve the networking team if an ACME challenge is failing due to a firewall/DNS change.

## 6. Prevention Follow-up
- Confirm a monitoring alert exists that fires at least 21 days before expiry for every cert, and file a ticket if this cert had no such alert.
- Add the manually-issued cert to renewal automation so it never recurs.
