---
name: universal-website-factory
description: Recover, build, repair, and test business websites using one brand-independent workflow and isolated company adapters. Use for website starts, redesigns, frontend upgrades, mobile/accessibility QA, forms/CRM integrations, and private release review. Reuse existing DEBO projects, site source, design systems, and QA skills before creating new assets.
---

# DEBO Universal Website Factory v0.1 (REVIEW CANDIDATE)

**Owner:** DEBO Core / Skill Lifecycle Manager. **State:** source candidate on a review branch, not installed, tested end-to-end, approved, or live.

## Purpose and nonduplication

This is one cross-brand website workflow, not a new CRM, component framework, project registry, deployment service, or AI operating system. Inherit the current DEBO bootstrap, runtime brief, selected company adapter, and latest verified checkpoint. Before building, compare the existing site, project skills, designs, repo, and private preview. If an existing skill covers at least 70% of the requested job, route to or extend that skill. Use the existing Skill Registry and project-scoped IDs.

**Trigger examples:** "DEBO BUILD SITE", "Recover this website", "Upgrade the frontend", "DEBO POLISH", "DEBO TEST SITE", "Prepare private release".

## Required input contract

- Project identity and approved tenant, or a source pointer sufficient to resolve it.
- Requested outcome: RECOVER / BUILD / REPAIR / POLISH / TEST / RELEASE-REVIEW.
- Existing canonical repo, branch/commit, preview and design source when available; unknowns stay UNKNOWN.
- Business truth source, brand assets, audience, sensitive-data restrictions, and owner gates.
- Authorized tools and budget. No new spending, permissions, messaging, production write or public launch by default.

If only a project name is supplied, recover the above from authorized sources; do not ask for already recorded details.

## Workflow

### 1. RECOVER and reconcile

1. Load DEBO Core, project adapter, prior checkpoint and source/preview revisions.
2. Inventory relevant repo files and accessible design/Drive/Notion artifacts without treating a search as exhaustive.
3. For an authorized local directory/ZIP, run the existing read-only inventory tool documented in docs/DEBO_UNIVERSAL_WEBSITE_AND_PROJECT_RECOVERY.md; keep detailed report private.
4. Identify canonical source using commits, owner decisions, tests and deployment receipts, not filename recency.
5. Preserve working features and historical evidence. Classify gaps REUSE / UPDATE / BUILD / MERGE-CANDIDATE / HOLD.

### 2. DEFINE the site contract

Capture the minimum complete requirements: pages, user roles, core actions, navigation, approved claims, forms, data flow, mobile behavior, analytics, accessibility, SEO, acceptance checks, and release gate. For existing sites, produce a delta instead of a fresh giant specification.

### 3. DESIGN with brand isolation

Reuse approved logos, colors, typography, imagery and content. Build project-specific tokens and accessible components. Keep brand and customer/youth data in the owning project. Figma, Canva and other design apps are optional adapters, not required dependencies. Never invent reviews, licenses, prices, service coverage, or business claims.

### 4. BUILD the smallest compatible change

Prefer the site's existing stack. Support HTML/CSS/JS, React, Next.js and TypeScript when appropriate. Reuse navigation, responsive layouts, forms, error/loading states, dashboard primitives and accessibility patterns. Avoid introducing a new framework, paid platform or backend without a demonstrated gap.

### 5. INTEGRATE only authorized systems

Recover the existing backend/CRM and data contracts. For forms and portals, check validation, consent, provenance, dedupe, authentication, tenant isolation, rate limits, errors, secrets and rollback. Do not create production customer records or enable outbound messaging without approval.

### 6. VERIFY proportionately

Use existing repo tests and, when available, Playwright, Vitest, axe, Lighthouse, static checks and authenticated private previews. At minimum inspect:

- 320px, 390px, 430px, tablet and desktop layouts; touch and keyboard use.
- Navigation, forms, errors, loading, metadata, links and approved business claims.
- Protected routes, negative authorization cases, privacy and cross-tenant separation.
- Existing feature regression and preview-to-source revision match.

Record exact commands, commit, results and skipped checks. Source inspection alone is not a runtime or visual test.

### 7. RELEASE REVIEW, not automatic release

Prepare a private preview, screenshots where supported, changed-feature list, test evidence, business-truth review, accessibility findings and rollback instructions. Respect project-specific approval gates (including John/Susan where applicable). No protected merge, public deployment or production activation without authorization.

### 8. FILE and CHECKPOINT

Update the existing project checkpoint, not a new tracker. Record canonical commit, design source, implemented changes, tests, unresolved conflicts, approval state, and one next safe action. Use the existing Notion/Drive/GitHub source hierarchy and ThreadOps. Verify writes by readback.

## Routing and reuse examples

- **JC's Towing:** inherit projects/jcs-towing/skills/jct-website-release-qa, jct-website-conversion, and jct-website-crm-sync. Do not overwrite the JCT business-truth or owner gate.
- **Celtic Wrestling Academy:** recover the actual site repository and current review checkpoint; use synthetic youth/tournament fixtures only until authorized.
- **D-Wing, Morgan's, ClaimEdge:** load their own project adapters, business truth, branding and approved integrations. Generic components may transfer; customer-specific content may not.
- **Project cleanup:** route to autonomous-ops-architect, chatgpt-workspace-steward, universal-file-vault, cross-ai-artifact-inventory and existing R19 continuity rather than building a second rescue registry.
- **Skill packaging:** route to skill-lifecycle-manager and Plugin Autopilot only if a real installable plugin is needed.

## Acceptance scenarios (must be executed, not merely listed)

1. Existing working site + cosmetic request: preserve routes and forms; isolated patch and regression check.
2. New brand with no repo: recover registry first, then propose minimal new setup; no duplicate project.
3. Same component in two businesses: reuse generic code, never reuse private customer content.
4. Unverified preview or inaccessible backend: report UNKNOWN/BLOCKED, not LIVE.
5. Missing approval for production release: produce private review packet and HOLD deployment.
6. Form auth negative case: unauthorized access fails safely; no real records touched.
7. Source present without runtime installation receipt: SOURCE CANDIDATE, not INSTALLED.

## Output contract

MISSION | RECOVERED CANON | REUSE/BUILD DECISION | CHANGED FILES | TEST RECEIPTS | PRIVATE PREVIEW STATUS | APPROVAL GATES | CHECKPOINT | NEXT ACTION.

**Failure behavior:** preserve original sources; one materially different authorized fallback; continue independent safe work; never fabricate file access, test results, connector status, or publication.
