/** JCT 90: source-parity adapter for existing Lovable/Supabase. Not deployed. */
export type TriState = "yes" | "no" | "unsure";
export type ContactMethod = "phone" | "text" | "email";
export type DeviceType = "mobile" | "tablet" | "desktop";
export type FirstTouch = {
  source_page:string;referrer:string;utm_source:string;utm_medium:string;
  utm_campaign:string;utm_content:string;device_type:DeviceType;
};
export type V3Form = {
  name:string;phone:string;email?:string;preferred_contact_method?:ContactMethod;
  pickup:string;destination?:string;vehicle_year?:string;vehicle_make?:string;
  vehicle_model?:string;vehicle_type?:string;service?:string;drivable?:TriState|"";
  rolls?:TriState;steers?:TriState;shifts?:TriState;keys_available?:TriState;
  accident?:TriState;wheel_damage?:TriState;clearance_issue?:TriState;
  access_notes?:string;notes?:string;consent:true;is_demo?:never;
};
const trim=(v:string|undefined,max:number)=>(v??"").trim().slice(0,max);
export function toV3Payload(form:V3Form,a:FirstTouch):Record<string,unknown>{
  return {
    name:trim(form.name,100),phone:trim(form.phone,30),email:trim(form.email,255),
    preferred_contact_method:form.preferred_contact_method??"phone",
    pickup:trim(form.pickup,300),destination:trim(form.destination,300),
    vehicle_year:trim(form.vehicle_year,10),vehicle_make:trim(form.vehicle_make,60),
    vehicle_model:trim(form.vehicle_model,60),vehicle_type:trim(form.vehicle_type,100),
    service:trim(form.service,100)||"Other / not sure",drivable:form.drivable??"",
    rolls:form.rolls??"unsure",steers:form.steers??"unsure",shifts:form.shifts??"unsure",
    keys_available:form.keys_available??"unsure",accident:form.accident??"unsure",
    wheel_damage:form.wheel_damage??"unsure",clearance_issue:form.clearance_issue??"unsure",
    access_notes:trim(form.access_notes,1200),notes:trim(form.notes,2000),
    consent:form.consent===true,is_demo:false,
    source_page:trim(a.source_page,500),referrer:trim(a.referrer,500),
    utm_source:trim(a.utm_source,255),utm_medium:trim(a.utm_medium,255),
    utm_campaign:trim(a.utm_campaign,255),utm_content:trim(a.utm_content,255),
    device_type:a.device_type
  };
}
/** Only the public sequential request number may be returned to a customer. */
export function redactV3Response(raw:unknown):{reference:number}{
  if(!raw||typeof raw!=="object"||Array.isArray(raw))throw new Error("Unexpected V3 response");
  const n=(raw as Record<string,unknown>)["lead_number"];
  if(typeof n!=="number"||!Number.isSafeInteger(n)||n<=0)throw new Error("Missing request number");
  return {reference:n};
}
