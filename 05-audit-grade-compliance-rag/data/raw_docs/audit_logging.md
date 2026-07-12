---
doc_id: AUDIT-001
title: Audit Logging and Monitoring Requirements
version: "1.0"
status: current
effective_date: 2024-07-01
superseded_by: ""
---

# Audit Logging and Monitoring Requirements

**Policy ID:** AUDIT-001
**Version:** 1.0 (CURRENT)
**Owner:** Information Security
**Applies to:** All systems that create, receive, maintain, or transmit ePHI

## 1. Purpose
This policy defines the audit logging and monitoring controls required to detect unauthorized access to electronic protected health information (ePHI), in compliance with the HIPAA Security Rule audit controls standard.

## 2. Events That Must Be Logged
All systems handling ePHI must log: user authentication attempts, record access (view, create, modify, delete), export or printing of PHI, changes to access permissions, and administrator actions.

## 3. Log Content
Each audit log entry must capture the user identity, timestamp, action performed, the patient record or resource affected, and the source system or device.

## 4. Log Retention
Audit logs must be retained for a minimum of **six (6) years** to support investigations and regulatory audits. Logs must be tamper-evident and stored separately from the systems that generate them.

## 5. Monitoring and Review
Security analysts review automated alerts daily and perform a documented review of high-risk access patterns (such as access to VIP or employee records) at least weekly.

## 6. Integrity Protection
Audit logs must be write-once or otherwise protected against modification and deletion. Any gap or anomaly in the audit trail is itself a reportable security event.
