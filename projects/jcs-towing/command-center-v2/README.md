# JC's Towing Command Center v2 — Private Build

Project: DEBO — JC's Towing Command, Dispatch & Growth OS  
Project ID: JCT  
Status: PRIVATE PREVIEW / CURRENT SAFE BASELINE  
Lovable Project ID: 2a656371-38ce-4ada-a7bf-d3b651723ef4  
Lovable preview: https://id-preview--2a656371-38ce-4ada-a7bf-d3b651723ef4.lovable.app  
Current Lovable build commit: 999cdbeec6ff266d20aea6b79dadbd4b9ab42c68

## Recovered

This v2 build supersedes the old single-file Website V1 as the active development build. The old Website V1 remains preserved under `projects/jcs-towing/site-v1` and must not be deleted.

The 2026-10-04 website pass upgraded the existing Lovable project in place rather than creating a duplicate website.

## Current operating decision — 2026-10-04

Proceed with the facts currently verified in the project. Do not wait for more owner answers for private development.

For anything unresolved:
- hide it,
- disable it,
- or use neutral wording.

Do not expose public placeholders such as TBD / owner verification required.

This decision does **not** authorize production publishing or unsupported public claims.

## Current safe public baseline

Use:
- JC's Towing
- (815) 474-7384
- Lockport, Illinois
- jcstowinginc.com
- red / black / white / metallic silver / dark charcoal brand direction
- only services enabled by Business Truth
- only service areas present in Business Truth

Do not invent or imply:
- 24/7 service
- operating hours
- street address
- response times
- rates or pricing
- fleet size
- heavy/semi capability
- roadside services unless enabled
- commercial services unless enabled
- review counts, ratings, or testimonials
- licenses or certifications
- police / municipal relationships
- additional cities

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
- Commercial / Fleet, gated by Business Truth
- Reviews
- About
- Contact / Request Service
- Sitemap / robots

## Website V2 changes completed

- stronger mobile-first Call Now hierarchy
- improved Request Service secondary CTA
- "Have these details ready" dispatch-prep panel
- safer three-step service flow
- improved approved-service cards
- safer service-area wording
- commercial navigation/promotion gated by service settings
- honest reviews empty state
- request form grouping and no-guarantee notice
- unverified default slogan removed from public display
- improved metadata
- subtle CSS-based industrial motion/effects
- prefers-reduced-motion handling
- responsive QA across phone, tablet, and desktop widths
- staff routes preserved

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
- Public Request Service uses a restricted lead-insert path
- Audit log table present

## Current blocker

Lovable workspace is currently out of build credits.

The current Website V2 private preview and database remain preserved. No further Lovable edits can run until workspace credits are restored.

This is not a blocker to using the current private preview as the JCT WEBSITE V2 — CURRENT SAFE BASELINE.

## Remaining internal-only gaps

- approved logo image swap
- Customers / Vehicles full UI
- full Billing editor / print view
- Evidence library
- Reviews follow-up screen
- Reports
- Settings / Business Truth editor completion
- final full end-to-end release QA after future code changes

## Stack routing

- Lovable: active app builder / private preview
- Supabase/Lovable Cloud: one production-intent CRM database/auth source
- GitHub: checkpoint/source-control mirror and historical website preservation
- Vercel: future preview/deployment only after source mirror + QA + approval
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

## Live review surface — 2026-10-04

Current Website V2 visual verification site:
https://jcs-towing-v2-review.higgsfield.app

Use this link for fast visual review of Website V2 changes while the canonical production-intent source remains protected. This is a review deployment only: no jcstowinginc.com DNS/domain change, no production publish authorization, and no unsupported public claims.

Review-surface rule: unresolved business facts should be hidden or neutral rather than blocking design/development. Hard stops are reserved for production publishing, DNS/domain changes, spend, destructive actions, and unsupported public claims.

## Owner-approved elite public website scope — 2026-10-04

Bobby reported John approved the full public website direction and confirmed 24-hour / 7-day service.

Approved public website lanes now include:
- towing
- roadside assistance
- accident / recovery
- vehicle transport
- heavy-duty / semi
- commercial / fleet
- insurance towing
- property towing inquiries
- local + long-distance positioning

Business Truth in the existing Lovable/Supabase settings was updated to reflect those approved service toggles and 24-hour hours.

Current elite review deployment:
https://jcs-towing-v2-review.higgsfield.app

Higgsfield source commit: d248f97

Typecheck and production build passed before deployment.

Still data-driven, not invented: fleet count, operator count, exact equipment models, rates, response-time guarantees, live review metrics, customer logos and named commercial relationships.
