-- Rapid Roadside Repair evidence-upload ticket architecture
-- PREPARED / NOT APPLIED
-- Creates server-side authorization records only. It does not grant anonymous bucket access.

create table if not exists public.rrr_upload_tickets (
  id uuid primary key default gen_random_uuid(),
  service_request_id uuid references public.rrr_service_requests(id) on delete cascade,
  job_id uuid references public.rrr_jobs(id) on delete cascade,
  ticket_token uuid not null default gen_random_uuid() unique,
  purpose text not null default 'CUSTOMER_EVIDENCE',
  max_files integer not null default 6 check (max_files between 1 and 20),
  max_file_bytes bigint not null default 8388608,
  allowed_mime_types text[] not null default array['image/jpeg','image/png','image/webp'],
  expires_at timestamptz not null default (now() + interval '30 minutes'),
  consumed boolean not null default false,
  created_at timestamptz not null default now(),
  notes text
);

alter table public.rrr_upload_tickets enable row level security;

drop policy if exists rrr_staff_all on public.rrr_upload_tickets;
create policy rrr_staff_all on public.rrr_upload_tickets
for all to authenticated using (public.rrr_is_staff()) with check (public.rrr_is_staff());

revoke all on public.rrr_upload_tickets from anon;

-- Production implementation should exchange a valid ticket for a time-limited signed
-- upload URL using trusted server-side code. Do not expose a service-role key to browsers.
