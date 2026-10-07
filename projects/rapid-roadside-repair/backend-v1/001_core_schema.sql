-- Rapid Roadside Repair backend v1
-- PREPARED / NOT APPLIED
-- PostgreSQL / Supabase

create extension if not exists pgcrypto;

do $$ begin
  create type public.rrr_truth_state as enum ('VERIFIED','OWNER_APPROVED','OWNER_CONFIRM','SOURCE_SUPPORTED','CONFLICT','TBD','HOLD','SUPERSEDED');
exception when duplicate_object then null; end $$;

do $$ begin
  create type public.rrr_request_status as enum (
    'NEW','TRIAGE','AWAITING_INFO','CAPABILITY_CHECK','DISPATCH_READY','ASSIGNED','EN_ROUTE',
    'ON_SITE','DIAGNOSING','AWAITING_AUTHORIZATION','AWAITING_PARTS','REPAIR_IN_PROGRESS',
    'TESTING','COMPLETE','INVOICE_READY','INVOICED','PAID','FOLLOW_UP','CLOSED','CANCELLED','LOST'
  );
exception when duplicate_object then null; end $$;

create table if not exists public.rrr_business_truth (
  id uuid primary key default gen_random_uuid(),
  truth_key text not null unique,
  value_text text,
  state public.rrr_truth_state not null default 'TBD',
  source_type text,
  source_ref text,
  owner_approved_by text,
  owner_approved_at timestamptz,
  effective_at timestamptz,
  review_at timestamptz,
  public_enabled boolean not null default false,
  propagation_notes text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_service_capabilities (
  id uuid primary key default gen_random_uuid(),
  service_code text not null unique,
  family text not null,
  public_label text not null,
  internal_description text,
  asset_classes text[] not null default '{}',
  delivery_mode text,
  urgency_mode text,
  required_tools text,
  credential_needed text,
  owner_approved boolean not null default false,
  public_enabled boolean not null default false,
  state public.rrr_truth_state not null default 'OWNER_CONFIRM',
  source_ref text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_leads (
  id uuid primary key default gen_random_uuid(),
  lead_number bigint generated always as identity unique,
  created_at timestamptz not null default now(),
  source text not null default 'website',
  source_page text,
  referrer text,
  utm_source text,
  utm_medium text,
  utm_campaign text,
  utm_content text,
  device_type text,
  name text not null,
  phone text not null,
  email text,
  company text,
  preferred_contact text,
  location_text text not null,
  geolocation_lat numeric(9,6),
  geolocation_lng numeric(9,6),
  geolocation_accuracy_m numeric,
  asset_type text not null,
  unit_number text,
  vin_serial text,
  year_make_model text,
  loaded_state text,
  problem_category text not null,
  symptoms text not null,
  fault_codes text,
  safety_notes text,
  status public.rrr_request_status not null default 'NEW',
  is_demo boolean not null default false,
  assigned_to uuid,
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_customers (
  id uuid primary key default gen_random_uuid(),
  customer_type text not null default 'one_off',
  name text not null,
  primary_contact text,
  phone text,
  email text,
  billing_address text,
  payment_terms text,
  status text not null default 'ACTIVE',
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_fleet_accounts (
  id uuid primary key default gen_random_uuid(),
  company text not null,
  primary_contact text,
  phone text,
  email text,
  yard_area text,
  po_required boolean,
  payment_terms text,
  rate_source_id text,
  status text not null default 'TARGET',
  asset_count integer not null default 0,
  next_review date,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_assets (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid references public.rrr_customers(id) on delete set null,
  fleet_account_id uuid references public.rrr_fleet_accounts(id) on delete set null,
  unit_number text,
  asset_type text not null,
  vin_serial text,
  year_text text,
  make text,
  model text,
  plate text,
  loaded_config text,
  odometer_hours text,
  last_service_at timestamptz,
  next_pm_at timestamptz,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_service_requests (
  id uuid primary key default gen_random_uuid(),
  request_number bigint generated always as identity unique,
  lead_id uuid references public.rrr_leads(id) on delete set null,
  customer_id uuid references public.rrr_customers(id) on delete set null,
  asset_id uuid references public.rrr_assets(id) on delete set null,
  created_at timestamptz not null default now(),
  location_text text not null,
  asset_type text not null,
  problem_category text not null,
  symptoms text not null,
  fault_codes text,
  photos_received integer not null default 0,
  capability_state public.rrr_truth_state not null default 'TBD',
  status public.rrr_request_status not null default 'NEW',
  priority text,
  preferred_contact text,
  dispatcher_id uuid,
  notes text,
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_dispatch (
  id uuid primary key default gen_random_uuid(),
  service_request_id uuid not null references public.rrr_service_requests(id) on delete cascade,
  technician_id uuid,
  service_truck text,
  dispatch_at timestamptz,
  en_route_at timestamptz,
  on_site_at timestamptz,
  eta_quoted text,
  eta_source text,
  status public.rrr_request_status not null default 'DISPATCH_READY',
  safety_notes text,
  parts_tools_needed text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_jobs (
  id uuid primary key default gen_random_uuid(),
  job_number bigint generated always as identity unique,
  service_request_id uuid not null references public.rrr_service_requests(id) on delete restrict,
  customer_id uuid references public.rrr_customers(id) on delete set null,
  asset_id uuid references public.rrr_assets(id) on delete set null,
  technician_id uuid,
  opened_at timestamptz not null default now(),
  status public.rrr_request_status not null default 'ASSIGNED',
  diagnosis text,
  authorized_scope text,
  authorization_ref text,
  repair_summary text,
  parts_status text,
  invoice_ready boolean not null default false,
  closed_at timestamptz,
  follow_up_state text,
  notes text,
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_job_events (
  id uuid primary key default gen_random_uuid(),
  job_id uuid references public.rrr_jobs(id) on delete cascade,
  lead_id uuid references public.rrr_leads(id) on delete cascade,
  service_request_id uuid references public.rrr_service_requests(id) on delete cascade,
  event_at timestamptz not null default now(),
  event_type text not null,
  actor_id uuid,
  actor_label text,
  old_state text,
  new_state text,
  summary text,
  evidence_ref text,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists public.rrr_evidence (
  id uuid primary key default gen_random_uuid(),
  lead_id uuid references public.rrr_leads(id) on delete cascade,
  service_request_id uuid references public.rrr_service_requests(id) on delete cascade,
  job_id uuid references public.rrr_jobs(id) on delete cascade,
  evidence_type text not null,
  captured_at timestamptz not null default now(),
  description text,
  storage_path text,
  mime_type text,
  file_size_bytes bigint,
  source text,
  privacy_state text not null default 'PRIVATE',
  marketing_approved boolean not null default false,
  sensitive boolean not null default true,
  notes text
);

create table if not exists public.rrr_charges (
  id uuid primary key default gen_random_uuid(),
  job_id uuid not null references public.rrr_jobs(id) on delete restrict,
  description text not null,
  qty numeric(12,3) not null default 1,
  unit text,
  rate numeric(12,2),
  amount numeric(12,2),
  rate_source_id text,
  evidence_ref text,
  authorization_ref text,
  status text not null default 'HOLD',
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.rrr_invoices (
  id uuid primary key default gen_random_uuid(),
  invoice_number text unique,
  job_id uuid not null references public.rrr_jobs(id) on delete restrict,
  customer_id uuid references public.rrr_customers(id) on delete set null,
  issue_date date,
  due_date date,
  original_amount numeric(12,2) not null default 0,
  payments_received numeric(12,2) not null default 0,
  credits numeric(12,2) not null default 0,
  balance numeric(12,2) generated always as (original_amount - payments_received - credits) stored,
  status text not null default 'DRAFT_HOLD',
  rate_source_id text,
  po_account text,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.rrr_payments (
  id uuid primary key default gen_random_uuid(),
  invoice_id uuid not null references public.rrr_invoices(id) on delete restrict,
  paid_at timestamptz not null default now(),
  amount numeric(12,2) not null check (amount >= 0),
  method text,
  reference text,
  verified boolean not null default false,
  notes text
);

create index if not exists rrr_leads_status_idx on public.rrr_leads(status, created_at desc);
create index if not exists rrr_service_requests_status_idx on public.rrr_service_requests(status, created_at desc);
create index if not exists rrr_jobs_status_idx on public.rrr_jobs(status, opened_at desc);
create index if not exists rrr_job_events_job_idx on public.rrr_job_events(job_id, event_at desc);
create index if not exists rrr_job_events_lead_idx on public.rrr_job_events(lead_id, event_at desc);
create index if not exists rrr_evidence_job_idx on public.rrr_evidence(job_id, captured_at desc);

create or replace function public.rrr_set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

do $$ declare t text; begin
  foreach t in array array[
    'rrr_business_truth','rrr_service_capabilities','rrr_leads','rrr_customers',
    'rrr_fleet_accounts','rrr_assets','rrr_service_requests','rrr_dispatch','rrr_jobs','rrr_invoices'
  ] loop
    execute format('drop trigger if exists %I on public.%I', t || '_set_updated_at', t);
    execute format('create trigger %I before update on public.%I for each row execute function public.rrr_set_updated_at()', t || '_set_updated_at', t);
  end loop;
end $$;
