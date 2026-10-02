---
name: rrr-business-truth-auditor
description: Verify and govern Rapid Roadside Repair business truth before downstream use.
---
# RRR Business Truth Auditor

Track each material business fact as VERIFIED, RECOVERED-PENDING-OWNER, CONFLICT, or TBD.

Required truth domains:
legal/public name; owner authority; phone/email/domain; hours; services; equipment/capabilities; territory; pricing authority; payment terms; licenses/insurance/certifications; networks; towing-vs-repair boundary; branding; review/contact links.

Do not treat recovered conversation facts as owner-approved public claims.
Output: truth register delta, conflicts, owner questions, downstream blocks.
