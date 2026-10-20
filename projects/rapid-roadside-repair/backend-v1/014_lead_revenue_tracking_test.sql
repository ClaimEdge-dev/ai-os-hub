-- Rapid Roadside Repair
-- RRR 91 synthetic tracking test
-- PREPARED / DO NOT RUN ON PRODUCTION WITHOUT APPROVAL
-- Expected to be executed on a reversible dev/branch database after 013.

begin;

insert into public.rrr_marketing_spend
(spend_date,channel,campaign,vendor,budget,spend,clicks,calls,forms,qualified_leads,jobs,collected_revenue,gross_profit,approval_status,source_ref,notes)
values
(current_date,'SYNTHETIC_TEST','rrr91-test','DEBO',0,0,1,1,1,1,1,0,0,'HOLD','RRR91_TEST','Synthetic only');

insert into public.rrr_fleet_sales_pipeline
(company,decision_maker,phone,email,fleet_size,tractors,trailers,equipment,location,source,stage,next_action,notes)
values
('DEMO FLEET','Synthetic Contact','555-010-0000','demo@example.invalid','DEMO',1,1,'DEMO','Synthetic Area','SYNTHETIC_TEST','TARGET','Do not contact','Synthetic only');

insert into public.rrr_referral_partners
(partner_type,company_or_person,status,source,approval_status,notes)
values
('SYNTHETIC','DEMO PARTNER','TARGET','SYNTHETIC_TEST','HOLD','Do not contact or pay');

insert into public.rrr_followups
(follow_up_type,eligibility,status,review_received,permission_to_use,notes)
values
('SYNTHETIC_TEST','DEMO','OPEN',false,false,'Synthetic only');

do $$
declare
  c_spend integer;
  c_fleet integer;
  c_partner integer;
  c_follow integer;
begin
  select count(*) into c_spend from public.rrr_marketing_spend where source_ref='RRR91_TEST';
  select count(*) into c_fleet from public.rrr_fleet_sales_pipeline where source='SYNTHETIC_TEST';
  select count(*) into c_partner from public.rrr_referral_partners where source='SYNTHETIC_TEST';
  select count(*) into c_follow from public.rrr_followups where follow_up_type='SYNTHETIC_TEST';

  if c_spend <> 1 or c_fleet <> 1 or c_partner <> 1 or c_follow <> 1 then
    raise exception 'RRR91 synthetic tracking test failed';
  end if;
end $$;

rollback;
