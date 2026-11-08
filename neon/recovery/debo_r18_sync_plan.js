'use strict';
// R18 nonproduction planner. Pure functions; no network, database, or writes.
const crypto = require('node:crypto');
const STATUSES = new Set(['Backlog','In Progress','Blocked','Review','Done']);
const PRIORITIES = new Set(['P0','P1','P2','P3']);
const REQUIRED = ['work_id','project_id','project_name','objective','state','priority','owner'];
const VERSION = 'R18-PRESERVE-1';
const asString = v => v == null ? '' : String(v);
const canonical = row => JSON.stringify(Object.fromEntries(Object.entries(row).sort(([a],[b])=>a.localeCompare(b))));
const hashRow = row => crypto.createHash('sha256').update(canonical(row)).digest('hex');
function parseSheet(rows) {
  if (!Array.isArray(rows)||rows.length===0) throw Error('Missing source rows');
  const headers=rows[0].map(asString);
  for(const key of REQUIRED) if(!headers.includes(key)) throw Error('Missing column: '+key);
  return rows.slice(1).filter(r=>asString(r[headers.indexOf('work_id')]).trim()).map(r=>Object.fromEntries(headers.map((h,i)=>[h,asString(r[i])])));
}
function validateApproval(rule, rawState) {
  return !!rule && rule.raw_state === rawState && STATUSES.has(rule.status)
     && typeof rule.approved_by==='string' && rule.approved_by.trim().length>0
     && /^\d{4}-\d{2}-\d{2}T/.test(asString(rule.approved_at));
}
function plan(rows, approvals={mappings:{}}, source={}) {
  if(!Array.isArray(rows)) throw Error('Rows array required');
  const mappings=approvals.mappings || {};
  const seen=new Set(), entries=[];
  for(const row of rows) {
    const id=asString(row.work_id).trim(),raw=asString(row.state);
    if(!id) throw Error('Missing work_id');
    if(seen.has(id)) throw Error('Duplicate work_id: '+id);
    seen.add(id);
    const full=Object.fromEntries(Object.entries(row).map(([k,v])=>[k,asString(v)]));
    const provenance={
      source_system:'google_drive',source_document_id:asString(source.document_id),
      source_tab:asString(source.tab||'Portfolio Work Stack'),
      work_id:id, raw_source_state:raw,source_row_hash:hashRow(full),
      mapping_rule_version:VERSION
    };
    let decision='QUARANTINE', reason='UNAPPROVED_STATUS_MAPPING', status=null;
    if(id === 'WORK-RENTALS-001' || raw.toUpperCase().includes('PARKED BY OWNER')){decision='HOLD_OWNER';reason='OWNER_PARKED';}
    else if(REQUIRED.some(k=>!asString(row[k]).trim())){decision='REJECT_REQUIRED_FIELDS';reason='MISSING_SOURCE_FIELD';}
    else if(!PRIORITIES.has(row.priority)){decision='REJECT_REQUIRED_FIELDS';reason='INVALID_PRIORITY';}
    else if(validateApproval(mappings[raw],raw)){
      status=mappings[raw].status;
      if(!asString(row.assignee_role).trim()||!asString(row.pillar).trim()){
        decision='REVIEW_FIELD_MAPPING';reason='MISSING_VERIFIED_TARGET_FIELDS';
      } else {decision='ACCEPT';reason='REVIEWED_EXACT_MAPPING';}
    }
    entries.push({task_id:id,decision,reason,status,provenance});
  }
  const counts={total:entries.length,accept:0,quarantine:0,hold_owner:0,reject:0,review_fields:0};
  for(const e of entries){
    if(e.decision==='ACCEPT')counts.accept++;
    else if(e.decision==='QUARANTINE')counts.quarantine++;
    else if(e.decision==='HOLD_OWNER')counts.hold_owner++;
    else if(e.decision==='REVIEW_FIELD_MAPPING')counts.review_fields++;
    else counts.reject++;
  }
  return {version:VERSION,counts,entries,write_eligible:false, note:'Dry-run only. No database mutation.'};
}
function reconcile(previous,planned){
  if(!Array.isArray(previous)||!planned||!Array.isArray(planned.entries)) throw Error('Invalid reconciliation input');
  const existing=new Map();
  for(const x of previous){
    if(!x||!x.work_id||typeof x.source_row_hash!=='string') throw Error('Invalid prior receipt');
    if(existing.has(x.work_id)) throw Error('Duplicate prior work_id: '+x.work_id);
    existing.set(x.work_id,x.source_row_hash);
  }
  return planned.entries.map(x=>{
    if(x.decision==='HOLD_OWNER') return {task_id:x.task_id,operation:'SKIP_OWNER_HOLD'};
    if(x.decision!=='ACCEPT') return {task_id:x.task_id,operation:'SKIP_UNAPPROVED'};
    const old=existing.get(x.task_id);
    return {task_id:x.task_id,operation:old===undefined?'STAGE_NEW':old===x.provenance.source_row_hash?'NOOP':'CONFLICT_REVIEW'};
  });
}
module.exports={VERSION,STATUSES,parseSheet,plan,reconcile,hashRow,validateApproval};
