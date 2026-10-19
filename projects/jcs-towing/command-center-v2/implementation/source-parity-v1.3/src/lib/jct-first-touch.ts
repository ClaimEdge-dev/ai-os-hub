import type {FirstTouch,DeviceType} from "./jct-v3-contract";
const KEY="jct:first-touch:v1";
function clean(s:string,n=255):string{return s.replace(/[\u0000-\u001f\u007f]/g,"").slice(0,n);}
function refPath(s:string):string{try{const u=new URL(s);return clean(u.origin+u.pathname,500);}catch{return "";}}
function device(n:number):DeviceType{return n<768?"mobile":n<1100?"tablet":"desktop";}
export function firstTouchFromUrl(url:string,referrer:string,width:number):FirstTouch{
  const u=new URL(url),q=u.searchParams;
  return {source_page:clean(u.pathname,500),referrer:refPath(referrer),
    utm_source:clean(q.get("utm_source")??""),utm_medium:clean(q.get("utm_medium")??""),
    utm_campaign:clean(q.get("utm_campaign")??""),utm_content:clean(q.get("utm_content")??""),
    device_type:device(width)};
}
export function getFirstTouch():FirstTouch{
  const empty:FirstTouch={source_page:"",referrer:"",utm_source:"",utm_medium:"",
    utm_campaign:"",utm_content:"",device_type:"desktop"};
  if(typeof window==="undefined")return empty;
  const fresh=firstTouchFromUrl(window.location.href,document.referrer,window.innerWidth);
  try{
    const saved=window.sessionStorage.getItem(KEY);
    if(saved){
      const parsed:unknown=JSON.parse(saved);
      if(parsed&&typeof parsed==="object"&&!Array.isArray(parsed)){
        const p=parsed as Record<string,unknown>;
        const ks=["source_page","referrer","utm_source","utm_medium","utm_campaign","utm_content","device_type"];
        if(ks.every(k=>typeof p[k]==="string")&&["mobile","tablet","desktop"].includes(String(p["device_type"]))){
          return {source_page:clean(String(p["source_page"]),500),referrer:refPath(String(p["referrer"])),
            utm_source:clean(String(p["utm_source"])),utm_medium:clean(String(p["utm_medium"])),
            utm_campaign:clean(String(p["utm_campaign"])),utm_content:clean(String(p["utm_content"])),
            device_type:p["device_type"] as DeviceType};
        }
      }
    }
    window.sessionStorage.setItem(KEY,JSON.stringify(fresh));
  }catch{/* sessionStorage may be disabled */}
  return fresh;
}
