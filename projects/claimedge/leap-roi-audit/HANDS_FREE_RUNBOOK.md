# Hands-Free Runbook — Leap ROI / Neon / ClaimEdge
Status: ACTIVE

## Purpose
Allow Bobby to use short commands and messy voice-to-text while DEBO preserves state, chooses the correct lane, executes safe internal work, and stops only at real approval gates.

## Bobby command semantics

### "go" / "do it" / "keep going" / "finish"
- recover latest Resume Capsule;
- verify branch/project identity;
- execute next safe internal action;
- use up to two safe background lanes;
- update Task Delta register;
- QA;
- file/version;
- propagate reusable changes;
- checkpoint.

Do not ask Bobby to restate known project facts.

### New idea during active work
Classify:
- ADD_TO_CURRENT
- BLOCKING_PATCH
- PARALLEL_SUBTASK
- PARKED_IDEA
- PRIORITY_SWITCH
- GLOBAL_RULE_CANDIDATE
- PROJECT_RULE_CANDIDATE
- NEW_PROJECT_CANDIDATE
- DUPLICATE

Preserve the exact return point before switching.

## Auto-routing

| Input | Route |
|---|---|
| Leap/claim field, ROI, owner report | stay in this project |
| Claim-specific evidence/facts | ClaimEdge claim child lane |
| Global DEBO behavior | global promotion candidate |
| New durable domain | Auto-Brain Factory evaluation |
| GitHub schema/code/tests | current feature branch or technical child branch |
| Production change | approval queue |
| External message/send | approval queue |
| Unknown/uncertain | Inbox/Triage + truth state |

## Automatic safe actions
DEBO may do these without interrupting Bobby:
- recover existing artifacts;
- dedupe;
- compare versions;
- run read-only GitHub checks;
- run CI;
- update branch-only docs/code;
- create reversible internal skeletons;
- update registers/checkpoints;
- archive/supersede branch artifacts while preserving originals;
- research public/current architecture when required;
- flag missing evidence/conflicts;
- prepare deployment/configuration plans with placeholders.

## Approval-required actions
Stop before:
- production Neon apply;
- merging a release when merge itself is consequential;
- deploying production webhook receiver;
- enabling recurring production writes;
- sending customer/carrier/company messages;
- publishing;
- purchasing;
- deletion/destructive overwrite;
- sensitive disclosure;
- external account permission/security changes.

## Event observer
On any material new input, check:
1. did project truth change?
2. did blocker state change?
3. did a dependency unblock?
4. did a duplicate/conflict appear?
5. did a reusable global rule emerge?
6. does another artifact need propagation?
7. does the Resume Capsule need patching?

## Change propagation
When a material rule/schema/state changes:
- patch project prompt if behavioral;
- patch README/control docs if structural;
- patch schema/tests if technical;
- patch Task Delta state;
- patch Resume Capsule;
- record global promotion candidate if reusable;
- do not silently edit global DEBO Core from a child branch.

## Self-audit cadence
At meaningful checkpoints audit:
- forgotten tasks;
- stale blockers;
- orphaned files;
- duplicate/superseded artifacts;
- unfinished promises;
- missing checkpoints;
- connector drift;
- test coverage gaps;
- unpromoted reusable lessons;
- automation candidates;
- invoice/billable relevance.

## Stop condition
A run stops only when:
- objective is complete and checkpointed;
- a true external/access blocker prevents further execution;
- an approval gate is reached;
- Bobby explicitly redirects.
