-- Rapid Roadside Repair backend v1 synthetic test
-- RUN ONLY ON A DEV/BRANCH DATABASE AFTER 001-006.
-- This test rolls back all data.

begin;

select public.rrr_submit_service_request(jsonb_build_object(
  'name','DEBO SYNTHETIC DRIVER',
  'phone','555-010-0000',
  'location','Synthetic I-80 roadside test location',
  'asset_type','Semi / Tractor',
  'problem_category','Air / Brake',
  'symptoms','Synthetic air-pressure loss used only for backend validation.',
  'fault_codes','DEMO-CODE',
  'safety_notes','Synthetic safe shoulder.',
  'preferred_contact','Phone Call',
  'source','backend-test',
  'utm_source','synthetic',
  'utm_campaign','rrr-backend-v1',
  'demo_consent',true,
  'is_demo',true
));

-- Validate that no seeded truth is public by default.
do $$
begin
  if exists (select 1 from public.rrr_business_truth where public_enabled = true) then
    raise exception 'unexpected_public_truth';
  end if;
  if exists (select 1 from public.rrr_service_capabilities where public_enabled = true) then
    raise exception 'unexpected_public_service';
  end if;
end $$;

-- Validate that request/event records were created.
do $$
declare
  c1 integer;
  c2 integer;
  c3 integer;
begin
  select count(*) into c1 from public.rrr_leads where is_demo = true;
  select count(*) into c2 from public.rrr_service_requests sr
    join public.rrr_leads l on l.id = sr.lead_id
    where l.is_demo = true;
  select count(*) into c3 from public.rrr_job_events je
    join public.rrr_leads l on l.id = je.lead_id
    where l.is_demo = true;
  if c1 < 1 or c2 < 1 or c3 < 1 then
    raise exception 'synthetic_request_chain_failed';
  end if;
end $$;

rollback;
