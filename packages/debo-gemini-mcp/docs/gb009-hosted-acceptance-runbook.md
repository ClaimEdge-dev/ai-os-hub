# GB-009 — existing private hosted acceptance, dry-run only

Status: **RUNBOOK PREPARED / ACTUAL PRIVATE TARGET NOT YET ATTESTED / NO HOSTED ACTION**.
Source baseline: PR #81, the private synthetic Site and existing R19 Lane 07 checkpoint.
This is not a deployment plan that can authorize itself. It cannot be executed
from a public GitHub file without owner-private target discovery and review.

## Exact target discovery is a blocking first step

1. Read the CURRENT existing DEBO owner-private Site identifier, source revision,
   hosting environment, signed-in owner, caller scope, project and D1 binding from
   its owning private checkpoint and actual authenticated host. Never copy its
   private URL, token, identity hash, receipt IDs or secret values into this PR.
2. Pin an exact tuple of (private Site ID, owner account, private plugin ID,
   verified source artifact/hash, existing D1 database/binding, schema version,
   provider-disabled runtime config). Read it back twice before testing.
3. If any field is missing, stale, contradictory, unverified or accessible only
   through a different owner/project, **STOP: TARGET_UNVERIFIED**. A public
   repository commit or successfully built bundle is not the deployed Site.

## GB-013: verify real Sites identity contract before relying on it

The official ChatGPT Sites documentation, consulted 2026-11-15,
https://learn.chatgpt.com/docs/sites/data-and-connections,
currently explicitly documents `oai-authenticated-user-email` and optional
`oai-authenticated-user-full-name` as sign-in identity headers. The existing
private `src/site_worker.mjs` and `src/mcp_worker.mjs` additionally require
`oai-authenticated-user-id`. That ID header is NOT established by the cited
public Sites text. Its absence from those pages does not prove the current
private managed-host dispatcher omits it. Treat this as HOST PROVENANCE UNKNOWN,
not a reason to remove owner-scoping or fabricate a fallback identifier.

For the EXACT existing private Site, the authorized owner must use a supported
authenticated host readback to verify all of the following before any release:
- The host supplies a stable server-trusted caller ID and an authenticated email,
  with spoofable client versions stripped or overwritten at the platform edge.
- Verified caller identity binds to the exact DEBO-CORE owner, plugin, source
  revision and D1 binding; client metadata cannot widen project scope.
- The host's protected resource / issuer / audience enforcement is documented or
  demonstrably equivalent for this Sites-managed identity mechanism. If separate
  OAuth 2.1 resource-token verification is required by the actual host topology,
  do not pretend platform headers are sufficient.
- Compare same-session owner reads, a signed-out negative case, and an isolated
  authorized other-caller negative case. Preserve private IDs/hashes off GitHub.
- NO credential, source publish, or permission change is made to collect proof.

Do not generate an SIWC bypass token to perform these identity tests: the
official Sites guide says bypass requests have NO signed-in visitor identity
headers, and creating a bypass token would rotate an existing token. The
existing owner-authenticated plugin receipt read is only synthetic data proof,
not proof of ID header provenance or deployed source revision.

**Acceptance status: HOLD until supported private host evidence is read back.**

## Required approvals, separated

- Existing private fixture receipt READ is allowed only at its current owner/
  project scope, with the host's supported authenticated connection.
- Running new hosted negative tests, changing host code/bindings, adding an
  execution migration, enabling credentials, independent reviews and release are
  separate actions, each requiring its relevant explicit approval.
- No nonbillable Gemini API entitlement, project/credential binding or real
  provider call has been verified. Keep DEBO_ENABLE_LIVE_GEMINI=false and
  staged execution disabled. Never use a copied API key, quota screenshot or
  synthetic approval callback as proof of account authority.

## Read-only checks before touching anything

Capture authenticated host source/version, exact caller and allowed DEBO-CORE
project only, available host plan/limits, secrets metadata without values, D1
migration state, and original synthetic receipt hash. Distinguish private host,
public PR source, fixture table and uninstalled candidate migration.

Use the source-only GB-003 preflight and GB-031 local schema checks to plan
the test. Their local success is not hosted evidence. The current Worker build
must still emit only four existing modules. Abort if there is a new external
fetch path, unapproved identity propagation, broadened project ACL, or new
client tool argument.

## Proposed authorized synthetic acceptance sequence (NOT RUN)

1. Read authenticated owner identity; verify verified-host provenance rather than
   accepting caller-supplied identity headers. Check exact destination.
2. Read the existing fixture receipt twice. Both results must have the same
   project, caller and receipt SHA; no new write on read.
3. Only with approved isolated test identities, check missing/expired session,
   mismatched owner, unexpected project and injected client headers are denied.
   Do not retry previously disallowed live cross-project reads by renaming IDs.
4. Verify request and response byte bounds, single durable claim owner,
   duplicate/timeout/replay/corruption cases in the approved isolated host
   with synthetic content and NO outgoing provider transport.
5. After separate explicit migration authorization, record target/version,
   inspect schema and rows metadata, apply only reviewed DDL once, read back
   exact schema/unique key and original receipt preservation. **This runbook
   itself does not apply SQL.**
6. Verify R19 result handoff using the existing private capsule store and an
   authorized genuinely separate session. A local Python checkpoint cannot
   prove automatic cross-chat host recovery.
7. Independently review exact source, host configuration, tenant boundary,
   credential-to-project eligibility, recorded output and rollback. Only
   after explicit owner release could an additional nonbillable provider
   contract check be considered.

## Rollback rehearsal prerequisites

Disable dispatch FIRST, verify it remains disabled and preserve original
CLAIMED / COMPLETED / UNCERTAIN records and synthetic receipts. Restore only
a recorded, independently approved private Site source version; preserve
request fingerprints, D1 tables and R19 capsules. Never DROP/DELETE claim
evidence or regenerate idempotency keys for uncertain operations. Avoid
force-push or unapproved private plugin reinstall. Document separate rollback
for code, host settings and migration; never conflate these.

## Acceptance report template

- Date/time, signed-in owner, exact private destination reference (private only)
- Public PR head, local build hash, actual deployed source/hash
- Authorized test scope and reviewer/owner approvals
- Host identity/audience/caller proof, D1 schema/migration evidence, fixture SHA
- Results per positive/negative check, no provider outbound requests
- Remaining financial authorization and R19 fresh-chat evidence
- Decision: PASS / FAIL / HOLD, with precise rollback and next action

Owner-private values belong in the existing Lane 07 private checkpoint, not in
GitHub. No live target, host test, permission change, migration, release, purchase,
or Gemini API request is claimed by saving this plan.
