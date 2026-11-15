# GB-004 / GB-005 — uncertainty and R19 acceptance contract

Status: DOCUMENTED / REVIEW-ONLY / NOT ACTIVATED. Source: the existing D1ExecutionGate, the transport receipt contract in PR #81, and canonical tools/debo_r19_continuity.py. No migration, provider API call, private content transfer or release is authorized by this document.

## GB-004 — uncertain-outcome reconciliation

| Current durable state | Permitted existing behavior | Forbidden behavior |
| --- | --- | --- |
| No claim | First new claim only after trusted owner, exact project and provider, fresh financial authority, primary-consistent insert and readback. These prerequisites are NOT established for live Gemini. | A client assertion or an assumed free tier cannot authorize a call. |
| CLAIMED | Original claim owner may finish only with matching saved request, owner token, complete result and checked immutable receipt, or mark UNCERTAIN. | New claim owner, changing the request, bypassing the same key. |
| COMPLETED | Check and replay the same receipt without a provider call. | Redispatch on replay. |
| UNCERTAIN | HOLD, retain original row indefinitely unless a separately approved operator process establishes outcome. | Time-based reclaim, automatic retry, rotating keys, automatic promotion to COMPLETED. |
| Provider outcome unknown | Stay UNCERTAIN; report ambiguity without guessing an expense or result. | Treat missing receipts as proof of zero provider calls. |

Who can reconcile in a future workflow: a specifically authorized incident operator, with independent reviewer and owner-approved hosted capability. Normal plugin callers, autonomous agents and background jobs never obtain reconciliation authority by using an execute or receipt-read permission. No such operator interface currently exists.

Minimum future evidence: original project, owner, provider scope and immutable request hash; durable claim ID/state; independently authenticated provider outcome tied to that request; human decision and reviewer identities; timestamps and evidence hashes; explicit approval record and rollback. Preserve an append-only adjudication trail. Any database state transition requires a separate audited, reviewed migration/action. This contract itself makes no state changes.

The current staged request sets store:false and background:false. Per Google's Interactions documentation, non-stored interactions cannot use previous_interaction_id. Do NOT presume that a GET can recover a lost non-stored response. If the outcome is unknowable, hold it permanently rather than redispatch. Changing retention to ease reconciliation requires separate privacy approval.

## GB-005 — provider result to the existing R19 capsule

The canonical format is debo.r19.capsule.v1 in tools/debo_r19_continuity.py. Existing fixed synthetic MCP fixture receipts do NOT establish Gemini execution.

A future separately approved private projection adapter must:
1. Retrieve a COMPLETED, primary-consistent durable execution through the owning authenticated caller, project and idempotency key. Validate the transport receipt schema, entire saved request/result, all recorded hashes and provider scope. Reject raw client/model receipt claims.
2. Resolve project, mission, existing task_id, objective and authorization from the owning R19 task source, not from model output. Project and owner mismatches fail closed.
3. Map only to the established R19 keys: schema, project_id, mission_id, task_id, objective, status, checkpoint, evidence, next_action, scope and as_of_utc. Use a new versioned checkpoint and private scope by default. Preserve the owner-defined task_id. Do not invent a task from an interaction ID.
4. Keep status BUILT until owner task acceptance proves TESTED with a typed test_receipt. A successful HTTP response does not automatically grant APPROVED, DEPLOYED or LIVE. Follow R19 status-to-evidence validation. Supported evidence types are source_readback, test_receipt, owner_approval, deployment_receipt and runtime_probe.
5. Save via the existing authorized private R19 continuity route, with no-overwrite semantics and exact readback. If save/readback fails, report NOT_SAVED. No parallel task table, public raw provider output, automatic cross-chat loader or new scheduler.
6. For CLAIMED, UNCERTAIN, corrupted, revoked, cross-project or mismatched receipts: no result projection. If a blocker note is needed, use an existing separately authorized private path.

Acceptance remains OPEN: local end-to-end projection against the real R19 validator and synthetic durable receipt; corruption, revocation, cross-project, duplicate-save and privacy tests; fresh separate chat recovery; approved hosted runtime identity and financial evidence. No such end-to-end or hosted run is claimed here.

## Scope and source anchors

- Existing staged executor and D1 gate remain excluded from both Worker entry points.
- PR #81 remains DRAFT / MERGE HOLD / LIVE API HOLD. PR #80, browser PR #74 and DEBO-05 remain separate.
- [R19 canonical source](https://github.com/ClaimEdge-dev/ai-os-hub/blob/main/tools/debo_r19_continuity.py)
- [Google Interactions API](https://ai.google.dev/api/interactions-api)
- [Google Interactions overview](https://ai.google.dev/gemini-api/docs/interactions-overview)
