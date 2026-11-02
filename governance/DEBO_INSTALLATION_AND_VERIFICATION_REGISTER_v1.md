# DEBO installation and verification register v1
Updated: 2026-11-02

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

This documentation update changed no CI workflow, anti-repeat control, owner approval, credential, schedule, or production system. The private decision record carries project-specific context outside this repository. The test-harness follow-up below supersedes the earlier unchanged-harness status. Rollback is reverting the relevant source commit.

### Same-day bootstrap test-harness repair
The automatic workflow on the decision-first documentation commit reproduced the previously investigated AR-08 failure: the temporary fixture deliberately removed AR-08, but `subTest` recorded rather than propagated the assertion expected by `assertRaises`.

The repair extracts the existing checks into `assert_anti_repeat_policy` without `subTest`. The positive test and both negative tests call that helper. AR-01 through AR-12, mandatory-gate and corrective-example checks, and temporary-copy isolation are retained. The canonical anti-repeat policy and workflow are unchanged.

Local verification: all 17 existing tests passed with `python3 -B -m unittest discover -s tests -p 'test_debo*.py' -v`. Hosted CI evidence must be associated with the follow-up commit; local success is not a claim about other AI runtimes or business integrations.

## 2026-11-02 compact golden-rule startup receipt

The existing runtime bootstrap now holds a ten-rule condensed working view of the canonical execution, JARVIS, communication, preventive and anti-repeat policies. Detailed requirements remain governing and load for their relevant triggers. Root `AGENTS.md`, `DEBO_BOOTSTRAP.md` and README now route to the same compact entry point. Unsupported automatic-sync wording and the stale fixed skill count were removed from README.

The existing read-only checker now supports `python tools/debo_bootstrap_check.py --brief --project JCT`, with `DEBO` for the master and all thirteen existing project profiles supported. Its default JSON integrity report is preserved. The brief extracts rules from the canonical bootstrap, selects one static project profile, lists detailed-policy triggers and fingerprints its actual local source files. It explicitly requires the latest authorized project checkpoint; no private checkpoint, account or live system is accessed by this command.

| Evidence | Result / limit |
|---|---|
| Before-change reproduction | The old checker ignored brief/project flags and returned only the integrity JSON; the focused project-brief regression failed for that missing output. |
| Existing integrity command | PASS: 23 required files, preserving the original 20 and adding the two root entry points and JARVIS source; thirteen profiles retained. |
| Repository test suite | PASS: 26 tests (17 inherited plus 9 focused brief/sync tests). Includes profile scoping, master scope, unknown-project rejection, missing-rule failure, source-fingerprint refresh, repeatable generation, global/project-only invalidation and symlink rejection. AR-01–AR-12 and durable-save failure tests remain intact. |
| Command route sweep | PASS locally: master plus all thirteen project IDs generated the intended scoped brief. |
| Startup text comparison | JCT sample: 15,159 characters for the prior three-policy startup plus the same profile, versus 6,380 characters for the derived brief, a 57.9% character reduction. This is an input-size comparison, not measured latency or model performance. |
| Automatic source refresh | Implemented in `.github/workflows/debo-runtime-briefs.yml`: trusted-main source changes regenerate all fourteen derived views; only changed outputs are committed, without force-pushing. PR validation is read-only. Local generation and freshness checks passed; hosted writeback still requires its actual run evidence. |
| Existing project-profile review | All thirteen profiles read. Twelve have shared generic controls plus a narrow domain scope; DWE has a more detailed source/identity map. Project-specific current facts and owner decisions must be recovered separately; no new domain authority was inferred or granted. |
| Runtime activation | UNKNOWN outside this local source command. No fresh ChatGPT, Kimi, Perplexity, Claude, Gemini or other runtime startup was demonstrated. |
| Hosted CI | Must be tied to the resulting source commit; no hosted pass is inferred from local tests. |

No required check, owner approval, budget boundary or anti-repeat rule was removed. The auto-update job has repository-content write access only for its authorized derived-file update; PR validation remains read-only. No ChatGPT schedule, new credential, customer data, production app or external AI setting was changed. This is a source/startup improvement, not autonomous model retraining. Roll back by reverting the source/workflow change and its derived-output commit. The next activation step is one supported clean-runtime task that loads the compact bootstrap and recovers its authorized project checkpoint.
