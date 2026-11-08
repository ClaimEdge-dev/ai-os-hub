# DEBO R75 | Work Stack provenance, alias correction and next-batch gate

Date 2026-11-08 America/Chicago. Mission DEBO-MASTER-036. Parent DEBO-00.
Checkpoint R75-WORKSTACK-PROVENANCE-AND-ALIAS-CORRECTION.
Status VERIFIED read-only historical source recovery; unresolved alias and project runtime claims held.

## Verified original Work Stack receipt
Read governance/dashboard/DEBO_MASTER_024_TASK_MAPPING_DRYRUN_2026-11-08.md. It documents two identical Google Drive/Sheets source reads, 15 source rows, 15 unique IDs, zero duplicates and 15 incompatible free-text source statuses. This is a historical verified receipt, not a fresh Google Sheets read in R75. Original 15: WORK-DEBO-001, WORK-JCT-001, WORK-CE-001, WORK-DWING-001, WORK-SETTLE-001, WORK-PLOG-001, WORK-RRR-001, WORK-MOL-001, WORK-BBS-001, WORK-WRESTLE-001, WORK-ATHLETE-001, WORK-BASEBALL-001, WORK-RENTALS-001, WORK-NEON-001, WORK-TPB-001.

Private isolated Neon dashboard has 14 of these, excluding WORK-RENTALS-001 by explicit hold. Original reported 20-task inventory still has five unsourced IDs. Do not fabricate missing records or treat held Rentals as a missing record.

## Alias correction to R74
- WRESTLE -> CWA is NOT VERIFIED. governance/sister-brains/CWA_PROFILE_v1.md explicitly identifies Celtic Wrestling Academy, whereas governance/dashboard/DEBO_MASTER_024_THREAD_HANDOFF_2026-11-07.md explicitly says CWA is distinct from WrestlingOS. Keep WRESTLE unmapped until a canonical WrestlingOS source is recovered.
- DEBO-TPB-OS -> BULLDOGS is NOT VERIFIED. governance/sister-brains/BULLDOGS_PROFILE_v1.md establishes the Tinley Park Bulldogs project, not an identity with DEBO-TPB-OS. Keep unresolved.
- ATHLETE, BASEBALL, NEON remain without matching public project register IDs. Do not create new public entries without governance review.
- Source IDs, project IDs and dashboard lanes are separate namespaces. Matching descriptions are not proof of identity.

## Freshness and status gate
governance/dashboard/DEBO_CORE_FEED_v1.json contains 14 public project entries; all have live_operational_status UNKNOWN, last_live_verification null and approval_state UNKNOWN. Static profiles and hashes do not establish current live state. The R73 protected private task endpoint is a distinct source, not a production cross-project sync.

## Next executable batch
1. Recover original Google Drive Live Project Index source and latest authorized Work Stack checkpoint; compare stable IDs, original free-text status and timestamps without coercion.
2. Locate WrestlingOS, DEBO-TPB-OS, AthleteOS, BaseballOS and Neon canonical adapter/brief; resolve aliases only with explicit project IDs.
3. Verify 15/15 original IDs against the isolated task branch with the held Rentals exclusion; test duplicate and freshness checks.
4. Preserve the five-row 20-task discrepancy as UNRESOLVED until source evidence.
5. Run authenticated browser interaction, VoiceOver, elapsed five-minute refresh and independent anonymous access denial tests when appropriate test contexts are available.
6. Only after verified project source evidence, prepare private source-health reconciliation; no public feed exposure of private work details, no production migration.

## Thread Index
R73 read-only dispatch audit -> R74 first public/private source crosswalk -> R75 historical Work Stack provenance and alias correction.

No production writes, new deployment, permission change, customer contact, spend, or release approval. Roles are responsibilities, not independently running agents.
