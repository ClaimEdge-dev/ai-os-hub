-- Rapid Roadside Repair customer authorization decision RPC
-- PREPARED / NOT APPLIED

create or replace function public.rrr_decide_authorization(
  token uuid,
  decision text,
  customer_name text
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  a public.rrr_authorizations%rowtype;
  normalized text := upper(trim(coalesce(decision,'')));
begin
  if normalized not in ('APPROVED','DECLINED') then
    raise exception 'invalid_decision';
  end if;
  if length(trim(coalesce(customer_name,''))) < 2 then
    raise exception 'customer_name_required';
  end if;

  select * into a
  from public.rrr_authorizations
  where public_token = token
    and status = 'PENDING'
    and (expires_at is null or expires_at > now())
  for update;

  if a.id is null then
    return jsonb_build_object('ok',false,'reason','not_found_or_expired');
  end if;

  update public.rrr_authorizations
  set status = normalized,
      authorized_by = trim(customer_name),
      decision_at = now(),
      decision_method = 'SECURE_LINK'
  where id = a.id;

  insert into public.rrr_job_events(job_id,service_request_id,event_type,actor_label,old_state,new_state,summary)
  values(
    a.job_id,a.service_request_id,'authorization_decision',trim(customer_name),
    'PENDING',normalized,
    case when normalized='APPROVED'
      then 'Customer approved additional work.'
      else 'Customer declined additional work.'
    end
  );

  return jsonb_build_object('ok',true,'status',normalized,'authorization_id',a.id);
end;
$$;

revoke all on function public.rrr_decide_authorization(uuid,text,text) from public;
grant execute on function public.rrr_decide_authorization(uuid,text,text) to anon, authenticated;
