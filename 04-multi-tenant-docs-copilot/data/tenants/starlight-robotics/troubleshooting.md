# Starlight Robotics — Skylark X2 Troubleshooting

**Doc ID:** SR-TRB-004
**Audience:** Operators and support engineers
**Last updated:** March 2026

## 1. Aircraft Fails Pre-Flight Self-Test
The most frequent cause is a partially mounted LiDAR pod or an unseated gimbal
ribbon cable. Power down, reseat the pod until it clicks, and confirm the gimbal
moves freely on restart. If the self-test still fails with error E-07, the IMU
needs recalibration: place the aircraft on a level surface and run "Calibrate
IMU" in the Field app.

## 2. Battery Not Recognized by Charger
An SL-B4 that shows no LEDs when inserted is usually too hot. The charger
refuses cells above 40°C by design. Let the battery rest for 15–20 minutes and
retry. A battery that reports health below 80% in the console should be retired
from survey work; degraded cells cause mid-flight voltage sag and premature
return-to-home.

## 3. Missing or Delayed Imagery Upload
If processed maps have not appeared 40 minutes after landing, check that the
raw images are still on the SD card (they are retained until the cloud copy is
confirmed). A stalled upload almost always traces to the Ground Link losing its
network path. Reconnect the Ground Link to a known network and the sync resumes
automatically from where it stopped.

## 4. Drone Returns Home Early
Early return-to-home is triggered by low battery, loss of Ground Link signal for
more than 10 seconds, or a geofence breach. Check the mission log's abort reason
field. If signal loss is the cause on a large site, you likely need an
additional Ground Link radio to eliminate the coverage gap.

## 5. Telemetry Webhook Not Firing
If your integration stops receiving `mission.completed` events, first verify the
webhook endpoint returns HTTP 200 quickly; Starlight treats any non-2xx or a
response slower than 5 seconds as a failed delivery. Failed deliveries retry for
6 hours, then stop. Check the webhook delivery log in the console for the exact
HTTP status recorded on each attempt.

## 6. Escalating a Hardware Fault
If an aircraft shows a persistent hardware error after the steps above, open a
support ticket with the aircraft serial, the firmware version, and the
`request_id` from any related API error. Starlight aims to respond to hardware
faults within one business day and will issue an RMA if the fault is confirmed
to be a manufacturing defect within the warranty period.
