const REQUESTS_KEY="rrr_v5_requests";
const FLEET_KEY="rrr_v5_fleet";
const AUTH_KEY="rrr_v5_authorizations";
const UPDATES_KEY="rrr_v5_customer_updates";
const INVOICE_KEY="rrr_v5_invoices";
const REVIEW_KEY="rrr_v5_reviews";
const PAYMENT_KEY="rrr_v5_payment_links";
const QA_KEY="rrr_v5_qa";
let selectedRequestId="";

const states=["NEW","TRIAGE","DISPATCH READY","ASSIGNED","EN ROUTE","ON SITE","DIAGNOSING","AWAITING AUTHORIZATION","AWAITING PARTS","REPAIR IN PROGRESS","TESTING","COMPLETE","INVOICE READY","INVOICED","PAID","FOLLOW UP","CLOSED"];
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const getJson=k=>{try{return JSON.parse(localStorage.getItem(k)||"[]")}catch{return[]}};
const saveJson=(k,v)=>localStorage.setItem(k,JSON.stringify(v));
const nowIso=()=>new Date().toISOString();
const makeId=p=>p+"-"+new Date().toISOString().slice(0,10).replaceAll("-","")+"-"+Math.random().toString(36).slice(2,6).toUpperCase();
const esc=(v="")=>String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

function showView(name){
  $$(".view").forEach(v=>v.classList.toggle("active",v.id===name));
  if(name==="dispatch") renderOwner();
  if(name==="fleet") renderFleet();
  if(name==="benchmarks") renderBenchmarks();
  if(name==="truth") renderTruth();
  if(name==="track") $("#trackResult").innerHTML="";
  window.scrollTo({top:0,behavior:"smooth"});
}
$$(".jump").forEach(b=>b.addEventListener("click",()=>showView(b.dataset.target)));
$$(".site-anchor").forEach(b=>b.addEventListener("click",()=>{
  showView("preview");
  setTimeout(()=>document.getElementById(b.dataset.scroll)?.scrollIntoView({behavior:"smooth",block:"start"}),100);
}));
$$(".quick-problem").forEach(b=>b.addEventListener("click",()=>{
  showView("request");
  setTimeout(()=>{const s=$("#serviceForm [name=problem]");if(s)s.value=b.dataset.problem||"Other"},80);
}));

function renderServices(){
  const root=$("#serviceCards"); if(!root)return;
  root.innerHTML=(window.RRR_DATA?.services||[]).map(s=>'<article class="service-card"><b>'+esc(s.label)+'</b><span>'+esc(s.description)+'</span><small>'+esc(s.state)+'</small></article>').join("");
}
function renderTruth(){
  const grid=$("#truthGrid"); if(grid)grid.innerHTML=(window.RRR_DATA?.truth||[]).map(t=>'<article class="truth-card"><b>'+esc(t.label)+'</b><span>'+esc(t.value)+'</span><small>'+esc(t.state)+'</small></article>').join("");
  const r=$("#releaseChecks"); if(r)r.innerHTML=(window.RRR_DATA?.releaseChecks||[]).map(x=>'<li><span>□</span>'+esc(x)+'</li>').join("");
}
function renderBenchmarks(){
  const root=$("#benchmarkGrid"); if(!root)return;
  root.innerHTML=(window.RRR_DATA?.benchmarks||[]).map(b=>'<article class="truth-card"><b>'+esc(b.label)+'</b><span>'+esc(b.value)+'</span><small>'+esc(b.range||"PRIVATE BENCHMARK")+'</small><p class="job-meta">'+esc(b.note||"")+'</p></article>').join("");
}
function calcModel(hours,miles,partsCost,after){
  const c=window.RRR_DATA?.benchmarkCalculator||{};
  const h=Math.max(Number(hours||0),Number(c.laborMinimumHours||0));
  const call=after?Number(c.afterHoursCall||0):Number(c.serviceCall||0);
  const labor=h*Number(c.laborHourly||0);
  const travel=Math.max(Number(miles||0),0)*Number(c.mileageRate||0);
  const parts=Math.max(Number(partsCost||0),0)*(1+Number(c.partsMarkupPct||0)/100);
  return {hours:h,call,labor,travel,parts,total:call+labor+travel+parts};
}
function calculateBenchmark(){
  const m=calcModel($("#bmHours")?.value,$("#bmMiles")?.value,$("#bmParts")?.value,$("#bmAfter")?.value==="after");
  const r=$("#bmResult"); if(!r)return;
  r.hidden=false;
  r.innerHTML="<b>PRIVATE BENCHMARK MODEL:</b> $"+m.total.toFixed(2)+"<br>Service call: $"+m.call.toFixed(2)+"<br>Labor: $"+m.labor.toFixed(2)+"<br>Travel: $"+m.travel.toFixed(2)+"<br>Parts with benchmark markup: $"+m.parts.toFixed(2)+"<br><small>Not a quote, invoice, or approved Rapid rate.</small>";
}
$("#bmCalc")?.addEventListener("click",calculateBenchmark);

$("#geoBtn")?.addEventListener("click",()=>{
  const input=$("#serviceForm [name=geo]");
  if(!navigator.geolocation){input.value="Geolocation unavailable";return}
  input.value="Requesting…";
  navigator.geolocation.getCurrentPosition(
    p=>input.value=p.coords.latitude.toFixed(5)+", "+p.coords.longitude.toFixed(5),
    ()=>input.value="Location permission not granted",
    {enableHighAccuracy:true,timeout:8000}
  );
});

function addCustomerUpdate(req,title,message,status){
  const arr=getJson(UPDATES_KEY);
  arr.unshift({id:makeId("UPD"),requestId:req.serviceRequestId,jobId:req.jobId||"",createdAt:nowIso(),title,message,status,sent:false});
  saveJson(UPDATES_KEY,arr);
}
function ensureReview(req){
  if(!["PAID","FOLLOW UP","CLOSED"].includes(req.status))return;
  const arr=getJson(REVIEW_KEY);
  if(arr.some(x=>x.requestId===req.serviceRequestId))return;
  arr.unshift({id:makeId("REV"),requestId:req.serviceRequestId,jobId:req.jobId||"",createdAt:nowIso(),status:"HOLD",eligible:true,reviewLink:"TBD",sent:false});
  saveJson(REVIEW_KEY,arr);
}
function requestStatusMessage(status){
  const map={
    "NEW":"Request received. Dispatch review is pending.",
    "TRIAGE":"Rapid is reviewing the breakdown details.",
    "DISPATCH READY":"The request is ready for technician assignment.",
    "ASSIGNED":"A technician has been assigned.",
    "EN ROUTE":"The technician is en route.",
    "ON SITE":"The technician is on site.",
    "DIAGNOSING":"Diagnosis is in progress.",
    "AWAITING AUTHORIZATION":"Additional-work authorization is needed.",
    "AWAITING PARTS":"The job is waiting on parts or vendor support.",
    "REPAIR IN PROGRESS":"Repair work is in progress.",
    "TESTING":"The repair is being tested.",
    "COMPLETE":"Repair work is marked complete.",
    "INVOICE READY":"Documentation is complete and the invoice is being prepared.",
    "INVOICED":"The job has been invoiced.",
    "PAID":"Payment is recorded.",
    "FOLLOW UP":"Rapid is in follow-up / closeout.",
    "CLOSED":"The job is closed."
  };
  return map[status]||status;
}

$("#serviceForm")?.addEventListener("submit",async e=>{
  e.preventDefault();
  const form=e.currentTarget,fd=new FormData(form),files=[...(form.querySelector("[name=photos]")?.files||[])];
  const req={
    serviceRequestId:makeId("SR"),leadId:makeId("LD"),createdAt:nowIso(),
    name:fd.get("name"),phone:fd.get("phone"),email:fd.get("email"),company:fd.get("company"),
    location:fd.get("location"),geo:fd.get("geo"),assetType:fd.get("assetType"),unit:fd.get("unit"),
    vin:fd.get("vin"),ymm:fd.get("ymm"),problem:fd.get("problem"),loaded:fd.get("loaded"),
    preferred:fd.get("preferred"),symptoms:fd.get("symptoms"),faultCodes:fd.get("faultCodes"),
    safety:fd.get("safety"),photoCount:files.length,photoNames:files.map(f=>f.name),
    status:"NEW",jobId:"",dispatchId:"",events:[{at:nowIso(),type:"created",newState:"NEW",summary:"Private V5 request created"}]
  };
  const submit=form.querySelector('button[type="submit"]'),result=$("#submitResult");
  submit.disabled=true; submit.textContent="CREATING…"; result.hidden=false;
  try{
    const mirror=window.RRR_BACKEND?await window.RRR_BACKEND.mirrorServiceRequest(req):{mirrored:false};
    const items=getJson(REQUESTS_KEY);items.unshift(req);saveJson(REQUESTS_KEY,items);
    addCustomerUpdate(req,"Request received",requestStatusMessage("NEW"),"NEW");
    result.innerHTML="<b>Demo request created:</b> "+esc(req.serviceRequestId)+"<br>Status: NEW • Photos noted: "+req.photoCount+"<br>"+(mirror.mirrored?"Mirrored to configured test backend.":"Local private-demo mode.")+"<br><button class='button secondary' id='trackNow'>TRACK THIS REQUEST</button>";
    form.reset();
    setTimeout(()=>$("#trackNow")?.addEventListener("click",()=>{
      showView("track");
      $("#trackForm [name=requestId]").value=req.serviceRequestId;
      $("#trackForm [name=phone]").value=req.phone;
      renderTracked(req);
    }),0);
  }catch(err){result.innerHTML="<b>Backend not used.</b><br>"+esc(err.message||String(err))}
  finally{submit.disabled=false;submit.textContent="CREATE DEMO SERVICE REQUEST"}
});

function updateStatus(id,newState){
  const items=getJson(REQUESTS_KEY),req=items.find(x=>x.serviceRequestId===id);if(!req)return;
  const old=req.status;req.status=newState;
  if(!req.dispatchId&&["DISPATCH READY","ASSIGNED","EN ROUTE","ON SITE"].includes(newState))req.dispatchId=makeId("DP");
  if(!req.jobId&&["ASSIGNED","EN ROUTE","ON SITE","DIAGNOSING","AWAITING AUTHORIZATION","AWAITING PARTS","REPAIR IN PROGRESS","TESTING","COMPLETE","INVOICE READY","INVOICED","PAID","FOLLOW UP","CLOSED"].includes(newState))req.jobId=makeId("JOB");
  req.events=req.events||[];req.events.push({at:nowIso(),type:"status_changed",oldState:old,newState,summary:requestStatusMessage(newState)});
  saveJson(REQUESTS_KEY,items);
  addCustomerUpdate(req,newState.replaceAll("_"," "),requestStatusMessage(newState),newState);
  ensureReview(req);renderOwner();
}
function eventHtml(req){return (req.events||[]).slice(-5).reverse().map(e=>'<li><b>'+esc(e.newState||e.type)+'</b><span>'+new Date(e.at).toLocaleString()+'</span></li>').join("")}

function renderDispatch(){
  const items=getJson(REQUESTS_KEY);
  $("#statOpen").textContent=items.filter(x=>x.status!=="CLOSED").length;
  $("#statAuth").textContent=items.filter(x=>x.status==="AWAITING AUTHORIZATION").length;
  $("#statInvoice").textContent=items.filter(x=>x.status==="INVOICE READY").length;
  $("#statClosed").textContent=items.filter(x=>x.status==="CLOSED").length;
  const root=$("#dispatchList");
  if(!items.length){root.innerHTML='<div class="panel">No demo requests yet. Create one from Request Service or load the synthetic test.</div>';return}
  root.innerHTML=items.map(req=>{
    const buttons=states.map(s=>'<button data-state="'+esc(s)+'" data-id="'+esc(req.serviceRequestId)+'">'+esc(s)+'</button>').join("");
    return '<article class="job-card"><div class="job-top"><div><div class="job-id">'+esc(req.serviceRequestId)+'</div><div class="job-meta">'+esc(req.assetType)+' • Unit '+esc(req.unit||"TBD")+' • '+esc(req.location)+'</div></div><span class="status-pill">'+esc(req.status)+'</span></div><div class="job-symptoms"><b>'+esc(req.problem)+'</b><br>'+esc(req.symptoms)+'</div><div class="job-grid"><div><small>CUSTOMER</small><span>'+esc(req.name)+' • '+esc(req.phone)+'</span></div><div><small>COMPANY</small><span>'+esc(req.company||"—")+'</span></div><div><small>JOB</small><span>'+esc(req.jobId||"Not opened")+'</span></div><div><small>DISPATCH</small><span>'+esc(req.dispatchId||"Not opened")+'</span></div><div><small>FAULT / WARNING</small><span>'+esc(req.faultCodes||"—")+'</span></div><div><small>PHOTOS</small><span>'+esc(req.photoCount||0)+'</span></div></div><details><summary>Recent event ledger</summary><ul class="event-list">'+eventHtml(req)+'</ul></details><div class="job-actions"><button class="button mini desk-open" data-id="'+esc(req.serviceRequestId)+'">JOB DESK</button></div><div class="state-row">'+buttons+'</div></article>';
  }).join("");
  $$(".state-row button",root).forEach(b=>b.addEventListener("click",()=>updateStatus(b.dataset.id,b.dataset.state)));
  $$(".desk-open",root).forEach(b=>b.addEventListener("click",()=>openDesk(b.dataset.id)));
}

$("#seedDemo")?.addEventListener("click",()=>{
  const items=getJson(REQUESTS_KEY);
  const req={serviceRequestId:makeId("SR"),leadId:makeId("LD"),createdAt:nowIso(),name:"Synthetic Driver",phone:"(555) 010-0000",email:"",company:"DEMO FLEET",location:"Synthetic I-80 roadside test location",geo:"",assetType:"Semi / Tractor",unit:"DEMO-101",vin:"DEMO-VIN",ymm:"2023 Demo Tractor",problem:"Air / Brake",loaded:"Yes",preferred:"Phone Call",symptoms:"Synthetic air-pressure loss used only to test V5.",faultCodes:"DEMO-CODE",safety:"Synthetic safe shoulder.",photoCount:0,photoNames:[],status:"NEW",jobId:"",dispatchId:"",events:[{at:nowIso(),type:"created",newState:"NEW",summary:"Synthetic V5 test created"}]};
  items.unshift(req);saveJson(REQUESTS_KEY,items);addCustomerUpdate(req,"Request received",requestStatusMessage("NEW"),"NEW");renderOwner();
});
$("#clearDemo")?.addEventListener("click",()=>{if(confirm("Clear private V5 demo data in this browser?")){[REQUESTS_KEY,FLEET_KEY,AUTH_KEY,UPDATES_KEY,INVOICE_KEY,REVIEW_KEY,PAYMENT_KEY].forEach(k=>localStorage.removeItem(k));selectedRequestId="";renderOwner()}});

function renderTracked(req){
  const root=$("#trackResult"),updates=getJson(UPDATES_KEY).filter(x=>x.requestId===req.serviceRequestId).sort((a,b)=>a.createdAt.localeCompare(b.createdAt));
  const auths=getJson(AUTH_KEY).filter(x=>x.requestId===req.serviceRequestId);
  const invoice=getJson(INVOICE_KEY).find(x=>x.requestId===req.serviceRequestId);
  const pending=auths.find(x=>x.status==="PENDING");
  root.innerHTML='<div class="track-card"><div class="track-head"><div><small>REQUEST</small><b>'+esc(req.serviceRequestId)+'</b></div><span class="status-pill">'+esc(req.status)+'</span></div><p>'+esc(requestStatusMessage(req.status))+'</p><div class="track-timeline">'+updates.map(u=>'<div><span></span><p><b>'+esc(u.title)+'</b><small>'+new Date(u.createdAt).toLocaleString()+' • '+esc(u.message)+'</small></p></div>').join("")+'</div>'+(pending?'<div class="auth-customer"><b>AUTHORIZATION NEEDED</b><p>'+esc(pending.work)+'</p><strong>$'+Number(pending.amount||0).toFixed(2)+'</strong><div><button class="button primary auth-decision" data-id="'+esc(pending.id)+'" data-decision="APPROVED">APPROVE DEMO</button><button class="button danger auth-decision" data-id="'+esc(pending.id)+'" data-decision="DECLINED">DECLINE</button></div></div>':'')+(invoice?'<div class="invoice-customer"><b>PRIVATE INVOICE MODEL</b><span>$'+Number(invoice.total).toFixed(2)+' • '+esc(invoice.status)+'</span><small>No payment processor is connected.</small></div>':'')+'</div>';
  $$(".auth-decision",root).forEach(b=>b.addEventListener("click",()=>decideAuthorization(b.dataset.id,b.dataset.decision)));
}
$("#trackForm")?.addEventListener("submit",e=>{
  e.preventDefault();const fd=new FormData(e.currentTarget),id=String(fd.get("requestId")||"").trim(),phone=String(fd.get("phone")||"").trim();
  const req=getJson(REQUESTS_KEY).find(x=>x.serviceRequestId===id&&x.phone===phone);
  if(!req){$("#trackResult").innerHTML='<div class="notice">No matching private demo request found in this browser.</div>';return}
  renderTracked(req);
});

function openDesk(id){
  selectedRequestId=id;const req=getJson(REQUESTS_KEY).find(x=>x.serviceRequestId===id);if(!req)return;
  $("#deskJobLabel").textContent=req.jobId||req.serviceRequestId;
  $("#jobDeskEmpty").hidden=true;$("#jobDesk").hidden=false;
  $("#deskSummary").innerHTML='<b>'+esc(req.problem)+'</b><span>'+esc(req.assetType)+' • '+esc(req.unit||"TBD")+' • '+esc(req.location)+'</span><small>'+esc(req.status)+' • '+esc(req.name)+'</small>';
  const invoice=getJson(INVOICE_KEY).find(x=>x.requestId===id);$("#invoiceResult").innerHTML=invoice?invoiceHtml(invoice):"";
  const pending=getJson(AUTH_KEY).filter(x=>x.requestId===id).slice(-1)[0];$("#authResult").innerHTML=pending?authHtml(pending):"";
}
function authHtml(a){return '<div class="mini-card"><b>'+esc(a.status)+'</b><span>'+esc(a.work)+'</span><small>$'+Number(a.amount||0).toFixed(2)+' • '+esc(a.rateSource)+'</small></div>'}
function invoiceHtml(i){return '<div class="mini-card"><b>$'+Number(i.total).toFixed(2)+'</b><span>'+esc(i.status)+'</span><small>Call $'+i.call.toFixed(2)+' • Labor $'+i.labor.toFixed(2)+' • Travel $'+i.travel.toFixed(2)+' • Parts $'+i.parts.toFixed(2)+'</small></div>'}

$("#createAuth")?.addEventListener("click",()=>{
  const req=getJson(REQUESTS_KEY).find(x=>x.serviceRequestId===selectedRequestId);if(!req){$("#authResult").innerHTML="Select a job first.";return}
  const a={id:makeId("AUTH"),requestId:req.serviceRequestId,jobId:req.jobId||"",createdAt:nowIso(),work:$("#authWork").value||"Additional work",amount:Number($("#authAmount").value||0),rateSource:"PRIVATE BENCHMARK / HOLD",status:"PENDING"};
  const arr=getJson(AUTH_KEY);arr.push(a);saveJson(AUTH_KEY,arr);
  if(req.status!=="AWAITING AUTHORIZATION")updateStatus(req.serviceRequestId,"AWAITING AUTHORIZATION");
  $("#authResult").innerHTML=authHtml(a);renderOwner();
});
function decideAuthorization(id,decision){
  const arr=getJson(AUTH_KEY),a=arr.find(x=>x.id===id);if(!a)return;a.status=decision;a.decisionAt=nowIso();saveJson(AUTH_KEY,arr);
  const reqs=getJson(REQUESTS_KEY),req=reqs.find(x=>x.serviceRequestId===a.requestId);
  if(req){req.events=req.events||[];req.events.push({at:nowIso(),type:"authorization_decision",newState:decision,summary:"Customer "+decision.toLowerCase()+" demo authorization"});if(decision==="APPROVED")req.status="REPAIR IN PROGRESS";saveJson(REQUESTS_KEY,reqs);addCustomerUpdate(req,"Authorization "+decision.toLowerCase(),"Additional work was "+decision.toLowerCase()+".",req.status)}
  renderOwner();if($("#trackResult")?.innerHTML&&req)renderTracked(req);
}
$("#buildInvoice")?.addEventListener("click",()=>{
  const req=getJson(REQUESTS_KEY).find(x=>x.serviceRequestId===selectedRequestId);if(!req){$("#invoiceResult").innerHTML="Select a job first.";return}
  const m=calcModel($("#invHours").value,$("#invMiles").value,$("#invParts").value,$("#invAfter").value==="after");
  const inv={id:makeId("INV"),requestId:req.serviceRequestId,jobId:req.jobId||"",createdAt:nowIso(),...m,status:"PRIVATE BENCHMARK / HOLD"};
  let arr=getJson(INVOICE_KEY);arr=arr.filter(x=>x.requestId!==req.serviceRequestId);arr.push(inv);saveJson(INVOICE_KEY,arr);
  $("#invoiceResult").innerHTML=invoiceHtml(inv)+'<button id="markInvoiceReady" class="button mini">MARK INVOICE READY</button><button id="createPaymentLink" class="button mini secondary">CREATE DEMO PAYMENT LINK</button>';
  $("#markInvoiceReady").addEventListener("click",()=>updateStatus(req.serviceRequestId,"INVOICE READY"));
  $("#createPaymentLink").addEventListener("click",()=>createPaymentLink(req,inv));
  renderOwner();
});
function createPaymentLink(req,inv){
  const arr=getJson(PAYMENT_KEY);
  if(!arr.some(x=>x.invoiceId===inv.id))arr.unshift({id:makeId("PAY"),invoiceId:inv.id,requestId:req.serviceRequestId,amount:inv.total,provider:"NOT CONNECTED",status:"HOLD",createdAt:nowIso()});
  saveJson(PAYMENT_KEY,arr);renderOwner();openDesk(req.serviceRequestId);
}

$("#fleetForm")?.addEventListener("submit",e=>{
  e.preventDefault();const fd=new FormData(e.currentTarget);
  const lead={id:makeId("FL"),createdAt:nowIso(),company:fd.get("company"),contact:fd.get("contact"),phone:fd.get("phone"),email:fd.get("email"),yard:fd.get("yard"),tractors:Number(fd.get("tractors")||0),trailers:Number(fd.get("trailers")||0),needs:fd.get("needs"),status:"TARGET / INTAKE",pmDue:0,openJobs:0};
  const arr=getJson(FLEET_KEY);arr.unshift(lead);saveJson(FLEET_KEY,arr);$("#fleetResult").hidden=false;$("#fleetResult").innerHTML="<b>Demo fleet lead created:</b> "+esc(lead.id)+"<br>No outreach or account terms were sent.";e.currentTarget.reset();renderFleet();renderOwner();
});
function renderFleet(){
  const arr=getJson(FLEET_KEY),root=$("#fleetList");if(!root)return;
  root.innerHTML=arr.length?arr.map(x=>'<article><b>'+esc(x.company)+'</b><span>'+esc(x.contact)+' • '+esc(x.phone)+'</span><small>'+x.tractors+' tractors • '+x.trailers+' trailers • '+esc(x.status)+'</small><p>'+esc(x.needs)+'</p></article>').join(""):'<div class="empty-state">No demo fleet leads yet.</div>';
}
function renderOwner(){
  renderDispatch();
  const updates=getJson(UPDATES_KEY).slice(0,8),fleet=getJson(FLEET_KEY),reviews=getJson(REVIEW_KEY),payments=getJson(PAYMENT_KEY);
  $("#customerUpdatesList").innerHTML=updates.length?updates.map(x=>'<article><b>'+esc(x.title)+'</b><span>'+esc(x.requestId)+' • '+esc(x.status)+'</span><small>'+esc(x.message)+'</small></article>').join(""):'<div class="empty-state">No demo customer updates yet.</div>';
  $("#fleetPortalList").innerHTML=fleet.length?fleet.map(x=>'<article><b>'+esc(x.company)+'</b><span>'+x.tractors+' tractors • '+x.trailers+' trailers</span><small>Portal: PRIVATE DEMO • PM due '+(x.pmDue||0)+' • Open jobs '+(x.openJobs||0)+'</small></article>').join(""):'<div class="empty-state">No demo fleet accounts yet.</div>';
  $("#reviewQueueList").innerHTML=reviews.length?reviews.map(x=>'<article><b>'+esc(x.id)+'</b><span>'+esc(x.requestId)+' • '+esc(x.status)+'</span><small>Review link: '+esc(x.reviewLink||"TBD")+' • Sent: '+(x.sent?"YES":"NO")+'</small></article>').join(""):'<div class="empty-state">Review queue is empty.</div>';
  $("#paymentLinkList").innerHTML=payments.length?payments.map(x=>'<article><b>'+esc(x.id)+'</b><span>$'+Number(x.amount).toFixed(2)+' • '+esc(x.status)+'</span><small>Provider: '+esc(x.provider)+' • No real URL created</small></article>').join(""):'<div class="empty-state">No payment links. Processor remains disconnected.</div>';
  const qa=[
    ["Customer Site","PASS"],["Request Service","PASS"],["Dispatch / Events","PASS"],["Authorization Demo","PASS"],
    ["Invoice Benchmark","PASS"],["Customer Tracking","PASS"],["Secure Photo Upload","HOLD"],["Real Payment Link","HOLD"],["Fleet Auth","HOLD"],["Public Release","HOLD"]
  ];
  $("#qaList").innerHTML=qa.map(x=>'<article><b>'+x[0]+'</b><span class="'+(x[1]==="PASS"?"qa-pass":"qa-hold")+'">'+x[1]+'</span></article>').join("");
  if(selectedRequestId)openDesk(selectedRequestId);
}

renderServices();renderBenchmarks();renderTruth();renderFleet();renderOwner();
