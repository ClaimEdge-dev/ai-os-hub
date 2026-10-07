-- Rapid Roadside Repair public request RPC
-- PREPARED / NOT APPLIED

create or replace function public.rrr_submit_service_request(payload jsonb)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_name text := trim(coalesce(payload->>'name',''));
  v_phone text := trim(coalesce(payload->>'phone',''));
  v_location text := trim(coalesce(payload->>'location',''));
  v_asset_type text := trim(coalesce(payload->>'asset_type',''));
  v_problem text := trim(coalesce(payload->>'problem_category',''));
  v_symptoms text := trim(coalesce(payload->>'symptoms',''));
  v_email text := nullif(trim(coalesce(payload->>'email','')), '');
  v_preferred text := nullif(trim(coalesce(payload->>'preferred_contact','')), '');
  v_lead public.rrr_leads%rowtype;
  v_request public.rrr_service_requests%rowtype;
begin
  if length(v_name) < 2 or length(v_name) > 120 then
    raise exception 'invalid_name';
  end if;
  if length(v_phone) < 7 or length(v_phone) > 40 then
    raise exception 'invalid_phone';
  end if;
  if length(v_location) < 3 or length(v_location) > 500 then
    raise exception 'invalid_location';
  end if;
  if length(v_asset_type) < 2 or length(v_asset_type) > 120 then
    raise exception 'invalid_asset_type';
  end if;
  if length(v_problem) < 2 or length(v_problem) > 160 then
    raise exception 'invalid_problem_category';
  end if;
  if length(v_symptoms) < 3 or length(v_symptoms) > 4000 then
    raise exception 'invalid_symptoms';
  end if;
  if v_email is not null and (length(v_email) > 254 or position('@' in v_email) < 2) then
    raise exception 'invalid_email';
  end if;
  if coalesce((payload->>'demo_consent')::boolean, false) is not true
     and coalesce((payload->>'service_request_consent')::boolean, false) is not true then
    raise exception 'consent_required';
  end if;

  -- Simple anti-duplicate / throttle: same phone + location + problem within 3 minutes.
  if exists (
    select 1 from public.rrr_leads
    where phone = v_phone
      and location_text = v_location
      and problem_category = v_problem
      and created_at > now() - interval '3 minutes'
  ) then
    raise exception 'recent_duplicate_request';
  end if;

  insert into public.rrr_leads (
    source, source_page, referrer, utm_source, utm_medium, utm_campaign, utm_content, device_type,
    name, phone, email, company, preferred_contact, location_text,
    geolocation_lat, geolocation_lng, geolocation_accuracy_m,
    asset_type, unit_number, vin_serial, year_make_model, loaded_state,
    problem_category, symptoms, fault_codes, safety_notes, is_demo
  ) values (
    coalesce(nullif(payload->>'source',''),'website'),
    nullif(payload->>'source_page',''), nullif(payload->>'referrer',''),
    nullif(payload->>'utm_source',''), nullif(payload->>'utm_medium',''),
    nullif(payload->>'utm_campaign',''), nullif(payload->>'utm_content',''),
    nullif(payload->>'device_type',''),
    v_name, v_phone, v_email, nullif(payload->>'company',''), v_preferred, v_location,
    nullif(payload->>'geolocation_lat','')::numeric,
    nullif(payload->>'geolocation_lng','')::numeric,
    nullif(payload->>'geolocation_accuracy_m','')::numeric,
    v_asset_type, nullif(payload->>'unit_number',''), nullif(payload->>'vin_serial',''),
    nullif(payload->>'year_make_model',''), nullif(payload->>'loaded_state',''),
    v_problem, v_symptoms, nullif(payload->>'fault_codes',''), nullif(payload->>'safety_notes',''),
    coalesce((payload->>'is_demo')::boolean,false)
  ) returning * into v_lead;

  insert into public.rrr_service_requests (
    lead_id, location_text, asset_type, problem_category, symptoms, fault_codes,
    capability_state, status, preferred_contact, notes
  ) values (
    v_lead.id, v_location, v_asset_type, v_problem, v_symptoms, v_lead.fault_codes,
    'TBD', 'NEW', v_preferred, 'Public request intake; capability/ETA/price not yet promised.'
  ) returning * into v_request;

  insert into public.rrr_job_events (
    lead_id, service_request_id, event_type, actor_label, old_state, new_state, summary
  ) values (
    v_lead.id, v_request.id, 'request_created', 'public_request', null, 'NEW',
    'Service request created; awaiting Rapid capability/dispatch review.'
  );

  return jsonb_build_object(
    'lead_id', v_lead.id,
    'lead_number', v_lead.lead_number,
    'service_request_id', v_request.id,
    'request_number', v_request.request_number,
    'status', v_request.status
  );
end;
$$;

revoke all on function public.rrr_submit_service_request(jsonb) from public;
grant execute on function public.rrr_submit_service_request(jsonb) to anon, authenticated;
