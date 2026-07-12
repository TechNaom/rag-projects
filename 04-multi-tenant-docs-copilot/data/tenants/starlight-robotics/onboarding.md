# Starlight Robotics — Skylark Drone Onboarding Guide

**Doc ID:** SR-ONB-001
**Product:** Skylark X2 Autonomous Survey Drone
**Audience:** New operators and integration engineers
**Last updated:** March 2026

## 1. What the Skylark X2 Is
The Skylark X2 is an autonomous quadcopter built for industrial site
surveying. It carries a 20-megapixel RGB camera and an optional LiDAR pod,
flies pre-planned grid missions, and streams telemetry to the Starlight Cloud
over LTE. A single charged battery gives roughly 34 minutes of flight time and
covers about 45 hectares on a standard overlap survey.

## 2. Unboxing and Hardware Checklist
Every Skylark X2 kit ships with the airframe, two SL-B4 smart batteries, a
dual-bay charger, four spare propellers, and a Ground Link radio. Before the
first flight, confirm the propeller arms click fully into the locked position
(you should hear two detents) and that the gimbal ribbon cable is seated. Do
not power the aircraft with the LiDAR pod half-mounted; this is the most common
cause of a failed self-test.

## 3. Creating Your Operator Account
Operators register at console.starlight-robotics.example using the invite email
sent by your fleet administrator. Each operator account is tied to a single
organization and cannot be shared across companies. Enable two-factor
authentication during first login; the FAA-compliant flight log requires a
uniquely attributable operator identity for every mission.

## 4. Your First Mission
Charge both SL-B4 batteries to 100%, then open the Starlight Field app and tap
"New Grid Survey." Draw the survey boundary on the map, set the target ground
sampling distance (2 cm/px is typical for stockpile volume work), and the app
computes the flight lines automatically. Keep the aircraft within 400 meters
horizontal and 120 meters vertical of the Ground Link radio.

## 5. Post-Flight Data Sync
When the drone lands, images upload to Starlight Cloud automatically over
Wi-Fi if the Ground Link is on the same network; otherwise they sync when the
aircraft next sees a known network. Processed orthomosaics and point clouds
appear in the console within 20–40 minutes depending on survey size. Raw
imagery is retained on the aircraft SD card until you confirm the cloud copy.

## 6. Getting Help
Operator support is available through the in-app chat during business hours
(09:00–18:00 Pacific) and through the community forum at any time. Firmware
release notes and known issues are published on the status page; subscribe to
be notified before a mandatory firmware update is pushed to your fleet.
