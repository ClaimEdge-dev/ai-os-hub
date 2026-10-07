-- Rapid Roadside Repair approved public truth projection
-- PREPARED / NOT APPLIED

create or replace view public.rrr_public_business_truth
with (security_invoker = true)
as
select truth_key, value_text, effective_at, review_at
from public.rrr_business_truth
where public_enabled = true
  and state in ('VERIFIED','OWNER_APPROVED');

create or replace view public.rrr_public_services
with (security_invoker = true)
as
select service_code, family, public_label, internal_description, asset_classes, delivery_mode, urgency_mode
from public.rrr_service_capabilities
where public_enabled = true
  and owner_approved = true
  and state in ('VERIFIED','OWNER_APPROVED');

grant select on public.rrr_public_business_truth to anon, authenticated;
grant select on public.rrr_public_services to anon, authenticated;
