---
name: jct-crm-data-model
description: Define and govern JC's Towing CRM objects, fields, relationships, statuses and source-of-truth rules across calls, customers, vehicles, jobs, invoices, accounts and evidence.
---
# JCT CRM Data Model
Core objects: Contact, Customer, Commercial Account, Call/Lead, Dispatch, Vehicle/Unit, Tow Job, Evidence, Rate Source, Quote, Invoice, Payment, Storage, Vendor, Municipal Opportunity and Approval. Use stable IDs and explicit relationships. Preserve source timestamps. Never overwrite verified evidence with inferred CRM values.
