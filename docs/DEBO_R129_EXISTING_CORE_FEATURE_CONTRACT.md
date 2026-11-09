# DEBO R129 | Existing-core feature contract (Spec Kit-style, adapted)

**Status:** Reusable source template only; GitHub Spec Kit CLI is **not installed**. Use DEBO Golden Rules as controlling authority.

## 1. Outcome
Mission ID:
Existing project / owner:
Target artifact or behavior:
Last verified checkpoint / source SHA:

## 2. Recovery and source truth
Canonical source path and version:
Current implementation and already-completed steps:
Relevant prior PR / rollback:
Source conflicts and evidence needed:

## 3. Authorization and isolation
Selected business tenant:
Required owner approvals:
Tools allowed (read / safe write):
Explicitly prohibited actions:
Private data handling / vault location:
External charges / network access:

## 4. Mack → Atlas → Forge → Proof
Mack: decide current missing task using R31/R128 (do not skip owner hold)
Atlas: design narrow change and rollback
Forge: implement in existing system only
Proof: test behavior, negative cases, security, actual readback
Shield: check actor, tenant, authorization
Vault: checkpoint one source-backed change

## 5. Acceptance tests
- [ ] Valid case passes
- [ ] Invalid / prompt-injected request cannot grant permission
- [ ] Duplicate step/action is not repeated
- [ ] Stale source and conflicting revision fail closed
- [ ] Cross-tenant attempt rejected
- [ ] Existing rollback is retained
- [ ] Actual current-commit test receipt recorded
- [ ] Installed/approved/live states distinguished

## 6. Completion record
Evidence refs (not unverified labels):
Actual test counts:
Production changes:
Known blockers:
Status (PROPOSED / BUILT / TESTED / INSTALLED / APPROVED / LIVE):
Next authorized action:

Do not reproduce private customer records or secrets in this public template.
