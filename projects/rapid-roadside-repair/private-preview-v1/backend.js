(function(){
  function cfg(){ return window.RRR_CONFIG || {backendMode:"local"}; }
  function isRemote(){
    const c=cfg();
    return c.backendMode==="supabase" && /^https:\/\//.test(c.supabaseUrl||"") && !!c.supabasePublishableKey;
  }
  function payloadFromRequest(r){
    let lat="",lng="";
    if(r.geo && r.geo.includes(",")){
      const parts=r.geo.split(",").map(x=>x.trim());
      lat=parts[0]||""; lng=parts[1]||"";
    }
    return {
      source:"website",
      source_page:cfg().sourcePage||"private-preview-v2",
      referrer:document.referrer||"",
      utm_source:new URLSearchParams(location.search).get("utm_source")||"",
      utm_medium:new URLSearchParams(location.search).get("utm_medium")||"",
      utm_campaign:new URLSearchParams(location.search).get("utm_campaign")||"",
      utm_content:new URLSearchParams(location.search).get("utm_content")||"",
      device_type:/Mobi|Android/i.test(navigator.userAgent)?"mobile":"desktop",
      name:r.name, phone:r.phone, email:r.email||"", company:r.company||"",
      preferred_contact:r.preferred||"", location:r.location,
      geolocation_lat:lat, geolocation_lng:lng,
      asset_type:r.assetType, unit_number:r.unit||"", vin_serial:r.vin||"",
      year_make_model:r.ymm||"", loaded_state:r.loaded||"",
      problem_category:r.problem, symptoms:r.symptoms,
      fault_codes:r.faultCodes||"", safety_notes:r.safety||"",
      demo_consent:true, is_demo:true
    };
  }
  async function mirrorServiceRequest(request){
    if(!isRemote()) return {mode:"local",mirrored:false};
    const c=cfg();
    const resp=await fetch(c.supabaseUrl.replace(/\/$/,"")+"/rest/v1/rpc/rrr_submit_service_request",{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "apikey":c.supabasePublishableKey,
        "Authorization":"Bearer "+c.supabasePublishableKey
      },
      body:JSON.stringify({payload:payloadFromRequest(request)})
    });
    const text=await resp.text();
    let body=null; try{body=text?JSON.parse(text):null;}catch{body={raw:text};}
    if(!resp.ok) throw new Error((body&&body.message)||"Backend request failed");
    return {mode:"supabase",mirrored:true,body};
  }
  window.RRR_BACKEND={isRemote,mirrorServiceRequest,payloadFromRequest};
})();
