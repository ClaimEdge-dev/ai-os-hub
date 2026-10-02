---
name: rrr-crm-lead-account
description: Define and govern Rapid Roadside Repair lead, customer, commercial-account and job CRM records.
---
# RRR CRM Lead & Account

Core objects:
lead; contact; customer/account; vehicle/unit; job; quote; invoice reference; follow-up; source; outcome.

Use stable IDs and dedupe before create.
Do not auto-send messages or create production CRM records unless the workflow and approval are explicit.
Separate prospect facts from assumptions.
Output: normalized CRM record/dry-run mapping + dedupe result + next action.
