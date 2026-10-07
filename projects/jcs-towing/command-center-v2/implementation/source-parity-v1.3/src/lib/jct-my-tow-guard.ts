/** Conservative My Tow display-only guard. Do not return raw RPC data. */
export type SafeTowStatus={status:string};
const states:Record<string,string>={
  NEW:"Request received",RECEIVED:"Request received",REQUEST_RECEIVED:"Request received",
  NEEDS_INFO:"More information needed",DISPATCH_PENDING:"Dispatch pending",
  DISPATCHED:"Dispatched",EN_ROUTE:"En route",ON_SCENE:"On scene",
  LOADED:"Service in progress",COMPLETE:"Service completed",COMPLETED:"Service completed",
  CANCELLED:"Request closed",CLOSED:"Request closed"
};
export const genericLookupError="We couldn't verify those details. Check the request number and phone, or call JC's Towing.";
export function safeStatusFromRpc(raw:unknown):SafeTowStatus|null{
  if(!raw||typeof raw!=="object"||Array.isArray(raw))return null;
  const p=raw as Record<string,unknown>;
  if(p["ok"]===false||p["success"]===false)return null;
  const s=p["status"]??p["job_status"]??p["request_status"];
  if(typeof s!=="string")return null;
  const text=s.trim().toUpperCase().replace(/[\s/-]+/g,"_");
  return states[text]?{status:states[text]}:null;
}
