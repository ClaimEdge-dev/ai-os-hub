-- Rapid Roadside Repair safe customer-status lookup
-- PREPARED / NOT APPLIED
-- A random public status token must be issued from a trusted workflow.

alter table public.rrr_service_requests
  add column if not exists public_status_token uuid default gen_random_uuid() unique;

create or replace function public.rrr_get_request_status(token uuid)
returns jsonb
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  r record;
  updates jsonb;
begin
  select
    sr.id, sr.request_number, sr.status, sr.problem_category, sr.asset_type,
    sr.created_at, sr.updated_at
  into r
  from public.rrr_service_requests sr
  where sr.public_status_token = token;

  if r.id is null then
    return jsonb_build_object('found',false);
  end if;

  select coalesce(jsonb_agg(jsonb_build_object(
    'created_at',u.created_at,
    'status',u.status_label,
    'title',u.title,
    'message',u.message
  ) order by u.created_at), '[]'::jsonb)
  into updates
  from public.rrr_customer_updates u
  where u.service_request_id = r.id
    and u.audience = 'customer';

  return jsonb_build_object(
    'found',true,
    'request_number',r.request_number,
    'status',r.status,
    'problem_category',r.problem_category,
    'asset_type',r.asset_type,
    'created_at',r.created_at,
    'updated_at',r.updated_at,
    'updates',updates
  );
end;
$$;

revoke all on function public.rrr_get_request_status(uuid) from public;
grant execute on function public.rrr_get_request_status(uuid) to anon, authenticated;
