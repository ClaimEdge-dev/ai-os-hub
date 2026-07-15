# ClaimEdge Ubiquitous Language Glossary

> **Domain:** Public Adjusting & Insurance Claims Consulting  
> **Organization:** ClaimEdge LLC  
> **Owner:** Robert Krapil  
> **Last Updated:** 2026-07-16  
> **Version:** 1.0  

---

## Purpose

This document establishes the canonical terminology for the ClaimEdge AI OS. All skills, prompts, database schemas, and external communications MUST use these terms consistently. Deviations create ambiguity, errors in legal documents, and confusion in carrier communications.

**Rules:**
- Use **canonical terms** in all AI-generated output
- **Never use** terms listed in "Aliases to Avoid"
- When a term is ambiguous, consult this glossary before deciding
- Updates require Warden (compliance) + Forge (skill) + Atlas (orchestration) approval

---

## Claim Lifecycle

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Claim** | A formal request by an insured for coverage under a policy | case, matter, file |
| **Insured** | The policyholder who filed the claim | client, customer, homeowner |
| **Carrier** | The insurance company obligated to respond to the claim | insurer, insurance company, company, provider |
| **Policy** | The insurance contract defining coverage, limits, and exclusions | contract (inaccurate — policy is more specific) |
| **Date of Loss** | The specific date when the damaging event occurred | loss date, incident date, storm date |
| **Proof of Loss** | A sworn statement documenting the amount of loss | POL (acronym only after first use) |
| **Scope of Work** | The complete list of repairs/replacement needed | scope, work order, repair list |
| **Estimate** | A detailed calculation of repair/replacement costs | quote, bid, pricing |
| **Supplement** | A request for additional scope/cost beyond the initial estimate | addendum, additional work |
| **Valuation** | The process of determining the dollar amount of loss | value, amount, price |
| **Actual Cash Value** | Replacement cost minus depreciation | ACV (acronym only after first use) |
| **Replacement Cost Value** | The cost to repair/replace with like kind and quality | RCV (acronym only after first use) |
| **Depreciation** | Reduction in value due to age, wear, or obsolescence | holdback, depreciation holdback |
| **Deductible** | The amount the insured pays before coverage applies | out-of-pocket, insured's portion |
| **Coverage Limit** | The maximum amount the carrier will pay for a covered loss | policy limit, max payout |
| **Exclusion** | A specific cause of loss or condition not covered by the policy | non-covered, exception |
| **Endorsement** | A modification to the standard policy terms | rider, add-on, amendment |
| **Reservation of Rights** | Carrier's notice that coverage may be denied | ROR (acronym only after first use) |
| **Denial** | A carrier's refusal to pay all or part of a claim | rejection, decline |
| **Partial Denial** | A carrier's refusal to pay specific items while accepting others | partial rejection, item denial |

---

## People & Roles

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Public Adjuster** | A licensed professional who represents the insured in the claims process | adjuster (ambiguous — could mean carrier adjuster), PA (acronym only after first use) |
| **Carrier Adjuster** | An employee or contractor of the insurance company who evaluates claims | insurance adjuster, company adjuster, their adjuster |
| **Independent Adjuster** | A third-party contractor hired by the carrier to evaluate claims | IA (acronym only after first use) |
| **Staff Adjuster** | A carrier employee who handles claims | inside adjuster, company adjuster |
| **Appraiser** | A neutral party who determines the amount of loss in an appraisal process | umpire (different role), valuation expert |
| **Umpire** | An arbitrator selected when appraisers disagree on the amount of loss | arbitrator (similar but distinct) |
| **Insured** | The policyholder — the person or entity who purchased the insurance | client, customer, homeowner, property owner |
| **Mortgagee** | The lender with a financial interest in the insured property | bank, lender, mortgage company |
| **Contractor** | A construction professional who performs repairs/replacement | builder, repairman, roofer (too narrow) |
| **Restoration Company** | A contractor specializing in property damage repair/mitigation | mitigation company, water guys |
| **Engineer** | A licensed professional engineer retained for expert opinions | PE, structural engineer (only if structural) |
| **Attorney** | A lawyer representing the insured in litigation | lawyer, counsel |

---

## Damage & Inspection

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Inspection** | A thorough examination of the damaged property | walkthrough, survey, look-see |
| **Photos** | Visual documentation of damage and conditions | pictures, images, snaps |
| **Evidence** | Any material supporting the claim (photos, reports, samples) | proof (too broad), documentation (too broad) |
| **Hail Damage** | Damage caused by hailstones impacting the property | storm damage (too broad) |
| **Wind Damage** | Damage caused by wind forces on the property | storm damage (too broad) |
| **Water Damage** | Damage caused by water intrusion | moisture damage, leak damage |
| **Fire Damage** | Damage caused by fire, smoke, or fire suppression | smoke damage (only if smoke-specific) |
| **Roof Covering** | The outermost weatherproof layer of the roof | shingles (too specific), roof material |
| **Underlayment** | The protective layer between the deck and roof covering | felt, paper, underlay |
| **Roof Deck** | The structural surface to which the roof covering is attached | sheathing, plywood, substrate |
| **Flashing** | Metal or other material used to prevent water penetration at joints | metal strips, drip edge (too specific) |
| **Siding** | The exterior protective material on walls | cladding, wall covering |
| **Gutter** | A channel for collecting and directing roof runoff | eave trough |
| **Downspout** | A vertical pipe carrying water from gutter to ground | leader, drain pipe |
| **Soffit** | The underside of the roof overhang | eave soffit |
| **Fascia** | The vertical board at the edge of the roof overhang | fascia board |
| **Drip Edge** | A metal flashing directing water into the gutter | edge metal |
| **Valley** | The internal angle formed where two roof slopes meet | roof valley (redundant) |
| **Ridge** | The horizontal line where two roof slopes meet at the top | roof ridge (redundant), peak |
| **Hip** | The external angle formed where two roof slopes meet | — |
| **Eave** | The lower edge of the roof that overhangs the wall | roof edge |

---

## Building Codes & Compliance

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Code Upgrade** | Work required by current building codes but not by the pre-loss condition | code compliance (less precise), ordinance upgrade |
| **Ordinance or Law Coverage** | Policy coverage for code upgrade costs | O&L (acronym only after first use), ordinance coverage |
| **Building Code** | Regulations governing construction standards | code (ambiguous without context) |
| **IRC** | International Residential Code — applies to 1- and 2-family dwellings | residential code |
| **IBC** | International Building Code — applies to commercial structures | commercial code |
| **IECC** | International Energy Conservation Code | energy code |
| **Permit** | Official authorization from a building department to perform work | building permit, work permit |
| **Plan Review** | Building department evaluation of construction plans | review, plan check |
| **Inspection (Code)** | Building department verification of work compliance | city inspection, municipal inspection |
| **Certificate of Occupancy** | Document certifying a building is safe to occupy | CO, occupancy permit |
| **Setback** | Minimum distance a structure must be from property lines | — |
| **Easement** | A right to use another's property for a specific purpose | — |

---

## Carrier Communications

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Letter of Representation** | Formal notice that a public adjuster represents the insured | LOR (acronym only after first use), letter of auth |
| **Assignment of Benefits** | Transfer of insurance claim rights to a third party | AOB (acronym only after first use), transfer, handoff |
| **Fee Agreement** | Contract between the insured and public adjuster defining compensation | retainer, contract |
| **Demand Letter** | Formal request for payment with supporting arguments | request letter, payment demand |
| **Rebuttal** | Response to a carrier's objection or denial | response, counter-argument |
| **Appraisal Clause** | Policy provision allowing neutral determination of loss amount | appraisal provision |
| **Bad Faith** | Carrier's unreasonable denial or delay of a valid claim | unfair claim practice, unreasonable denial |
| **Reservation of Rights** | Carrier notice that coverage may be denied pending investigation | ROR (acronym only after first use) |
| **Notice of Intent** | Formal notification before filing a lawsuit or complaint | NOI (acronym only after first use) |
| **Statute of Limitations** | Time limit for filing a lawsuit | SOL (acronym only after first use), deadline |
| **Depreciation Schedule** | Table showing how depreciation is calculated by age and condition | — |
| **Cash-Up-Front** | Payment of RCV without holdback for depreciation | non-recoverable depreciation, upfront payment |

---

## Documentation & Reports

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Report** | A formal document presenting findings and conclusions | write-up, summary |
| **Exhibit** | A document or object introduced as evidence | attachment, appendix |
| **Proof Pack** | A compiled package of evidence supporting the claim | evidence packet, support package |
| **CompanyCam Report** | A structured inspection report using CompanyCam photo documentation | photo report |
| **Narrative** | The written explanation of damage, cause, and scope | description, story |
| **Line Item** | A single entry in an estimate with quantity, unit, and price | item, entry |
| **Unit Price** | The cost per unit of measurement for a line item | rate, cost |
| **Quantity** | The amount of work/material for a line item | count, number |
| **Overhead and Profit** | Contractor overhead (10%) and profit (10%) added to trades | O&P (acronym only after first use), 10&10 |
| **Material Sales Tax** | Tax applied to materials (varies by jurisdiction) | sales tax, tax |
| **Dumpster/Debris** | Cost for waste removal from the work site | debris removal, waste |
| **Mobilization** | Cost for contractor to arrive and set up at the site | travel, trip charge |

---

## Xactimate & Estimating

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Xactimate** | The industry-standard estimating software | XM8, the estimating program |
| **Sketch** | The diagram/floor plan drawn in Xactimate | drawing, diagram |
| **Line Item** | An individual component of the estimate | item, entry |
| **Category** | The broad classification of a line item (e.g., RFG = Roofing) | — |
| **Selector** | The specific type within a category | — |
| **Price List** | The database of material and labor costs for a specific region | price file, cost list |
| **Labor Minimum** | The minimum charge for a labor operation | minimum labor |
| **Waste Factor** | Additional material percentage to account for cutting and fitting | waste, overage |
| **Remove** | The cost to demolish and dispose of existing material | demo, tear-off, R&R (remove and replace) |
| **Replace** | The cost to install new material | install, set |
| **Detach and Reset** | Remove, preserve, and reinstall existing material | D&R, save and reuse |
| **F9 Note** | A note attached to a specific line item in Xactimate | line note, item note |
| **Coverage/Loss** | The summary section showing total damages by coverage | — |

---

## Weather & Meteorology

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Date of Loss** | The specific date of the damaging weather event | loss date, storm date |
| **Hail Swath** | The geographic area affected by hail | hail path, storm track |
| **Wind Gust** | A brief increase in wind speed above the sustained wind | gust (alone) |
| **Sustained Wind** | The average wind speed over a specified period | average wind |
| **Hail Size** | Diameter of hailstones, typically measured in inches | — |
| **NOAA** | National Oceanic and Atmospheric Administration | weather service |
| **NWS** | National Weather Service | — |
| **Storm Report** | Official NWS documentation of severe weather | severe weather report |
| **Radar Data** | Doppler radar imagery showing precipitation intensity | — |
| **Hail Report** | Documentation of hail size, location, and time | hail verification |
| **Wind Report** | Documentation of measured wind speeds | wind verification |

---

## AI OS Infrastructure

| Term | Definition | Aliases to Avoid |
|------|-----------|------------------|
| **Skill** | A specialized AI capability with defined triggers and outputs | module, plugin, function |
| **Command Council** | The governance structure of 22 AI agent roles | council, agents |
| **Golden Path** | The standard 8-stage claim workflow | workflow, process |
| **Pillar** | One of 12 functional domains in the ClaimEdge architecture | domain, category |
| **Human Review Gate** | A checkpoint requiring human approval before output | review gate, signoff |
| **Risk Level** | Classification of output risk (Low/Medium/High) | risk, severity |
| **Migration** | Moving a skill from Huuso to ClaimEdge branding | transfer, move |
| **Rebrand** | Updating skill content to use ClaimEdge terminology | rename, update |
| **Archive** | Moving a deprecated skill to storage | retire, delete |
| **Seed Data** | Initial data loaded into a database | initial data, starter data |
| **Trigger** | The condition that activates a skill | activation, condition |
| **Session** | A single continuous interaction with an AI | thread, conversation |

---

## Relationships

- A **Claim** belongs to exactly one **Insured**
- A **Claim** may have multiple **Policies** (if multiple structures)
- An **Insured** may have multiple **Claims** over time
- A **Claim** progresses through the **Golden Path** stages
- Each **Golden Path** stage maps to one or more **Pillars**
- Each **Pillar** contains one or more **Skills**
- Each **Skill** has one **Lifecycle State**
- A **Public Adjuster** represents the **Insured**, not the **Carrier**
- A **Carrier Adjuster** represents the **Carrier**
- An **Estimate** contains many **Line Items**
- A **Scope of Work** is derived from the **Inspection** findings
- **Code Upgrades** are triggered by **Building Code** requirements, not damage

---

## Example Dialogue

> **Dev:** "When an **Insured** files a **Claim**, does the **Public Adjuster** create the **Fee Agreement** before or after the **Inspection**?"
>
> **Domain Expert:** "Before — the **Fee Agreement** and **Letter of Representation** are signed at **Intake**, before any **Inspection** occurs. The **Public Adjuster** cannot act on behalf of the **Insured** without a signed **LOR**."
>
> **Dev:** "So the **Insured** is technically a **client** of the **Public Adjuster**, but we never use the word 'client' in external documents?"
>
> **Domain Expert:** "Correct. In all external communications — especially to the **Carrier** — we refer to them as the **Insured**. The term **Insured** establishes their rights under the **Policy**. 'Client' has no legal meaning in the claims process."
>
> **Dev:** "What about when we're discussing the **Scope of Work** with a **Contractor**?"
>
> **Domain Expert:** "With **Contractors**, we use **Estimate** and **Line Item** terminology. The **Scope of Work** becomes the **Estimate** in Xactimate. Each repair task is a **Line Item** with **Quantity**, **Unit Price**, and **Description**."
>
> **Dev:** "And **Code Upgrades** are separate **Line Items** in the **Estimate**?"
>
> **Domain Expert:** "Yes — **Code Upgrades** are distinct from damage-related **Line Items**. They're labeled with the specific **Building Code** reference, like 'IRC R905.1 — Ice Barrier'. This makes them defensible when the **Carrier** questions them."

---

## Flagged Ambiguities

1. **"Adjuster" alone is ambiguous.** Always specify: **Public Adjuster**, **Carrier Adjuster**, **Independent Adjuster**, or **Staff Adjuster**.

2. **"Storm damage" is too vague.** Always specify the peril: **Hail Damage**, **Wind Damage**, **Water Damage**, or **Fire Damage**.

3. **"Code compliance" vs "Code Upgrade."** Use **Code Upgrade** when referring to work required by current codes that exceeds the pre-loss condition. Use **Code Compliance** only when referring to the general state of meeting code requirements.

4. **"Client" vs "Insured."** Never use **client** in external documents. Use **Insured** for all carrier-facing and legal communications. **Client** is acceptable only in informal internal discussions.

5. **"Documentation" is overloaded.** Use specific terms: **Photos** for images, **Evidence** for supporting materials, **Report** for formal findings, **Exhibit** for claim attachments.

---

## Banned Terms Registry

These terms are PROHIBITED in all ClaimEdge AI-generated output:

| Banned Term | Reason | Use Instead |
|-------------|--------|-------------|
| "client" (external) | No legal standing in claims | **Insured** |
| "insurance company" | Redundant, verbose | **Carrier** |
| "storm damage" (alone) | Too vague, unspecified peril | **Hail Damage** / **Wind Damage** etc. |
| "pictures" | Unprofessional | **Photos** |
| "bid" | Suggests competitive pricing | **Estimate** |
| "quote" | Not a binding document | **Estimate** |
| "adjuster" (alone) | Ambiguous — which type? | **Public Adjuster** / **Carrier Adjuster** |
| "walkthrough" | Casual, unprofessional | **Inspection** |
| "their adjuster" | Vague, adversarial tone | **Carrier Adjuster** |
| "scope" (alone) | Abbreviated, unclear | **Scope of Work** |
| "holdback" | Carrier terminology | **Depreciation** |
| "provider" | Healthcare term | **Carrier** |
| "value" (alone) | Ambiguous — ACV? RCV? market? | **Actual Cash Value** / **Replacement Cost Value** |

---

*End of ClaimEdge Ubiquitous Language Glossary v1.0*
