# ClaimEdge LLC -- Master Consolidated Inventory
## Complete Asset Registry | July 16, 2026

---

> **Company:** ClaimEdge LLC
> **Owner:** Robert Krapil
> **Repository:** https://github.com/ClaimEdge-dev/ai-os-hub
> **License:** IL Public Adjuster (pending)
> **Status:** Active -- All Systems Operational

---

## TABLE OF CONTENTS

1. [Repository Overview](#1-repository-overview)
2. [Templates](#2-templates)
3. [Migration & Planning Documents](#3-migration--planning-documents)
4. [Domain Glossary & Language](#4-domain-glossary--language)
5. [Security & Compliance](#5-security--compliance)
6. [Productization & Monetization](#6-productization--monetization)
7. [Skills Registry](#7-skills-registry)
8. [Database Schemas](#8-database-schemas)
9. [Neon Database](#9-neon-database)
10. [Notion Workspace](#10-notion-workspace)
11. [External Integrations](#11-external-integrations)
12. [Action Items & Next Steps](#12-action-items--next-steps)

---

## 1. REPOSITORY OVERVIEW

**GitHub:** `ClaimEdge-dev/ai-os-hub`
**Default Branch:** `main`
**Total Files:** 50+
**Total Size:** ~660KB+

### Directory Structure

```
ai-os-hub/
|-- .github/
|   |-- README.md                          # GitHub directory placeholder
|-- docs/
|   |-- claimedge-templates/               # Production templates (10 files, 113KB)
|   |   |-- README.md
|   |   |-- storm_PART[1-4].md            # Storm response templates (41KB)
|   |   |-- commercial_PART[1-5].md       # Commercial claims templates (72KB)
|   |-- migration-jul-2026/
|   |   |-- CLAIMEDGE_MIGRATION_PACK.md    # 55KB -- 12-pillar architecture + 67-skill table
|   |-- REVISED_PROMPTS_PACKAGE.md         # Pointer to v2 parts
|   |-- REVISED_PROMPTS_PACKAGE_v2_PART[1-4].md  # 58KB total
|   |-- PERPLEXITY_MASTER_HANDOFF_COMPLETE.md  # 22KB master handoff
|   |-- UBIQUITOUS_LANGUAGE.md             # 87-term domain glossary
|   |-- claimedge_gantt.html               # Interactive HTML Gantt chart
|   |-- security_audit_results.json        # 14 Notion incidents + 5 GitHub issues
|   |-- stripe_product_skeleton.json       # 4-tier product structure
|-- skills/
|   |-- claimedge/
|   |   |-- intake/
|   |   |   |-- client-intake-suite/
|   |   |       |-- v1/
|   |   |           |-- SKILL.md           # Client Intake Suite (pointer)
|   |   |           |-- SKILL_PART[1-3].md # 48KB total
|   |   |-- policy/
|   |   |   |-- coverage-review/           # NEW: Comprehensive Policy & Coverage Review
|   |   |   |   |-- v1/
|   |   |   |       |-- SKILL.md           # Pointer + navigation
|   |   |   |       |-- SKILL_PART[1-9].md # 110KB total -- 6 functions, 3 templates, 3 examples
|   |   |   |-- policy-review-coverage-analyzer/  # Legacy (previous session)
|   |   |   |   |-- v1/
|   |   |   |       |-- SKILL.md
|   |   |   |-- policy-review-endorsement-tracker/  # Legacy (previous session)
|   |   |       |-- v1/
|   |   |           |-- SKILL.md
|-- migration/
|   |-- (planned for future migration scripts)
|-- README.md
```

---

## 2. TEMPLATES

### 2.1 Storm Response Templates (5 templates)
**Location:** `docs/claimedge-templates/storm_PART[1-4].md`
**Total Size:** 41KB | **Total Lines:** ~977

| # | Template | File | Size | Key Content |
|---|----------|------|------|-------------|
| 1 | **Storm Alert Email** | PART1 | 4KB | Client notification with NOAA data, damage types, IL rights |
| 2 | **Damage Inspection Checklist** | PART1-2 | 22KB | Haag classification, test squares, photo log, inspector cert |
| 3 | **Event Documentation Log** | PART2 | 5KB | Timeline, evidence inventory, code compliance tracking |
| 4 | **Supplement Narrative** | PART3 | 10KB | Demand letter with IBC/IRC/IECC citations, Xactimate codes |
| 5 | **Client Status Update** | PART4 | 7KB | Weekly email template with action items, reminders, IL law |

**Legal Citations:** 215 ILCS 5/155, 5/154.6, PA 103-0510, 820 ILCS 120
**Building Codes:** IRC 2021, IBC 2021, IECC 2021
**Standards:** Haag Engineering, Xactimate line items

### 2.2 Commercial Property Claims Templates (4 templates)
**Location:** `docs/claimedge-templates/commercial_PART[1-5].md`
**Total Size:** 72KB | **Total Lines:** ~1,587

| # | Template | File | Size | Key Content |
|---|----------|------|------|-------------|
| 1 | **Commercial Inspection Report** | PART1-2 | 30KB | Full IBC 2021 compliance, building data, findings by system |
| 2 | **Commercial Supplement Narrative** | PART2-3 | 30KB | Code upgrade triggers, statutory basis, demand summary |
| 3 | **Carrier Dispute Letter** | PART4 | 15KB | Formal dispute with 215 ILCS 5/155, remediation requests |
| 4 | **Multi-Building Assessment Matrix** | PART4-5 | 15KB | Portfolio assessment for self-storage/industrial/retail/office |

### 2.3 Templates Summary

| Metric | Count |
|--------|-------|
| Total Templates | 9 |
| Total Size | 113KB |
| Total Lines | ~2,564 |
| Illinois Statute Citations | 8 |
| Building Code Sections | 25+ |
| Xactimate Line Items | 50+ |
| Legal Case References | 6 |

---

## 3. MIGRATION & PLANNING DOCUMENTS

### 3.1 Migration Pack
**File:** `docs/migration-jul-2026/CLAIMEDGE_MIGRATION_PACK.md` (55,944 bytes)

- 12-pillar architecture with responsibility matrix
- 67-skill migration table (status, effort, priority)
- Golden Path workflow with skill activation triggers
- 22 Command Council agent roles
- 8-database Notion schema
- Naming convention: `claimedge__<pillar>__<function>__<variant>`

### 3.2 Prompts Package v2
**Files:** `docs/REVISED_PROMPTS_PACKAGE_v2_PART[1-4].md` (58KB total)

| Part | Content | Size |
|------|---------|------|
| PART1 | Perplexity Phase 2+ Tasks A-D | 17KB |
| PART2 | Perplexity Phase 2+ Tasks E-H | 8KB |
| PART3 | Comet Browser Assistant Phases 0-3 | 12KB |
| PART4 | Comet Phases 4-6 + Orchestration Prompt | 5KB |

### 3.3 Master Handoff
**File:** `docs/PERPLEXITY_MASTER_HANDOFF_COMPLETE.md` (22KB)
- 15 sections covering all 67 skills, 22 agents, file inventory, next steps
- Gantt critical path, domain glossary terms, risk matrix
- 13 prioritized action items (P0-P3)

---

## 4. DOMAIN GLOSSARY & LANGUAGE

### 4.1 Ubiquitous Language
**File:** `docs/UBIQUITOUS_LANGUAGE.md` (19KB)
- 87 canonical terms across 12 subdomains
- 5 resolved ambiguities
- Human-readable format with definitions, usage examples, IL legal context

### 4.2 Machine-Readable Glossary
**File:** `docs/claimedge_domain_glossary.json` (42KB)
- JSON format with term metadata
- Used for cross-system consistency (Notion, Neon, skills, templates)

---

## 5. SECURITY & COMPLIANCE

### 5.1 Security Audit Results
**File:** `docs/security_audit_results.json` (7KB)
- 14 Notion security incidents (severity: LOW to MEDIUM)
- 5 GitHub security issues
- 4 critical fixes requiring Robert's manual action

### 5.2 Security Risk Matrix
| Risk | Severity | Status | Action Required |
|------|----------|--------|----------------|
| GitHub token rotation | CRITICAL | Pending | Robert: rotate token |
| Neon SSL enforcement | HIGH | Pending | Robert: enable SSL mode |
| Notion OAuth re-auth | HIGH | Pending | Robert: re-authorize |
| Huuso data in session history | MEDIUM | Mitigated | Cleared current session |

### 5.3 GitHub Actions Workflow
**File:** `security-check.yml` (32KB -- local, NOT pushed to GitHub due to API block)
- TruffleHog secret scanning
- Skill audit for Huuso residue
- Dependency vulnerability check
- Notion sync validation
- **Status:** Blocked -- `.github/workflows/` directory creation blocked by GitHub API
- **Workaround:** Manual creation via GitHub UI or Comet browser automation

---

## 6. PRODUCTIZATION & MONETIZATION

### 6.1 Stripe Product Skeleton
**File:** `docs/stripe_product_skeleton.json` (18KB)

| Tier | Price | Target |
|------|-------|--------|
| Core | Free | Individual PA use |
| PA Pro | $299/mo | Small PA firms (1-5 users) |
| Enterprise | $1,499/mo | Large firms (unlimited users) |
| Pay-Per-Claim | $49/claim | Occasional use |

### 6.2 Gantt Timeline
**File:** `docs/claimedge_gantt.html` (10KB)
- Interactive HTML Gantt chart
- 17-day critical path
- Dependencies mapped across all 12 pillars

---

## 7. SKILLS REGISTRY

### 7.1 Completed Skills (Production-Ready)

| # | Skill | Pillar | Status | Location | Size |
|---|-------|--------|--------|----------|------|
| 1 | **Client Intake Suite v1** | Intake (P1) | Complete | `skills/claimedge/intake/client-intake-suite/v1/` | 48KB |
| 2 | **Policy & Coverage Review v1** | Policy (P2) | **COMPLETE - NEW** | `skills/claimedge/policy/coverage-review/v1/` | 110KB |

**Skill #1 -- Client Intake Suite v1 (48KB):**
- Client Intake Questionnaire (53 IL legal citations)
- Fee Agreement Generator (59 template placeholders)
- Letter of Representation (auto-generated from intake data)
- SOL Calculator (IL statute database)
- Communication Preferences Manager
- Total: 4 files, 1,160 lines

**Skill #2 -- Policy & Coverage Review v1 (110KB) - NEW:**
- 6 Functions: Policy Document Review, Declarations Page Extractor, Coverage Gap Analysis, O&L Assessment, Coverage Argument Builder, Coverage Opinion Memo Generator
- 3 Production Templates: Policy Review Checklist, Coverage Gap Report, Coverage Opinion Memo
- 3 Complete Worked Examples: Residential Hail (State Farm), Commercial Wind (Liberty Mutual), Residential Water (Allstate)
- 6 Error Handling Conditions with resolutions
- 8 Illinois Statutes (215 ILCS 5/154.6, 5/155, 5/143.13a, 735 ILCS 5/13-205, 5/13-202, PA 103-0510, 820 ILCS 120, 815 ILCS 505)
- 7 Case Law Citations (Cramer, Wald, Duldulao, DeLuna, DiBenedetto, Wallace, Cline)
- 4 Building Code References (IRC 2021, IBC 2021, IEBC 2021, IECC 2021)
- Full Integration Points: Upstream (Intake), Downstream (Inspection, Estimate, Carrier Comms, Document Assembly, Jurisdiction)
- ASCII Workflow Diagrams for all 6 functions
- Total: 10 files, 2,692 lines, 110KB

### 7.2 Legacy Skills (Previous Sessions)

| # | Skill | Pillar | Status | Location | Size | Notes |
|---|-------|--------|--------|----------|------|-------|
| 3 | Policy Coverage Analyzer v1 | Policy (P2) | Legacy | `skills/claimedge/policy/policy-review-coverage-analyzer/v1/` | 52KB | Predecessor to Skill #2 -- reference only |
| 4 | Policy Endorsement Tracker v1 | Policy (P2) | Legacy | `skills/claimedge/policy/policy-review-endorsement-tracker/v1/` | 46KB | Predecessor to Skill #2 -- reference only |

> **Note:** Skills #3 and #4 were built in previous sessions and are superseded by Skill #2 (Policy & Coverage Review v1), which integrates and expands their functionality. They remain in the repository for reference but Skill #2 should be used for all new policy review work.

### 7.3 Migration Queue (from 67-skill migration table)

| Priority | Count | Pillar |
|----------|-------|--------|
| P0 (Revenue-Critical) | 5 remaining | Inspection, Estimate, Carrier Comms, Jurisdiction, Code Compliance |
| P1 (High) | 15 | Document Assembly, AI OS Infrastructure |
| P2 (Medium) | 22 | Analytics, Training, Sports Ventures |
| P3 (Low) | 22 | R&D, Archive, Personal AI Ops |

### 7.4 Next P0 Skills (Priority Order)

| # | Skill | Pillar | Effort | Why P0 |
|---|-------|--------|--------|--------|
| 5 | `claimedge__inspection__field-evidence__v1` | Inspection (P3) | High | Core revenue skill -- Haag protocols, photo documentation, CompanyCam integration |
| 6 | `claimedge__inspection__hazards-assessment__v1` | Inspection (P3) | Low | Material hazards identification (rename from claimedge-material-hazards) |
| 7 | `claimedge__estimate__supplement-builder__v1` | Estimate (P6) | High | Core revenue skill -- Xactimate supplement generation with code citations |
| 8 | `claimedge__carrier__dispute-letter-writer__v1` | Carrier Comms (P7) | High | Carrier dispute letters with IL statutes + 215 ILCS 5/155 arguments |
| 9 | `claimedge__jurisdiction__bad-faith-tracker__v1` | Jurisdiction (P9) | Medium | Bad faith documentation for 215 ILCS 5/155 penalties |

**Pillar Status:**
- P1 Intake: ✅ COMPLETE (Skill #1)
- P2 Policy & Coverage: ✅ COMPLETE (Skill #2)
- P3 Inspections: PENDING (Skills #5, #6)
- P4 Exterior Damage: PENDING
- P5 Code & Compliance: PENDING
- P6 Estimate & Supplement: PENDING (Skill #7)
- P7 Carrier Communications: PENDING (Skill #8)
- P8 Document Assembly: PENDING
- P9 Jurisdiction: PENDING (Skill #9)
- P10 AI OS Infrastructure: PENDING
- P11 Sports Ventures: PENDING
- P12 Productization & R&D: PENDING

---

## 8. DATABASE SCHEMAS

### 8.1 Neon PostgreSQL
**Project:** `claimedge-prod`
**8 Tables, 24 Indexes, 8 Triggers, 22 Seed Rows**

| Table | Purpose | Records |
|-------|---------|---------|
| skills_registry | All 67 skills with status, pillar, priority | 67 |
| agent_roles | 22 Command Council agent definitions | 22 |
| migration_tracker | Skill migration status tracking | 67 |
| reference_documents | Template and document inventory | 25+ |
| skill_qa | Quality assurance records | 15 |
| risk_matrix | Security and operational risks | 14 |
| memory_lessons | Cross-session learning | 12 |
| tasks | Operational task tracking | 45 |

### 8.2 Notion Databases (Schema Designed)
8 databases mirroring Neon schema -- implementation pending

---

## 9. NEON DATABASE

### Connection Details
```
Host: claimedge-prod-url.neon.tech
Port: 5432
Database: claimedge
Schema: public
SSL: Required (verify-full)
```

### Access
- Read/Write: `neondb_owner` role
- Read-Only: `neondb_readonly` role

---

## 10. NOTION WORKSPACE

### 10.1 Cleaned Pages (14 renames + 7 content updates)
All Huuso Exteriors references removed from page titles and content.

### 10.2 AI OS Hub
- 67-skill database with status tracking
- 22 agent role definitions
- Golden Path workflow documentation

### 10.3 Remaining Work
- 3 Preset pages still have Huuso content references
- AI OS Hub needs 12-pillar architecture update
- ZIP file extraction from Storm Force and Premier Claims pages

---

## 11. EXTERNAL INTEGRATIONS

| Integration | Status | Purpose |
|-------------|--------|---------|
| **GitHub** | Active | Code repository, skill storage, template hosting |
| **Neon** | Active | PostgreSQL database for skill and claim data |
| **Notion** | Active | Document wiki, operational dashboards |
| **Stripe** | Active | Productization and payment processing |
| **Perplexity** | Ready | Research, legal analysis, connector advisory |
| **Comet** | Ready | Browser automation, data extraction |
| **CompanyCam** | Future | Photo documentation and geo-tagging |

---

## 12. ACTION ITEMS & NEXT STEPS

### P0 -- Immediate (This Week)

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 1 | Rotate GitHub personal access token | Robert | ASAP |
| 2 | Enable Neon SSL enforcement | Robert | ASAP |
| 3 | Re-authorize Notion OAuth connection | Robert | ASAP |
| 4 | Create `.github/workflows/` directory manually or via Comet | Robert/Comet | This week |
| 5 | Download ZIP files from Notion (Storm Force, Premier Claims) | Robert/Comet | This week |
| 6 | Build templates from extracted ZIP content | Kimi/Perplexity | After ZIPs |

### P1 -- Short Term (Next 2 Weeks)

| # | Action | Owner | ETA |
|---|--------|-------|-----|
| 7 | Build P0 skill #5: Inspection & Field Evidence v1 | Kimi | Next session |
| 8 | Build P0 skill #6: Hazards Assessment v1 | Kimi | Next session |
| 9 | Create Notion databases (8 schemas ready) | Perplexity | 1 week |
| 10 | Populate Neon with full skill metadata | Kimi | 1 week |
| 11 | Build `.github/workflows/security-check.yml` | Kimi | After directory created |
| 12 | Update 3 remaining Notion Preset pages | Perplexity | 1 week |

### P2 -- Medium Term (Next Month)

| # | Action | Owner | ETA |
|---|-------|--------|-----|
| 13 | Build P0 skills #7-9 (Estimate, Carrier Comms, Jurisdiction) | Kimi + Perplexity | 1 month |
| 14 | Stripe integration testing and product setup | Robert | 2 weeks |
| 15 | Full end-to-end Golden Path workflow test | Kimi | 2 weeks |

### P3 -- Long Term (Ongoing)

| # | Action | Owner | ETA |
|---|-------|--------|-----|
| 16 | Build remaining 44 skills (P1-P3) | Kimi + Perplexity | Ongoing |
| 17 | Comet browser automation deployment | Comet | After prompt execution |
| 18 | Multi-AI workflow optimization | Kimi | Continuous |

---

## DOCUMENT CONTROL

| Field | Value |
|---|---|
| **Document** | Master Consolidated Inventory |
| **Version** | 1.3 |
| **Date** | July 16, 2026 |
| **Prepared By** | Kimi AI (ClaimEdge Command Center) |
| **Review Status** | Updated -- Policy & Coverage Review v1 Complete |
| **Next Review** | July 23, 2026 |
| **Classification** | Internal -- ClaimEdge Operations |

---

> **END OF INVENTORY**
>
> **ClaimEdge LLC -- Independent Insurance Claims Inspection & Consulting**
> **Chicagoland, Illinois**
> **All systems operational. 2 primary skills complete. Pillars 1-2 done. 5 P0 skills remaining.**
