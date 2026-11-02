# DEBO installation and verification register v1
Updated: 2026-11-01

## Verification rule
VERIFIED means actual operation observed with evidence. DOCUMENTED means instructions saved, not runtime activated. BLOCKED means a required capability or permission was unavailable. UNKNOWN means untested. Never convert DOCUMENTED to VERIFIED merely because a repository file exists.

| Component | Status | Evidence / next test |
|---|---|---|
| GitHub master execution standard | DOCUMENTED | governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md |
| GitHub runtime bootstrap | DOCUMENTED | governance/DEBO_RUNTIME_BOOTSTRAP_v2.md |
| Communication and recovery standard | DOCUMENTED | governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md |
| Sister-brain profile template | DOCUMENTED | governance/SISTER_BRAIN_PROFILE_TEMPLATE_v2.md |
| D-Wing profile | DOCUMENTED | projects/dwing-exterior/DEBO_PROFILE_v2.md |
| Notion DEBO master control page | VERIFIED (page creation) | https://app.notion.com/p/3feb37124b6781ff8ea8fb9f245352e9 |
| Notion communication rules | VERIFIED (page creation) | https://app.notion.com/p/3feb37124b6781f184e4db058f5ecd3a |
| Individual sister-brain profiles (13) | VERIFIED (repository retrieval only) | All 13 GitHub profiles fetched on 2026-10-19; Neon tasks read back PROFILE_VERIFIED; runtime activation remains DOCUMENTED |
| ChatGPT account-wide instruction activation | BLOCKED | No project/global instruction write control exposed in current chat |
| Existing ChatGPT threads updated | UNKNOWN | No verified cross-thread write mechanism |
| Plugin permission changes | NOT REQUESTED | Do not grant blanket unrestricted access |
| Neon Live Bridge registry | VERIFIED (database access and metadata) | Project damp-math-10052614: 13 projects, 13 sister brains, 13 tasks read back PROFILE_VERIFIED; runtime sync not certified |
| Kimi/Perplexity/other AI autoload | UNKNOWN | Test independently in each runtime |

## Sister-brain audit queue
DWE, JCT, RRR, MOR, CE, PLG, BULLDOGS/ATHLETEOS, CWA/WRESTLINGOS, BBS, CREDIT, SCHOOL, HOUSING, SETTLESURE. Each must have distinct scope, source of truth, evidence and safe permissions.

## Per-project test
1. Load canonical bootstrap and project profile.
2. Recover last verified checkpoint without asking user to repeat known details.
3. Perform one safe reversible action.
4. Verify resulting record or artifact.
5. Record date, evidence, limitations and next action.

## Confusion flags
Use communication recovery standard: change explanation modality, distinguish misunderstanding from failure to execute, interpret imperfect speech-to-text contextually.


## 2026-10-19 sister-brain profile installation receipt
Twelve new repository profiles were successfully created under `governance/sister-brains/`: JCT, RRR, MOR, CE, PLG, BULLDOGS, CWA, BBS, CREDIT, SCHOOL, HOUSING, SETTLESURE. DWE was previously documented under `projects/dwing-exterior/DEBO_PROFILE_v2.md`. Status for each: DOCUMENTED (persistent GitHub file), not VERIFIED runtime autoload. Do not infer live project activation.

## 2026-11-01 decision-first delivery receipt
Routine implementation choices are delegated within the requested outcome, existing authority, and approved budget. The existing JARVIS policy now defines Quick / Build / Deep verification; the five-task benchmark is optional. Startup recovers the current checkpoint and loads specialist detail by relevance. Applicable controls remain governing.

| Surface | Status | Evidence / remaining scope |
|---|---|---|
| JARVIS decision and verification policy | DOCUMENTED | `debo/policies/DEBO_JARVIS_AUTONOMOUS_V2.md` v2.1; proportionate completion evidence replaces a blanket live-integration requirement. |
| Shared execution and startup | DOCUMENTED | Execution standard v2.1 and runtime bootstrap v2.2; scoped decisions, checkpoint-first recovery, and independent work through blockers. |
| Repository agent entry point | DOCUMENTED | Root `AGENTS.md` routes compatible repository sessions into the existing bootstrap; fresh-session execution remains unverified. |
| Repository file integrity | VERIFIED (source checks only) | `python tools/debo_bootstrap_check.py` passes on the patched pinned snapshot; link targets and whitespace checked before commit. |
| Other chats, AI runtimes, and live integrations | UNKNOWN | Verify their supported startup and operation separately; this source update does not establish account-wide activation. |

No test, CI workflow, anti-repeat control, owner approval, credential, schedule, or production system is changed by this patch. The previously investigated bootstrap negative-test harness remains unchanged; no full-suite pass is claimed. Rollback is reverting this documentation commit. The private decision record carries project-specific context outside this repository.
