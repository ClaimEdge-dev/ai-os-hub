---
name: claimedge-policy-review-coverage-analyzer
description: >
  Comprehensive insurance policy coverage analysis system for property damage claims.
  Analyzes homeowner policies to identify coverage types, limits, exclusions, and code
  upgrade provisions. Generates coverage verification checklists and dispute arguments
  for carrier negotiations. Integrates with ClaimEdge claim investigation workflow and
  Illinois insurance statutes. Triggers on policy review requests, coverage verification,
  exclusion challenges, or when analyzing homeowners insurance policies for hail, wind,
  water, fire, or storm damage claims.

  **Pillar:** Policy & Coverage Review
  **ClaimEdge OS Layer:** Pillar 2 (of 7)
  **Built:** 2026-07-16
  **Author:** ClaimEdge AI OS Build System
---

# Policy Coverage Analyzer

## Overview

Insurance policy coverage analysis system for property damage claims. Analyzes homeowner policies to identify coverage types, limits, exclusions, and code upgrade provisions. Generates coverage verification checklists and dispute arguments for carrier negotiations.

**Trigger Condition:**
- User asks to review a policy
- User needs coverage verification
- User wants to challenge an exclusion
- Analyzing homeowners insurance for property damage
- Preparing for carrier negotiation on coverage disputes

**Integration:**
- Layer: Pillar 2 (Policy & Coverage Review)
- Upstream: Client Intake Suite (Pillar 1)
- Downstream: Inspection & Photo Documentation (Pillar 3)
- External: TrackActive for policy document retrieval

## Workflow

### Phase 1: Policy Document Intake
1. Receive policy documents from intake or direct upload
2. Extract key policy provisions using analysis framework
3. Identify policy type, carrier, and effective dates
4. Flag pre-existing endorsements or modifications

### Phase 2: Coverage Analysis
1. Apply 4-Type Coverage Classification to all provisions
2. Identify coverage limits and sub-limits
3. Locate code upgrade / ordinance & law provisions
4. Map exclusions to specific claim scenarios
5. Generate Coverage Verification Checklist

### Phase 3: Exclusion Challenge Analysis
1. Cross-reference exclusions against Illinois statutes
2. Apply Exclusion Challenge Framework
3. Identify ambiguous or unconscionable exclusions
4. Generate challenge arguments with statutory citations

### Phase 4: Dispute Preparation
1. Compile coverage findings into structured report
2. Generate carrier dispute letters
3. Prepare IDOI complaint documentation
4. Create appraisal brief sections

## Output

### Coverage Analysis Report
- Coverage type classification (4-Type system)
- Limits and sub-limits inventory
- Code upgrade provisions identified
- Exclusion analysis with challenge recommendations
- Carrier dispute letter template

### Dispute Documentation
- Statute-based challenge arguments
- Case law citations
- Carrier-specific counter-arguments
- IDOI complaint template

## Reference Files

### 1. Policy Analysis Framework (`references/policy-analysis-framework.md`)
- 4-Type Coverage Classification system
- Coverage verification checklists
- Carrier negotiation templates
- Output format specifications

### 2. Coverage Types Library (`references/coverage-types-library.md`)
- 12+ coverage type definitions
- Common exclusions by coverage type
- Code upgrade trigger analysis
- Cross-reference tables

### 3. Exclusion Database (`references/exclusion-database.md`)
- 25+ common exclusion types
- Challenge framework for each exclusion
- Illinois statutory counter-arguments
- Case law database

### 4. Illinois Statutes (`references/illinois-statutes.md`)
- Primary statutes: 215 ILCS 5/143, 5/154, 5/154.6, 5/155
- Administrative regulations: 50 Ill. Adm. Code Part 919
- Case law compilation
- Practical application guide

## Activation

```
Skill: claimedge-policy-review-coverage-analyzer
Trigger: policy review, coverage verification, exclusion challenge
Context: property damage claim + homeowner policy
Output: Coverage Analysis Report + dispute documentation
```

## Dependencies
- claimedge-client-intake-suite (Pillar 1)
- claimedge-illinois-legal-resource-directory
- Illinois insurance statutes reference

## Version History
- v1.0 (2026-07-16): Initial release with 4-type classification, 12+ coverage types, 25+ exclusion types, full Illinois statute integration
