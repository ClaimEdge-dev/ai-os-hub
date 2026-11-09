# DEBO MASTER | R129 Plugin Optimization and Connected Tool Evidence

**Mission:** DEBO-MASTER-044 joined to DEBO-MASTER-043 / R129. **Date:** 2026-11-09.
**Suggested chat:** DEBO-00 | Plugin Intelligence & Secure Execution.
**Status vocabulary:** CATALOG-EXPOSED / TOOL-AVAILABLE / CONNECTED-READ / VERIFIED-WRITE / VERIFIED-E2E / TENANT-UNVERIFIED / PROPOSED / AUTH-REQUIRED. Presence in a tool directory is not authority for every sister business.

## First: evidence hierarchy and current high-value findings

- **GitHub** is verified E2E for source recovery, PR branch editing, exact-commit CI checks and safe merges on existing DEBO source. This session verified **20** accessible ClaimEdge-dev repositories. Private `claimedge-command-center` schemas and `claimedge-vault` manifests are reusable concepts but not automatically transferable across tenants or suitable for public copying.
- **TinyFish** has an authorized saved browser profile that ran DEBO-05 authenticated private dashboard acceptance in R126: 14 unique tasks and private isolated Neon task feed. A profile does not grant SSO bypass or any other business account.
- **PostHog** is **CONNECTED-READ to a workspace called Default project**, but it is not verified as belonging to the DEBO-05 Vercel application or any target business. Read-only `project-get` on 2026-11-09 reported `ingested_event=false`, `completed_snippet_onboarding=false`, `session_recording_opt_in=false`, `anonymize_ips=false`, with console/performance capture toggles available. **Do not install an SDK, turn on capture, or send claims/customer/youth/PII data until an exact tenant match, privacy review, event taxonomy, and intended outcome are approved.** No project token/host was copied into this public repository.
- **Neon** verified restricted dashboard reader and real isolated R127 transactional create/update/archive/reversal acceptance; the live dashboard editor UI and separate writer login remain NOT INSTALLED.
- **Notion** master checkpoint and thread-index writes/readbacks verified previously. This plugin register should be appended to those existing pages after CI, not a new duplicate master.
- **Vercel** SSO and authenticated DEBO-05 site were actually tested through browser; project `live=false` remains a control-plane distinction from private signed-in acceptance.
- **Automations** includes established morning brief, System Scout, JCT readiness and Chase opportunity recurring tasks from user-visible control context. Verify each current status before any schedule modification. Never create a duplicate.
- **GitHub R129 pilots** Agents SDK scripted actual handoff CI PASS, Promptfoo 8/8 offline contract cases PASS at first branch head; Gitleaks reported 2 potential findings and is deliberately BLOCKING pending safe file/rule triage.

## Priority plugin and software routing matrix (1–25)

| Rank | Provider | Evidence this session | DEBO task and next real gate |
|---:|---|---|---|
| 1 | GitHub | Verified read/write/PR/CI via authenticated tool | Reuse current main, R31/R128, and source-safe branch/CI receipts |
| 2 | TinyFish | Verified authenticated DEBO-05 browser R126 | Existing profile only; no blanket external site access |
| 3 | PostHog | Connected workspace read, **no ingested events**, tenant match UNVERIFIED | Privacy review + exact DEBO site ownership before error telemetry |
| 4 | Neon | Verified isolated read role and transaction rollback backend write | R127 owner editor login/preview still separate; preserve reader privilege |
| 5 | Notion | Verified existing Master + Thread Index append/readback | Save one checkpoint delta; do not duplicate lifecycle registry |
| 6 | Google Drive | Plugin tool available, target source/tenant not checked here | First-party claims/evidence only under correct business owner permissions |
| 7 | Vercel | Verified private deployment/SSO and R126 signed-in task feed | Keep UI preview/rollback and mobile VoiceOver release gate |
| 8 | ChatGPT Automations | Existing scheduled tasks reported; no edits this run | Check actual task status/run receipts; dedupe before new schedule |
| 9 | Plugin Creator | Tool available, no proven missing product integration | Defer private connector until concrete gap vs current GitHub/Notion |
| 10 | Firecrawl | Tool available, no user tenant/operation tested | Public reference extraction only, never protected records |
| 11 | Supabase | Tool available; no tenant checked this session | Only authorized JCT/RRR or existing named project DB |
| 12 | CompanyCam | Two related tool families exposed; tenant UNVERIFIED | Restricted claim/job evidence with real account permission readback |
| 13 | Airtable | Tool available, tenant UNVERIFIED | Use only if project has an existing canonical register |
| 14 | Linear | Tool available, engineering queue not designated canonical | Avoid making another global backlog |
| 15 | PLAUD | User reports available, not connected; **no install performed** | Consent-aware voice-to-task source ingestion once connected |
| 16 | Figma | Tool available; project/design binding UNVERIFIED | Edit existing DEBO/JCT flows; do not recreate app |
| 17 | HubSpot | Tool available; CRM tenant not checked | Scope leads/deals per approved business |
| 18 | Apollo.io | Tool available; customer/account status UNVERIFIED | B2B prospect research with source and outreach approval |
| 19 | Metricool | Tool available; brands unverified | Source-backed authorized brand results |
| 20 | Superpowers | User-provided catalog claim, not executable plugin tested here | Reuse code-review/TDD methodology; avoid extra tooling until verified |
| 21 | Slack | Tool available; workspace/permission unverified | Owner-approved decisions only; no customer notifications |
| 22 | G2 MCP | Tool available; source-review pilot pending | Vendor comparison when choosing real service costs |
| 23 | tldraw | User reports available, not connected | Defer unless editable diagram requirement unmet by existing tools |
| 24 | Supermetrics Marketing Agent | User reports available, not connected | Defer until Metricool/HubSpot reporting proved inadequate |
| 25 | DocuSign | User reports available, not connected | Only legal agreements with signer consent and owner review |

**Lower priority:** Replit, Lovable, Asana, Todoist, Otter and Fireflies if existing platforms suffice. User directory statuses are historical input; runtime and tenant claims must be independently checked for each targeted action. No vendor software is to be installed solely to increase a plugin count.

## Target workflow: reused, no extra control plane

~~~mermaid
flowchart TD
    OWNER["Owner and business approval"] --> M["Mack / One DEBO Core"]
    M --> G["GitHub / source and CI"]
    M --> B["TinyFish / authenticated browser"]
    M --> R["Notion + scoped Drive / evidence"]
    M --> N["Neon / tenant-bound tasks"]
    G --> QA["Proof + Shield / verification"]
    B --> QA
    N --> QA
    QA --> V["Vault / existing checkpoint"]
    V --> M
    PH["PostHog / optional privacy-safe observability"] -.-> QA
~~~

The dashed PostHog connection is NOT installed in DEBO-05 and has no verified incoming events. Reusing external service actions requires exactly scoped tenant checks, not simply a "plugin installed" label.

## Highest priority acceptance tests and decisions

1. **R129 security / software upgrade:** Gitleaks finding triage first. Block CI until real source findings are classified/remediated; no blanket bypass or exposed tokens. Promptfoo deterministic guardrail tests and SDK scripted handoffs are available only through ephemeral pinned CI, not independent deployed agents.
2. **GitHub → QA → Notion:** Use exact source SHAs, CI results, and current PR state to append ONE R129 delta to the original Notion Master and Thread Index, then read back. This is a real integration chain with existing connectors, not a new project register.
3. **PostHog:** Existing default project is connected, has no recorded events and lacks verified binding to DEBO-05. Leave untouched until owner/source/PII handling are verified.
4. **TinyFish / Vercel / Neon:** R126 already passed. Do **not** rerun merely to claim repeat activity; keep R127 editor preview and identity gate separate.
5. **R19 fresh cross-chat:** still unverified. Browser and ChatGPT external session limitations do not become a success just because policy docs and generated briefs exist.

**Current work boundary:** No plugin installation, purchase, new schedule, PostHog event capture, CRM mutation, public deployment or production database permission change in this batch. ClaimEdge review gates, JCT John fixture, R119 Work Stack mappings and Housing hold remain.
