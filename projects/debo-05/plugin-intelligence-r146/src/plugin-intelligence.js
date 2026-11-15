"use strict";
const rows=Object.freeze(window.DEBO_R146_CATALOG||[]);let visibleLimit=6;
const $=id=>document.getElementById(id);
function render(reset=false){
 if(reset)visibleLimit=6;
 const q=$("searchInput").value.trim().toLowerCase(),cat=$("category").value;
 const filtered=rows.filter(r=>(!cat||r.category===cat)&&(!q||[r.name,r.category,r.feature,r.projects,r.state].join(" ").toLowerCase().includes(q)));
 $("count").textContent=filtered.length+" matches of "+rows.length+" records; showing "+Math.min(visibleLimit,filtered.length);
 const root=$("toolResults");root.replaceChildren();
 for(const r of filtered.slice(0,visibleLimit)){
   const el=document.createElement("article");el.className="tool";
   const heading=document.createElement("h3");heading.textContent=r.name;
   const state=document.createElement("div");state.className="state";state.textContent=r.state;
   const feat=document.createElement("p");feat.textContent=r.feature;
   const projects=document.createElement("p");projects.textContent="Project fit: "+r.projects;
   el.append(heading,state,feat,projects);root.append(el);
 }
 $("more").hidden=filtered.length<=visibleLimit;
}
function makePrompt(){
 const objective=$("task").value.trim()||"Find the next unfinished authorized task";
 return "DEBO START | "+$("project").value+" | "+objective+". Recover canonical DEBO_BOOTSTRAP.md, the relevant runtime brief and latest verified checkpoint. Reuse existing skills and R144 capability matrix; check plugin installation, identity, authorization, costs and callable actions. Execute permitted safe steps, test and read back source evidence, update the existing Thread Index and report one exact next action. Do not replace the Elite v2 compiler or bypass owner/release gates.";
}
$("searchInput").addEventListener("input",()=>render(true));
$("category").addEventListener("change",()=>render(true));
$("more").addEventListener("click",()=>{visibleLimit+=12;render(false);});
$("generate").addEventListener("click",()=>{$("output").value=makePrompt();$("copyStatus").textContent="Prompt ready; no external action performed.";});
$("copy").addEventListener("click",async()=>{if(!$("output").value)$("output").value=makePrompt();
try{await navigator.clipboard.writeText($("output").value);$("copyStatus").textContent="Copied.";}
catch(e){$("output").focus();$("output").select();$("copyStatus").textContent="Copy the highlighted text.";}}
);
$("output").value=makePrompt();render();