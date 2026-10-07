/** My Tow client display guard: never forward raw lookup RPC data to customers. */
export type SafeTowStatus={status:string};
const labels:Record<string,string>={
 NEW:"Request received",RECEIVED:"Request received",REQUEST_RECEIVED:"Request received",
 NEEDS_INFO:"More information needed",DISPATCH_PENDING:"Dispatch pending",
 DISPATCHED:"Dispatched",EN_ROUTE:"En route",ON_SCENE:"On scene",
 LOADED:"Service in progress",COMPLETE:"Service completed",COMPLETED:"Service completed",
 CANCELLED:"Request closed",CLOSED:"Request closed"
};
export const genericLookupError="We couldn't verify the details. Check your request number and phone, or call JC's Towing.";
export function safeStatus(raw:unknown):SafeTowStatus|null {
 if(!raw||typeof raw!=="object"||Array.isArray(raw))return null;
 const x=raw as Record<string,unknown>;
 if(x.ok===false||x.success===false)return null;
 const value=x.status??x.job_status??x.request_status;
 if(typeof value!=="string")return null;
 const key=value.trim().toUpperCase().replace(/[\s/-]+/g,"_");
 return labels[key]?{status:labels[key]}:null;
}
