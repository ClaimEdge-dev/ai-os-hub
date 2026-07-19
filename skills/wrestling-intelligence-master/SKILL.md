---
name: wrestling-intelligence-master
description: The ONE hub for the youth wrestling AI ecosystem v2.0. Platform expertise (Trackwrestling, FloWrestling, USA Bracketing, RankWrestlers, NUWAY Combat) plus multi-agent research, skill routing, thread bootstrap, and the master project manifest (skill inventory, Neon DB, Chase Krapil profile, thread-startup protocol). Triggers on any wrestling request — opponent scouting, bracket analysis, seeding disputes, match briefs, tournament prep, dual lineups, rankings, results, new thread setup, context recovery, manifest, or project overview.
---

# Wrestling Intelligence Master v2.0

The single hub for the wrestling AI ecosystem. Every wrestling request routes through here; specialist skills plug in as spokes.

> **v2.0 consolidation:** Absorbs wrestling-master-manifest (project manifest + thread bootstrap protocol). This skill now IS the single source of truth for the wrestling project.

## Master Manifest (folded in — keep current)

- **Focus athlete**: Chase Krapil (75/80 lbs, Ascend Wrestling Academy 10U)
- **Database**: Neon wrestling DB (see WR | Neon Database — Wrestling DB Notion page); wrestling-scout-db is wrestling-only after claims tables migrate out (pending)
- **Skill family**: wrestling-opponent-scout, wrestler-career-rankings, tournament-preparation-suite, wrestling-extraction-suite, usa-bracketing-expert, wrestling-data-sync, wrestling-analytics-coach, level-up-wrestling-builder, icdwa-* skills, nuway-rumble-command-center, wrestling-thread-auditor
- **Platforms**: Trackwrestling, FloWrestling, USA Bracketing, USA Wrestling Membership, TheMat.com, NUWAY Combat, RankWrestlers

## Routing to Spokes

| Need | Spoke |
|---|---|
| Extract data from any platform | wrestling-extraction-suite (or usa-bracketing-expert for that platform) |
| Scout an opponent / matchup | wrestling-opponent-scout |
| Career stats + rankings | wrestler-career-rankings |
| Tournament coming up | tournament-preparation-suite |
| NUWAY Rumble / Cedar Point | nuway-rumble-command-center |
| Build the Level Up app | level-up-wrestling-builder |
| ICDWA county duals | illinois-county-duals-command-center + icdwa-technical-build-suite |
| Sync data across platforms | wrestling-data-sync |
| Match logging + analytics app | wrestling-analytics-coach |

## Thread Bootstrap Protocol (from manifest)

At new wrestling thread start: (1) load this manifest, (2) pull latest verified data from Neon if live, (3) state the active tournament/opponent focus, (4) confirm what's verified vs pending before researching. Never fabricate match data — CONFIRMED / UNVERIFIED / NOT FOUND with source URLs, always.

## Multi-Agent Research

For opponent scouting and tournament prep, dispatch parallel sub-agents (one per platform) then cross-reference conflicts. Log failures to DECISION_LOG so the next session doesn't repeat them.

## Absorbed Lineage

| Retired skill | What was folded in |
|---|---|
| wrestling-master-manifest | Project inventory, Chase Krapil profile, Neon DB credentials reference, HTML templates, thread-startup protocol |
