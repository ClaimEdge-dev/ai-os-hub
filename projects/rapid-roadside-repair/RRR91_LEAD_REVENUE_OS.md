# RRR 91 — Lead Engine, Revenue Tracking & Go-Live OS

Status: **ACTIVE / PRIVATE TRACKING BUILD**  
Recovered: 2026-10-19

## Current public state

- Higgsfield production URL: `https://rapid-roadside-repair-il.higgsfield.app`
- Higgsfield D1 tables: `service_requests`, `request_updates`, `fleet_leads`
- Recovered live counts: 0 service requests, 0 updates, 0 fleet leads
- `robots.txt` currently blocks all crawling with `Disallow: /`
- Sitemap and 404 routes exist
- Paid marketing remains HOLD until attribution works

## Canonical money lineage

Traffic  
→ Source  
→ Lead  
→ Service Request  
→ Dispatch  
→ Job  
→ Authorization  
→ Invoice  
→ Payment  
→ Collected Revenue  
→ Gross Profit  
→ Bobby Commission  
→ Review  
→ Repeat / Fleet Revenue

## Recovery working copy

Google Sheet:
`RRR — Operations CRM — Recovery Working Copy 2026-10-19`

Tracking tabs:

- 38 Lead Attribution
- 39 Marketing Spend
- 40 Bobby Commission
- 41 Fleet Sales Pipeline
- 42 Referral Partners
- 43 Repeat & Review
- 44 Go-Live Checklist
- 45 Revenue Dashboard
- 46 Daily Money Command
- 47 RRR91 Recovery Architecture

The original RRR CRM remains preserved as the source workbook for the existing review-staging sync.

## Website attribution

Higgsfield repo migration:

`app/migrations/0002_attribution.sql`

Prepared fields:
- UTM source / medium / campaign / term / content
- landing page
- referrer
- device type
- visitor ID
- session ID
- append-only attribution events

Status: **pushed to repo / not deployed**

Reason: deploying changes the live public site and is release-gated.

## Operations backend

Prepared migrations:

- `backend-v1/013_lead_revenue_tracking.sql`
- `backend-v1/014_lead_revenue_tracking_test.sql`

013 adds:
- attribution events
- marketing spend
- operator commissions
- fleet sales pipeline
- referral partners
- followups

014 is a rollback-only synthetic test.

Status: **prepared / not applied**

## Compensation controls

The tracker supports:
- collected-revenue percentage
- gross-profit percentage
- gross-invoice percentage
- flat lead
- flat job
- monthly management
- fleet origination

No tracker row or schema creates a compensation agreement.

Default reconciliation recommendation until written terms say otherwise:
**COLLECTED REVENUE**

## Go-live P0

1. Controlled live Request Service / tracking / fleet-intake test
2. Business identity / phone / email / service-area truth
3. Privacy policy + disclosures
4. UTM/event tracking deployment
5. Analytics selection
6. Source → CRM → job → payment lineage
7. Staff authentication
8. Secure evidence upload
9. Official rate authority
10. Payment processor
11. Google Business Profile + review link
12. Billy/Bobby compensation agreement
13. Spam / abuse protection
14. Custom domain + Search Console
15. Remove crawl block only when release gates are complete

## Governance

Do not:
- start ad spend without approval
- send fleet/referral outreach without approval
- publish benchmark prices as official
- claim credentials without evidence
- calculate owed commission before a written rule is adopted
- apply production DB migrations without the release gate
- enable search crawling before launch controls are ready
