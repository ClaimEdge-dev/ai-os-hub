# DEBO installation and verification register v1
Updated: 2026-10-19

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
| Other individual sister-brain profiles | UNKNOWN | Locate and test per-project profile loading |
| ChatGPT account-wide instruction activation | BLOCKED | No project/global instruction write control exposed in current chat |
| Existing ChatGPT threads updated | UNKNOWN | No verified cross-thread write mechanism |
| Plugin permission changes | NOT REQUESTED | Do not grant blanket unrestricted access |
| Neon Live Bridge synchronization | BLOCKED | Read attempt rejected; do not claim database writes |
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
