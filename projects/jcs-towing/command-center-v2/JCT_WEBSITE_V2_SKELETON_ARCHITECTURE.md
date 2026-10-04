# JCT Website V2 — Full Skeleton Architecture

Status: **STAGED / NOT LIVE**
Branch: `jct-website-v2-skeleton`

This is the implementation skeleton for the current JC's Command Center. It is not a second website. It is the staging plan for the existing Lovable project.

## Public route skeleton

Existing:
- `/`
- `/services`
- `/service-area`
- `/commercial`
- `/reviews`
- `/about`
- `/contact`

Stage for addition:
- `/services/towing`
- `/services/[verified-service-slug]`
- `/emergency-towing`
- `/commercial/inquiry`
- `/insurance-towing`
- `/body-shops`
- `/dealerships`
- `/municipal`
- `/resources`
- `/resources/accident-checklist`
- `/resources/breakdown-checklist`
- `/privacy`
- `/accessibility`
- branded `404`

Truth-gated routes, do not activate until verified:
- `/heavy-duty-towing`
- `/semi-towing`
- `/recovery`
- `/roadside-assistance`
- `/fleet`
- `/property-management`
- `/trucking-companies`
- `/careers`
- city/service SEO routes

## Public component skeleton

### Emergency / conversion
- `MobileCallBar`
- `CallNowButton`
- `RequestServiceButton`
- `GetMyLocationButton`
- `DispatchPrepPanel`
- `VehicleConditionFields`
- `PhotoUploadField`
- `ServiceSelector`
- `RequestDisclaimer`
- `FormRecoveryState`

### Trust / proof
- `VerifiedTrustStrip`
- `ApprovedReviewCard`
- `ReviewEmptyState`
- `WorkGallery`
- `GalleryFilter`
- `EquipmentProofCard`
- `BusinessTruthBadge` (internal only, never public)

### Services / local SEO
- `ServicePageTemplate`
- `ServiceFAQ`
- `ServiceAreaList`
- `VerifiedAreaMap`
- `CityPageTemplate`
- `Breadcrumbs`
- `StructuredData`

### B2B
- `CommercialInquiryForm`
- `FleetNeedsFields`
- `BusinessTypeSelector`
- `CommercialCTA`

### Legal / safety
- `PrivacyNotice`
- `AccessibilityContact`
- `ServiceRequestTerms`

## Staff route skeleton

Existing staff surface should be expanded, not replaced:

- `/staff/settings/business-truth`
- `/staff/customers`
- `/staff/vehicles`
- `/staff/evidence`
- `/staff/reviews`
- `/staff/reports`
- `/staff/approvals`
- `/staff/analytics`
- `/staff/marketing`
- `/staff/calls`
- `/staff/tow-tickets`

Future:
- `/staff/automations`
- `/staff/ai-assist`
- `/staff/commercial-portal-admin`

## Business Truth fields to add/complete

Public basics:
- logo_url
- tagline (optional, owner-approved only)
- hours
- show_hours
- service_areas[]
- review_url
- about
- email
- public_address_mode
- public_address
- sms_enabled
- directions_enabled

Service toggles:
- towing
- roadside
- transport
- commercial
- recovery
- heavy_duty
- semi
- insurance_towing
- property_towing

Capability proof references:
- verified_fleet_units[]
- verified_equipment[]
- verified_certifications[]
- verified_review_source
- approved_marketing_media[]

Never infer a public capability from a photo alone.

## Lead / request-service fields

Existing fields stay compatible.

Stage additions:
- source_page
- referrer
- utm_source
- utm_medium
- utm_campaign
- utm_content
- device_type
- geolocation_lat (optional, consent-based)
- geolocation_lng (optional, consent-based)
- location_accuracy_m
- rolls
- steers
- shifts
- keys_available
- accident
- wheel_damage
- clearance_issue
- access_notes
- evidence_upload_ids[]
- preferred_contact_method
- commercial_company
- commercial_vehicle_type
- commercial_frequency

## Evidence upload skeleton

Public lead upload:
- private storage only
- signed/expiring access URLs
- no public bucket
- validate MIME type
- validate size
- strip unsafe filenames
- tie file to lead ID
- preserve original upload time
- no AI inference written back as verified fact

Staff evidence:
- lead/job/customer linkage
- category
- caption
- marketing_approved boolean
- privacy/sensitivity tag
- source timestamp

## Analytics event skeleton

Public:
- page_view
- call_click
- request_service_click
- request_form_start
- request_form_error
- request_form_submit
- request_form_success
- get_location_click
- geolocation_granted
- geolocation_denied
- photo_upload_start
- photo_upload_success
- service_selected
- commercial_inquiry_click
- review_click
- directions_click

CRM:
- lead_created
- lead_contacted
- lead_dispatch_pending
- job_created
- job_completed
- lead_lost
- review_followup_created

Never claim a call click equals a completed job.

## Feature-gating rules

1. Public service navigation reads Business Truth.
2. Disabled service = no marketing claim.
3. Truth-gated page may exist in code but should not be linked/indexed.
4. Review schema requires verified review content.
5. LocalBusiness/TowingService schema reads the same Business Truth as visible content.
6. City page only activates when city is verified.
7. Heavy/semi/recovery/equipment pages require verified capability evidence.
8. No price/rate schema or price copy without approved rate authority.

## Security skeleton

- RLS remains mandatory.
- No service-role key in browser.
- Public forms write through narrow server function.
- Public uploads go to private storage.
- Staff routes require authenticated role.
- External messaging defaults to draft/manual approval.
- Audit material mutations.
- Rate limit public form endpoints.
- Honeypot first; CAPTCHA only if spam requires it.

## Accessibility / performance skeleton

- WCAG 2.2 AA target
- keyboard navigation
- focus visibility
- semantic headings/landmarks
- form labels and error summaries
- aria-live for success/error
- reduced motion
- minimum 44px tap targets
- responsive images
- no heavy animation framework required
- no autoplay video
- Core Web Vitals monitoring

## Release rule

This branch is staging only.

Do not publish production until:
1. public facts are verified or hidden,
2. forms work,
3. mobile QA passes,
4. security/privacy checks pass,
5. analytics behavior is documented,
6. John/Bobby explicitly approves production release.
