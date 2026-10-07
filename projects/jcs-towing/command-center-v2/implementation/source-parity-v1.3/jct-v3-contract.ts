/** JCT 90 private-preview parity helper. No database writes in this module. */
export type TriState="yes"|"no"|"unsure";
export type Attribution={source_page:string;referrer:string;utm_source:string;utm_medium:string;utm_campaign:string;utm_content:string;device_type:"mobile"|"tablet"|"desktop"};
export type V3Form={name:string;phone:string;pickup:string;consent:true;email?:string;destination?:string;service?:string;vehicle_year?:string;vehicle_make?:string;vehicle_model?:string;vehicle_type?:string;preferred_contact_method?:"phone"|"text"|"email";rolls?:TriState;steers?:TriState;shifts?:TriState;keys_available?:TriState;accident?:TriState;wheel_damage?:TriState;clearance_issue?:TriState;access_notes?:string;notes?:string};
const clip=(v:string|undefined,n:number)=>(v??"").trim().slice(0,n);
export function toV3Payload(form:V3Form,a:Attribution):Record<string,unknown>{
 return {
  name:clip(form.name,100),phone:clip(form.phone,30),pickup:clip(form.pickup,300),
  email:clip(form.email,255),destination:clip(form.destination,300),service:clip(form.service,100),
  vehicle_year:clip(form.vehicle_year,10),vehicle_make:clip(form.vehicle_make,60),
  vehicle_model:clip(form.vehicle_model,60),vehicle_type:clip(form.vehicle_type,100),
  preferred_contact_method:form.preferred_contact_method??"phone",
  rolls:form.rolls??"unsure",steers:form.steers??"unsure",shifts:form.shifts??"unsure",
  keys_available:form.keys_available??"unsure",accident:form.accident??"unsure",
  wheel_damage:form.wheel_damage??"unsure",clearance_issue:form.clearance_issue??"unsure",
  access_notes:clip(form.access_notes,1200),notes:clip(form.notes,2000),
  consent:form.consent===true,is_demo:false,...a
 };
}
export function publicV3Receipt(raw:unknown):{reference:number}{
 if(!raw||typeof raw!=="object"||Array.isArray(raw))throw Error("Unrecognized result");
 const n=(raw as Record<string,unknown>).lead_number;
 if(typeof n!=="number"||!Number.isSafeInteger(n)||n<1)throw Error("No public reference");
 return {reference:n};
}
