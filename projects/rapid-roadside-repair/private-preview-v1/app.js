const STORAGE_KEY = "rrr_private_demo_requests_v1";

const states = [
  "NEW","TRIAGE","DISPATCH READY","ASSIGNED","EN ROUTE","ON SITE",
  "DIAGNOSING","AWAITING AUTHORIZATION","AWAITING PARTS",
  "REPAIR IN PROGRESS","TESTING","COMPLETE","INVOICE READY","CLOSED"
];

const $ = (sel, root=document) => root.querySelector(sel);
const $$ = (sel, root=document) => [...root.querySelectorAll(sel)];

function getRequests(){
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); }
  catch { return []; }
}
function saveRequests(items){ localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); }
function nowIso(){ return new Date().toISOString(); }
function makeId(prefix){
  const d = new Date();
  const ds = d.toISOString().slice(0,10).replaceAll("-","");
  return prefix + "-" + ds + "-" + Math.random().toString(36).slice(2,6).toUpperCase();
}
function esc(v=""){ return String(v).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }

function showView(name){
  $$(".view").forEach(v => v.classList.toggle("active", v.id === name));
  $$(".tab").forEach(t => t.classList.toggle("active", t.dataset.view === name));
  if(name === "dispatch") renderDispatch();
}
$$(".tab").forEach(t => t.addEventListener("click", () => showView(t.dataset.view)));

$("#serviceForm").addEventListener("submit", e => {
  e.preventDefault();
  const fd = new FormData(e.currentTarget);
  const request = {
    serviceRequestId: makeId("SR"),
    leadId: makeId("LD"),
    createdAt: nowIso(),
    name: fd.get("name"),
    phone: fd.get("phone"),
    company: fd.get("company"),
    location: fd.get("location"),
    assetType: fd.get("assetType"),
    unit: fd.get("unit"),
    problem: fd.get("problem"),
    loaded: fd.get("loaded"),
    symptoms: fd.get("symptoms"),
    faultCodes: fd.get("faultCodes"),
    safety: fd.get("safety"),
    status: "NEW",
    events: [{at: nowIso(), type:"created", oldState:"", newState:"NEW", summary:"Private demo service request created"}]
  };
  const items = getRequests();
  items.unshift(request);
  saveRequests(items);
  const result = $("#submitResult");
  result.hidden = false;
  result.innerHTML = "<b>Demo request created:</b> " + esc(request.serviceRequestId) +
    "<br>Status: NEW. Open the Dispatch Board to move it through the workflow.";
  e.currentTarget.reset();
});

function updateStatus(id, newState){
  const items = getRequests();
  const item = items.find(x => x.serviceRequestId === id);
  if(!item) return;
  const old = item.status;
  item.status = newState;
  item.events = item.events || [];
  item.events.push({at:nowIso(), type:"status_changed", oldState:old, newState, summary:"Private demo workflow state changed"});
  saveRequests(items);
  renderDispatch();
}

function renderDispatch(){
  const items = getRequests();
  $("#statOpen").textContent = items.filter(x => !["CLOSED"].includes(x.status)).length;
  $("#statAuth").textContent = items.filter(x => x.status === "AWAITING AUTHORIZATION").length;
  $("#statInvoice").textContent = items.filter(x => x.status === "INVOICE READY").length;
  $("#statClosed").textContent = items.filter(x => x.status === "CLOSED").length;

  const root = $("#dispatchList");
  if(!items.length){
    root.innerHTML = '<div class="panel">No demo requests yet. Use Request Service to create one.</div>';
    return;
  }
  root.innerHTML = items.map(item => {
    const buttons = states.map(s => '<button data-id="'+esc(item.serviceRequestId)+'" data-state="'+esc(s)+'">'+esc(s)+'</button>').join("");
    return '<article class="job-card">'+
      '<div class="job-top"><div><div class="job-id">'+esc(item.serviceRequestId)+'</div>'+
      '<div class="job-meta">'+esc(item.assetType)+' • Unit '+esc(item.unit || "TBD")+' • '+esc(item.location)+'</div></div>'+
      '<span class="status-pill">'+esc(item.status)+'</span></div>'+
      '<div class="job-symptoms"><b>'+esc(item.problem)+'</b><br>'+esc(item.symptoms)+'</div>'+
      '<div class="job-meta">Customer: '+esc(item.name)+' • '+esc(item.phone)+' • Company: '+esc(item.company || "—")+'</div>'+
      '<div class="job-meta">Fault codes: '+esc(item.faultCodes || "—")+' • Loaded: '+esc(item.loaded || "Unknown")+'</div>'+
      '<div class="state-row" style="margin-top:.8rem">'+buttons+'</div>'+
    '</article>';
  }).join("");

  $$(".state-row button", root).forEach(btn => btn.addEventListener("click", () => updateStatus(btn.dataset.id, btn.dataset.state)));
}

$("#clearDemo").addEventListener("click", () => {
  if(confirm("Clear only the local private demo requests in this browser?")){
    localStorage.removeItem(STORAGE_KEY);
    renderDispatch();
  }
});

renderDispatch();
