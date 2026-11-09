# DEBO-05 R127 | Task editor for the EXISTING private Mission Control

**Status:** REVIEW CANDIDATE. Isolated Neon backend schema/function installed and tested via rolled-back fixture; live editor UI and editor LOGIN remain disabled/unprovisioned.
**Mission:** DEBO-MASTER-042 / R127. **Owner instruction:** enable task create, update, and delete from the dashboard.
**Canonical app:** Vercel `debo-private-command-r55`, protected by Vercel Authentication; latest authenticated task feed passed at R126.
**Current DB:** isolated Neon branch `br-sparkling-forest-a6n5v8rd`, existing `claimedge_os.tasks`, 14 mapped task rows. Current role `debo_dashboard_ro_r55` has SELECT but no INSERT/UPDATE/DELETE.

## Implementation contract
1. **KEEP READ-ONLY ROLE.** It remains the summary/API reader; no privilege escalation or shared database-owner credential.
2. Add separate **owner-only task-write role**, with EXECUTE on a tightly scoped, audited Postgres function, not unrestricted table DML.
3. Same-origin POST/PATCH/DELETE editor API has a dedicated high-entropy editor secret, no cross-origin support, no-store responses, validated fields, idempotency keys, stale-revision checks, and fail-closed disabled state.
4. POST creates new `DEBO-LOCAL-*` tasks. PATCH updates validated fields. DELETE means reversible **archive**. Hard delete disabled.
5. Imported `WORK-*` rows cannot be altered until an independent owner-approved authorization record is granted. `WORK-RENTALS-001` always denied. This preserves R119 mapping/owner and Housing holds.
6. The same current dashboard gets a small **Task Editor** panel and its original summary query is patched to return editor revisions and hide archived records. Reuse original source, navigation, styles, deployment and rollback. No second site or database.
7. Feature flag `DEBO_TASK_EDITOR_ENABLED` defaults false. Writer DSN is distinct from `DEBO_NEON_READONLY_DSN`; all secrets are configured through protected Vercel env after owner approval.
8. Run positive/negative API/SQL/auth/CSRF/RBAC tests and real signed-in preview acceptance before production promotion. A Vercel SSO viewer is **not** automatically an editor; Vercel deployment auth admits viewers and shareable links. Per-person identity is not proven by a single owner editor secret.
9. Preserve source, authorization and all before/after audit evidence. Never publish private task titles, claim/client/child details or passwords to this public repository.

## Exact current blocker and release boundary

The existing deployed API source is readable via the Vercel connector. The larger original `src/index.html`, `src/app.js`, `src/style.css` files returned **truncated contents**. Do not reconstruct or overwrite these original UI assets from truncated output. Obtain the complete editable originals first, apply the in-page patch and versioned summary change, then test in private preview before any production release.

Current R127 offline candidate has local Node unit tests and Python policy checks; uploaded to GitHub in this review branch only when exact source is present and verified. **Schema installed on isolated slice-day1 branch (November 9, 2026):** 9-statement additive migration committed, function+NOLOGIN group role read back. Original read-only role still cannot write; 14 existing tasks untouched. Transactional create → update → archive fixture passed and was rolled back to zero residual rows/audits. Imported WORK edit and held Rentals negative checks passed. No writer login, Vercel secret or UI release has been installed. User request to make tasks editable is an authorization to build this capability, not permission to silently expand everyone else's access, erase imported source rows, or bypass existing R119/John/Housing gates.

**Next action:** review exact existing UI source and owner write-key provisioning, then use an isolated branch for SQL + end-to-end authenticated write and rollback tests. Do not flip the live read-only DSN permissions as a shortcut.