-- Rapid Roadside Repair fleet portal + reviews + payment-link placeholders
-- PREPARED / NOT APPLIED

create table if not exists public.rrr_fleet_portal_members (
  id uuid primary key default gen_random_uuid(),
  fleet_account_id uuid not null references public.rrr_fleet_accounts(id) on delete cascade,
  user_id uuid not null,
  role text not null default 'viewer',
  active boolean not null default true,
  created_at timestamptz not null default now(),
  unique(fleet_account_id,user_id)
);

create table if not exists public.rrr_review_queue (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid references public.rrr_customers(id) on delete set null,
  job_id uuid references public.rrr_jobs(id) on delete set null,
  invoice_id uuid references public.rrr_invoices(id) on delete set null,
  created_at timestamptz not null default now(),
  eligibility text not null default 'HOLD',
  channel text,
  status text not null default 'HOLD',
  review_url text,
  sent boolean not null default false,
  sent_at timestamptz,
  notes text
);

create table if not exists public.rrr_payment_links (
  id uuid primary key default gen_random_uuid(),
  invoice_id uuid references public.rrr_invoices(id) on delete cascade,
  job_id uuid references public.rrr_jobs(id) on delete set null,
  provider text,
  provider_ref text,
  created_at timestamptz not null default now(),
  amount numeric(12,2) not null default 0,
  currency text not null default 'USD',
  status text not null default 'HOLD',
  public_url text,
  sent boolean not null default false,
  sent_at timestamptz,
  notes text
);

alter table public.rrr_fleet_portal_members enable row level security;
alter table public.rrr_review_queue enable row level security;
alter table public.rrr_payment_links enable row level security;

drop policy if exists rrr_staff_all on public.rrr_fleet_portal_members;
create policy rrr_staff_all on public.rrr_fleet_portal_members
for all to authenticated using (public.rrr_is_staff()) with check (public.rrr_is_staff());

drop policy if exists rrr_staff_all on public.rrr_review_queue;
create policy rrr_staff_all on public.rrr_review_queue
for all to authenticated using (public.rrr_is_staff()) with check (public.rrr_is_staff());

drop policy if exists rrr_staff_all on public.rrr_payment_links;
create policy rrr_staff_all on public.rrr_payment_links
for all to authenticated using (public.rrr_is_staff()) with check (public.rrr_is_staff());

revoke all on public.rrr_fleet_portal_members from anon;
revoke all on public.rrr_review_queue from anon;
revoke all on public.rrr_payment_links from anon;
