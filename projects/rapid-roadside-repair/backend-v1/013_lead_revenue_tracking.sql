-- Rapid Roadside Repair backend v1
-- RRR 91 Lead + Revenue Tracking
-- PREPARED / NOT APPLIED

create table if not exists public.rrr_attribution_events (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  lead_id uuid references public.rrr_leads(id) on delete set null,
  service_request_id uuid references public.rrr_service_requests(id) on delete set null,
  job_id uuid references public.rrr_jobs(id) on delete set null,
  event_type text not null,
  first_touch_source text,
  last_touch_source text,
  source text,
  medium text,
  campaign text,
  term text,
  content text,
  landing_page text,
  referrer text,
  call_tracking_number text,
  form_source text,
  device_type text,
  city_area text,
  service_category text,
  visitor_id text,
  session_id text,
  metadata jsonb not null default '{}'::jsonb
);

create table if not exists public.rrr_marketing_spend (
  id uuid primary key default gen_random_uuid(),
  spend_date date not null,
  channel text not null,
  campaign text,
  vendor text,
  budget numeric(12,2),
  spend numeric(12,2) not null default 0,
  clicks integer not null default 0,
  calls integer not null default 0,
  forms integer not null default 0,
  qualified_leads integer not null default 0,
  jobs integer not null default 0,
  collected_revenue numeric(12,2) not null default 0,
  gross_profit numeric(12,2),
  approval_status text not null default 'HOLD',
  source_ref text,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.rrr_operator_commissions (
  id uuid primary key default gen_random_uuid(),
  effective_date date,
  lead_id uuid references public.rrr_leads(id) on delete set null,
  job_id uuid references public.rrr_jobs(id) on delete set null,
  invoice_id uuid references public.rrr_invoices(id) on delete set null,
  payment_id uuid references public.rrr_payments(id) on delete set null,
  fleet_account_id uuid references public.rrr_fleet_accounts(id) on delete set null,
  compensation_rule text,
  commission_basis text not null,
  gross_invoice numeric(12,2),
  amount_collected numeric(12,2),
  direct_job_cost numeric(12,2),
  gross_profit numeric(12,2),
  rate_or_flat_amount numeric(12,4),
  commission_amount numeric(12,2),
  paid_to_operator numeric(12,2) not null default 0,
  payment_date date,
  status text not null default 'DRAFT_NOT_AGREED',
  dispute_status text,
  source_ref text,
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.rrr_fleet_sales_pipeline (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  company text not null,
  decision_maker text,
  phone text,
  email text,
  fleet_size text,
  tractors integer,
  trailers integer,
  equipment text,
  location text,
  current_vendor text,
  pain_point text,
  source text,
  stage text not null default 'TARGET',
  last_contact_at timestamptz,
  next_action text,
  next_action_at timestamptz,
  first_job_id uuid references public.rrr_jobs(id) on delete set null,
  fleet_account_id uuid references public.rrr_fleet_accounts(id) on delete set null,
  collected_revenue numeric(12,2) not null default 0,
  operator_commission numeric(12,2) not null default 0,
  notes text
);

create table if not exists public.rrr_referral_partners (
  id uuid primary key default gen_random_uuid(),
  partner_type text,
  company_or_person text not null,
  contact text,
  phone text,
  email text,
  area text,
  source text,
  status text not null default 'TARGET',
  last_contact_at timestamptz,
  referrals integer not null default 0,
  jobs integer not null default 0,
  collected_revenue numeric(12,2) not null default 0,
  referral_fee_basis text,
  referral_fee numeric(12,2),
  approval_status text not null default 'HOLD',
  notes text,
  created_at timestamptz not null default now()
);

create table if not exists public.rrr_followups (
  id uuid primary key default gen_random_uuid(),
  customer_id uuid references public.rrr_customers(id) on delete set null,
  job_id uuid references public.rrr_jobs(id) on delete set null,
  invoice_id uuid references public.rrr_invoices(id) on delete set null,
  created_at timestamptz not null default now(),
  follow_up_type text not null,
  due_at timestamptz,
  eligibility text,
  status text not null default 'OPEN',
  review_source text,
  review_link text,
  review_received boolean not null default false,
  rating numeric(2,1),
  permission_to_use boolean not null default false,
  repeat_opportunity text,
  next_pm_at timestamptz,
  notes text
);

create index if not exists rrr_attribution_lead_idx on public.rrr_attribution_events(lead_id, created_at desc);
create index if not exists rrr_attribution_job_idx on public.rrr_attribution_events(job_id, created_at desc);
create index if not exists rrr_attribution_campaign_idx on public.rrr_attribution_events(source, medium, campaign, created_at desc);
create index if not exists rrr_marketing_spend_date_idx on public.rrr_marketing_spend(spend_date desc, channel);
create index if not exists rrr_commission_status_idx on public.rrr_operator_commissions(status, effective_date desc);
create index if not exists rrr_fleet_pipeline_stage_idx on public.rrr_fleet_sales_pipeline(stage, next_action_at);
create index if not exists rrr_followups_due_idx on public.rrr_followups(status, due_at);

alter table public.rrr_attribution_events enable row level security;
alter table public.rrr_marketing_spend enable row level security;
alter table public.rrr_operator_commissions enable row level security;
alter table public.rrr_fleet_sales_pipeline enable row level security;
alter table public.rrr_referral_partners enable row level security;
alter table public.rrr_followups enable row level security;

do $$ declare t text; begin
  foreach t in array array[
    'rrr_attribution_events','rrr_marketing_spend','rrr_operator_commissions',
    'rrr_fleet_sales_pipeline','rrr_referral_partners','rrr_followups'
  ] loop
    execute format('drop policy if exists rrr_staff_all on public.%I', t);
    execute format(
      'create policy rrr_staff_all on public.%I for all to authenticated using (public.rrr_is_staff()) with check (public.rrr_is_staff())',
      t
    );
  end loop;
end $$;

revoke all on public.rrr_attribution_events from anon;
revoke all on public.rrr_marketing_spend from anon;
revoke all on public.rrr_operator_commissions from anon;
revoke all on public.rrr_fleet_sales_pipeline from anon;
revoke all on public.rrr_referral_partners from anon;
revoke all on public.rrr_followups from anon;

-- Control notes:
-- 1. Commission rows are accounting records only; no compensation agreement is implied.
-- 2. Marketing spend requires approval evidence before it is treated as authorized spend.
-- 3. Referral-fee fields do not authorize payment.
-- 4. This migration is additive and remains NOT APPLIED until approved for the verified RRR target.
