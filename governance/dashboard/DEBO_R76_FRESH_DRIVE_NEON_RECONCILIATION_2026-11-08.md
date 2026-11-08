# DEBO R76 | Fresh Drive-to-Neon reconciliation receipt

Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-036. Suggested title DEBO-00 | Work Stack Reconciliation & Source Freshness. Status READ_ONLY_VERIFIED, no production sync.

## Fresh source reads
Google Drive connected claimedgecompany account: CURRENT — DEBO Live Project Index — v1.0, spreadsheet 1T1udeSNxYEOU5HrS79V4hX6BTEw8XIfXB06-wUf8Gm8. Metadata returned 17 tabs including Portfolio Work Stack. Fresh A1:O25 read returned 15 populated work rows and the full 15-column source schema, preserving original free-text state, owner, priority, last_touched_at, blocker and next_action. Spreadsheet metadata modified 2026-10-30T11:08:43.858Z, source row last_touched_at mostly 2026-10-30; these are not live project acceptance times.

Neon connected claimedge isolated branch br-sparkling-forest-a6n5v8rd in project snowy-block-04251510: fresh SELECT of task_id, pillar, status, priority, updated_at returned 14 records. Fresh aggregate SELECT: rows=14, unique_ids=14, rentals_rows=0, earliest/latest updated_at=2026-11-08T11:35:22.858Z. These timestamps indicate the isolated copy's update, not source project freshness.

## Exact stable-ID crosswalk
All 14 isolated Neon task IDs are in the 15-row original Work Stack and retain their stable IDs. Original source contains one additional WORK-RENTALS-001, intentionally excluded due to owner HOLD. No missing authorized task IDs, no duplicate IDs, no unauthorized Rentals row. Historical reported 20-task inventory remains five unsourced records beyond the 15 actually read.

## Explicit source identities recovered
- WORK-WRESTLE-001: source project_id WRESTLE, project_name WrestlingOS. CWA is a separate project profile; do not equate CWA with WrestlingOS merely because a governance role map groups their scope.
- WORK-TPB-001: source project_id DEBO-TPB-OS, project_name Tinley Park Bulldogs Football / Film OS. This provides a documented functional link to Bulldogs; does not collapse all AthleteOS or Bulldogs project namespaces.
- WORK-ATHLETE-001: source project_id ATHLETE, project_name AthleteOS / Bulldogs QB. Separate team truth from Chase learning.
- WORK-BASEBALL-001: source project_id BASEBALL, project_name BaseballOS. Do not equate it with BBS just because baseball research appears in BBS hub.
- WORK-NEON-001: source project_id NEON, project_name Neon / Postgres Recovery. Infrastructure work, not a public project health entry.
Other exact source project IDs: DEBO, JCT, CE-OS, DWING, SETTLE, PLOG, RRR, MORGANS, BBS.

## Freshness/conflict
Original Work Stack status strings are 15 free-text project checkpoints, not native task workflow states. Isolated Neon statuses Backlog=1, Blocked=4, In Progress=4, Review=5 are normalized derived task statuses. They must NOT overwrite source free-text statuses. Original WORK-NEON-001 says 2026-10-30 connector showed zero visible projects; fresh 2026-11-08 authorized Neon read proves this isolated project and branch accessible, NOT recovery of all historical Neon projects. Mark original blocker as STALE_OR_SCOPE_SPECIFIC_PENDING_RECHECK rather than silently closing it. Original RRR/JCT status likewise does not prove current public customer intake.

## Tests executed
PASS: Google Drive source discovery, sheet metadata and source range read.
PASS: isolated Neon read-only 14-row listing and aggregate counts.
PASS: stable ID set membership comparison from these returned values (14/14 included, 1/15 held).
PASS: 14/14 unique IDs and 0 Rentals in isolated branch.
NOT TESTED: five-minute browser timer, anonymous SSO denial, VoiceOver, production task data, project-specific runtime E2E, missing five historical records.

## Next batch
Use original project-specific source references (Notion WrestlingOS S1, Bulldogs Film Mapping & Completeness, Floot AthleteOS, BaseballOS canonical unknown, Neon org inventory) to establish source-freshness per project. Update only private, nonproduction reconciliation receipt when evidence exists. Keep public project health UNKNOWN until operational verification. Do not edit source Google Sheet, public feed, or Neon task rows as a side effect of this audit.

## Thread Index
R74 initial source crosswalk -> R75 original Work Stack provenance and alias correction -> R76 fresh Google Drive/Neon crosscheck, verified source identities and freshness gap.

No spending, external contact, access changes, production deployment or data mutation.
