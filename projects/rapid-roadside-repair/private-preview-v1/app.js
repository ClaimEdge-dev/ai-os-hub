const REQUESTS_KEY = "rrr_private_demo_requests_v2";
const FLEET_KEY = "rrr_private_demo_fleet_v1";

const states = [
  "NEW","TRIAGE","DISPATCH READY","ASSIGNED","EN ROUTE","ON SITE",
  "DIAGNOSING","AWAITING AUTHORIZATION","AWAITING PARTS",
  "REPAIR IN PROGRESS","TESTING","COMPLETE","INVOICE READY","CLOSED"
];

const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => [...root.querySelectorAll(sel)];

function getJson(key){ try{return JSON.parse(localStorage.getItem(key)||"[]");}catch{return [];} }
function saveJson(key, value){ localStorage.setItem(key, JSON.stringify(value)); }
function nowIso(){ return new Date().toISOString(); }
function makeId(prefix){
  const ds=new Date().toISOString().slice(0,10).replaceAll("-","");
  return prefix+"-"+ds+"-"+Math.random().toString(36).slice(2,6).toUpperCase();
}
function esc(v=""){ return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function showView(name){
  $$(".view").forEach(v=>v.classList.toggle("active",v.id===name));
  $$(".tab").forEach(t=>t.classList.toggle("active",t.dataset.view===name));
  if(name==="dispatch") renderDispatch();
  if(name==="fleet") renderFleet();
  if(name==="benchmarks") renderBenchmarks();
  if(name==="truth") renderTruth();
  window.scrollTo({top:0,behavior:"smooth"});
}

$(".tab").forEach(t=>t.addEventListener("click",()=>showView(t.dataset.view)));
$(".jump").forEach(b=>b.addEventListener("click",()=>showView(b.dataset.target)));
$(".site-anchor").forEach(b=>b.addEventListener("click",()=>{
  showView("preview");
  setTimeout(()=>document.getElementById(b.dataset.scroll)?.scrollIntoView({behavior:"smooth",block:"start"}),120);
}));
$(".quick-problem").forEach(b=>b.addEventListener("click",()=>{
  showView("request");
  setTimeout(()=>{
    const select=$("#serviceForm [name=problem]");
    if(select) select.value=b.dataset.problem||"Other";
  },80);
}));

function renderServices(){
  const root=$("#serviceCards");
  root.innerHTML=(window.RRR_DATA?.services||[]).map(s=>`
    <article class="service-card ${s.state==="HOLD"?"hold":""}">
      <b>${esc(s.label)}</b>
      <span>${esc(s.description)}</span>
      <small>${esc(s.state)}</small>
    </article>`).join("");
}

function renderTruth(){
  const grid=$("#truthGrid");
  grid.innerHTML=(window.RRR_DATA?.truth||[]).map(t=>`
    <article class="truth-card ${t.state==="HOLD"?"hold":"pending"}">
      <b>${esc(t.label)}</b><span>${esc(t.value)}</span><small>${esc(t.state)}</small>
    </article>`).join("");
  $("#releaseChecks").innerHTML=(window.RRR_DATA?.releaseChecks||[]).map(x=>`<li><span>□</span>${esc(x)}</li>`).join("");
}

$("#geoBtn").addEventListener("click",()=>{
  const input=$("#serviceForm [name=geo]");
  if(!navigator.geolocation){ input.value="Geolocation unavailable"; return; }
  input.value="Requesting…";
  navigator.geolocation.getCurrentPosition(
    p=>input.value=`${p.coords.latitude.toFixed(5)}, ${p.coords.longitude.toFixed(5)}`,
    ()=>input.value="Location permission not granted",
    {enableHighAccuracy:true,timeout:8000}
  );
});

$("#serviceForm").addEventListener("submit",async e=>{
  e.preventDefault();
  const form=e.currentTarget;
  const submit=form.querySelector('button[type="submit"]');
  const fd=new FormData(form);
  const files=[...(form.querySelector("[name=photos]").files||[])];
  const request={
    serviceRequestId:makeId("SR"),leadId:makeId("LD"),createdAt:nowIso(),
    name:fd.get("name"),phone:fd.get("phone"),email:fd.get("email"),
    company:fd.get("company"),location:fd.get("location"),geo:fd.get("geo"),
    assetType:fd.get("assetType"),unit:fd.get("unit"),vin:fd.get("vin"),ymm:fd.get("ymm"),
    problem:fd.get("problem"),loaded:fd.get("loaded"),preferred:fd.get("preferred"),
    symptoms:fd.get("symptoms"),faultCodes:fd.get("faultCodes"),safety:fd.get("safety"),
    photoCount:files.length,photoNames:files.map(f=>f.name),
    status:"NEW",jobId:"",dispatchId:"",
    events:[{at:nowIso(),type:"created",oldState:"",newState:"NEW",summary:"Private demo service request created"}]
  };
  const result=$("#submitResult"); result.hidden=false;
  submit.disabled=true; submit.textContent="CREATING…";
  try{
    const mirror=window.RRR_BACKEND ? await window.RRR_BACKEND.mirrorServiceRequest(request) : {mode:"local",mirrored:false};
    const items=getJson(REQUESTS_KEY); items.unshift(request); saveJson(REQUESTS_KEY,items);
    const backendLine=mirror.mirrored
      ? "<br><b>Backend:</b> mirrored to configured test backend."
      : "<br><b>Backend:</b> local private-demo mode only.";
    result.innerHTML=`<b>Demo request created:</b> ${esc(request.serviceRequestId)}<br>Status: NEW • Photos recorded: ${request.photoCount}.${backendLine}<br>Open Dispatch to move the synthetic record through the workflow.`;
    form.reset();
  }catch(err){
    result.innerHTML=`<b>Request not submitted to backend.</b><br>${esc(err.message||String(err))}<br>No public dispatch or billing action occurred.`;
  }finally{
    submit.disabled=false; submit.textContent="CREATE DEMO SERVICE REQUEST";
  }
});

function updateStatus(id,newState){
  const items=getJson(REQUESTS_KEY);
  const item=items.find(x=>x.serviceRequestId===id); if(!item)return;
  const old=item.status; item.status=newState;
  if(!item.dispatchId && ["DISPATCH READY","ASSIGNED","EN ROUTE","ON SITE"].includes(newState)) item.dispatchId=makeId("DP");
  if(!item.jobId && ["ASSIGNED","EN ROUTE","ON SITE","DIAGNOSING","AWAITING AUTHORIZATION","AWAITING PARTS","REPAIR IN PROGRESS","TESTING","COMPLETE","INVOICE READY","CLOSED"].includes(newState)) item.jobId=makeId("JOB");
  item.events=item.events||[];
  item.events.push({at:nowIso(),type:"status_changed",oldState:old,newState,summary:"Private demo workflow state changed"});
  saveJson(REQUESTS_KEY,items); renderDispatch();
}

function eventHtml(item){
  const recent=(item.events||[]).slice(-4).reverse();
  return recent.map(e=>`<li><b>${esc(e.newState||e.type)}</b><span>${new Date(e.at).toLocaleString()}</span></li>`).join("");
}

function renderDispatch(){
  const items=getJson(REQUESTS_KEY);
  $("#statOpen").textContent=items.filter(x=>x.status!=="CLOSED").length;
  $("#statAuth").textContent=items.filter(x=>x.status==="AWAITING AUTHORIZATION").length;
  $("#statInvoice").textContent=items.filter(x=>x.status==="INVOICE READY").length;
  $("#statClosed").textContent=items.filter(x=>x.status==="CLOSED").length;
  const root=$("#dispatchList");
  if(!items.length){ root.innerHTML='<div class="panel">No demo requests yet. Create one from Request Service or load the synthetic test scenario.</div>'; return; }
  root.innerHTML=items.map(item=>{
    const buttons=states.map(s=>`<button data-id="${esc(item.serviceRequestId)}" data-state="${esc(s)}">${esc(s)}</button>`).join("");
    return `<article class="job-card">
      <div class="job-top">
        <div><div class="job-id">${esc(item.serviceRequestId)}</div>
        <div class="job-meta">${esc(item.assetType)} • Unit ${esc(item.unit||"TBD")} • ${esc(item.location)}</div></div>
        <span class="status-pill">${esc(item.status)}</span>
      </div>
      <div class="job-symptoms"><b>${esc(item.problem)}</b><br>${esc(item.symptoms)}</div>
      <div class="job-grid">
        <div><small>CUSTOMER</small><span>${esc(item.name)} • ${esc(item.phone)}</span></div>
        <div><small>COMPANY</small><span>${esc(item.company||"—")}</span></div>
        <div><small>JOB</small><span>${esc(item.jobId||"Not opened")}</span></div>
        <div><small>DISPATCH</small><span>${esc(item.dispatchId||"Not opened")}</span></div>
        <div><small>FAULT / WARNING</small><span>${esc(item.faultCodes||"—")}</span></div>
        <div><small>PHOTOS</small><span>${esc(item.photoCount||0)}</span></div>
      </div>
      <details><summary>Recent event ledger</summary><ul class="event-list">${eventHtml(item)}</ul></details>
      <div class="state-row">${buttons}</div>
    </article>`;
  }).join("");
  $$(".state-row button",root).forEach(btn=>btn.addEventListener("click",()=>updateStatus(btn.dataset.id,btn.dataset.state)));
}

$("#seedDemo").addEventListener("click",()=>{
  const items=getJson(REQUESTS_KEY);
  items.unshift({
    serviceRequestId:makeId("SR"),leadId:makeId("LD"),createdAt:nowIso(),
    name:"Synthetic Driver",phone:"(555) 010-0000",email:"",company:"DEMO FLEET",
    location:"Synthetic I-80 roadside test location",geo:"",
    assetType:"Semi / Tractor",unit:"DEMO-101",vin:"DEMO-VIN",ymm:"2023 Demo Tractor",
    problem:"Air / Brake",loaded:"Yes",preferred:"Phone Call",
    symptoms:"Synthetic air-pressure loss used only to test the private workflow.",
    faultCodes:"DEMO-CODE",safety:"Synthetic safe shoulder for prototype testing.",
    photoCount:0,photoNames:[],status:"NEW",jobId:"",dispatchId:"",
    events:[{at:nowIso(),type:"created",oldState:"",newState:"NEW",summary:"Synthetic end-to-end test record created"}]
  });
  saveJson(REQUESTS_KEY,items); renderDispatch();
});

$("#clearDemo").addEventListener("click",()=>{
  if(confirm("Clear only local private demo requests in this browser?")){
    localStorage.removeItem(REQUESTS_KEY); renderDispatch();
  }
});

$("#fleetForm").addEventListener("submit",e=>{
  e.preventDefault(); const fd=new FormData(e.currentTarget);
  const lead={id:makeId("FL"),createdAt:nowIso(),company:fd.get("company"),contact:fd.get("contact"),
    phone:fd.get("phone"),email:fd.get("email"),yard:fd.get("yard"),tractors:fd.get("tractors"),
    trailers:fd.get("trailers"),needs:fd.get("needs"),status:"TARGET / INTAKE"};
  const items=getJson(FLEET_KEY); items.unshift(lead); saveJson(FLEET_KEY,items);
  const result=$("#fleetResult"); result.hidden=false;
  result.innerHTML=`<b>Demo fleet lead created:</b> ${esc(lead.id)}<br>No outreach, pricing or account terms were sent.`;
  e.currentTarget.reset(); renderFleet();
});

function renderFleet(){
  const items=getJson(FLEET_KEY),root=$("#fleetList");
  if(!items.length){root.innerHTML='<div class="empty">No demo fleet leads yet.</div>';return;}
  root.innerHTML=items.map(x=>`<article><b>${esc(x.company)}</b><span>${esc(x.contact)} • ${esc(x.phone)}</span><small>${esc(x.tractors||0)} tractors • ${esc(x.trailers||0)} trailers • ${esc(x.status)}</small><p>${esc(x.needs)}</p></article>`).join("");
}


function renderBenchmarks(){
  const root=$("#benchmarkGrid");
  if(!root) return;
  const items=window.RRR_DATA?.benchmarks||[];
  root.innerHTML=items.map(b=>'<article class="truth-card pending"><b>'+esc(b.label)+'</b><span>'+esc(b.value)+'</span><small>'+esc(b.range||"PRIVATE BENCHMARK")+'</small><p class="job-meta">'+esc(b.note||"")+'</p></article>').join("");
}

function calculateBenchmark(){
  const cfg=window.RRR_DATA?.benchmarkCalculator||{};
  const hours=Math.max(Number($("#bmHours")?.value||0),Number(cfg.laborMinimumHours||0));
  const miles=Math.max(Number($("#bmMiles")?.value||0),0);
  const partsCost=Math.max(Number($("#bmParts")?.value||0),0);
  const after=$("#bmAfter")?.value==="after";
  const call=after?Number(cfg.afterHoursCall||0):Number(cfg.serviceCall||0);
  const labor=hours*Number(cfg.laborHourly||0);
  const travel=miles*Number(cfg.mileageRate||0);
  const parts=partsCost*(1+(Number(cfg.partsMarkupPct||0)/100));
  const total=call+labor+travel+parts;
  const result=$("#bmResult");
  if(!result) return;
  result.hidden=false;
  result.innerHTML="<b>PRIVATE BENCHMARK MODEL:</b> $"+total.toFixed(2)+"<br>Service call: $"+call.toFixed(2)+"<br>Labor: $"+labor.toFixed(2)+"<br>Travel: $"+travel.toFixed(2)+"<br>Parts with benchmark markup: $"+parts.toFixed(2)+"<br><small>Not a quote, invoice, or approved Rapid Roadside Repair rate.</small>";
}

renderServices();
renderBenchmarks();
renderTruth();
renderDispatch();
renderFleet();
$("#bmCalc")?.addEventListener("click",calculateBenchmark);
