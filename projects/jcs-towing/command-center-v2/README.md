# JC's Towing Command Center V2

**State:** PRIVATE BUILD / REVIEW ONLY  
**Production domain:** NOT CHANGED  
**Branch:** `jct-command-center-v2`

This is the recover-before-rebuild successor to `projects/jcs-towing/site-v1`.

## Surfaces
- `index.html` — public conversion website
- `staff.html` — private employee CRM / dispatch portal
- `supabase-schema.sql` — database + role/RLS starter migration

## Verified working facts used
- JC's Towing
- Lockport, Illinois
- (815) 474-7384
- jcstowinginc.com

Everything else that can change a public claim (hours, service cities, fleet/capabilities, rates, licenses, review count, legal entity/address) is intentionally configurable or held back.

## Brand
- JC Red: #E10600
- Black: #000000
- White: #FFFFFF
- Silver: #D1D5DB
- Dark Gray: #3A3A3A

The exact approved logo is wired through a single `.brand-logo` image/component path so it can be replaced once without redesigning the site.

## CRM modules
Dashboard, Leads, Dispatch, Customers/Vehicles, Fleet/Operators, Billing Drafts, Commercial Accounts, Evidence, Review Follow-up, Municipal Opportunities, Reports, Settings.

## Backend
The front end is Supabase-ready. Do **not** connect it to an unrelated existing database. Create/connect a dedicated JC's Towing Supabase project, apply `supabase-schema.sql`, then set `window.JCT_CONFIG` in `config.js`.

Do not place a Supabase service-role key in browser code.

## Deployment gate
A Vercel Preview may be created for review only after a dedicated backend is connected and the staff routes are tested. Production/domain release still requires explicit approval.
