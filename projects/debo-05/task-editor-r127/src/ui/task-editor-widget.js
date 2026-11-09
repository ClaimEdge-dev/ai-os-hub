/** In-page editor panel for the EXISTING private DEBO-05 dashboard.
 * Include as script on the existing HTML only after current source recovery.
 * Secret is volatile, not persisted. DELETE means reversible archive.
 */
(function initDeboTaskEditor() {
  'use strict';
  if (!document.querySelector('main') || !document.getElementById('refresh')) return;
  const $ = (tag, content, css) => {
    const e = document.createElement(tag);
    if (content !== undefined) e.textContent = String(content);
    if (css) e.className = css;
    return e;
  };
  const section = $('section', undefined, 'panel');
  section.id = 'task-editor';
  section.setAttribute('aria-labelledby', 'task-editor-heading');
  const heading = $('h2', 'Task editor (owner controlled)');
  heading.id = 'task-editor-heading';
  const help = $('p', 'Create, update, or archive tasks. Imported Work Stack edits require source-owner authorization.');
  const status = $('p', 'Locked. Existing read-only task feed remains available.');
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  const keyLabel = $('label', 'Private editor key');
  const keyInput = $('input'); keyInput.type='password';keyInput.autocomplete='off';keyInput.required=true;
  keyInput.placeholder='Session-only key';keyLabel.append(keyInput);
  const unlock=$('button','Unlock editor');unlock.type='button';
  const lock=$('button','Lock');lock.type='button';lock.hidden=true;
  const form=$('form');form.hidden=true;
  const taskPickLabel=$('label','Existing task / new local task');
  const taskPick=$('select');taskPickLabel.append(taskPick);
  const fields={};
  const controls=[
    ['title','Title','text'],['status','Status','select'],['priority','Priority','select'],
    ['assignee_role','Assigned role','text'],['pillar','Project / pillar','text'],
    ['blocked_reason','Blocker (optional)','text']
  ];
  for(const [name,label,type] of controls) {
    const wrapper=$('label',label);
    const input=$(type==='select'?'select':'input');
    if(type==='select')for(const value of name==='status'
      ?['Backlog','Blocked','In Progress','Review','Done']:['P0','P1','P2','P3']){
      const option=$('option',value);option.value=value;input.append(option);
    }
    else{input.type='text';input.maxLength=name==='title'?200:name==='blocked_reason'?1000:100;}
    wrapper.append(input);form.append(wrapper);fields[name]=input;
  }
  const save=$('button','Save new task');save.type='submit';
  const archive=$('button','Delete (archive and keep audit)');archive.type='button';
  const reload=$('button','Reload task list');reload.type='button';
  form.prepend(taskPickLabel);form.append(save,archive,reload);
  section.append(heading,help,status,keyLabel,unlock,lock,form);
  document.getElementById('refresh').closest('section')?.after(section);
  let editorKey=null;
  let tasks=[];
  function choose(){
    const item=tasks.find(t=>t.id===taskPick.value);
    for(const k of Object.keys(fields))fields[k].value=item
      ?({...item,assignee_role:item.owner,pillar:item.project,blocked_reason:item.blocker||''})[k]||''
      :({status:'Backlog',priority:'P2',pillar:'DEBO',assignee_role:'Mack'})[k]||'';
    save.textContent=item?'Update selected task':'Create local task';
    archive.disabled=!item||!Number.isSafeInteger(item.revision);
    if(item&&!Number.isSafeInteger(item.revision))
      status.textContent='Editing locked: read feed lacks verified editor revision.';
  }
  async function refresh(){
    status.textContent='Loading task versions…';
    try{
      const r=await fetch('/api/summary',{credentials:'same-origin',cache:'no-store'});
      if(!r.ok)throw Error('read source unavailable');
      const data=await r.json();
      tasks=Array.isArray(data.tasks)?data.tasks.filter(t=>t.id!=='WORK-RENTALS-001'):[];
      taskPick.replaceChildren();
      const fresh=$('option','Create new DEBO-local task');fresh.value='';taskPick.append(fresh);
      for(const item of tasks){const o=$('option',item.id+' · '+item.status);o.value=item.id;taskPick.append(o);}
      choose();
      status.textContent='Loaded '+tasks.length+' private tasks; owner holds still apply.';
    }catch{status.textContent='Private source unavailable. No write attempted.';}
  }
  unlock.onclick=async()=>{
    if(keyInput.value.length<32){status.textContent='Editor key must be at least 32 characters.';return;}
    // Never show write controls based only on key length. The isolated server
    // must confirm this exact credential; unexpected 200s and SSO redirects fail.
    const candidate=keyInput.value;keyInput.value='';
    unlock.disabled=true;status.textContent='Checking owner editor access…';
    try{
      const reply=await fetch('/api/task-editor',{
        method:'HEAD',credentials:'same-origin',cache:'no-store',redirect:'error',
        headers:{'X-DEBO-Editor-Key':candidate}
      });
      if(reply.status!==204)throw Error('editor_access_not_confirmed');
      editorKey=candidate;
      keyLabel.hidden=true;unlock.hidden=true;lock.hidden=false;form.hidden=false;
      status.textContent='Editor credential accepted. Source-owner holds still apply.';
      await refresh();
    }catch{
      editorKey=null;form.hidden=true;keyLabel.hidden=false;unlock.hidden=false;lock.hidden=true;
      status.textContent='Editor remains locked. Credential rejected or owner service unavailable.';
    }finally{unlock.disabled=false;}
  };
  lock.onclick=()=>{editorKey=null;form.hidden=true;keyLabel.hidden=false;unlock.hidden=false;lock.hidden=true;status.textContent='Editor key discarded from volatile page memory.';};
  taskPick.onchange=choose;reload.onclick=refresh;
  async function mutate(method,body){
    if(!editorKey){status.textContent='Unlock owner editor first.';return;}
    status.textContent='Submitting audited change…';save.disabled=true;archive.disabled=true;
    try{
      const r=await fetch('/api/task-editor',{method,credentials:'same-origin',headers:{
        'Content-Type':'application/json','X-DEBO-Editor-Key':editorKey,'Idempotency-Key':crypto.randomUUID()
      },body:JSON.stringify(body)});
      const result=await r.json();
      if(!r.ok)throw Error(result.error||'edit_rejected');
      status.textContent='Confirmed '+result.record.action+' for '+result.record.task_id+' revision '+result.record.revision;
      await refresh();
      document.getElementById('refresh')?.click();
    }catch(e){status.textContent='Change not applied: '+String(e.message||'unknown');}
    finally{save.disabled=false;choose();}
  }
  form.onsubmit=async event=>{
    event.preventDefault();
    const old=tasks.find(t=>t.id===taskPick.value);
    if(old&&!Number.isSafeInteger(old.revision)){status.textContent='Stale task version; refresh first.';return;}
    const taskId=old?old.id:'DEBO-LOCAL-'+crypto.randomUUID().replaceAll('-','').slice(0,16).toUpperCase();
    const data={task_id:taskId,fields:{}};
    for(const k of Object.keys(fields))if(fields[k].value.trim())data.fields[k]=fields[k].value.trim();
    if(old)data.expected_revision=old.revision;
    await mutate(old?'PATCH':'POST',data);
  };
  archive.onclick=async()=>{
    const old=tasks.find(t=>t.id===taskPick.value);
    if(!old||!Number.isSafeInteger(old.revision))return;
    if(!window.confirm('Archive '+old.id+'? Task remains recoverable and audited.'))return;
    await mutate('DELETE',{task_id:old.id,expected_revision:old.revision});
  };
})();
