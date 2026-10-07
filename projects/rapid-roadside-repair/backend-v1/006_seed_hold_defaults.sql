-- Rapid Roadside Repair backend v1 seed
-- PREPARED / NOT APPLIED
-- All seeded values remain non-public until owner approval.

insert into public.rrr_business_truth (truth_key,value_text,state,source_type,public_enabled,notes)
values
('public_name','Rapid Roadside Repair','OWNER_CONFIRM','current logo / project context',false,'Working public name only'),
('phone','(815) 749-3811','OWNER_CONFIRM','current logo',false,'Owner confirmation required'),
('state','Illinois','OWNER_CONFIRM','user-provided',false,'Exact service territory TBD'),
('core_service_1','Emergency mobile roadside assistance','OWNER_CONFIRM','user-provided',false,'Owner public confirmation required'),
('core_service_2','On-site repair','OWNER_CONFIRM','user-provided',false,'Owner public confirmation required'),
('asset_class_1','Semi trucks','OWNER_CONFIRM','user-provided',false,'Owner public confirmation required'),
('asset_class_2','Trailers','OWNER_CONFIRM','user-provided',false,'Owner public confirmation required'),
('hours_24_7',null,'HOLD','unverified',false,'Do not publish 24/7 until verified'),
('service_area',null,'HOLD','unverified',false,'Radius/counties/corridors unknown'),
('rate_authority',null,'HOLD','unverified',false,'No official RRR rate source loaded'),
('credentials',null,'HOLD','unverified',false,'Licenses/insurance/certifications require evidence')
on conflict (truth_key) do nothing;

insert into public.rrr_service_capabilities
(service_code,family,public_label,internal_description,asset_classes,delivery_mode,urgency_mode,owner_approved,public_enabled,state,source_ref,notes)
values
('SVC-ROAD','Emergency Roadside','Emergency Roadside Assistance','Breakdown triage and roadside repair intake',array['Semi','Trailer','Commercial','Equipment'],'Mobile','Emergency',false,false,'OWNER_CONFIRM','user-provided core scope',null),
('SVC-DIESEL','Mobile Diesel / Mechanical','Mobile Truck Repair','Mechanical, starting, cooling, fuel, belts/hoses categories',array['Semi','Commercial'],'Mobile','Both',false,false,'OWNER_CONFIRM','broad user-provided scope','Exact services verify'),
('SVC-ELEC','Electrical / Diagnostics','Electrical & Diagnostic Repair','Electrical, charging, fault-code and diagnostic categories',array['Semi','Trailer','Equipment'],'Mobile','Both',false,false,'OWNER_CONFIRM','broad user-provided scope','Tool capability verify'),
('SVC-AIR','Air / Brake','Air & Brake Repair','Air-line, leak and brake-system repair categories',array['Semi','Trailer'],'Mobile','Both',false,false,'OWNER_CONFIRM','broad user-provided scope','Exact service verify'),
('SVC-TRAILER','Trailer','Mobile Trailer Repair','Trailer electrical, air, brake, suspension, landing gear and hardware categories',array['Trailer'],'Mobile','Both',false,false,'OWNER_CONFIRM','user-provided trailer scope','Exact service verify'),
('SVC-TIRE','Tire / Wheel','Tire & Wheel Service','Tire, wheel and hub categories',array['Semi','Trailer','Commercial'],'Mobile','Both',false,false,'HOLD','candidate capability','Equipment/vendor model verify'),
('SVC-EMISS','Aftertreatment','DPF / DEF / Aftertreatment','Fault diagnosis or regen only when tools and capability are verified',array['Semi','Commercial'],'Mobile','Both',false,false,'HOLD','candidate capability','Specialty/tooling verify'),
('SVC-HYD','Hydraulics','Mobile Hydraulic Service','Field hydraulic diagnosis/repair',array['Equipment','Commercial'],'Mobile','Both',false,false,'HOLD','candidate capability','Equipment/parts support verify'),
('SVC-WELD','Welding / Fabrication','Mobile Welding / Fabrication','Roadside/job-site fabrication',array['Semi','Trailer','Equipment'],'Mobile','Both',false,false,'HOLD','candidate capability','Welder/equipment capability verify'),
('SVC-HEAVY','Heavy Equipment','Heavy Equipment Service','On-site equipment repair for owner-confirmed classes',array['Equipment'],'Mobile','Both',false,false,'OWNER_CONFIRM','broad user-provided scope','Exact classes verify'),
('SVC-FLEET','Fleet / PM','Fleet Maintenance','Scheduled yard service and preventive maintenance',array['Semi','Trailer','Commercial','Equipment'],'Mobile','Scheduled',false,false,'OWNER_CONFIRM','growth lane','Owner confirmation required')
on conflict (service_code) do nothing;
