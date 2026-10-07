-- Rapid Roadside Repair backend v1
-- Customer updates + authorization records
-- PREPARED / NOT APPLIED

create table if not exists public.rrr_customer_updates (
  id uuid primary key default gen_random_uuid(),
  service_request_id uuid references public.rrr_service_requests(id) on delete cascade,
  job_id uuid references public.rrr_jobs(id) on delete cascade,
  created_at timestamptz not null default now(),
  channel text not null default 'system',
  audience text not null default 'customer',
  status_label text,
  title text not null,
  message text not null,
  sent boolean not null default false,
  sent_at timestamptz,
  provider_ref text,
  notes text
);

create table if not exists public.rrr_authorizations (
  id uuid primary key default gen_random_uuid(),
  service_request_id uuid references public.rrr_service_requests(id) on delete cascade,
  job_id uuid references public.rrr_jobs(id) on delete cascade,
  created_at timestamptz not null default now(),
  authorization_type text not null default 'ADDITIONAL_WORK',
  requested_work text not null,
  amount_limit numeric(12,2),
  rate_source_id text,
  status text not null default 'PENDING',
  authorized_by text,
  decision_at timestamptz,
  decision_method text,
  evidence_ref text,
  public_token uuid not null default gen_random_uuid() unique,
  expires_at timestamptz,
  notes text
);

alter table public.rrr_customer_updates enable row level security;
alter table public.rrr_authorizations enable row level security;

drop policy if exists rrr_staff_all on public.rrr_customer_updates;
create policy rrr_staff_all on public.rrr_customer_updates
for all to authenticated
using (public.rrr_is_staff())
with check (public.rrr_is_staff());

drop policy if exists rrr_staff_all on public.rrr_authorizations;
create policy rrr_staff_all on public.rrr_authorizations
for all to authenticated
using (public.rrr_is_staff())
with check (public.rrr_is_staff());

revoke all on public.rrr_customer_updates from anon;
revoke all on public.rrr_authorizations from anon;
