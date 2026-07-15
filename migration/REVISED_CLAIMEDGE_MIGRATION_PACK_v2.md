# ClaimEdge Skill Migration Pack v2
## Complete Reorganization: 67 Skills → 12-Pillar Architecture + Notion Schema + GitHub Starter Pack

**Owner:** Robert Krapil, ClaimEdge LLC  
**Email:** robert@claimedge.com  
**Prepared:** July 2025  
**Status:** Ready for Execution  
**Total Skills:** 67 | **Pillars:** 12 | **Naming Convention:** `claimedge__<pillar>__<function>__<variant>`

---

## 1. Executive Summary

### What We're Doing
Robert Krapil is no longer affiliated with Huuso Exteriors. All Huuso-branded skills (7 core + scattered references) must migrate to ClaimEdge branding. This pack provides the complete roadmap to reorganize all 67 existing skills into a clean, 12-pillar ClaimEdge-only architecture.

In addition to skill migration, this pack includes:
- **Notion 8-Database Schema** — a complete operational backbone with Skills Registry, Roles, Tasks, Migration Tracker, References, Skill QA, Risk Matrix, and Memory/Lessons Learned
- **GitHub Starter Pack** — the first 5 core ClaimEdge skills as GitHub-ready folders with standard `SKILL.md` patterns
- **Step-by-step setup guides** for both Notion and GitHub

### Why
- **Brand separation** from Huuso Exteriors is complete and must be reflected in all AI skills
- **Operational clarity** — current naming is inconsistent and hard to navigate
- **Future-proofing** — new hires, clients, and systems need clean taxonomy
- **Productization** — ClaimEdge is becoming a standalone brand; skills must match
- **Governance** — Notion databases provide skill tracking, QA, risk control, and audit history
- **Version control** — GitHub repository gives proper skill versioning, review gates, and deployment tracking

### Expected Outcome
- 67 skills organized into 12 clean pillars
- 0 Huuso references in active skills
- Consistent `claimedge__pillar__function__variant` naming across all skills
- 8 linked Notion databases serving as operational source of truth
- 5 starter skills deployed in GitHub with `SKILL.md` structure
- Clear migration tracker with priorities and effort estimates
- Golden path workflow mapping skills to the claim lifecycle

### Migration Scope Summary
| Category | Count | Action |
|----------|-------|--------|
| ClaimEdge-native (no change needed) | 27 | Minor naming alignment only |
| Migrated-from-Huuso | 7 | Rebrand + content update |
| Wrestling/Sports domain | 18 | Reorganize under `sports-ventures` pillar |
| Personal AI Ops | 15 | Reorganize under `ai-os-infrastructure` pillar |
| **Total** | **67** | **Phased rollout** |

---

## 2. The 12-Pillar Architecture

Each pillar owns a distinct phase of ClaimEdge operations. Every skill maps to exactly one pillar.

| # | Pillar | Scope | Skill Count | Color Code |
|---|--------|-------|-------------|------------|
| 1 | **claim-intake-triage** | New claim intake, triage, routing | 5 | |
| 2 | **policy-coverage-review** | Policy analysis, coverage verification | 1 | |
| 3 | **inspections-field-evidence** | Field inspections, photo documentation, evidence collection | 4 | |
| 4 | **exterior-damage-assessment** | Roof, siding, gutter damage evaluation | 3 | |
| 5 | **code-compliance** | IRC/IBC/IECC codes, municipal compliance | 2 | |
| 6 | **estimate-supplement-support** | Xactimate, supplements, scope building | 2 | |
| 7 | **carrier-communications** | Letters, negotiations, disputes | 1 | |
| 8 | **document-assembly** | Report generation, packet assembly | 2 | |
| 9 | **jurisdiction-research-library** | State laws, case law, legal resources | 1 | |
| 10 | **ai-os-infrastructure** | Skills, automation, connectors, vault | 16 | |
| 11 | **sports-ventures** | Wrestling, Buddy Boy Sports | 18 | |
| 12 | **productization-rd** | New products, courses, monetization | 6 | |

### Pillar Responsibility Matrix

| Pillar | Primary Role | Key Outputs | Related Legacy Skills |
|--------|-------------|-------------|----------------------|
| claim-intake-triage | Initial claim intake, severity scoring | Triage reports, routing decisions | claimed-master-workflow |
| policy-coverage-review | Policy interpretation, coverage mapping | Coverage memos, exclusion analysis | claimedge-complete-system |
| inspections-field-evidence | Photo evidence, field notes, damage docs | Photo logs, inspection reports | claims-evidence-orchestrator, claimedge-full-claims-investigation |
| exterior-damage-assessment | Damage scoping for roofing/siding/gutters | Damage assessments, Haag classifications | claimedge-roof-valley-claims, wind-hail-property-claims |
| code-compliance | Building code research, municipal lookups | Code citations, compliance reports | municipal-code-compliance-toolkit, claimedge-material-hazards |
| estimate-supplement-support | Xactimate scope, supplement writing | Estimates, supplement narratives | huuso-estimate-builder, huuso-supplement-writer, chicago-xactimate-pricing |
| carrier-communications | Letters, representation, dispute letters | Carrier correspondence, demand letters | huuso-supplement-writer (partial) |
| document-assembly | Final packet assembly, attorney-ready docs | Complete claim packets, timelines | claimedge-auto-deploy, claimedge-vault-system |
| jurisdiction-research-library | IL legal resources, case law, statutes | Legal research, precedent finder | illinois-legal-resource-directory |
| ai-os-infrastructure | Skill management, session memory, automation | Deployed skills, memory persistence | claimedge-skill-forge, claimedge-session-memory, all personal AI ops |
| sports-ventures | Wrestling analytics, Buddy Boy Sports | Rankings, scouting reports, team mgmt | All 18 wrestling/sports skills |
| productization-rd | Training courses, new products, monetization | Training materials, product specs | claimedge-training-builder, social-proof-builder, content-repurposer |

---

## 3. Complete Skill Migration Table

### CLAIMS DOMAIN (27 Skills)

| # | Current Name | New Name (Proposed) | Pillar | Status | Effort | Priority | Notes |
|---|-------------|---------------------|--------|--------|--------|----------|-------|
| 1 | claim-command-center | `claimedge__claim-intake__command-center__multi-agent` | claim-intake-triage | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 2 | claimed-master-workflow | `claimedge__claim-intake__master-workflow__5-phase` | claim-intake-triage | ClaimEdge-native | Low | P0 | Rename to fit convention |
| 3 | claimedge-auto-deploy | `claimedge__document-assembly__auto-deploy__notion-neon-github` | document-assembly | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 4 | claimedge-complete-system | `claimedge__policy-coverage__complete-system__15-course` | policy-coverage-review | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 5 | claimedge-full-claims-investigation | `claimedge__inspections__claims-investigation__12-agent` | inspections-field-evidence | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 6 | claimedge-master-coach | `claimedge__ai-os__master-coach__personal` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 7 | claimedge-material-hazards | `claimedge__code-compliance__material-hazards__identification` | code-compliance | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 8 | claimedge-roof-valley-claims | `claimedge__exterior-damage__roof-valley__wood-cedar-metal` | exterior-damage-assessment | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 9 | claimedge-session-memory | `claimedge__ai-os__session-memory__persistent` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 10 | claimedge-skill-forge | `claimedge__ai-os__skill-forge__arsenal-mgmt` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 11 | claimedge-training-builder | `claimedge__productization__training-builder__auto-generate` | productization-rd | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 12 | claimedge-vault-system | `claimedge__document-assembly__vault-system__archive` | document-assembly | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 13 | claimedge-weather-researcher | `claimedge__inspections__weather-researcher__noaa-nws` | inspections-field-evidence | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 14 | claims-evidence-orchestrator | `claimedge__inspections__evidence-orchestrator__12-agent` | inspections-field-evidence | ClaimEdge-native | Low | P0 | Rename from "claims" to "inspections" pillar |
| 15 | chicago-xactimate-pricing | `claimedge__estimate-supplement__xactimate-pricing__chicago` | estimate-supplement-support | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 16 | municipal-code-compliance-toolkit | `claimedge__code-compliance__municipal-toolkit__lookup` | code-compliance | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 17 | illinois-legal-resource-directory | `claimedge__jurisdiction-research__legal-directory__il` | jurisdiction-research-library | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 18 | wind-hail-property-claims | `claimedge__exterior-damage__claims-master__roofing-siding` | exterior-damage-assessment | ClaimEdge-native | Low | P0 | Already branded; align naming |
| 19 | premier-claims-investigation | `claimedge__inspections__commercial-claims__premier` | inspections-field-evidence | ClaimEdge-native | Low | P1 | Rename to fit convention |
| 20 | pi-case-analyzer | `claimedge__claim-intake__pi-case-analyzer__personal-injury` | claim-intake-triage | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 21 | vehicle-collision-case-analyzer | `claimedge__claim-intake__vehicle-collision__auto` | claim-intake-triage | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 22 | credit-repair-master-orchestrator | `claimedge__productization__credit-repair__master-orchestrator` | productization-rd | ClaimEdge-native | Medium | P2 | May be client-facing product; review scope |
| 23 | credit-repair-orchestrator | `claimedge__productization__credit-repair__dispute-coord` | productization-rd | ClaimEdge-native | Medium | P2 | Merge potential with #22 |
| 24 | credit-bureau-dispute-puller | `claimedge__productization__credit-repair__dispute-puller` | productization-rd | ClaimEdge-native | Low | P2 | Tightly coupled with #22, #23 |
| 25 | stripe-setup-wizard | `claimedge__productization__stripe-wizard__payments` | productization-rd | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 26 | social-proof-builder | `claimedge__productization__social-proof__trust-building` | productization-rd | ClaimEdge-native | Low | P1 | Already branded; align naming |
| 27 | content-repurposer | `claimedge__productization__content-repurposer__multi-platform` | productization-rd | ClaimEdge-native | Low | P1 | Already branded; align naming |

### HUUSO LEGACY — MUST MIGRATE (7 Skills)

| # | Current Name | New Name (Proposed) | Pillar | Status | Effort | Priority | Notes |
|---|-------------|---------------------|--------|--------|--------|----------|-------|
| 28 | huuso-brand-presentation-suite | `claimedge__document-assembly__presentation-suite__brand` | document-assembly | Migrated-from-Huuso | High | P1 | Remove Huuso refs; adapt to ClaimEdge brand |
| 29 | huuso-claimedge-master | `claimedge__claim-intake__master-claims__unified` | claim-intake-triage | Migrated-from-Huuso | High | P0 | Merges Huuso + ClaimEdge into single system |
| 30 | huuso-claims-master | `claimedge__exterior-damage__claims-master__roofing-siding` | exterior-damage-assessment | Migrated-from-Huuso | High | P0 | Remove Huuso refs; keep exterior damage content |
| 31 | huuso-estimate-builder | `claimedge__estimate-supplement__estimate-builder__xactimate` | estimate-supplement-support | Migrated-from-Huuso | Medium | P0 | Remove Huuso refs; merge with chicago-xactimate-pricing |
| 32 | huuso-operations-suite | `claimedge__ai-os__operations-suite__catalog` | ai-os-infrastructure | Legacy-archive | Low | P2 | 40-skill catalog is outdated; archive, extract useful items |
| 33 | huuso-review-generator | `claimedge__productization__review-generator__google` | productization-rd | Migrated-from-Huuso | Low | P1 | Remove Huuso refs; adapt for ClaimEdge reviews |
| 34 | huuso-supplement-writer | `claimedge__carrier-comms__supplement-writer__narrative` | carrier-communications | Migrated-from-Huuso | Medium | P0 | Remove Huuso refs; merge with supplement support |

### WRESTLING DOMAIN (16 Skills)

| # | Current Name | New Name (Proposed) | Pillar | Status | Effort | Priority | Notes |
|---|-------------|---------------------|--------|--------|--------|----------|-------|
| 35 | wrestling-intelligence-master | `claimedge__sports-ventures__wrestling-intelligence__master` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 36 | wrestling-opponent-scout | `claimedge__sports-ventures__wrestling-scout__opponent` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 37 | wrestling-bracket-scraper | `claimedge__sports-ventures__bracket-scraper__auto-login` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 38 | wrestling-analytics-coach | `claimedge__sports-ventures__wrestling-analytics__youth` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 39 | wrestling-data-sync | `claimedge__sports-ventures__wrestling-sync__cross-platform` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 40 | wrestling-tournament-intelligence-extractor | `claimedge__sports-ventures__tournament-extractor__intelligence` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 41 | wrestling-thread-auditor | `claimedge__sports-ventures__thread-auditor__wrestling` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 42 | wrestling-master-manifest | `claimedge__sports-ventures__master-manifest__ecosystem` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 43 | wrestler-career-rankings | `claimedge__sports-ventures__career-rankings__analytics` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 44 | tournament-preparation-suite | `claimedge__sports-ventures__tournament-prep__suite` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 45 | nuway-rumble-command-center | `claimedge__sports-ventures__nuway-rumble__cedar-point` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 46 | usa-bracketing-expert | `claimedge__sports-ventures__usa-bracketing__navigation` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 47 | level-up-wrestling-builder | `claimedge__sports-ventures__level-up-app__react-builder` | sports-ventures | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 48 | icdwa-levelup-bridge | `claimedge__sports-ventures__icdwa-bridge__level-up` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 49 | icdwa-technical-build-suite | `claimedge__sports-ventures__icdwa-tech__execution` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 50 | illinois-county-duals-command-center | `claimedge__sports-ventures__il-county-duals__command-center` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |

### BUDDY BOY SPORTS (2 Skills)

| # | Current Name | New Name (Proposed) | Pillar | Status | Effort | Priority | Notes |
|---|-------------|---------------------|--------|--------|--------|----------|-------|
| 51 | buddy-boy-sports-manager | `claimedge__sports-ventures__buddy-boy__team-manager` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 52 | sports-tournament-scout | `claimedge__sports-ventures__tournament-scout__baseball` | sports-ventures | ClaimEdge-native | Low | P2 | Add claimedge prefix |

### PERSONAL AI OPS (16 Skills)

| # | Current Name | New Name (Proposed) | Pillar | Status | Effort | Priority | Notes |
|---|-------------|---------------------|--------|--------|--------|----------|-------|
| 53 | robert-master-os | `claimedge__ai-os__master-os__robert` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Add claimedge prefix |
| 54 | bobby-ai-command-center | `claimedge__ai-os__ai-command-center__auto-detect` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Add claimedge prefix |
| 55 | bobby-autopilot-system | `claimedge__ai-os__autopilot-system__ultimate` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Add claimedge prefix |
| 56 | bobby-focus-system | `claimedge__ai-os__focus-system__adhd` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 57 | bobby-skill-activator | `claimedge__ai-os__skill-activator__multi-ai` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Add claimedge prefix |
| 58 | bobbys-ai-translator | `claimedge__ai-os__ai-translator__tech-terms` | ai-os-infrastructure | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 59 | ai-workflow-decoder | `claimedge__ai-os__workflow-decoder__master` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 60 | kimi-miyagi-coach | `claimedge__ai-os__kimi-coach__feature-max` | ai-os-infrastructure | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 61 | kimi-usage-optimizer | `claimedge__ai-os__kimi-optimizer__usage` | ai-os-infrastructure | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 62 | multi-ai-router | `claimedge__ai-os__multi-ai-router__routing` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 63 | session-boot-loader | `claimedge__ai-os__boot-loader__session-init` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 64 | session-context-preserver | `claimedge__ai-os__context-preserver__cross-session` | ai-os-infrastructure | ClaimEdge-native | Low | P0 | Add claimedge prefix |
| 65 | thread-audit-manager | `claimedge__ai-os__thread-audit__organization` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 66 | thread-handoff-manager | `claimedge__ai-os__thread-handoff__context-preserve` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |
| 67 | perplexity-connector-advisor | `claimedge__ai-os__perplexity-advisor__connectors` | ai-os-infrastructure | ClaimEdge-native | Low | P2 | Add claimedge prefix |
| 68 | skill-lifecycle-manager | `claimedge__ai-os__skill-lifecycle__manager` | ai-os-infrastructure | ClaimEdge-native | Low | P1 | Add claimedge prefix |

### Skill Count by Pillar

| Pillar | Skills | Huuso Migrations | Quick Wins |
|--------|--------|-----------------|------------|
| claim-intake-triage | 5 | 1 (#29) | 4 |
| policy-coverage-review | 1 | 0 | 1 |
| inspections-field-evidence | 4 | 0 | 4 |
| exterior-damage-assessment | 3 | 1 (#30) | 2 |
| code-compliance | 2 | 0 | 2 |
| estimate-supplement-support | 2 | 1 (#31) | 1 |
| carrier-communications | 1 | 1 (#34) | 0 |
| document-assembly | 2 | 1 (#28) | 1 |
| jurisdiction-research-library | 1 | 0 | 1 |
| ai-os-infrastructure | 16 | 1 (#32) | 14 |
| sports-ventures | 18 | 0 | 18 |
| productization-rd | 6 | 1 (#33) | 5 |
| **TOTAL** | **61** | **7** | **53** |

---

## 4. Golden Path Workflow

### The Ideal ClaimEdge Claim Lifecycle

```
INTAKE → POLICY REVIEW → INSPECTION → EVIDENCE → CODE/COMPLIANCE → SCOPE/ESTIMATE → SUPPLEMENT → CARRIER COMMS → SETTLEMENT
```

### Stage-by-Stage Skill Activation

| Stage | Trigger | Skills Activated | Outputs |
|-------|---------|-----------------|---------|
| **1. INTAKE** | New claim call/email/form | `claimedge__claim-intake__command-center__multi-agent`<br>`claimedge__claim-intake__master-claims__unified` | Triage report, claim file opened, routing decision |
| **2. POLICY REVIEW** | Claim file assigned | `claimedge__policy-coverage__complete-system__15-course` | Coverage memo, exclusions identified, limits documented |
| **3. INSPECTION** | Site visit scheduled | `claimedge__inspections__claims-investigation__12-agent`<br>`claimedge__inspections__weather-researcher__noaa-nws` | Photo log, inspection report, weather data for date of loss |
| **4. EVIDENCE** | Photos/notes collected | `claimedge__inspections__evidence-orchestrator__12-agent`<br>`claimedge__exterior-damage__claims-master__roofing-siding` | Evidence packet, damage classification, causation analysis |
| **5. CODE/COMPLIANCE** | Damage scope drafted | `claimedge__code-compliance__municipal-toolkit__lookup`<br>`claimedge__code-compliance__material-hazards__identification` | Code citations, compliance report, hazard identification |
| **6. SCOPE/ESTIMATE** | Code report complete | `claimedge__estimate-supplement__estimate-builder__xactimate` | Xactimate estimate, line items, pricing |
| **7. SUPPLEMENT** | Initial estimate low | `claimedge__carrier-comms__supplement-writer__narrative` | Supplement narrative, dispute letter, revised scope |
| **8. CARRIER COMMS** | All docs ready | `claimedge__carrier-comms__supplement-writer__narrative`<br>`claimedge__jurisdiction-research__legal-directory__il` | LOR, demand letter, legal precedent (if disputed) |
| **9. SETTLEMENT** | Agreement reached | `claimedge__document-assembly__auto-deploy__notion-neon-github`<br>`claimedge__document-assembly__vault-system__archive` | Final packet archived, Notion updated, settlement logged |

### Parallel Skills (Run Anytime)

| Skill | When Activated | Purpose |
|-------|---------------|---------|
| `claimedge__exterior-damage__roof-valley__wood-cedar-metal` | When roof claim involves wood/cedar + metal valleys | Specialized roof damage assessment |
| `claimedge__inspections__commercial-claims__premier` | When commercial property claim | Premier Claims commercial workflow |
| `claimedge__claim-intake__pi-case-analyzer__personal-injury` | When injury component exists | PI case valuation |
| `claimedge__claim-intake__vehicle-collision__auto` | When auto claim component | Vehicle collision analysis |
| `claimedge__ai-os__master-coach__personal` | Daily | AI coaching and guidance |
| `claimedge__ai-os__session-memory__persistent` | Every session | Cross-session context |

---

## 5. Notion 8-Database Schema

This schema is the Notion source of truth for the ClaimEdge-only operating system, with linked databases for skills, migration, governance, and operational workflows. It follows modular registry practices for AI skills and custom agents by keeping context tight, separating roles and records, and making each recurring workflow auditable.

### Build Order

Create the following databases in this order so relations are easier to wire after the core tables exist.

| Order | Database | Purpose |
|-------|----------|---------|
| 1 | Skills Registry | Master source of truth for all ClaimEdge skills |
| 2 | Roles | Human and AI role ownership |
| 3 | Tasks | Action queue and implementation tracking |
| 4 | Migration Tracker | Conversion log from legacy artifacts to ClaimEdge |
| 5 | References | Code, policy, carrier, legal, and manufacturer sources |
| 6 | Skill QA | Testing, approval, and review history |
| 7 | Risk Matrix | Output control and review-gate policy |
| 8 | Memory / Lessons Learned | Reusable outcomes and precedent patterns |

---

### 5.1. Skills Registry

#### Purpose
Tracks every skill, version, risk level, owner, connector dependency, and GitHub path in one place.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Skill ID | Title | Immutable ID matching GitHub folder |
| Skill Name | Text | Human-readable label |
| Domain | Select | ClaimEdge pillar |
| Subdomain | Select | Narrower function |
| Migration Status | Select | ClaimEdge-native / Migrated-from-Huuso / Needs-conversion / Legacy-archive / Duplicate-review / Deprecated |
| Lifecycle Status | Select | Draft / Testing / Approved / Restricted / Deprecated / Archived |
| Version | Text | Example: 1.0.0 |
| Owner | Text/Person | Responsible human |
| AI Role | Relation → Roles | Primary operating role |
| Trigger | Text | When the skill should run |
| Allowed Sources | Multi-select | Web, Notion, GitHub, Files, Email, Calendar |
| Connectors Used | Multi-select | Notion, GitHub, Gmail, Calendar, Slack, Drive |
| Input Schema | Text | Required structured inputs |
| Output Schema | Text | Required output format |
| Risk Level | Select | Low / Medium / High |
| Review Gate | Select | None / Internal / Human Signoff |
| GitHub Path | URL/Text | Relative repo location |
| Related References | Relation → References | Source library ties |
| QA Records | Relation → Skill QA | Test history |
| Last Reviewed | Date | Governance freshness |
| Notes | Text | Additional operating notes |

#### Suggested Database Views

| View | Filter |
|------|--------|
| Approved Skills | Lifecycle Status = Approved |
| Draft Queue | Lifecycle Status = Draft |
| High Risk Skills | Risk Level = High |
| Needs Conversion | Migration Status = Needs-conversion |
| Sync Review | GitHub Path is empty OR Version is empty |

---

### 5.2. Roles

#### Purpose
Defines which human or AI roles own which kinds of tasks and skills.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Role Name | Title | Example: Claim Intake Analyst |
| Role Type | Select | Human / AI / Hybrid |
| Domain | Select | Functional area |
| Responsibilities | Text | Core duties |
| Owned Skills | Relation → Skills Registry | Skills tied to role |
| Assigned Tasks | Relation → Tasks | Current action queue |
| Review Authority | Select | None / Internal / Final signoff |
| Notes | Text | Constraints and boundaries |

---

### 5.3. Tasks

#### Purpose
Operational work queue for implementation, reviews, migrations, and testing.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Task Name | Title | Action item |
| Domain | Select | ClaimEdge pillar |
| Task Type | Select | Build / Review / Test / Migration / Security / Research |
| Priority | Select | P0 / P1 / P2 / P3 |
| Status | Select | Backlog / Ready / In Progress / Blocked / Review / Done |
| Assigned Role | Relation → Roles | Responsible role |
| Related Skill | Relation → Skills Registry | Optional skill linkage |
| Due Date | Date | Delivery target |
| Risk Level | Select | Low / Medium / High |
| Notes | Text | Execution notes |

---

### 5.4. Migration Tracker

#### Purpose
Captures every rename, archive, conversion, or duplication discovered during the ClaimEdge-only migration.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Artifact Name | Title | Current or legacy item |
| Artifact Type | Select | Skill / Page / Folder / Prompt / Template / Database / Repo File |
| Old Name | Text | Legacy Huuso or other label |
| New Name | Text | New ClaimEdge label |
| Old Location | Text | Where it lived |
| New Location | Text | Where it should live |
| Migration Status | Select | ClaimEdge-native / Migrated-from-Huuso / Needs-conversion / Legacy-archive / Duplicate-review / Deprecated |
| Owner | Text/Person | Responsible for change |
| Action Needed | Text | Rename / Archive / Merge / Rebuild |
| Completed Date | Date | Completion log |
| Notes | Text | Extra details |

---

### 5.5. References

#### Purpose
Structured library for code, policy, manufacturer, and carrier-support materials.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Reference Title | Title | Source name |
| Source Type | Select | Code / Policy / Manufacturer / Carrier / Legal / Internal |
| Jurisdiction | Text | City / state / national scope |
| URL | URL | Source link |
| Citation Note | Text | Exact wording or summary |
| Related Skills | Relation → Skills Registry | Connected skills |
| Status | Select | Active / Needs Review / Archived |
| Notes | Text | Context |

---

### 5.6. Skill QA

#### Purpose
Logs testing, review, defects, and approvals for each skill.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| QA Record | Title | Example: claim-triage v1 smoke test |
| Skill | Relation → Skills Registry | Skill under review |
| Test Type | Select | Smoke / Functional / Prompt QA / Security / Review Gate |
| Result | Select | Pass / Fail / Needs Revision |
| Reviewer | Text/Person | Who reviewed |
| Test Date | Date | When it happened |
| Findings | Text | Key issues |
| Follow-up Task | Relation → Tasks | Fix task |

---

### 5.7. Risk Matrix

#### Purpose
Controls what can auto-run, what needs internal review, and what requires mandatory signoff before external use.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Risk Record | Title | Example: supplement-rebuttal control |
| Skill | Relation → Skills Registry | Controlled skill |
| Risk Level | Select | Low / Medium / High |
| External Use | Checkbox | Can leave the system |
| Review Required | Select | None / Internal / Human Signoff |
| Allowed Audience | Multi-select | Internal / Client / Carrier / Municipality |
| Failure Impact | Text | What goes wrong if output is wrong |
| Notes | Text | Constraints |

---

### 5.8. Memory / Lessons Learned

#### Purpose
Preserves winning arguments, recurring failures, accepted citations, and process lessons for future reuse.

#### Properties

| Property | Type | Notes |
|----------|------|-------|
| Lesson Title | Title | Short name |
| Scenario Type | Select | Intake / Inspection / Code / Estimate / Carrier / Ops |
| Carrier | Text | If applicable |
| Jurisdiction | Text | If applicable |
| Outcome | Select | Success / Failure / Mixed |
| Key Lesson | Text | Main learning |
| Related Skill | Relation → Skills Registry | Connected skill |
| Reuse Level | Select | High / Medium / Low |
| Notes | Text | Supporting context |

---

### Starter Records for Skills Registry

Use these as the first five records so Notion and GitHub can stay aligned from day one.

| Skill ID | Skill Name | Domain | Subdomain | Lifecycle Status | Migration Status | Risk Level | Review Gate |
|----------|------------|--------|-----------|-----------------|------------------|------------|-------------|
| claimedge__intake__claim-triage__v1 | Claim Triage | Claim Intake & Triage | Intake | Draft | ClaimEdge-native | Medium | Internal |
| claimedge__intake__document-request__v1 | Document Request Builder | Claim Intake & Triage | Intake | Draft | ClaimEdge-native | Low | None |
| claimedge__coverage__policy-summary__v1 | Policy Summary | Policy & Coverage Review | Coverage | Draft | ClaimEdge-native | High | Human Signoff |
| claimedge__inspection__site-visit-checklist__v1 | Site Visit Checklist | Inspections & Field Evidence | Inspection | Draft | ClaimEdge-native | Medium | Internal |
| claimedge__code__jurisdiction-lookup__v1 | Jurisdiction Lookup | Code & Compliance | Jurisdiction Research | Draft | ClaimEdge-native | Medium | Internal |

### Build Notes

Keep the top-level Notion instruction page short and use linked databases instead of giant prompt pages, because Notion guidance emphasizes tighter context and clearer definitions of what agents should do. The Skills Registry and Migration Tracker should be the first two databases actively used during the ClaimEdge-only conversion.

---

## 6. Notion Setup Guide

### Prerequisites
- Notion account (robert@claimedge.com)
- A dedicated ClaimEdge workspace or top-level page
- 30-45 minutes of uninterrupted time

### Overview
You will create 8 linked databases in a specific order. Each database after the first uses Relations that point to earlier databases, so the order matters.

### Step 1: Create the ClaimEdge Hub Page

1. In Notion, create a new page titled **"ClaimEdge AI Operating System"**
2. Add a simple description: *Source of truth for ClaimEdge skills, migration tracking, governance, and operational workflows.*
3. This page will contain all 8 databases as linked views
4. Bookmark this page — it is your mission control

### Step 2: Create Database 1 — Skills Registry

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Skills Registry"**
3. Set the title property to **"Skill ID"**
4. Add each property from Section 5.1 in this exact order:
   - Click **"+ New property"** for each field
   - Use the Type column from the schema table to select the correct property type
   - For **Select** and **Multi-select** properties, add the options from the Notes column
5. Create the 5 suggested views:
   - Click **"+ New view"** for each view
   - Set the filter according to the Suggested Database Views table
6. Add the 5 starter records from the Starter Records table in Section 5.1
   - Click **"New"** and fill in each field

### Step 3: Create Database 2 — Roles

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Roles"**
3. Set the title property to **"Role Name"**
4. Add all properties from Section 5.2
5. For the **Owned Skills** property:
   - Set type to **Relation**
   - Select **Skills Registry** as the target database
   - Enable **"Show on Skills Registry"** to create a two-way link
6. For the **Assigned Tasks** property:
   - Set type to **Relation**
   - You will point this to the Tasks database after creating it (come back to this)

### Step 4: Create Database 3 — Tasks

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Tasks"**
3. Set the title property to **"Task Name"**
4. Add all properties from Section 5.3
5. For **Assigned Role**, create a Relation pointing to the **Roles** database
6. For **Related Skill**, create a Relation pointing to the **Skills Registry** database
7. Go back to the Roles database and complete the **Assigned Tasks** relation pointing to Tasks

### Step 5: Create Database 4 — Migration Tracker

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Migration Tracker"**
3. Set the title property to **"Artifact Name"**
4. Add all properties from Section 5.4
5. This database operates independently — no relations needed yet
6. Optional: Import the 67 skills from Section 3 as starter records

### Step 6: Create Database 5 — References

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"References"**
3. Set the title property to **"Reference Title"**
4. Add all properties from Section 5.5
5. For **Related Skills**, create a Relation pointing to **Skills Registry**

### Step 7: Create Database 6 — Skill QA

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Skill QA"**
3. Set the title property to **"QA Record"**
4. Add all properties from Section 5.6
5. For **Skill**, create a Relation pointing to **Skills Registry**
6. For **Follow-up Task**, create a Relation pointing to **Tasks**

### Step 8: Create Database 7 — Risk Matrix

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Risk Matrix"**
3. Set the title property to **"Risk Record"**
4. Add all properties from Section 5.7
5. For **Skill**, create a Relation pointing to **Skills Registry**

### Step 9: Create Database 8 — Memory / Lessons Learned

1. On the ClaimEdge hub page, type `/database` and select **"Database - Full page"**
2. Name it **"Memory / Lessons Learned"**
3. Set the title property to **"Lesson Title"**
4. Add all properties from Section 5.8
5. For **Related Skill**, create a Relation pointing to **Skills Registry**

### Step 10: Verify Relations

Go to the **Skills Registry** database and confirm these Relation columns are visible (they appear automatically from the two-way links you created):
- Owned Skills (from Roles)
- Assigned Tasks (from Roles, via Tasks)
- Related References (from References)
- QA Records (from Skill QA)
- Related Lessons (from Memory / Lessons Learned)

### Step 11: Add 5 Starter Records to Skills Registry

Enter the 5 starter records from Section 5.1. These align with the 5 GitHub starter skills in Section 7.

| Done? | Step |
|-------|------|
| [ ] | Hub page created |
| [ ] | Database 1: Skills Registry |
| [ ] | Database 2: Roles |
| [ ] | Database 3: Tasks |
| [ ] | Database 4: Migration Tracker |
| [ ] | Database 5: References |
| [ ] | Database 6: Skill QA |
| [ ] | Database 7: Risk Matrix |
| [ ] | Database 8: Memory / Lessons Learned |
| [ ] | All relations verified |
| [ ] | 5 starter records added |

---

## 7. GitHub Starter Pack

This starter pack establishes the first five ClaimEdge core skills as GitHub-ready folders using a standard `SKILL.md` pattern, which aligns with documented agent-skill structures where each skill lives in its own directory with a `SKILL.md` file at the root.

### Repository Structure

```text
claimedge-ai-os/
└── skills/
    └── claimedge/
        ├── intake/
        │   ├── claimedge__intake__claim-triage__v1/
        │   │   └── SKILL.md
        │   └── claimedge__intake__document-request__v1/
        │       └── SKILL.md
        ├── coverage/
        │   └── claimedge__coverage__policy-summary__v1/
        │       └── SKILL.md
        ├── inspection/
        │   └── claimedge__inspection__site-visit-checklist__v1/
        │       └── SKILL.md
        └── code/
            └── claimedge__code__jurisdiction-lookup__v1/
                └── SKILL.md
```

### Starter Skills Included

| Skill ID | Purpose | Risk |
|----------|---------|------|
| `claimedge__intake__claim-triage__v1` | Standardize first-pass claim intake and routing | Medium |
| `claimedge__intake__document-request__v1` | Generate missing-document request lists | Low |
| `claimedge__coverage__policy-summary__v1` | Summarize core policy sections and flags | High |
| `claimedge__inspection__site-visit-checklist__v1` | Generate site-visit checklists for inspections | Medium |
| `claimedge__code__jurisdiction-lookup__v1` | Identify relevant jurisdiction/code lookup tasks | Medium |

### SKILL.md Template

Each `SKILL.md` file follows this standard structure:

```markdown
# Skill: <Skill ID>

## Metadata
- **Skill ID:** <claimedge__pillar__function__variant>
- **Domain:** <ClaimEdge pillar>
- **Subdomain:** <Narrower function>
- **Version:** 1.0.0
- **Risk Level:** Low | Medium | High
- **Review Gate:** None | Internal | Human Signoff
- **Owner:** Robert Krapil <robert@claimedge.com>

## Purpose
<Brief description of what this skill does and when to activate it.>

## Trigger
<When should this skill be activated?>

## Input Schema
<Required structured inputs.>

## Output Schema
<Required output format.>

## Workflow
<Step-by-step execution flow.>

## Allowed Sources
<Web, Notion, GitHub, Files, Email, Calendar>

## Connectors Used
<Notion, GitHub, Gmail, Calendar, Slack, Drive>

## Notes
<Additional operating notes.>
```

### Implementation Notes

- These skills should remain in Draft until tested and linked to matching Notion records with QA and review controls
- GitHub secret scanning should be enabled on the repository because GitHub scans repositories and history for hardcoded credentials and other secrets
- Each skill folder is self-contained — all assets, prompts, and tests for that skill live in its folder
- Future skills follow the same pattern: create folder, add `SKILL.md`, link to Notion Skills Registry

---

## 8. GitHub Setup Guide

### Prerequisites
- GitHub account (robert@claimedge.com)
- Git installed locally (or use GitHub web interface)
- 15-20 minutes

### Step 1: Create the Repository

1. Go to github.com and sign in as robert@claimedge.com
2. Click **New Repository**
3. Name it **"claimedge-ai-os"**
4. Set to **Private**
5. Add description: *ClaimEdge AI skill registry, governance, and operational source of truth*
6. Initialize with a **README**
7. Click **Create repository**

### Step 2: Enable Secret Scanning

1. In the new repo, go to **Settings → Security → Code security and analysis**
2. Enable **Secret scanning** and **Push protection**
3. This prevents accidental commits of API keys, tokens, or credentials

### Step 3: Create the Directory Structure

Option A: Via GitHub web interface:
1. Click **"Add file" → "Create new file"**
2. Enter path: `skills/claimedge/intake/.gitkeep`
3. Click **Commit new file**
4. Repeat for each directory in the structure

Option B: Via command line:
```bash
git clone https://github.com/claimedge/claimedge-ai-os.git
cd claimedge-ai-os
mkdir -p skills/claimedge/intake
mkdir -p skills/claimedge/coverage
mkdir -p skills/claimedge/inspection
mkdir -p skills/claimedge/code
git add .
git commit -m "Initial directory structure for ClaimEdge skills"
git push origin main
```

### Step 4: Create the First SKILL.md

1. Navigate to `skills/claimedge/intake/`
2. Create a new folder named: `claimedge__intake__claim-triage__v1`
3. Inside that folder, create a file named `SKILL.md`
4. Paste the SKILL.md Template from Section 7, filling in:
   - Skill ID: `claimedge__intake__claim-triage__v1`
   - Domain: Claim Intake & Triage
   - Subdomain: Intake
   - Risk Level: Medium
   - Review Gate: Internal
5. Commit the file

### Step 5: Create the Remaining 4 SKILL.md Files

Repeat Step 4 for each remaining starter skill:

| Folder Path | Skill ID | Risk Level | Review Gate |
|-------------|----------|------------|-------------|
| `skills/claimedge/intake/claimedge__intake__document-request__v1/` | claimedge__intake__document-request__v1 | Low | None |
| `skills/claimedge/coverage/claimedge__coverage__policy-summary__v1/` | claimedge__coverage__policy-summary__v1 | High | Human Signoff |
| `skills/claimedge/inspection/claimedge__inspection__site-visit-checklist__v1/` | claimedge__inspection__site-visit-checklist__v1 | Medium | Internal |
| `skills/claimedge/code/claimedge__code__jurisdiction-lookup__v1/` | claimedge__code__jurisdiction-lookup__v1 | Medium | Internal |

### Step 6: Link GitHub to Notion

1. Open your Notion Skills Registry database
2. For each of the 5 starter records, fill in the **GitHub Path** field:
   - `skills/claimedge/intake/claimedge__intake__claim-triage__v1/`
   - `skills/claimedge/intake/claimedge__intake__document-request__v1/`
   - `skills/claimedge/coverage/claimedge__coverage__policy-summary__v1/`
   - `skills/claimedge/inspection/claimedge__inspection__site-visit-checklist__v1/`
   - `skills/claimedge/code/claimedge__code__jurisdiction-lookup__v1/`
3. Now your Notion Skills Registry and GitHub repo are linked

### Step 7: Verify the Setup

| Done? | Check |
|-------|-------|
| [ ] | Repository created as private |
| [ ] | Secret scanning enabled |
| [ ] | All 4 pillar folders exist (intake, coverage, inspection, code) |
| [ ] | All 5 skill folders created with SKILL.md |
| [ ] | SKILL.md files use correct naming convention |
| [ ] | Notion Skills Registry has GitHub paths filled in |
| [ ] | README.md describes the repo purpose |

---

## 9. Migration Tracker Template

### Copy this table and update as you progress:

```markdown
| # | Current Name | New Name | Status | Assigned | Started | Completed | Notes |
|---|-------------|----------|--------|----------|---------|-----------|-------|
| 1 | claim-command-center | claimedge__claim-intake__command-center__multi-agent | NOT_STARTED | | | | |
| 2 | claimed-master-workflow | claimedge__claim-intake__master-claims__unified | NOT_STARTED | | | | Merge with huuso-claimedge-master |
| 3 | claimedge-auto-deploy | claimedge__document-assembly__auto-deploy__notion-neon-github | NOT_STARTED | | | | |
| 4 | claimedge-complete-system | claimedge__policy-coverage__complete-system__15-course | NOT_STARTED | | | | |
| 5 | claimedge-full-claims-investigation | claimedge__inspections__claims-investigation__12-agent | NOT_STARTED | | | | |
| 6 | claimedge-master-coach | claimedge__ai-os__master-coach__personal | NOT_STARTED | | | | |
| 7 | claimedge-material-hazards | claimedge__code-compliance__material-hazards__identification | NOT_STARTED | | | | |
| 8 | claimedge-roof-valley-claims | claimedge__exterior-damage__roof-valley__wood-cedar-metal | NOT_STARTED | | | | |
| 9 | claimedge-session-memory | claimedge__ai-os__session-memory__persistent | NOT_STARTED | | | | |
| 10 | claimedge-skill-forge | claimedge__ai-os__skill-forge__arsenal-mgmt | NOT_STARTED | | | | |
| 11 | claimedge-training-builder | claimedge__productization__training-builder__auto-generate | NOT_STARTED | | | | |
| 12 | claimedge-vault-system | claimedge__document-assembly__vault-system__archive | NOT_STARTED | | | | |
| 13 | claimedge-weather-researcher | claimedge__inspections__weather-researcher__noaa-nws | NOT_STARTED | | | | |
| 14 | claims-evidence-orchestrator | claimedge__inspections__evidence-orchestrator__12-agent | NOT_STARTED | | | | |
| 15 | chicago-xactimate-pricing | claimedge__estimate-supplement__xactimate-pricing__chicago | NOT_STARTED | | | | Merge into estimate-builder |
| 16 | municipal-code-compliance-toolkit | claimedge__code-compliance__municipal-toolkit__lookup | NOT_STARTED | | | | |
| 17 | illinois-legal-resource-directory | claimedge__jurisdiction-research__legal-directory__il | NOT_STARTED | | | | |
| 18 | wind-hail-property-claims | claimedge__exterior-damage__claims-master__roofing-siding | NOT_STARTED | | | | Merge with huuso-claims-master |
| 19 | premier-claims-investigation | claimedge__inspections__commercial-claims__premier | NOT_STARTED | | | | |
| 20 | pi-case-analyzer | claimedge__claim-intake__pi-case-analyzer__personal-injury | NOT_STARTED | | | | |
| 21 | vehicle-collision-case-analyzer | claimedge__claim-intake__vehicle-collision__auto | NOT_STARTED | | | | |
| 22 | credit-repair-master-orchestrator | claimedge__productization__credit-repair__unified | NOT_STARTED | | | | Merge group |
| 23 | credit-repair-orchestrator | claimedge__productization__credit-repair__unified | NOT_STARTED | | | | Merge group |
| 24 | credit-bureau-dispute-puller | claimedge__productization__credit-repair__unified | NOT_STARTED | | | | Merge group |
| 25 | stripe-setup-wizard | claimedge__productization__stripe-wizard__payments | NOT_STARTED | | | | |
| 26 | social-proof-builder | claimedge__productization__social-proof__trust-building | NOT_STARTED | | | | |
| 27 | content-repurposer | claimedge__productization__content-repurposer__multi-platform | NOT_STARTED | | | | |
| 28 | huuso-brand-presentation-suite | claimedge__document-assembly__presentation-suite__brand | NOT_STARTED | | | | HIGH EFFORT |
| 29 | huuso-claimedge-master | claimedge__claim-intake__master-claims__unified | NOT_STARTED | | | | HIGH EFFORT |
| 30 | huuso-claims-master | claimedge__exterior-damage__claims-master__roofing-siding | NOT_STARTED | | | | HIGH EFFORT |
| 31 | huuso-estimate-builder | claimedge__estimate-supplement__estimate-builder__xactimate | NOT_STARTED | | | | MEDIUM EFFORT |
| 32 | huuso-operations-suite | claimedge__ai-os__operations-suite__catalog | NOT_STARTED | | | | ARCHIVE ONLY |
| 33 | huuso-review-generator | claimedge__productization__review-generator__google | NOT_STARTED | | | | LOW EFFORT |
| 34 | huuso-supplement-writer | claimedge__carrier-comms__supplement-writer__narrative | NOT_STARTED | | | | MEDIUM EFFORT |
| 35-50 | [wrestling skills] | claimedge__sports-ventures__* | NOT_STARTED | | | | Batch rename |
| 51-52 | [buddy boy skills] | claimedge__sports-ventures__* | NOT_STARTED | | | | Batch rename |
| 53-68 | [personal AI ops] | claimedge__ai-os__* | NOT_STARTED | | | | Batch rename |
```

### Status Options
- `NOT_STARTED` — No work done
- `IN_PROGRESS` — Currently being migrated
- `REVIEW` — Migration done, needs review
- `COMPLETE` — Fully migrated and tested
- `ARCHIVED` — Moved to legacy archive
- `MERGED` — Merged into another skill, original deleted

---

## 10. Quick Wins by Tier

These skills need **zero or minimal changes** — just add the `claimedge__` prefix and align to naming convention.

### Tier 1: Rename Only (Zero Content Changes)

| # | Current Name | New Name | Pillar | Time |
|---|-------------|----------|--------|------|
| 9 | claimedge-session-memory | `claimedge__ai-os__session-memory__persistent` | ai-os | 5 min |
| 10 | claimedge-skill-forge | `claimedge__ai-os__skill-forge__arsenal-mgmt` | ai-os | 5 min |
| 3 | claimedge-auto-deploy | `claimedge__document-assembly__auto-deploy__notion-neon-github` | doc-assembly | 5 min |
| 12 | claimedge-vault-system | `claimedge__document-assembly__vault-system__archive` | doc-assembly | 5 min |
| 7 | claimedge-material-hazards | `claimedge__code-compliance__material-hazards__identification` | code-compliance | 5 min |
| 8 | claimedge-roof-valley-claims | `claimedge__exterior-damage__roof-valley__wood-cedar-metal` | exterior-damage | 5 min |
| 13 | claimedge-weather-researcher | `claimedge__inspections__weather-researcher__noaa-nws` | inspections | 5 min |
| 25 | stripe-setup-wizard | `claimedge__productization__stripe-wizard__payments` | productization | 5 min |

### Tier 2: Minor Alignment (Low Effort)

| # | Current Name | New Name | Pillar | Time |
|---|-------------|----------|--------|------|
| 1 | claim-command-center | `claimedge__claim-intake__command-center__multi-agent` | claim-intake | 10 min |
| 16 | municipal-code-compliance-toolkit | `claimedge__code-compliance__municipal-toolkit__lookup` | code-compliance | 10 min |
| 17 | illinois-legal-resource-directory | `claimedge__jurisdiction-research__legal-directory__il` | jurisdiction | 10 min |
| 18 | wind-hail-property-claims | `claimedge__exterior-damage__claims-master__roofing-siding` | exterior-damage | 10 min |
| 19 | premier-claims-investigation | `claimedge__inspections__commercial-claims__premier` | inspections | 10 min |
| 20 | pi-case-analyzer | `claimedge__claim-intake__pi-case-analyzer__personal-injury` | claim-intake | 10 min |
| 21 | vehicle-collision-case-analyzer | `claimedge__claim-intake__vehicle-collision__auto` | claim-intake | 10 min |
| 26 | social-proof-builder | `claimedge__productization__social-proof__trust-building` | productization | 10 min |
| 27 | content-repurposer | `claimedge__productization__content-repurposer__multi-platform` | productization | 10 min |

### Tier 3: Batch Sports Rename (18 Skills, 30 Minutes Total)

All wrestling and Buddy Boy skills just need `claimedge__sports-ventures__` prefix added. Do them all at once.

**Total quick wins: ~30 skills in under 2 hours**

---

## 11. 3-Week Execution Timeline

### Week 1: Foundation + Quick Wins

| Day | Morning (2h) | Afternoon (2h) |
|-----|-------------|----------------|
| Mon | Set up Notion hub page + Databases 1-4 (Skills Registry, Roles, Tasks, Migration Tracker) | Set up Notion Databases 5-8 (References, Skill QA, Risk Matrix, Memory) + add 5 starter records |
| Tue | Set up GitHub repo `claimedge-ai-os` + directory structure + enable secret scanning | Create 5 SKILL.md starter files + link to Notion |
| Wed | Tier 1 renames (8 skills) — 1 hour | Test golden path with renamed skills |
| Thu | Tier 2 renames (9 skills) — 2 hours | Verify all Tier 1+2 skills still activate correctly |
| Fri | Batch sports rename (18 skills) — 30 min | Personal AI ops rename (15 skills) — 1 hour |

### Week 2: High-Effort Migrations

| Day | Morning (2h) | Afternoon (2h) |
|-----|-------------|----------------|
| Mon | #29 huuso-claimedge-master merge | Test merged master workflow |
| Tue | #30 huuso-claims-master merge | Test exterior damage unified skill |
| Wed | #31 huuso-estimate-builder merge | Test supplement generation with sample claim |
| Thu | #34 huuso-supplement-writer rebrand | Test carrier letter output |
| Fri | #28 huuso-brand-presentation-suite rebrand | Test presentation generation |

### Week 3: Cleanup + Governance

| Day | Morning (2h) | Afternoon (2h) |
|-----|-------------|----------------|
| Mon | #32 huuso-operations-suite archive + extract | Document extracted patterns |
| Tue | #33 huuso-review-generator rebrand | Test review request generation |
| Wed | Credit repair trio decision + merge | Update Migration Tracker in Notion |
| Thu | Final testing of all migrated skills | Populate Risk Matrix for all High-risk skills |
| Fri | Update session memory with new skill names | Celebrate — migration complete |

### Daily Standup Checklist

Each day during the migration, update the Notion Migration Tracker with:
1. Which skills were touched today
2. Any blockers encountered
3. Any new merge decisions made
4. QA results (pass/fail) for tested skills

---

## 12. Post-Migration Checklist

### Infrastructure
- [ ] All active skills use `claimedge__` prefix
- [ ] Zero Huuso references in active skill content
- [ ] Session memory updated with new skill names
- [ ] Skill forge catalog reflects new naming
- [ ] Vault system archived old Huuso versions
- [ ] Notion 8-database schema fully operational
- [ ] GitHub repo has all 5 starter skills with SKILL.md
- [ ] Notion Skills Registry linked to GitHub paths

### Verification
- [ ] Test golden path workflow end-to-end with sample claim
- [ ] Verify all merged skills work correctly
- [ ] Confirm archived skills are excluded from activation
- [ ] Check that sports skills activate under sports-ventures pillar
- [ ] Validate AI ops skills still route correctly
- [ ] Confirm Notion relations work between all 8 databases
- [ ] Verify GitHub secret scanning is active

### Documentation
- [ ] This migration pack is complete and reviewed
- [ ] Migration tracker is filled out
- [ ] Robert has confirmed all high-effort migrations
- [ ] Any new skills created post-migration follow naming convention
- [ ] Notion starter records expanded beyond the initial 5
- [ ] Risk Matrix populated for all High and Medium risk skills

---

## 13. Naming Convention Quick Reference

### Template
```
claimedge__<pillar>__<function>__<variant>
```

### Pillar Abbreviations (for internal use)
| Pillar | Short | Example |
|--------|-------|---------|
| claim-intake-triage | `claim-intake` | `claimedge__claim-intake__command-center__multi-agent` |
| policy-coverage-review | `policy-coverage` | `claimedge__policy-coverage__complete-system__15-course` |
| inspections-field-evidence | `inspections` | `claimedge__inspections__claims-investigation__12-agent` |
| exterior-damage-assessment | `exterior-damage` | `claimedge__exterior-damage__roof-valley__wood-cedar-metal` |
| code-compliance | `code-compliance` | `claimedge__code-compliance__municipal-toolkit__lookup` |
| estimate-supplement-support | `estimate-supplement` | `claimedge__estimate-supplement__estimate-builder__xactimate` |
| carrier-communications | `carrier-comms` | `claimedge__carrier-comms__supplement-writer__narrative` |
| document-assembly | `document-assembly` | `claimedge__document-assembly__auto-deploy__notion-neon-github` |
| jurisdiction-research-library | `jurisdiction-research` | `claimedge__jurisdiction-research__legal-directory__il` |
| ai-os-infrastructure | `ai-os` | `claimedge__ai-os__master-os__robert` |
| sports-ventures | `sports-ventures` | `claimedge__sports-ventures__wrestling-intelligence__master` |
| productization-rd | `productization` | `claimedge__productization__training-builder__auto-generate` |

### Rules
1. Always lowercase
2. Always use double underscores `__` as separators
3. Pillar name must match exactly (use abbreviations above)
4. Function should be 2-4 words, descriptive
5. Variant should indicate sub-type, version, or specialization
6. Max total length: 64 characters
7. No special characters except hyphens within segments

---

*End of ClaimEdge Migration Pack v2. This is a living document — update the Notion Migration Tracker as work progresses. For questions, contact Robert Krapil at robert@claimedge.com.*