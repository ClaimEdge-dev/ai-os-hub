-- Rapid Roadside Repair backend v1 RLS
-- PREPARED / NOT APPLIED
-- Conservative policy: authenticated users only for operating tables.
-- Anonymous service intake is allowed only through the security-definer RPC in 003.

alter table public.rrr_business_truth enable row level security;
alter table public.rrr_service_capabilities enable row level security;
alter table public.rrr_leads enable row level security;
alter table public.rrr_customers enable row level security;
alter table public.rrr_fleet_accounts enable row level security;
alter table public.rrr_assets enable row level security;
alter table public.rrr_service_requests enable row level security;
alter table public.rrr_dispatch enable row level security;
alter table public.rrr_jobs enable row level security;
alter table public.rrr_job_events enable row level security;
alter table public.rrr_evidence enable row level security;
alter table public.rrr_charges enable row level security;
alter table public.rrr_invoices enable row level security;
alter table public.rrr_payments enable row level security;

do $$ declare t text; begin
  foreach t in array array[
    'rrr_business_truth','rrr_service_capabilities','rrr_leads','rrr_customers',
    'rrr_fleet_accounts','rrr_assets','rrr_service_requests','rrr_dispatch','rrr_jobs',
    'rrr_job_events','rrr_evidence','rrr_charges','rrr_invoices','rrr_payments'
  ] loop
    execute format('drop policy if exists authenticated_staff_all on public.%I', t);
    execute format(
      'create policy authenticated_staff_all on public.%I for all to authenticated using (true) with check (true)',
      t
    );
  end loop;
end $$;

-- Append-only control for job events from authenticated clients:
revoke update, delete on public.rrr_job_events from authenticated;
grant select, insert on public.rrr_job_events to authenticated;

-- Anonymous users get no direct table access.
revoke all on public.rrr_business_truth from anon;
revoke all on public.rrr_service_capabilities from anon;
revoke all on public.rrr_leads from anon;
revoke all on public.rrr_customers from anon;
revoke all on public.rrr_fleet_accounts from anon;
revoke all on public.rrr_assets from anon;
revoke all on public.rrr_service_requests from anon;
revoke all on public.rrr_dispatch from anon;
revoke all on public.rrr_jobs from anon;
revoke all on public.rrr_job_events from anon;
revoke all on public.rrr_evidence from anon;
revoke all on public.rrr_charges from anon;
revoke all on public.rrr_invoices from anon;
revoke all on public.rrr_payments from anon;
