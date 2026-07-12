# Starlight Robotics — Fleet API Reference

**Doc ID:** SR-API-002
**API version:** v3
**Base URL:** https://api.starlight-robotics.example/v3
**Audience:** Developers integrating the Skylark fleet

## 1. Authentication
All requests authenticate with a bearer token issued per organization from the
console under Settings > API Keys. Tokens are scoped to a single organization
and never grant access to another organization's aircraft or missions. Include
the header `Authorization: Bearer <token>` on every request. Tokens expire
after 90 days and can be rotated without downtime by keeping two active keys.

## 2. Rate Limits
The default plan allows 600 requests per minute per organization, with a burst
ceiling of 100 requests per second. Exceeding the limit returns HTTP 429 with a
`Retry-After` header in seconds. Telemetry streaming over the websocket
endpoint does not count against the REST rate limit.

## 3. Listing Aircraft
`GET /aircraft` returns every drone registered to your organization, including
serial number, firmware version, battery health, and last-known GPS position.
Results are paginated at 50 items per page; follow the `next` cursor in the
response envelope. Filter by status with `?status=in_flight` or `?status=idle`.

## 4. Launching a Mission
`POST /missions` accepts a JSON body with a `survey_boundary` polygon, a
`ground_sampling_distance_cm` value, and an `aircraft_id`. The API validates
that the aircraft is idle, has at least 80% battery, and is within radio range
before accepting the mission. A successful call returns a `mission_id` and the
mission enters the `queued` state.

## 5. Telemetry Webhooks
Register a webhook under Settings > Webhooks to receive mission lifecycle
events: `mission.started`, `mission.progress`, `mission.completed`, and
`mission.aborted`. Each payload is signed with an HMAC-SHA256 signature in the
`X-Starlight-Signature` header; verify it against your webhook secret before
trusting the body. Failed deliveries are retried with exponential backoff for
up to 6 hours.

## 6. Error Format
Errors return a consistent envelope: an `error.code` machine-readable string, a
human-readable `error.message`, and a `request_id` you should include when
contacting support. Codes in the `4xx` range indicate client problems (bad
input, insufficient battery); `5xx` indicates a Starlight-side fault and is
safe to retry idempotently for GET requests.
