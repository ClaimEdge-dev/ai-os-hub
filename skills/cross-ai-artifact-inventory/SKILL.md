---
name: cross-ai-artifact-inventory
description: Inventory accessible AI accounts, projects, threads, uploaded sources, generated artifacts, skills, automations, settings and connectors without inventing coverage or duplicating DEBO's canonical registries. Use when asked to recover everything in Perplexity, Manus, Kimi, Claude, Gemini or another AI workspace.
---

# Cross-AI Artifact Inventory v1.0

Owner: DEBO / Vault, Sweep and Shield. Source candidate only. Inherit \`DEBO_BOOTSTRAP.md\` and canonical skill lifecycle rules.

## Objective
Produce an evidence-backed *coverage map*, not a false claim of inspecting every account. Respect tenancy, youth/private records, owner approvals and accessible connector limits.

## Recover first
1. Identify target provider and owning account/workspace. Never collect or print credentials, login emails, tokens, private record contents or personal secrets to public logs.
2. Inspect existing DEBO GitHub registry, Notion Skill Registry (94 rows in the R141 historical snapshot), source artifact register and latest Thread Index before creating records.
3. Determine actual access: NO ACCESS / UI READ / CONNECTOR READ / EXPORT READ / WRITE AUTHORIZED. A plugin being listed is not evidence of a connected tenant.
4. Reuse previous inventory by stable IDs, hashes and source path; refresh only changed or unknown scopes. Preserve originals.

## Inventory checklist per provider
- Provider, account/workspace (redacted ID), plan/feature menu and timestamp.
- Projects/workspaces, old/migrated names and instructions.
- Accessible threads, agents/tasks and continuation states.
- Attachments/uploads, export files, documents, source links, generated apps/sites/slides and versions.
- Skills/SKILL.md packages, triggers, owners, install status, source status, tests.
- Models/modes, connector permissions, automations, scheduled tasks, usage/cost visibility, account settings.
- Decisions, prior prompts, structured returns, failed work, unsaved handoffs and blocker receipts.
- Explicit inaccessible/private areas; report UNKNOWN, NEVER zero, when no read route exists.

## Canonical artifact row
\`\`\`json
{
  "provider": "Perplexity|Manus|Other",
  "workspace_key_redacted": "non-identifying-alias",
  "artifact_id": "stable-observed-id-or-UNKNOWN",
  "type": "project|thread|task|skill|file|model|connector|automation|decision|other",
  "title_redacted": "safe display title",
  "source_uri_private": "PRIVATE-POINTER-OR-NONE",
  "source_version_or_hash": "observed-or-UNKNOWN",
  "observed_at": "ISO8601",
  "status": "OBSERVED|RETRIEVED|SOURCED|TESTED|INSTALLED|APPROVED|LIVE|UNKNOWN",
  "owner_project": "DEBO|JCT|CE|DWE|RRR|PLG|MOR|CHASE|OTHER",
  "sensitivity": "PUBLIC|INTERNAL|PRIVATE|RESTRICTED",
  "canonical_destination": "existing-register-or-PRIVATE-HOLD",
  "dedupe_key": "provider/workspace/type/source-id",
  "gap_or_next_action": "concrete step"
}
\`\`\`

## Reconciliation
- Never assume two same-title artifacts are duplicates. Compare stable provider ID, owner, date, version/hash and semantic purpose.
- Never merge across business tenants or minor/credit/legal/claims domains without explicit authorization.
- Group each item as REUSE / UPDATE / MERGE-CANDIDATE / ARCHIVE-CANDIDATE / UNKNOWN; archives/deletions require owner approval.
- Assign source labels: VERIFIED READ, REPORTED, INFERRED, UNKNOWN, CONFLICTED. Only VERIFIED READ supports fresh completion.
- In existing Notion Skill Registry, ACTIVE is a historical catalog label, not working installation.
- Write one bounded delta into the existing private Notion Master/Thread Index only with verified write permission, then read back. Do not create a new master database.
- Return a coverage matrix: scope requested, scope accessible, records enumerated, files/skills/projects actually found, unreadable scopes, evidence links, unresolved conflicts, and ONE NEXT ACTION.

## Provider-specific routes
**Perplexity Pro without Computer:** use account's visible history/Projects and supported self-service export; export is controlled by the account owner. A public search or another AI cannot enumerate private history. No Perplexity account connector is currently verified in this ChatGPT context.

**Manus:** prefer authenticated Projects/Tasks/Skills/Connectors navigation or first-party authorized export; existing ChatGPT Manus connector may initiate a new research task but may not provide account-wide list/read APIs. Reuse preexisting task IDs such as the separate R148 dashboard task; no duplicate start.

## Tests
1. Missing connector returns UNREADABLE/UNKNOWN, not an empty complete inventory.
2. Identical title across two tenants remains separate.
3. Same stable ID/hash in same tenant dedupes safely.
4. Source file without install receipt stays SOURCE PRESENT only.
5. A private account export stays in authorized private storage and is never pushed to public GitHub.
6. Write confirmation without readback stays UNVERIFIED.
