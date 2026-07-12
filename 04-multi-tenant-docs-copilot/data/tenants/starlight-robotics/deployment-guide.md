# Starlight Robotics — Fleet Deployment Guide

**Doc ID:** SR-DEP-003
**Audience:** Site managers rolling out a Skylark fleet
**Last updated:** February 2026

## 1. Network Requirements
Each survey site needs either an LTE signal of at least -105 dBm or a local
Wi-Fi network reachable by the Ground Link radio. The Ground Link uploads over
port 443 (HTTPS) and maintains a websocket on port 8443 for live telemetry. If
your site firewall blocks outbound 8443, live map tracking will be unavailable
but missions and post-flight sync still work.

## 2. Ground Link Placement
Mount the Ground Link radio with a clear line of sight to the survey area, at
least 3 meters above ground, away from metal structures that cause multipath
interference. One Ground Link covers roughly a 2 km radius of open terrain. For
larger sites, deploy multiple radios; the aircraft hands off to the strongest
signal automatically without interrupting the mission.

## 3. Battery Logistics
Plan for a 3-to-1 battery-to-aircraft ratio for continuous operation: while one
SL-B4 flies, a second charges and a third cools. Batteries must cool to below
40°C before charging, which the dual-bay charger enforces. Store batteries at
40–60% charge if they will sit unused for more than a week to preserve cell
health.

## 4. Fleet Provisioning
Register each aircraft to your organization by scanning its QR code in the
console under Fleet > Add Aircraft. Provisioning binds the serial number to
your org and pushes your organization's flight-geofence and firmware channel.
An aircraft can belong to exactly one organization at a time; transferring it
requires a de-provision step that wipes the local mission cache.

## 5. Firmware Channels
Choose a firmware channel per fleet: `stable` (default, updated quarterly),
`rapid` (monthly, newer features), or `pinned` (locked to a specific version
for regulated environments). Mandatory security updates are pushed to all
channels. Schedule a maintenance window before enabling `rapid`, since new
firmware occasionally recalibrates the gimbal on first boot.

## 6. Go-Live Checklist
Before your first production survey, confirm: all aircraft show green in the
fleet health view, the Ground Link reports a stable uplink, at least two
batteries per aircraft are charged, the geofence matches the permitted airspace,
and one operator has completed a supervised test flight. Keep this checklist in
your site's standard operating procedure.
