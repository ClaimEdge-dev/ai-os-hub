---
name: claimedge-policy-review-endorsement-tracker
description: >
  Insurance policy endorsement tracking and mid-claim change detection system for ClaimEdge LLC.
  Monitors for carrier endorsement additions, modifications, or removals that occur after a loss
  event to restrict coverage. Detects retroactive endorsements, tracks effective dates vs loss dates,
  generates dispute arguments under Illinois law, and produces carrier challenge documentation.
  Triggers on: endorsement change, mid-claim endorsement, retroactive endorsement, policy change
  after loss, endorsement effective date dispute, coverage restriction after claim filing, carrier
  added endorsement, policy modification during claim, endorsement backdating, Illinois insurance
  endorsement law, 215 ILCS 5/154.6 endorsement issues, or any request involving endorsement
  tracking, monitoring, or dispute.
---

# Policy Endorsement Tracker

Detect and dispute carrier endorsement changes made mid-claim to restrict coverage.

## Purpose

Carriers frequently add restrictive endorsements *after* a loss occurs but *before* claim resolution.
These mid-claim endorsement changes are often unlawful when applied retroactively or without proper
notice. This skill provides the detection framework, legal countermeasures, and dispute templates
to challenge improper endorsement changes under Illinois law.

## When This Skill Activates

- Carrier notifies of a "policy update" or "endorsement change" during an active claim
- Comparing initial policy (at loss date) to current policy reveals differences
- Adjuster cites a newly-added exclusion or limitation not present in original policy
- Carrier claims an endorsement reduces coverage for the pending claim
- Effective date of endorsement is on or after the date of loss
- Need to document endorsement history for bad faith or appraisal proceedings

## 4-Phase Endorsement Tracking Workflow

### Phase 1: Endorsement Detection

Compare the policy-in-force at date of loss against the policy presented by carrier.

**Required Documents:**
- Policy declarations page (as of date of loss)
- Current declarations page (carrier's latest version)
- Complete endorsement list from both versions
- Agent/broker records of when endorsements were issued
- Insured's correspondence about any policy changes

**Detection Checklist:**
- [ ] Obtain full policy packet from date of loss (not current version)
- [ ] Request complete endorsement history from carrier
- [ ] Compare endorsement lists line-by-line
- [ ] Flag any endorsement with effective date on or after date of loss
- [ ] Identify endorsements that reduce or exclude coverage
- [ ] Check for endorsements never disclosed to insured

**Output:** Endorsement Comparison Report (see `references/endorsement-tracking-framework.md`)

### Phase 2: Date Analysis & Legal Classification

Determine if each changed endorsement is lawful under Illinois regulations.

**Classification Matrix:**

| Category | Description | Legal Status | Action |
|----------|-------------|--------------|--------|
| **Type A** | Effective BEFORE date of loss | Generally lawful | Document only |
| **Type B** | Effective ON date of loss | Suspicious | Investigate timing |
| **Type C** | Effective AFTER date of loss | Likely unlawful | Challenge immediately |
| **Type D** | Never disclosed to insured | Unlawful per 50 Ill. Adm. Code 919 | Challenge + report to IDOI |
| **Type E** | Reduces coverage for pending claim | Bad faith indicator | Challenge + document for 215 ILCS 5/155 |

**Illinois Regulatory Framework:**
- 215 ILCS 5/143.1: Changes in policy terms must be conspicuous
- 50 Ill. Adm. Code Part 919: Standards for policy forms and endorsements
- 215 ILCS 5/154.6: Unfair claims settlement practices include misrepresenting policy provisions

See `references/illinois-endorsement-statutes.md` for full statute details.

### Phase 3: Countermeasure Development

Build legal and factual arguments against improper endorsement changes.

**Counter-Argument Categories:**

1. **Retroactivity Challenge:** Endorsement cannot apply to loss that already occurred
2. **Notice Failure:** Insured was never informed of the endorsement per 215 ILCS 5/143.1
3. **Conspicuousness Failure:** Endorsement change not prominently displayed
4. **Unfair Claims Practice:** Mid-claim coverage reduction violates 215 ILCS 5/154.6
5. **Estoppel:** Carrier accepted premium for broader coverage; cannot now restrict
6. **Waiver:** Prior claim handling under broader coverage waives right to enforce restriction

See `references/retroactive-endorsement-countermeasures.md` for detailed arguments,
case law, and evidence requirements for each category.

### Phase 4: Dispute Documentation

Generate carrier dispute letters and regulatory complaints.

**Output Documents:**
1. **Endorsement Challenge Letter** — to carrier, citing specific unlawful changes
2. **IDOI Complaint Addendum** — if endorsement change constitutes unfair practice
3. **Appraisal Brief Section** — if endorsement dispute goes to appraisal
4. **Bad Faith Evidence Entry** — for 215 ILCS 5/155 documentation

Templates and language in `references/endorsement-tracking-framework.md`.

## Critical Rules

1. **Always compare policy at date of loss, not current policy.** The policy-in-force at the
time of loss controls coverage, not any later version.
2. **Effective date is dispositive.** An endorsement with an effective date after the loss
cannot legally reduce coverage for that loss unless the policy explicitly permits retroactive
changes (rare and must be conspicuous).
3. **Notice to insured is mandatory.** Under 215 ILCS 5/143.1, any endorsement that reduces
coverage must be conspicuous and the insured must receive actual notice.
4. **Document everything before challenging.** Once the carrier knows you're tracking
endorsements, they may alter records. Secure all documents first.
5. **This skill pairs with Coverage Analyzer.** Run the Coverage Analyzer first to establish
baseline coverage, then use this skill to detect any mid-claim changes.

## Reference Files

| File | Content | When to Read |
|------|---------|--------------|
| `references/endorsement-tracking-framework.md` | Full 4-phase workflow, templates, checklists, output formats | When executing endorsement detection or building dispute documents |
| `references/retroactive-endorsement-countermeasures.md` | 6 counter-argument categories with case law, evidence checklists, sample language | When developing legal challenges to improper endorsement changes |
| `references/illinois-endorsement-statutes.md` | IL statutes, regulations, and case law specific to endorsement changes | When citing legal authority in dispute letters or IDOI complaints |

## Integration Points

**Upstream:**
- `claimedge-policy-review-coverage-analyzer` — Provides baseline coverage analysis;
this skill detects deviations from that baseline

**Downstream:**
- `claimedge-carrier-comms-supplement-letter-writer` — Receives endorsement challenge
language for inclusion in carrier correspondence
- `claimedge-jurisdiction-bad-faith-tracker` — Receives Type D/E findings for
bad faith documentation under 215 ILCS 5/155
- `claimedge-document-assembly-proof-of-loss-generator` — Receives endorsement
history for inclusion in claim packets

## Document Control

| Field | Value |
|---|---|
| **Skill** | Policy Endorsement Tracker |
| **Version** | 1.0 |
| **Date** | July 16, 2026 |
| **Pillar** | Policy & Coverage Review |
| **Part of** | ClaimEdge LLCDocument Control AI OS |
| **Skills** | #3 of 67 |
| **Status** | Production |
