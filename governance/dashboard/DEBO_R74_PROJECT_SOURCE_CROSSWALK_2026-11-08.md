# DEBO R74 | Canonical source crosswalk and freshness gate

Mission DEBO-MASTER-036. Date 2026-11-08 America/Chicago.
Checkpoint R74-READONLY-CROSSWALK-SAVED. Status: verified source inventory comparison; live project runtime still UNKNOWN.

## Two different inventories
- Private protected isolated Neon task branch: 14 distinct task IDs, not production, with status Backlog 1, Blocked 4, In Progress 4, Review 5. Its task IDs are WORK-ATHLETE-001, WORK-BASEBALL-001, WORK-BBS-001, WORK-CE-001, WORK-DEBO-001, WORK-DWING-001, WORK-JCT-001, WORK-MOL-001, WORK-NEON-001, WORK-PLOG-001, WORK-RRR-001, WORK-SETTLE-001, WORK-TPB-001, WORK-WRESTLE-001.
- Public GitHub governance/dashboard/DEBO_CORE_FEED_v1.json: 14 project source-health entries, all with live_operational_status UNKNOWN, last_live_verification null and approval_state UNKNOWN. These are project metadata, NOT the same 14 task records. No one-to-one equivalence or automatic synchronization is established.

## Crosswalk: task pillar -> governance project ID
| Task pillar | Public project | Evidence |
|---|---|---|
| DEBO | DEBO | Core project listed; profile_path null |
| CE-OS | CE | governance/sister-brains/CE_PROFILE_v1.md fetched |
| DWING | DWE | projects/dwing-exterior/DEBO_PROFILE_v2.md fetched |
| JCT | JCT | governance/sister-brains/JCT_PROFILE_v1.md fetched |
| RRR | RRR | governance/sister-brains/RRR_PROFILE_v1.md fetched |
| PLOG | PLG | governance/sister-brains/PLG_PROFILE_v1.md fetched |
| MORGANS | MOR | Listed in public source register; live not verified |
| BBS | BBS | Listed in public source register; live not verified |
| SETTLE | SETTLESURE | governance/sister-brains/SETTLESURE_PROFILE_v1.md fetched |
| DEBO-TPB-OS | BULLDOGS | Tentative alias; requires canonical confirmation |
| WRESTLE | CWA | Tentative alias; requires canonical confirmation |
| ATHLETE | NONE DIRECT | Task exists; no dedicated matching entry in public feed |
| BASEBALL | NONE DIRECT | Task exists; no dedicated matching entry in public feed |
| NEON | NONE DIRECT | Infrastructure task exists; no dedicated matching entry in public feed |

Additional public projects without directly mapped tasks: CREDIT, SCHOOL, HOUSING. These are not missing tasks by themselves. Rentals task WORK-RENTALS-001 remains deliberately excluded from isolated feed; do not reinsert without authority.

## Observations and gates
1. Verified six canonical project profile paths by fetching GitHub files: CE, DWE, JCT, RRR, PLG, SETTLESURE. Profiles are governance and routing evidence, not current operational status.
2. Public feed schema debo.core.public_feed.v1, classification PUBLIC_GOVERNANCE_METADATA_ONLY; explicitly no customer, financial or youth data and no writes.
3. The feed's source-health fields are UNKNOWN and last live verification null. Therefore do NOT display 14/14 project-health green or claim complete source reconciliation.
4. Three task aliases (ATHLETE, BASEBALL, NEON) have no direct public-feed project ID; two sports aliases (DEBO-TPB-OS, WRESTLE) are tentative. Resolve using existing private source registers and project checkpoints, not guesswork.
5. Public project source-health feed and private task feed must remain separated by provenance, permissions, timestamp and purpose. Do not merge private titles into the public JSON.
6. Existing source register filename governance/dashboard/DEBO_PROJECT_SOURCE_REGISTER_v1.json was not found at that exact path; this does not prove no register exists elsewhere.

## Safe next steps
Read latest authorized project-specific private checkpoints and establish task-to-source provenance for the five unresolved aliases; then generate a private read-only reconciliation receipt. Resolve source freshness per project, never infer from static profile hashes. Run actual iPhone/VoiceOver and unauthenticated access tests when respective test contexts are available. No production, deployment, role, permissions or data changes authorized or performed.

## Thread Index
R69 dispatch -> R72 iPhone JCT/RRR interaction -> R73 source and six-lane audit -> R74 project source crosswalk (this record).

Evidence: VERIFIED for read-only GitHub/Neon source queries and six file fetches; TENTATIVE for sports aliases; UNKNOWN for project live operational state.
