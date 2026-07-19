---
name: usa-bracketing-expert
description: Complete USA Bracketing (usabracketing.com) and USA Wrestling membership portal system v2.0 — the ONE USA Bracketing skill. Handles login authentication, CSRF token management, bracket discovery, dual vs individual bracket navigation, score formats, platform quirks, opponent data extraction, and cross-platform wrestling intelligence. Covers Cedar Point Rumble, NUWAY events, and any USA Bracketing tournament. Triggers on any request involving USA Bracketing, usabracketing.com navigation, bracket extraction, tournament data from USA Bracketing, USA Wrestling login or membership portal, dual meet scores, or when the user provides USA Bracketing credentials or event links.
---

# USA Bracketing Expert v2.0

The single skill for everything usabracketing.com — login through extraction through cross-platform intel.

> **v2.0 consolidation:** Absorbs usa-bracketing-extraction-guide (login flows, CSRF handling, dual-vs-individual bracket differences, score formats, platform quirks). One skill, complete coverage.

## Quick Start

```
User: "Get Chase Krapil's bracket from Cedar Point Rumble"
→ Login (stored credential reference, never ask for passwords in chat)
→ Navigate event → division → bracket
→ Extract matches, seeds, results
→ Tag every data point CONFIRMED / UNVERIFIED / NOT FOUND with source URL
```

## Platform Knowledge (folded from extraction guide)

- **Login flow**: USA Wrestling membership credentials; session cookies + CSRF token required for bracket endpoints. Token refreshes per session — re-acquire on 403.
- **Dual vs individual brackets**: duals show team scores + per-weight bout boxes; individual shows standard bracket trees. Extraction logic differs — confirm bracket type first.
- **Score formats**: `W 8-2` (decision), `TF 12-0` (tech fall), `F 1:34` (fall), `MD` (major), `FFT/BYE` (forfeit/bye). Normalize to a standard schema on extraction.
- **Known quirks**: lazy-loaded brackets (scroll/wait before scraping), event UUIDs in URLs (store them for direct access), division naming varies by event (verify age/weight labels against the event's own labels, never assume).

## Extraction Output Schema

| Field | Notes |
|---|---|
| wrestler_name | As shown on bracket |
| club / team | Verify against roster when possible |
| weight_class + division | Event's own labels |
| seed | If shown |
| matches[] | opponent, result, score, round |
| placement | Final, if available |
| source_url | Event/bracket URL — mandatory |

## Cross-Platform Intelligence

After extraction, cross-reference with Trackwrestling/FloWrestling data (via wrestling-extraction-suite) and flag conflicts. Persist verified results to the Neon wrestling DB when the connector is live.

## Security

Never ask for, store, or repeat passwords in chat or files. Use stored credential references only; if login fails twice, stop and hand the user the manual steps.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| usa-bracketing-extraction-guide | Login flows, CSRF handling, bracket navigation, dual/individual differences, score formats, platform quirks |
