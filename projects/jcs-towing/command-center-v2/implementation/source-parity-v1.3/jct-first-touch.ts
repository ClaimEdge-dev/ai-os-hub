import type {Attribution} from "./jct-v3-contract";
/** First-party session attribution. No user contact data, query-bearing referrer, or location stored. */
const KEY="jct:first-touch:v1";
const sanitize=(s:string,n=255)=>s.replace(/[\u0000-\u001f\u007f]/g,"").slice(0,n);
export function fromLanding(url:string,referrer:string,width:number):Attribution {
 const u=new URL(url);
 let cleanRef="";
 try{const r=new URL(referrer);cleanRef=r.origin+r.pathname;}catch{}
 return {
  source_page:sanitize(u.pathname,500),referrer:sanitize(cleanRef,500),
  utm_source:sanitize(u.searchParams.get("utm_source")??""),
  utm_medium:sanitize(u.searchParams.get("utm_medium")??""),
  utm_campaign:sanitize(u.searchParams.get("utm_campaign")??""),
  utm_content:sanitize(u.searchParams.get("utm_content")??""),
  device_type:width<768?"mobile":width<1100?"tablet":"desktop"
 };
}
export function firstTouch():Attribution {
 const empty:Attribution={source_page:"",referrer:"",utm_source:"",utm_medium:"",utm_campaign:"",utm_content:"",device_type:"desktop"};
 if(typeof window==="undefined")return empty;
 const current=fromLanding(window.location.href,document.referrer,window.innerWidth);
 try{
  const raw=window.sessionStorage.getItem(KEY);
  if(raw){
   const x:unknown=JSON.parse(raw);
   if(x&&typeof x==="object"&&!Array.isArray(x)){
    const p=x as Record<string,unknown>;
    const fields=["source_page","referrer","utm_source","utm_medium","utm_campaign","utm_content","device_type"];
    if(fields.every(f=>typeof p[f]==="string")&&["mobile","tablet","desktop"].includes(String(p["device_type"]))){
      let safeRef="";
      try{const u=new URL(String(p["referrer"]));safeRef=u.origin+u.pathname;}catch{}
      return {
        source_page:sanitize(String(p["source_page"]),500),
        referrer:sanitize(safeRef,500),
        utm_source:sanitize(String(p["utm_source"])),
        utm_medium:sanitize(String(p["utm_medium"])),
        utm_campaign:sanitize(String(p["utm_campaign"])),
        utm_content:sanitize(String(p["utm_content"])),
        device_type:p["device_type"] as Attribution["device_type"]
      };
    }
   }
  }
  window.sessionStorage.setItem(KEY,JSON.stringify(current));
 }catch{/* storage disabled; use current non-identifying values */}
 return current;
}
