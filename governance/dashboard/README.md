# DEBO Dashboard Core feed v1 (public metadata only)

This is **DEBO's official read-only instrument panel feed**, not another brain, database, task registry, public business API or approval authority. The private iPhone dashboard reads it as **source health**, not as production project status.

## Canonical producer

The existing `.github/workflows/debo-runtime-briefs.yml` job regenerates `governance/runtime-briefs/DEBO.md` and then runs:

```bash
python tools/debo_dashboard_core_feed.py --write
python tools/debo_dashboard_core_feed.py --check
```

Only changes to the derived JSON are committed alongside the existing runtime briefs. The workflow does **not** introduce a second schedule, connector, database, authorization flow or production deployment. Pull request runs only validate; trusted main runs may commit derived output using their existing narrowly scoped token.

## Data contract

`DEBO_CORE_FEED_v1.json` is deterministic and includes only:

- Public repository path and SHA-256 fingerprints for explicitly allowlisted public governance sources
- Canonical project IDs, static public profile paths and profile hashes from `tools/debo_bootstrap_check.py`
- Ten golden-rule count and explicit safety/approval boundaries
- UNKNOWN operational status and UNKNOWN approvals for every project

It does **not** include customer/claim details, youth information, credentials, personal finances, private Drive/Notion documents, customer workflows, or ChatGPT history exports.

## Client verification

The iPhone dashboard fetches public JSON with `credentials: omit` on page open, validates its schema and privacy flags, then shows `PUBLIC CORE FEED REACHABLE` only for a valid response. Failed fetch, incorrect schema or unavailable network must show `UNAVAILABLE / UNKNOWN`; use the existing dated dashboard snapshot, never invent freshness or operational readiness.

This public feed is **not** a private read-only Drive adapter. Later permissioned project adapters require separate, tested authorization and owner approvals. Never make a publicly served feed the destination for confidential data.

## Change and release controls

- Source changes are reviewed on GitHub; publishing derived metadata does not authorize other changes.
- Owner approval, customer contact, billing, dispatch, deployments and sensitive source access remain separate gates.
- The original `DEBO_Progress_Command_Center_v0.2.2_Guided_iPhone.html` stays private as rollback; never commit it or a user export to this public repository.
- A passing PR workflow does not prove the dashboard works on an actual iPhone or that private sources are live.

Mission: `DEBO-DASH-005`. Current status: public source adapter proposed until its PR is merged and end-to-end feed fetch is checked.
