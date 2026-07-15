# ClaimEdge Skill Migration Pack
## Complete Reorganization: 67 Skills → 12-Pillar Architecture

**Owner:** Robert Krapil, ClaimEdge LLC  
**Prepared:** July 2026  
**Status:** Ready for Execution  
**Total Skills:** 67 | **Pillars:** 12 | **Naming Convention:** `claimedge__<pillar>__<function>__<variant>`

---

## 1. Executive Summary

### What We're Doing
Robert Krapil is no longer affiliated with Huuso Exteriors. All Huuso-branded skills (7 core + scattered references) must migrate to ClaimEdge branding. This pack provides the complete roadmap to reorganize all 67 existing skills into a clean, 12-pillar ClaimEdge-only architecture.

### Why
- **Brand separation** from Huuso Exteriors is complete and must be reflected in all AI skills
- **Operational clarity** — current naming is inconsistent and hard to navigate
- **Future-proofing** — new hires, clients, and systems need clean taxonomy
- **Productization** — ClaimEdge is becoming a standalone brand; skills must match

### Expected Outcome
- 67 skills organized into 12 clean pillars
- 0 Huuso references in active skills
- Consistent `claimedge__pillar__function__variant` naming across all skills
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

| # | Pillar | Scope | Description |
|---|--------|-------|-------------|
| 1 | **claim-intake-triage** | New claim intake, triage, routing | First contact with potential clients. Lead qualification, initial loss info gathering, conflict checks, engagement decisions. |
| 2 | **policy-coverage-review** | Policy analysis, coverage verification | Reading and analyzing insurance policies, identifying coverage limits, exclusions, endorsements, and gaps. |
| 3 | **inspections-field-evidence** | Field inspections, photo documentation, evidence | On-site inspections, photo/video documentation, moisture mapping, drone surveys, evidence preservation. |
| 4 | **exterior-damage-assessment** | Roof, siding, gutter damage evaluation | Specific damage assessment for roofing, siding, gutters, windows, doors. Haag Engineering standards. |
| 5 | **code-compliance** | IRC/IBC/IECC codes, municipal compliance | Building code research, municipal amendments, permit requirements, code upgrade arguments. |
| 6 | **estimate-supplement-support** | Xactimate, supplements, scope building | Building estimates, identifying missed line items, supplement preparation, negotiation support. |
| 7 | **carrier-communications** | Letters, negotiations, disputes | All communication with insurance carriers: demand letters, rebuttals, negotiation strategy, appraisal demands. |
| 8 | **document-assembly** | Report generation, packet assembly | Creating comprehensive claim packets: inspection reports, proof of loss, exhibit organization. |
| 9 | **jurisdiction-research-library** | State laws, case law, legal resources | Illinois/Indiana legal research, bad faith statutes, case precedents, regulatory guidance. |
| 10 | **ai-os-infrastructure** | Skills, automation, connectors, vault | The AI operating system itself: skill management, session memory, cross-AI orchestration, vault/archive. |
| 11 | **sports-ventures** | Wrestling, Buddy Boy Sports | Revenue diversification: youth wrestling tracking, baseball team management, tournament intelligence. |
| 12 | **productization-rd** | New products, courses, monetization | Turning ClaimEdge expertise into sellable products: courses, templates, SaaS tools. |

---

## 3. Complete Skill Migration Table

### Legend
- **Status:** N = ClaimEdge-native | M = Migrated-from-Huuso | A = Legacy-archive | C = Needs-conversion
- **Effort:** L = Low (<1hr) | M = Medium (1-3hrs) | H = High (3-6hrs)
- **Priority:** P0 = Do first | P1 = Do soon | P2 = Do later

### Pillar 1: claim-intake-triage
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | *(none)* | `claimedge__intake-triage__client-intake` | NEW | H | P0 | **GAP — no intake skill exists** |
| 2 | *(none)* | `claimedge__intake-triage__fee-agreement-generator` | NEW | M | P0 | **GAP — no fee agreement skill** |
| 3 | *(none)* | `claimedge__intake-triage__conflict-checker` | NEW | M | P0 | **GAP — no conflict check system** |

### Pillar 2: policy-coverage-review
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | *(none)* | `claimedge__policy-review__coverage-analyzer` | NEW | H | P0 | **GAP — no policy analysis skill** |
| 2 | *(none)* | `claimedge__policy-review__endorsement-tracker` | NEW | M | P1 | **GAP — no endorsement tracking** |

### Pillar 3: inspections-field-evidence
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `claimedge-material-hazards` | `claimedge__inspections__hazards-assessment` | N | L | P1 | Rename only |
| 2 | *(none)* | `claimedge__inspections__photo-documentation` | NEW | M | P1 | **GAP — no photo standards skill** |
| 3 | *(none)* | `claimedge__inspections__drone-integration` | NEW | H | P2 | **GAP — no drone documentation** |
| 4 | *(none)* | `claimedge__inspections__moisture-mapping` | NEW | M | P1 | **GAP — no moisture documentation** |

### Pillar 4: exterior-damage-assessment
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `claimedge-roof-valley-claims` | `claimedge__exterior-damage__roof-valley-specialist` | N | L | P1 | Rename only |
| 2 | `wind-hail-property-claims` | `claimedge__exterior-damage__wind-hail-assessor` | N | L | P1 | Rename only |
| 3 | `premier-claims-investigation` | `claimedge__exterior-damage__commercial-investigation` | N | M | P1 | Scope to exterior commercial |

### Pillar 5: code-compliance
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `municipal-code-compliance-toolkit` | `claimedge__code-compliance__municipal-toolkit` | N | L | P0 | Rename only |
| 2 | *(none)* | `claimedge__code-compliance__upgrade-argument-library` | NEW | H | P0 | **GAP — no code upgrade library** |
| 3 | *(none)* | `claimedge__code-compliance__permit-tracker` | NEW | M | P1 | **GAP — no permit tracking** |

### Pillar 6: estimate-supplement-support
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `chicago-xactimate-pricing` | `claimedge__estimate-support__xactimate-pricing-chicago` | N | L | P0 | Rename only |
| 2 | `huuso-estimate-builder` | `claimedge__estimate-support__supplement-builder` | C | H | P0 | Remove Huuso refs, merge with supplement support |
| 3 | *(none)* | `claimedge__estimate-support__supplement-aging-tracker` | NEW | M | P0 | **GAP — tracks supplement status** |
| 4 | *(none)* | `claimedge__estimate-support__line-item-library` | NEW | H | P0 | **GAP — commonly missed items** |
| 5 | *(none)* | `claimedge__estimate-support__depreciation-calculator` | NEW | M | P1 | **GAP — recoverable depreciation** |

### Pillar 7: carrier-communications
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `huuso-supplement-writer` | `claimedge__carrier-comms__supplement-letter-writer` | C | H | P0 | Remove Huuso, expand carrier coverage |
| 2 | `claims-evidence-orchestrator` | `claimedge__carrier-comms__evidence-packet-assembler` | N | M | P0 | Rename + enhance for carrier-facing output |
| 3 | *(none)* | `claimedge__carrier-comms__state-farm-playbook` | NEW | H | P0 | **GAP — carrier-specific tactics** |
| 4 | *(none)* | `claimedge__carrier-comms__allstate-playbook` | NEW | H | P0 | **GAP — carrier-specific tactics** |
| 5 | *(none)* | `claimedge__carrier-comms__liberty-mutual-playbook` | NEW | H | P0 | **GAP — carrier-specific tactics** |
| 6 | *(none)* | `claimedge__carrier-comms__negotiation-tracker` | NEW | M | P1 | **GAP — tracks negotiation stages** |

### Pillar 8: document-assembly
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `claimedge-auto-deploy` | `claimedge__document-assembly__auto-deploy` | N | L | P1 | Rename only |
| 2 | *(none)* | `claimedge__document-assembly__proof-of-loss-generator` | NEW | M | P0 | **GAP — POL preparation** |
| 3 | *(none)* | `claimedge__document-assembly__lor-generator` | NEW | M | P0 | **GAP — Letter of Representation** |
| 4 | *(none)* | `claimedge__document-assembly__aob-generator` | NEW | M | P1 | **GAP — Assignment of Benefits** |

### Pillar 9: jurisdiction-research-library
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `illinois-legal-resource-directory` | `claimedge__jurisdiction__illinois-legal-library` | N | L | P0 | Rename only |
| 2 | *(none)* | `claimedge__jurisdiction__bad-faith-tracker` | NEW | H | P0 | **GAP — bad faith documentation** |
| 3 | *(none)* | `claimedge__jurisdiction__sol-tracker` | NEW | M | P0 | **GAP — statute of limitations** |
| 4 | `pi-case-analyzer` | `claimedge__jurisdiction__pi-case-analyzer` | N | L | P1 | Rename only |
| 5 | `vehicle-collision-case-analyzer` | `claimedge__jurisdiction__vehicle-collision-analyzer` | N | L | P1 | Rename only |

### Pillar 10: ai-os-infrastructure
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `robert-master-os` | `claimedge__ai-os__master-orchestrator` | C | M | P0 | Rename + update triggers |
| 2 | `claimedge-session-memory` | `claimedge__ai-os__session-memory` | N | L | P0 | Rename only |
| 3 | `claimedge-skill-forge` | `claimedge__ai-os__skill-forge` | N | L | P1 | Rename only |
| 4 | `claimedge-vault-system` | `claimedge__ai-os__vault-system` | N | L | P1 | Rename only |
| 5 | `claimedge-training-builder` | `claimedge__ai-os__training-builder` | N | L | P1 | Rename only |
| 6 | `bobby-focus-system` | `claimedge__ai-os__focus-system` | C | M | P1 | Remove "Bobby" references |
| 7 | `bobbys-ai-translator` | `claimedge__ai-os__tech-translator` | C | M | P2 | Remove "Bobby" references |
| 8 | `ai-workflow-decoder` | `claimedge__ai-os__workflow-decoder` | C | M | P1 | Remove personal refs |
| 9 | `kimi-miyagi-coach` | `claimedge__ai-os__kimi-optimizer` | C | M | P2 | Rename + generalize |
| 10 | `kimi-usage-optimizer` | *(merge into above)* | — | — | — | **MERGE — redundant** |
| 11 | `multi-ai-router` | `claimedge__ai-os__ai-router` | C | M | P1 | Remove personal refs |
| 12 | `session-boot-loader` | `claimedge__ai-os__session-boot` | C | M | P1 | Remove personal refs |
| 13 | `session-context-preserver` | *(merge into session-memory)* | — | — | — | **MERGE — redundant** |
| 14 | `thread-audit-manager` | `claimedge__ai-os__thread-audit` | C | M | P2 | Remove personal refs |
| 15 | `thread-handoff-manager` | `claimedge__ai-os__thread-handoff` | C | M | P2 | Remove personal refs |
| 16 | `perplexity-connector-advisor` | `claimedge__ai-os__connector-advisor` | N | L | P2 | Rename only |
| 17 | `skill-lifecycle-manager` | `claimedge__ai-os__skill-lifecycle` | N | L | P1 | Rename only |

### Pillar 11: sports-ventures
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `wrestling-intelligence-master` | `claimedge__sports__wrestling-orchestrator` | N | L | P2 | Rename only |
| 2 | `wrestling-opponent-scout` | `claimedge__sports__opponent-scout` | N | L | P2 | Rename only |
| 3 | `wrestling-bracket-scraper` | `claimedge__sports__bracket-scraper` | N | L | P2 | Rename only |
| 4 | `wrestling-analytics-coach` | `claimedge__sports__analytics-coach` | N | L | P2 | Rename only |
| 5 | `wrestling-data-sync` | `claimedge__sports__data-sync` | N | L | P2 | Rename only |
| 6 | `wrestling-tournament-intelligence-extractor` | `claimedge__sports__tournament-intel` | N | L | P2 | Rename only |
| 7 | `wrestling-thread-auditor` | `claimedge__sports__thread-auditor` | N | L | P2 | Rename only |
| 8 | `wrestling-master-manifest` | `claimedge__sports__wrestling-manifest` | N | L | P2 | Rename only |
| 9 | `wrestler-career-rankings` | `claimedge__sports__career-rankings` | N | L | P2 | Rename only |
| 10 | `tournament-preparation-suite` | `claimedge__sports__tournament-prep` | N | L | P2 | Rename only |
| 11 | `nuway-rumble-command-center` | `claimedge__sports__nuway-command` | N | L | P2 | Rename only |
| 12 | `usa-bracketing-expert` | `claimedge__sports__usa-bracketing` | N | L | P2 | Rename only |
| 13 | `level-up-wrestling-builder` | `claimedge__sports__level-up-builder` | N | L | P2 | Rename only |
| 14 | `icdwa-levelup-bridge` | `claimedge__sports__icdwa-bridge` | N | L | P2 | Rename only |
| 15 | `icdwa-technical-build-suite` | `claimedge__sports__icdwa-tech-suite` | N | L | P2 | Rename only |
| 16 | `illinois-county-duals-command-center` | `claimedge__sports__il-county-duals` | N | L | P2 | Rename only |
| 17 | `buddy-boy-sports-manager` | `claimedge__sports__buddy-boy-manager` | N | L | P2 | Rename only |
| 18 | `sports-tournament-scout` | `claimedge__sports__tournament-scout` | N | L | P2 | Rename only |
| 19 | `content-repurposer` | `claimedge__sports__content-repurposer` | N | L | P2 | Rename only |

### Pillar 12: productization-rd
| # | Current Name | New Name | Status | Effort | Priority | Notes |
|---|-------------|----------|--------|--------|----------|-------|
| 1 | `claimedge-master-coach` | `claimedge__productization__master-coach` | N | L | P1 | Rename only |
| 2 | `social-proof-builder` | `claimedge__productization__social-proof` | N | L | P2 | Rename only |
| 3 | `stripe-setup-wizard` | `claimedge__productization__payment-setup` | N | L | P2 | Rename only |
| 4 | `credit-repair-master-orchestrator` | `claimedge__productization__credit-repair-suite` | C | H | P2 | Evaluate if still active business line |
| 5 | `credit-repair-orchestrator` | *(merge into above)* | — | — | — | **MERGE** |
| 6 | `credit-bureau-dispute-puller` | *(merge into above)* | — | — | — | **MERGE** |

---

## 4. Huuso → ClaimEdge Conversion Guide

### Skill-by-Skill Conversion

#### 1. huuso-brand-presentation-suite
| Field | Value |
|-------|-------|
| **Action** | ARCHIVE |
| **Reason** | Brand assets for a former employer. ClaimEdge needs its own brand skill. |
| **New Skill** | Build `claimedge__productization__brand-system` from scratch (P2) |
| **Content to Save** | Presentation templates, slide structures, formatting rules |
| **Content to Discard** | Huuso colors, logos, fonts, voice/tone references |

#### 2. huuso-claimedge-master
| Field | Value |
|-------|-------|
| **Action** | MERGE into `claimedge__master-workflow` |
| **Reason** | Duplicate workflow orchestrator. Merge unique Huuso-specific tactics into the master. |
| **Merge Target** | Consolidated master workflow (see Pillar 10) |
| **Content to Save** | Any Huuso-specific carrier counter-strategies not in ClaimEdge skills |
| **Content to Discard** | Huuso branding, Huuso SOPs, employee references |

#### 3. huuso-claims-master
| Field | Value |
|-------|-------|
| **Action** | MERGE into `claim-command-center` |
| **Reason** | Duplicate claims management. huuso-claims-master is Huuso-branded version of claim-command-center. |
| **Merge Target** | `claimedge__claims__command-center` |
| **Content to Save** | Any unique inspection checklists, damage assessment templates |
| **Content to Discard** | Huuso branding, all Huuso-specific references |

#### 4. huuso-estimate-builder
| Field | Value |
|-------|-------|
| **Action** | CONVERT to `claimedge__estimate-support__supplement-builder` |
| **Reason** | Core functionality is valuable — Xactimate supplement building. Just needs rebrand. |
| **Changes Needed** | 1. Remove all Huuso references 2. Replace Huuso examples with ClaimEdge 3. Update line item library to ClaimEdge standards 4. Rename carrier-specific sections |
| **Effort** | 2-3 hours |

#### 5. huuso-operations-suite
| Field | Value |
|-------|-------|
| **Action** | ARCHIVE |
| **Reason** | 40-skill operations catalog for Huuso. Not applicable to ClaimEdge solo operation. |
| **New Skill** | Build lean `claimedge__ai-os__operations-guide` (P2) — focused on ClaimEdge's actual ops |
| **Content to Save** | Automation recipes that are tool-agnostic (Zapier, Make) |
| **Content to Discard** | Huuso-specific SOPs, employee management, 40-skill catalog |

#### 6. huuso-review-generator
| Field | Value |
|-------|-------|
| **Action** | CONVERT to `claimedge__productization__review-generator` |
| **Reason** | Google review requests are useful for ANY business. Genericize. |
| **Changes Needed** | 1. Remove Huuso branding 2. Replace with ClaimEdge templates 3. Make business-name configurable |
| **Effort** | 1 hour |

#### 7. huuso-supplement-writer
| Field | Value |
|-------|-------|
| **Action** | CONVERT to `claimedge__carrier-comms__supplement-letter-writer` |
| **Reason** | Most valuable Huuso skill — dispute letter writing is core to ClaimEdge. |
| **Changes Needed** | 1. Remove all Huuso letterhead/branding 2. Replace with ClaimEdge templates 3. Expand beyond exterior to all claim types 4. Add Illinois statute references 5. Update carrier address database |
| **Effort** | 3-4 hours |

### Merge Strategy Summary

| Merge Group | Skills Combined | Result | Net Change |
|-------------|----------------|--------|------------|
| Master Workflow | `huuso-claimedge-master` + `claimed-master-workflow` + `claim-command-center` | Single master workflow | -2 skills |
| Session Management | `claimedge-session-memory` + `session-context-preserver` | Unified session system | -1 skill |
| AI Tool Selection | `ai-workflow-decoder` + `kimi-usage-optimizer` | Single AI optimizer | -1 skill |
| Credit Repair | `credit-repair-master-orchestrator` + `credit-repair-orchestrator` + `credit-bureau-dispute-puller` | Single credit repair suite | -2 skills |
| Investigation | `claimedge-complete-system` + `claimedge-full-claims-investigation` | Unified investigation (phased) | -1 skill |
| Operations | `huuso-operations-suite` → archive, build lean replacement | Minimal ops guide | -1 skill |
| **Total** | **14 skills** | **6 consolidated** | **-8 skills** |

**Result: 67 skills → ~59 active skills after merges**

---

## 5. Golden Path Workflow

The ideal ClaimEdge claim lifecycle, with skills that activate at each stage.

```
[1] INTAKE ──────────────────────────────────────
    Trigger: New lead/contact
    Skills: claimedge__intake-triage__client-intake
            claimedge__intake-triage__conflict-checker
    Output: Qualified lead / Conflict check pass

[2] POLICY REVIEW ───────────────────────────────
    Trigger: Signed fee agreement
    Skills: claimedge__intake-triage__fee-agreement-generator
            claimedge__policy-review__coverage-analyzer
    Output: Coverage summary, limits, exclusions identified

[3] INSPECTION ──────────────────────────────────
    Trigger: Policy confirmed, date scheduled
    Skills: claimedge__inspections__photo-documentation
            claimedge__inspections__hazards-assessment
            claimedge__inspections__moisture-mapping
    Output: Photo report, hazard ID, moisture readings

[4] DAMAGE ASSESSMENT ───────────────────────────
    Trigger: Inspection complete
    Skills: claimedge__exterior-damage__wind-hail-assessor
            claimedge__exterior-damage__roof-valley-specialist
    Output: Damage assessment report

[5] CODE COMPLIANCE ─────────────────────────────
    Trigger: Damage identified
    Skills: claimedge__code-compliance__municipal-toolkit
            claimedge__code-compliance__upgrade-argument-library
    Output: Code compliance letter, upgrade arguments

[6] ESTIMATE / SUPPLEMENT ───────────────────────
    Trigger: Scope of damage known
    Skills: claimedge__estimate-support__xactimate-pricing-chicago
            claimedge__estimate-support__supplement-builder
            claimedge__estimate-support__line-item-library
            claimedge__estimate-support__supplement-aging-tracker
    Output: Supplement demand, line item justifications

[7] CARRIER COMMUNICATIONS ──────────────────────
    Trigger: Supplement ready
    Skills: claimedge__carrier-comms__supplement-letter-writer
            claimedge__carrier-comms__state-farm-playbook
            claimedge__carrier-comms__allstate-playbook
            claimedge__carrier-comms__liberty-mutual-playbook
            claimedge__carrier-comms__negotiation-tracker
    Output: Demand letter, negotiation strategy

[8] DOCUMENT ASSEMBLY ───────────────────────────
    Trigger: All evidence collected
    Skills: claimedge__document-assembly__proof-of-loss-generator
            claimedge__document-assembly__lor-generator
            claimedge__document-assembly__auto-deploy
    Output: Complete claim packet

[9] SETTLEMENT / CLOSE ──────────────────────────
    Trigger: Negotiation complete
    Skills: claimedge__jurisdiction__sol-tracker
            claimedge__ai-os__session-memory (archive case)
    Output: Settlement, closed file
```

### Parallel Support Skills (activate throughout)
- `claimedge__jurisdiction__illinois-legal-library` — Legal research as needed
- `claimedge__jurisdiction__bad-faith-tracker` — If carrier acts in bad faith
- `claimedge__ai-os__master-orchestrator` — Session management, skill routing
- `claimedge__estimate-support__depreciation-calculator` — When depreciation disputed

---

## 6. Migration Tracker Template

Copy this table to track progress. Update status as you work.

| # | Current Skill | New Name | Pillar | Status | Started | Complete | Notes |
|---|--------------|----------|--------|--------|---------|----------|-------|
| 1 | huuso-brand-presentation-suite | ARCHIVE | N/A | NOT_STARTED | | | Archive — not migrating |
| 2 | huuso-claimedge-master | MERGE | N/A | NOT_STARTED | | | Merge into master workflow |
| 3 | huuso-claims-master | MERGE | N/A | NOT_STARTED | | | Merge into claim-command-center |
| 4 | huuso-estimate-builder | claimedge__estimate-support__supplement-builder | 6 | NOT_STARTED | | | Remove Huuso refs |
| 5 | huuso-operations-suite | ARCHIVE | N/A | NOT_STARTED | | | Archive — build lean replacement later |
| 6 | huuso-review-generator | claimedge__productization__review-generator | 12 | NOT_STARTED | | | Genericize for any business |
| 7 | huuso-supplement-writer | claimedge__carrier-comms__supplement-letter-writer | 7 | NOT_STARTED | | | Most important conversion |
| 8 | robert-master-os | claimedge__ai-os__master-orchestrator | 10 | NOT_STARTED | | | Remove personal refs |
| 9 | bobby-focus-system | claimedge__ai-os__focus-system | 10 | NOT_STARTED | | | Remove "Bobby" refs |
| 10 | bobbys-ai-translator | claimedge__ai-os__tech-translator | 10 | NOT_STARTED | | | Remove "Bobby" refs |
| 11 | ai-workflow-decoder | claimedge__ai-os__workflow-decoder | 10 | NOT_STARTED | | | Merge kimi-usage-optimizer |
| 12 | kimi-miyagi-coach | claimedge__ai-os__kimi-optimizer | 10 | NOT_STARTED | | | Generalize |
| 13 | session-boot-loader | claimedge__ai-os__session-boot | 10 | NOT_STARTED | | | Remove personal refs |
| 14 | thread-audit-manager | claimedge__ai-os__thread-audit | 10 | NOT_STARTED | | | Remove personal refs |
| 15 | thread-handoff-manager | claimedge__ai-os__thread-handoff | 10 | NOT_STARTED | | | Remove personal refs |
| 16 | *(continue for all 67 skills)* | | | | | | |

**Status options:** NOT_STARTED | IN_PROGRESS | REVIEW | COMPLETE | ARCHIVED

---

## 7. Quick Wins List

Skills that need zero or minimal changes — batch these first for momentum.

### Tier 1: Rename Only (~15 minutes each)
- [ ] `claimedge-session-memory` → `claimedge__ai-os__session-memory`
- [ ] `claimedge-skill-forge` → `claimedge__ai-os__skill-forge`
- [ ] `claimedge-vault-system` → `claimedge__ai-os__vault-system`
- [ ] `claimedge-training-builder` → `claimedge__ai-os__training-builder`
- [ ] `claimedge-auto-deploy` → `claimedge__document-assembly__auto-deploy`
- [ ] `claimedge-master-coach` → `claimedge__productization__master-coach`
- [ ] `social-proof-builder` → `claimedge__productization__social-proof`
- [ ] `stripe-setup-wizard` → `claimedge__productization__payment-setup`
- [ ] `perplexity-connector-advisor` → `claimedge__ai-os__connector-advisor`
- [ ] `skill-lifecycle-manager` → `claimedge__ai-os__skill-lifecycle`

### Tier 2: Minor Alignment (~30 minutes each)
- [ ] `claimedge-material-hazards` → `claimedge__inspections__hazards-assessment`
- [ ] `claimedge-roof-valley-claims` → `claimedge__exterior-damage__roof-valley-specialist`
- [ ] `wind-hail-property-claims` → `claimedge__exterior-damage__wind-hail-assessor`
- [ ] `premier-claims-investigation` → `claimedge__exterior-damage__commercial-investigation`
- [ ] `municipal-code-compliance-toolkit` → `claimedge__code-compliance__municipal-toolkit`
- [ ] `chicago-xactimate-pricing` → `claimedge__estimate-support__xactimate-pricing-chicago`
- [ ] `illinois-legal-resource-directory` → `claimedge__jurisdiction__illinois-legal-library`
- [ ] `pi-case-analyzer` → `claimedge__jurisdiction__pi-case-analyzer`
- [ ] `vehicle-collision-case-analyzer` → `claimedge__jurisdiction__vehicle-collision-analyzer`

### Tier 3: Batch Sports Rename (~10 minutes each, do all at once)
All 18 sports-ventures skills — simple prefix change from `wrestling-*` / `buddy-boy-*` to `claimedge__sports__*`

---

## 8. High-Effort Migrations

Ranked by difficulty. Tackle one per day.

| Rank | Skill | Effort | Why It's Hard | Mitigation |
|------|-------|--------|---------------|------------|
| 1 | `huuso-supplement-writer` → `claimedge__carrier-comms__supplement-letter-writer` | 3-4 hrs | Most carrier letter templates reference Huuso | Do template-by-template, not all at once |
| 2 | `huuso-estimate-builder` → `claimedge__estimate-support__supplement-builder` | 2-3 hrs | Xactimate line items reference Huuso pricing | Update pricing tables first |
| 3 | `robert-master-os` → `claimedge__ai-os__master-orchestrator` | 2 hrs | Personal references throughout triggers | Batch find/replace "Bobby" → "user" |
| 4 | Master workflow merge (3 skills → 1) | 3-4 hrs | Need to identify which features from each to keep | Create feature matrix first |
| 5 | Credit repair trio merge | 2-3 hrs | Three skills into one cohesive suite | Keep orchestrator as base |

### Recommended Timeline
- **Week 1:** All Tier 1 renames + archive 7 Huuso skills
- **Week 2:** All Tier 2 renames + huuso-supplement-writer conversion
- **Week 3:** High-effort migrations + master workflow merge

---

## 9. Post-Migration Checklist

### Infrastructure
- [ ] All 67 skills reviewed and dispositioned
- [ ] 7 Huuso skills archived (not deleted — kept in GitHub archive branch)
- [ ] 6 merge groups executed
- [ ] 0 Huuso references remain in active skills
- [ ] Naming convention applied consistently

### Verification
- [ ] Search all skills for "Huuso" — should return 0 results in active
- [ ] Search all skills for "bobby" in triggers — should return 0 (use "user" or "owner")
- [ ] Notion AI OS Hub updated with new pillar structure
- [ ] GitHub repo has archive branch with pre-migration state

### Documentation
- [ ] Migration tracker table fully updated to COMPLETE
- [ ] Golden Path workflow tested with a sample claim
- [ ] New skill creation follows naming convention
- [ ] Team (if any) trained on new structure

---

## 10. Naming Convention Quick Reference

### Format
```
claimedge__<pillar>__<function>__<variant>
```

### Pillar Abbreviations
| Pillar | Abbreviation | Example |
|--------|-------------|---------|
| claim-intake-triage | `intake-triage` | `claimedge__intake-triage__client-intake` |
| policy-coverage-review | `policy-review` | `claimedge__policy-review__coverage-analyzer` |
| inspections-field-evidence | `inspections` | `claimedge__inspections__photo-documentation` |
| exterior-damage-assessment | `exterior-damage` | `claimedge__exterior-damage__wind-hail-assessor` |
| code-compliance | `code-compliance` | `claimedge__code-compliance__municipal-toolkit` |
| estimate-supplement-support | `estimate-support` | `claimedge__estimate-support__supplement-builder` |
| carrier-communications | `carrier-comms` | `claimedge__carrier-comms__state-farm-playbook` |
| document-assembly | `document-assembly` | `claimedge__document-assembly__proof-of-loss-generator` |
| jurisdiction-research-library | `jurisdiction` | `claimedge__jurisdiction__illinois-legal-library` |
| ai-os-infrastructure | `ai-os` | `claimedge__ai-os__master-orchestrator` |
| sports-ventures | `sports` | `claimedge__sports__wrestling-orchestrator` |
| productization-rd | `productization` | `claimedge__productization__brand-system` |

### Rules
1. Always lowercase
2. Always double-underscore (`__`) between segments
3. Always start with `claimedge__`
4. Function name should be verb-noun (e.g., `supplement-builder`, not `supplements`)
5. Variant is optional — only add when there's more than one skill for the same function
6. No spaces, no hyphens in variant (use underscore if needed)
7. Maximum 80 characters total

---

*End of ClaimEdge Skill Migration Pack*