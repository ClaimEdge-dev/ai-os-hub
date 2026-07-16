# Endorsement Tracking Framework

Complete 4-phase workflow with document templates, checklists, and output formats.

---

## TABLE OF CONTENTS

1. [Phase 1: Endorsement Detection](#phase-1-endorsement-detection)
2. [Phase 2: Date Analysis & Legal Classification](#phase-2-date-analysis--legal-classification)
3. [Phase 3: Countermeasure Development](#phase-3-countermeasure-development)
4. [Phase 4: Dispute Documentation](#phase-4-dispute-documentation)
5. [Output Templates](#output-templates)

---

## Phase 1: Endorsement Detection

### Step 1A: Secure Policy-at-Loss

The policy that was in force on the date of loss is the controlling document.
Carriers may attempt to substitute a current policy with restrictive endorsements.

**Sources for Policy-at-Loss:**
1. Insured's original policy documents (mail, email, agent portal)
2. Insurance agent/broker records (independent of carrier)
3. Mortgage company escrow records (they require proof of coverage)
4. Prior claims under the same policy (shows coverage that existed)
5. State insurance department filings (public record of policy forms)
6. Premium invoices showing coverage levels paid for

**Document Request Language (to carrier):**

> "Under 215 ILCS 5/154.6 and 50 Ill. Adm. Code Part 919, please provide the complete
> policy-in-force as of [DATE OF LOSS], including all declarations pages, coverage forms,
> endorsements, and amendments that were effective on that date. Please also provide a
> complete endorsement history showing the effective date, description, and notice date
> for each endorsement added, modified, or removed from the policy since inception."

### Step 1B: Line-by-Line Comparison

Create a side-by-side comparison of all endorsements.

| Endorsement # | Description | Original Effective Date | Current Version Effective Date | Change Detected |
|---------------|-------------|------------------------|-------------------------------|-----------------|
| | | | | |

**Fields to Compare:**
- Endorsement number/code
- Endorsement title/description
- Effective date
- Coverage impact (broader, narrower, no change)
- Whether endorsement was disclosed to insured
- Premium impact (increase, decrease, no change)

### Step 1C: Flag for Review

Flag any endorsement where ANY of the following is true:

- [ ] Effective date is on or after date of loss
- [ ] Reduces or excludes any coverage
- [ ] Was never disclosed to insured in writing
- [ ] Was added after claim was reported
- [ ] Increases deductible or adds new deductible
- [ ] Adds new exclusion not in original policy
- [ ] Reduces coverage limits below amount at time of loss
- [ ] Changes replacement cost to actual cash value
- [ ] Adds cosmetic damage exclusion (post-PA 103-0509)
- [ ] Modifies ordinance or law coverage
- [ ] Changes water damage provisions
- [ ] Adds mold limitation

---

## Phase 2: Date Analysis & Legal Classification

### Date Comparison Matrix

For each flagged endorsement, compare three critical dates:

1. **Date of Loss (DOL):** When the damage occurred
2. **Endorsement Effective Date:** When carrier claims endorsement took effect
3. **Notice Date:** When (if) insured was informed of the endorsement

```
Timeline Analysis:

Policy Inception -------- DOL -------- Notice -------- Claim Filed -------- Now
              |           |              |                  |              |
              |     [Endorsement       [When insured    [When claim    [Current
              |      Effective Date]     learned of it]    reported]     dispute]
              |
        [If endorsement effective date is HERE or later -> UNLAWFUL]
```

### Classification Rules

**Type A: Effective BEFORE DOL**
- Status: Generally lawful
- Action: Verify insured received proper notice per 215 ILCS 5/143.1
- If no notice: Escalate to Type D

**Type B: Effective ON DOL**
- Status: Highly suspicious
- Action: Demand proof of when endorsement was issued vs when loss occurred
- Burden shifts to carrier to prove endorsement preceded loss
- If loss time-of-day is known, compare to endorsement time stamp

**Type C: Effective AFTER DOL**
- Status: Presumptively unlawful
- Action: Challenge immediately
- Cannot reduce coverage for loss that already occurred
- Exception: Only if policy explicitly permits retroactive changes AND insured
  received conspicuous notice (extremely rare)

**Type D: Never Disclosed**
- Status: Unlawful per 50 Ill. Adm. Code 919.30
- Action: Challenge + report to IDOI
- Carrier must provide proof of mailing or delivery
- Email without open confirmation is insufficient

**Type E: Reduces Coverage for Pending Claim**
- Status: Bad faith indicator
- Action: Challenge + document for 215 ILCS 5/155
- Strong evidence of carrier attempting to avoid payment
- Document pattern if carrier has done this on other claims

---

## Phase 3: Countermeasure Development

### Countermeasure Selection Guide

| If the endorsement... | Use Countermeasure | Cite |
|-----------------------|-------------------|------|
| Has effective date after DOL | Retroactivity Challenge | Basic contract law + policy construction |
| Was never disclosed to insured | Notice Failure | 215 ILCS 5/143.1 |
| Was buried in renewal packet | Conspicuousness Failure | 215 ILCS 5/143.1 + 50 Ill. Adm. Code 919.20 |
| Added after claim reported | Unfair Claims Practice | 215 ILCS 5/154.6(d)(1) |
| Reduces coverage claim is for | Bad Faith Indicator | 215 ILCS 5/155 |
| Accepted premium for broader coverage | Estoppel | Common law + contract principles |
| Previously handled claim under broader terms | Waiver | Common law + course of dealing |

### Evidence Collection Checklist

For each countermeasure, collect:

**Retroactivity Challenge:**
- [ ] Exact date and time of loss (police report, weather data, witness statements)
- [ ] Endorsement effective date from carrier records
- [ ] When endorsement was actually processed (check carrier system timestamps)
- [ ] Whether policy language permits retroactive changes

**Notice Failure:**
- [ ] All correspondence from carrier for 12 months before and after endorsement
- [ ] Proof of mailing (certified mail receipt, email read receipt)
- [ ] Agent/broker testimony about whether they informed insured
- [ ] Insured's sworn affidavit about receipt (or non-receipt)
- [ ] USPS informed delivery records if available

**Conspicuousness Failure:**
- [ ] Copy of document that supposedly contained notice
- [ ] Whether endorsement was highlighted, bolded, or called out
- [ ] Comparison to industry standard for conspicuous notice
- [ ] Whether endorsement language was clear and plain (not buried in fine print)

**Unfair Claims Practice:**
- [ ] Date claim was reported
- [ ] Date endorsement was added
- [ ] Whether adjuster mentioned endorsement before or after claim valuation
- [ ] Whether carrier delayed claim to add endorsement first

**Estoppel:**
- [ ] Premium payment records showing payment for broader coverage
- [ ] Prior claims handled under broader coverage terms
- [ ] Agent representations about coverage scope
- [ ] Marketing materials showing broader coverage

**Waiver:**
- [ ] Prior claims paid under broader coverage
- [ ] Inspection reports acknowledging broader coverage
- [ ] Agent statements about coverage scope
- [ ] Course of dealing between carrier and insured

---

## Phase 4: Dispute Documentation

### Template A: Endorsement Challenge Letter (to Carrier)

---

[Date]

[Carrier Name]
[Carrier Address]
Re: Claim #[CLAIM NUMBER]
Policy #[POLICY NUMBER]
Insured: [INSURED NAME]
Date of Loss: [DATE OF LOSS]

Dear Claims Manager:

We represent [INSURED NAME] regarding the above-referenced claim. Our review of the
policy history has revealed [NUMBER] endorsement[s] that [was/were] [added/modified]
[during/after] the pendency of this claim that [reduces/excludes] coverage for the loss
that occurred on [DATE OF LOSS].

**Endorsement[s] at Issue:**

[For each endorsement:]
- Endorsement [NUMBER]: [DESCRIPTION]
- Effective Date: [DATE]
- Date of Loss: [DATE]
- [Effective date is AFTER date of loss / Never disclosed to insured]

**Legal Basis for Challenge:**

[Select applicable:]

Under well-established principles of insurance law, an endorsement that purports to be
effective after the date of loss cannot reduce coverage for a loss that has already
occurred. [Carrier] is attempting to apply [ENDORSEMENT NAME] retroactively to a loss
that took place on [DATE OF LOSS], [NUMBER] days [before/after] the endorsement
effective date of [DATE]. This is unlawful.

[AND/OR]

Under 215 ILCS 5/143.1, any change in policy terms that reduces coverage must be
"conspicuous" and the insured must receive actual notice. [Insured] never received
notice of this endorsement. [Carrier] cannot produce [mailing receipts / email
confirmations / agent testimony] showing disclosure.

[AND/OR]

215 ILCS 5/154.6(d) prohibits insurers from [misrepresenting pertinent facts or
insurance policy provisions / failing to adopt and implement reasonable standards for
the prompt investigation of claims]. By adding a restrictive endorsement mid-claim and
attempting to apply it to this loss, [Carrier] has engaged in an unfair claims practice.

**Demand:**

We demand that [Carrier]:
1. Withdraw any reliance on [ENDORSEMENT NAME] for this claim
2. Apply the policy terms as they existed on [DATE OF LOSS]
3. Re-evaluate the claim under the pre-endorsement coverage terms
4. Provide written confirmation within 15 business days

Failure to comply will result in referral to the Illinois Department of Insurance and
pursuit of all remedies available under 215 ILCS 5/155.

Respectfully,

[SIGNATURE]
Robert Krapil
ClaimEdge LLCDocument Control

---

### Template B: IDOI Complaint Addendum

If endorsement change constitutes unfair practice, add to IDOI complaint:

> **Unfair Practice Allegation: Mid-Claim Endorsement Change**
>
> After [Insured] filed a claim on [DATE], [Carrier] added [ENDORSEMENT NAME] with an
effective date of [DATE], which [reduces/excludes] coverage for [TYPE OF DAMAGE]. This
endorsement was [never disclosed to the insured / added after the claim was reported /
effective after the date of loss]. This constitutes:
>
> 1. A misrepresentation of policy provisions (215 ILCS 5/154.6(d)(1))
> 2. An unfair claim settlement practice (215 ILCS 5/154.6(d)(7))
> 3. Potentially bad faith under 215 ILCS 5/155
>
> [Carrier] has [NUMBER] other complaints for similar conduct in Illinois [if known].

### Template C: Appraisal Brief Section

If endorsement dispute goes to appraisal:

> **III. Policy Terms Controlling This Loss**
>
> The policy in force on [DATE OF LOSS] controls the coverage for this loss. Any
endorsement with an effective date after [DATE OF LOSS] is inapplicable. The
[ENDORSEMENT NAME], which [Carrier] now relies upon, has an effective date of
[EFFECTIVE DATE], which is [NUMBER] days [after/before] the date of loss.
>
> Under standard principles of insurance policy construction, endorsements apply
prospectively unless the policy explicitly provides for retroactive application.
[Policy Form] does not contain any provision permitting retroactive endorsement
application. Therefore, the [ENDORSEMENT NAME] cannot affect coverage for this loss.

### Template D: Bad Faith Evidence Entry

For 215 ILCS 5/155 bad faith documentation:

| Element | Evidence |
|---------|----------|
| **Date of Loss** | [DATE] |
| **Date Claim Reported** | [DATE] |
| **Endorsement Added** | [ENDORSEMENT NAME] on [DATE] |
| **Effective Date** | [DATE] (after DOL) |
| **Coverage Impact** | [Reduces/excludes] [TYPE] |
| **Notice to Insured** | [None / insufficient / disputed] |
| **Carrier Defense** | [What carrier claims] |
| **Legal Violation** | 215 ILCS 5/154.6(d)(1), (d)(7) |
| **Damages** | Delayed claim payment, coverage denial, emotional distress |

---

## Output Templates

### Endorsement Comparison Report (Quick Format)

```
ENDORSEMENT COMPARISON REPORT
Claim: [NUMBER] | Policy: [NUMBER] | Insured: [NAME]
Date of Loss: [DATE] | Report Date: [DATE]

BASELINE POLICY (at DOL): [POLICY FORM] effective [DATE]
CURRENT POLICY (carrier version): [POLICY FORM] effective [DATE]

ENDORSEMENT CHANGES DETECTED: [NUMBER]

| # | Endorsement | Eff. Date | vs DOL | Disclosed | Coverage Impact | Class | Action |
|---|-------------|-----------|--------|-----------|-----------------|-------|--------|
| 1 | | | | | | | |
| 2 | | | | | | | |

LEGAL CLASSIFICATION SUMMARY:
Type A (Lawful): [NUMBER]
Type B (Suspicious): [NUMBER]
Type C (Unlawful - retroactive): [NUMBER]
Type D (Unlawful - no notice): [NUMBER]
Type E (Bad faith indicator): [NUMBER]

RECOMMENDED ACTIONS:
1.
2.
3.

Prepared by: [NAME] | Date: [DATE]
```

### Endorsement Tracking Log (For Multi-Claim Monitoring)

Use this to track if a carrier has a pattern of mid-claim endorsement changes:

```
CARRIER ENDORSEMENT PATTERN TRACKER
Carrier: [NAME] | Tracking Since: [DATE]

| Claim # | DOL | Endorsement Added | Eff. Date | Days After DOL | Disclosed? | Outcome |
|---------|-----|-------------------|-----------|----------------|------------|---------|
| | | | | | | |

Pattern Summary:
Total claims tracked:
Claims with mid-claim endorsements:
Average days after DOL endorsement added:
Disclosure rate:
Success rate in challenging:
```
