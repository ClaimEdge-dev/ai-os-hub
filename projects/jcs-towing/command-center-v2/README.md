# JC's Towing Command Center v2 — Private Build

Project: DEBO — JC's Towing Command, Dispatch & Growth OS  
Project ID: JCT  
Status: PRIVATE PREVIEW / WORKING BUILD  
Lovable Project ID: 2a656371-38ce-4ada-a7bf-d3b651723ef4  
Lovable preview: https://id-preview--2a656371-38ce-4ada-a7bf-d3b651723ef4.lovable.app

## Recovered

This v2 build supersedes the old single-file Website V1 as the active development build. The old Website V1 remains preserved under `projects/jcs-towing/site-v1` and must not be deleted.

## Architecture

- Public website + internal employee CRM in one app
- TanStack Start / React / TypeScript / Tailwind / shadcn
- Supabase-compatible Lovable Cloud backend
- Supabase Auth
- Postgres with RLS
- Drizzle schema/migrations
- Staff roles: admin, dispatcher, driver, office
- Private preview only
- No production domain changes

## Public pages

- Home
- Services
- Service Area
- Commercial / Fleet
- Reviews
- About
- Contact / Request Service
- Sitemap / robots

## Staff modules

- Dashboard
- Leads / Calls
- Dispatch / Jobs
- Customers / Vehicles
- Fleet / Operators
- Billing drafts
- Commercial accounts
- Evidence
- Review follow-up
- Municipal opportunities
- Reports
- Settings / Business Truth

## Database tables verified live

audit_log, commercial_accounts, customers, evidence_files, fleet_units,
invoice_line_items, invoices, job_status_history, jobs, leads, operators,
opportunities, profiles, review_followups, settings, user_roles, vehicles.

## Security

- RLS enabled in the generated CRM schema
- Admin / Dispatcher / Driver / Office role model
- Driver job access restricted to assigned operator jobs
- CRM data not exposed to anonymous users
- Public Request Service is intended to use a restricted lead-insert path
- Audit log table present

## Current blocker

Lovable workspace is out of build credits. The current code and database remain preserved, but the next completion/QA edit cannot run in Lovable until credits are restored.

Known incomplete UI discovered during QA:
- Settings / Business Truth still contains an in-progress placeholder in the current commit.
- A full placeholder sweep and end-to-end build/test pass is still required.

## Stack routing

- Lovable: active app builder / private preview
- Supabase/Lovable Cloud: one production-intent CRM database/auth source
- GitHub: checkpoint/source-control mirror and historical website preservation
- Vercel: preview deployment after source mirror + QA
- Mermaid: architecture documentation
- Neon: optional future analytics/branching layer only; do not create a second operational CRM database without a deliberate migration decision

## Approval gates

Do not:
- publish the production domain
- alter DNS
- launch ads
- send external customer messages
- invent rates/services/fleet/licenses/hours
- merge or delete the old Website V1
without explicit approval and verified business facts.
