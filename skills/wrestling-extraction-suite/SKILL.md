---
name: wrestling-extraction-suite
description: >
  The ONE wrestling data extraction skill. Two modes: direct browser extraction and copy-paste prompts for Manus/Comet/other browser agents. Extracts records, placements, match histories, credentials from Trackwrestling, FloWrestling, USA Bracketing, USA Wrestling, TheMat.com, NUWAY Combat. Cross-references platforms; never fabricates — marks CONFIRMED/UNVERIFIED/NOT FOUND with source URLs. Triggers on extract/scrape/pull wrestling data, match history lookups, opponent records, bracket results, credential verification.
---

# Wrestling Extraction Suite

One skill, two modes: **direct extraction** (browser automation by this agent) and **prompt generation** (copy-paste prompts for Manus/Comet/other browser agents).

> **Merger (2026-07-19):** Combines wrestling-tournament-intelligence-extractor (verified methodology) + manus-wrestling-data-extractor (prompt library). Nothing lost from either.

## Mode 1: Direct Extraction (browser tools available)

1. Identify platform + target (wrestler profile, tournament, bracket).
2. Navigate: profile → tournament history tab → specific event → bracket/results. For trophy/placement data, check trophy sections separately.
3. Extract into the standard schema (below).
4. Cross-reference at least 2 platforms when possible; flag conflicts.
5. Tag every data point: **CONFIRMED** (seen on a platform, source URL) / **UNVERIFIED** (single source, not cross-checked) / **NOT FOUND** (searched, absent — say so).

## Mode 2: Browser-Agent Prompts (Manus / Comet / other)

Generate a complete copy-paste prompt containing:

```
GOAL: Extract [target] from [platform]
LOGIN: [stored credential reference or "public access"]
NAVIGATE: [exact click path: profile → tab → event → bracket]
EXTRACT: [fields from the schema below]
VERIFY: cross-check [second platform]; mark conflicts
FORMAT: table + source URLs for every row
RULES: never guess; mark NOT FOUND when absent; report blockers immediately
```

Platform-specific navigation paths live in the platform notes below.

## Standard Extraction Schema

| Field | Notes |
|---|---|
| wrestler_name, club, weight_class, division | Event's own labels — never assume |
| event_name, event_date, event_url | URL mandatory |
| matches[] | opponent, result, score (normalized), round |
| placement / record | Season or career as requested |
| credentials | State/national/regional placements, verified with source |
| verification_tag + source_url | Per data point — mandatory |

## Platform Notes

- **Trackwrestling**: access via FloWrestling NextGen where applicable; profile → events → matches.
- **FloWrestling**: search profile → results tab; some content paywalled — mark BLOCKED, don't guess.
- **USA Bracketing**: defer to `usa-bracketing-expert` for login/CSRF/quirks.
- **USA Wrestling Membership**: membership portal; requires login.
- **TheMat.com / NUWAY Combat**: public brackets; verify event names against flyers.

## Standing Rules

- Never fabricate. A missing result is data too — report NOT FOUND.
- Persist verified results to the Neon wrestling DB when live (via wrestling-data-sync patterns).
- Log extraction failures (blockers, paywalls, changed layouts) so the next attempt starts smarter.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| wrestling-tournament-intelligence-extractor | Verification methodology, CONFIRMED/UNVERIFIED/NOT FOUND standard, profile/trophy/bracket navigation, cross-platform cross-referencing |
| manus-wrestling-data-extractor | Copy-paste prompt templates for Manus/Comet, platform coverage list, blocker-reporting format |
