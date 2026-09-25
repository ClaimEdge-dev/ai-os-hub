---
name: proactive-build-ahead
description: >
  Detects predictable downstream needs while DEBO or any specialist is working and automatically
  builds low-risk internal skeletons before Bobby has to ask. Use when a dependency, missing register,
  future artifact, repeated workflow, schema, checklist, template, folder, test, prompt, or handoff
  will obviously be needed next.
---

# DEBO Proactive Build-Ahead v1.0

## Mission

Anticipate useful next infrastructure without creating uncontrolled scope.

When an agent finds something we are very likely to need:
do not merely leave a note.
Build the safe internal skeleton now.

## Decision rule

### AUTO-BUILD
Proceed automatically when ALL are true:
- internal/private
- reversible
- no money spent
- no external message sent
- no public publishing
- no account/permission ownership change
- no destructive overwrite/delete
- does not invent facts
- does not duplicate an existing canonical object
- clearly supports the active objective or a near-certain dependency

Examples:
- empty folder structure
- register schema
- checklist
- form template
- draft prompt
- API/interface schema
- test harness
- readme
- manifest
- handoff packet shell
- approval packet shell
- spreadsheet headings
- Notion subpage skeleton
- GitHub docs/code scaffold
- Kimi Skill skeleton

### BUILD-SKELETON-ONLY
If useful but facts/approval are missing:
create structure + placeholders + explicit UNKNOWN fields.

### APPROVAL-QUEUE
Do not execute, only prepare, when action would:
- send email/SMS/DM
- publish
- launch ad spend
- sign/submit legal material
- change passwords/access
- purchase
- delete/overwrite important data
- bind the user/business contractually
- represent an unverified fact externally

## Anticipation scan

After every substantial task, silently ask:

1. What will this output depend on next?
2. What will Bobby probably ask for after seeing this?
3. Is there a reusable schema/template/Skill missing?
4. Will another project need the same generic layer?
5. Is there an obvious QA/test/checklist we have not created?
6. Will this create a future handoff problem?
7. Is there a predictable external approval we should package now?

If yes, create the smallest safe useful skeleton.

## Scope brake

Do not build ahead when:
- relevance confidence is below 70%;
- it adds a new business/domain unrelated to active work;
- maintenance burden exceeds likely reuse;
- it requires facts that are unknown;
- a canonical artifact already exists;
- it causes the active objective to be abandoned.

Classify discoveries as:
BUILD_NOW
SKELETON_NOW
PARK
APPROVAL_REQUIRED
REJECT_DUPLICATE

## Task Delta integration

Every proactive build creates a Task Delta:

DELTA_ID
DISCOVERED_DURING
WHY_NEEDED
CLASSIFICATION
ARTIFACT_CREATED
DEPENDENCIES
OWNER
STATUS
RETURN_POINT

After creation, resume the original active objective automatically.

## Build-ahead quality gate

A proactive skeleton must:
- be clearly named
- have purpose
- have owner
- show missing facts
- link to parent project
- avoid sensitive data unless required
- be easy to delete/supersede
- not claim completion
