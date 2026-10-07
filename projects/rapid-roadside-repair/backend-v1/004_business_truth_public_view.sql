-- Rapid Roadside Repair approved public truth projection
-- PREPARED / NOT APPLIED
-- Security-definer functions expose only explicitly approved/public-enabled fields.

create or replace function public.rrr_get_public_business_truth()
returns table (
  truth_key text,
  value_text text,
  effective_at timestamptz,
  review_at timestamptz
)
language sql
stable
security definer
set search_path = public
as $$
  select b.truth_key, b.value_text, b.effective_at, b.review_at
  from public.rrr_business_truth b
  where b.public_enabled = true
    and b.state in ('VERIFIED','OWNER_APPROVED');
$$;

create or replace function public.rrr_get_public_services()
returns table (
  service_code text,
  family text,
  public_label text,
  internal_description text,
  asset_classes text[],
  delivery_mode text,
  urgency_mode text
)
language sql
stable
security definer
set search_path = public
as $$
  select s.service_code, s.family, s.public_label, s.internal_description,
         s.asset_classes, s.delivery_mode, s.urgency_mode
  from public.rrr_service_capabilities s
  where s.public_enabled = true
    and s.owner_approved = true
    and s.state in ('VERIFIED','OWNER_APPROVED');
$$;

revoke all on function public.rrr_get_public_business_truth() from public;
revoke all on function public.rrr_get_public_services() from public;
grant execute on function public.rrr_get_public_business_truth() to anon, authenticated;
grant execute on function public.rrr_get_public_services() to anon, authenticated;
