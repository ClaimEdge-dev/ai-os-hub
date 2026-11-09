import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import {handleEditor} from '../src/api/task-editor.js';
const secret = 'A'.repeat(48);
// Synthetic fixture values: generated in tests, never credentials.
const idempotencyFixture = 'test-' + '0'.repeat(32);
const env = {
  DEBO_TASK_EDITOR_ENABLED:'true',
  DEBO_EDITOR_ALLOWED_ORIGIN:'https://debo-private-command-r55-claimedge.vercel.app',
  DEBO_EDITOR_KEY_SHA256: createHash('sha256').update(secret).digest('hex'),
  DEBO_NEON_EDITOR_DSN:'REDACTED-TEST-ONLY',
  DEBO_EDITOR_ACTOR:'DEBO_OWNER'
};
function makeReq(overrides={}) {
 return {method:'POST',headers:{origin:env.DEBO_EDITOR_ALLOWED_ORIGIN,'sec-fetch-site':'same-origin','x-debo-editor-key':secret,'content-type':'application/json','idempotency-key':idempotencyFixture},body:{task_id:'DEBO-LOCAL-TEST-001',fields:{title:'Demo Task',status:'Backlog',priority:'P2',assignee_role:'Mack',pillar:'DEBO'}},...overrides};
}
function makeRes(){return{code:0,body:null,headers:{},setHeader(k,v){this.headers[k]=v;return this},status(n){this.code=n;return this},json(obj){this.body=obj;return obj},end(){this.body=null;return this}}}
async function run(overrides={},opts={}){
 const res=makeRes(),req=makeReq(overrides);let calls=0;
 const sql=async()=>{
  calls++;
  return [{result:{
   task_id:req.body.task_id,
   action:{POST:'create',PATCH:'update',DELETE:'archive'}[req.method],
   revision:req.method==='POST'?0:req.body.expected_revision+1,
   archived:req.method==='DELETE'
  }}];
 };
 await handleEditor(req,res,{env:{...env,...(opts.env||{})},sql:opts.sql||sql});
 return {...res,calls};
}
test('disabled editor rejects changes without database call',async()=>{const r=await run({}, {env:{DEBO_TASK_EDITOR_ENABLED:'false'}});assert.equal(r.code,503);assert.equal(r.calls,0)});
test('authenticated new local task may use transactional function',async()=>{const r=await run();assert.equal(r.code,201);assert.equal(r.calls,1);assert.equal(r.body.record.revision,0)});
test('wrong key is denied',async()=>{const r=await run({headers:{...makeReq().headers,'x-debo-editor-key':'wrong'}});assert.equal(r.code,403);assert.equal(r.calls,0)});
test('cross-site origin is denied',async()=>{const r=await run({headers:{...makeReq().headers,origin:'https://attacker.example'}});assert.equal(r.code,403);assert.equal(r.calls,0)});
test('missing origin is denied',async()=>{const headers={...makeReq().headers};delete headers.origin;const r=await run({headers});assert.equal(r.code,403)});
test('read-only GET is not allowed on write endpoint',async()=>{const r=await run({method:'GET'});assert.equal(r.code,405)});
test('imported WORK tasks cannot be created',async()=>{const r=await run({body:{...makeReq().body,task_id:'WORK-JCT-001'}});assert.equal(r.code,400)});
test('held rentals task is blocked',async()=>{const r=await run({body:{...makeReq().body,task_id:'WORK-RENTALS-001'}});assert.equal(r.code,400)});
test('update requires revision',async()=>{const r=await run({method:'PATCH',body:makeReq().body});assert.equal(r.code,400)});
test('archive requires revision and is accepted as soft deletion',async()=>{const r=await run({method:'DELETE',body:{task_id:'DEBO-LOCAL-TEST-001',expected_revision:0}});assert.equal(r.code,200)});
test('invalid status rejected',async()=>{const body=makeReq().body;const r=await run({body:{...body,fields:{...body.fields,status:'Launch'}}});assert.equal(r.code,400)});
test('unexpected fields rejected',async()=>{const body=makeReq().body;const r=await run({body:{...body,fields:{...body.fields,is_admin:true}}});assert.equal(r.code,400)});
test('missing idempotency key rejected',async()=>{const headers={...makeReq().headers};delete headers['idempotency-key'];const r=await run({headers});assert.equal(r.code,400)});
test('misconfigured secrets fail-closed',async()=>{const r=await run({}, {env:{DEBO_EDITOR_KEY_SHA256:'invalid'}});assert.equal(r.code,403)});
test('missing editor DSN rejects writes',async()=>{const r=await run({}, {env:{DEBO_NEON_EDITOR_DSN:''}});assert.equal(r.code,503)});
test('database conflict returns sanitized 409',async()=>{const r=await run({}, {sql:async()=>{throw Object.assign(new Error('private task details'),{code:'P0001'})}});assert.equal(r.code,409);assert.ok(!JSON.stringify(r.body).includes('private task'))});
test('unexpected DB error returns sanitized 503',async()=>{const r=await run({}, {sql:async()=>{throw new Error('db secret')}});assert.equal(r.code,503);assert.ok(!JSON.stringify(r.body).includes('db secret'))});
test('missing schema disallowed to client',async()=>{const body=makeReq().body;const r=await run({body:{...body,fields:{...body.fields,status:'Done',meta:'override'}}});assert.equal(r.code,400)});

test('empty SQL result cannot claim write success',async()=>{const r=await run({}, {sql:async()=>[]});assert.equal(r.code,503);assert.equal(r.body.error,'editor_confirmation_unavailable');assert.notEqual(r.body.ok,true)});
test('mismatched task identity is rejected after SQL result',async()=>{const r=await run({}, {sql:async()=>[{result:{task_id:'DEBO-LOCAL-OTHER-001',action:'create',revision:0,archived:false}}]});assert.equal(r.code,503);assert.notEqual(r.body.ok,true)});
test('update must confirm exact next revision',async()=>{const req={method:'PATCH',body:{task_id:'DEBO-LOCAL-TEST-001',expected_revision:2,fields:{status:'Review'}}};const r=await run(req,{sql:async()=>[{result:{task_id:'DEBO-LOCAL-TEST-001',action:'update',revision:2,archived:false}}]});assert.equal(r.code,503);assert.notEqual(r.body.ok,true)});
test('archive must confirm archived flag and revision',async()=>{const req={method:'DELETE',body:{task_id:'DEBO-LOCAL-TEST-001',expected_revision:1}};const r=await run(req,{sql:async()=>[{result:{task_id:'DEBO-LOCAL-TEST-001',action:'archive',revision:2,archived:false}}]});assert.equal(r.code,503);assert.notEqual(r.body.ok,true)});

test('valid HEAD preflight confirms credential without a database call or mutation',async()=>{
 const r=await run({method:'HEAD'});
 assert.equal(r.code,204);assert.equal(r.body,null);assert.equal(r.calls,0);
});
test('HEAD preflight rejects invalid owner credential without SQL',async()=>{
 const r=await run({method:'HEAD',headers:{...makeReq().headers,'x-debo-editor-key':'wrong'}});
 assert.equal(r.code,403);assert.equal(r.calls,0);
});
test('HEAD preflight fails closed when the editor is not configured',async()=>{
 const r=await run({method:'HEAD'},{env:{DEBO_NEON_EDITOR_DSN:''}});
 assert.equal(r.code,503);assert.equal(r.calls,0);
});

// Minimal native-DOM fixture for checking the preflight gate, no external
// browser, credentials, network, database or deployment.
const widgetSource=readFileSync(new URL('../src/ui/task-editor-widget.js',import.meta.url),'utf8');
function createEditorFixture(preflightStatus) {
 let section;
 const requests=[];
 const element=tag=>({
   tag,children:[],hidden:false,disabled:false,value:'',textContent:'',
   setAttribute(){},append(...nodes){this.children.push(...nodes)},
   prepend(...nodes){this.children.unshift(...nodes)},
   replaceChildren(...nodes){this.children=[...nodes]}
 });
 const refresh={closest(){return {after(node){section=node}}},click(){}};
 const document={
   querySelector(name){return name==='main'?{}:null},
   getElementById(name){return name==='refresh'?refresh:null},
   createElement:element
 };
 const fetch=async(url,opts={})=>{
   requests.push({url,opts});
   if(url==='/api/summary')return {ok:true,status:200,json:async()=>({tasks:[]})};
   return {ok:preflightStatus===204,status:preflightStatus};
 };
 runInNewContext(widgetSource,{document,fetch,crypto:{randomUUID:()=> 'synthetic-only'},window:{confirm:()=>true}});
 return {requests,unlock:section.children[4],lock:section.children[5],
   form:section.children[6],input:section.children[3].children[0],
   status:section.children[2]};
}
test('browser editor remains locked when server rejects the key',async()=>{
 const x=createEditorFixture(403);
 x.input.value='A'.repeat(48);
 await x.unlock.onclick();
 assert.equal(x.form.hidden,true);assert.equal(x.lock.hidden,true);
 assert.equal(x.input.value,'');assert.match(x.status.textContent,/remains locked/);
 assert.equal(x.requests.length,1);
 assert.equal(x.requests[0].opts.method,'HEAD');
 assert.equal(x.requests[0].opts.redirect,'error');
});
test('unexpected successful HTTP 200 cannot unlock owner editor',async()=>{
 const x=createEditorFixture(200);
 x.input.value='A'.repeat(48);
 await x.unlock.onclick();
 assert.equal(x.form.hidden,true);assert.equal(x.requests.length,1);
});
test('confirmed HEAD 204 reveals editor only after server check',async()=>{
 const x=createEditorFixture(204);
 assert.equal(x.form.hidden,true);
 x.input.value='A'.repeat(48);
 await x.unlock.onclick();
 assert.equal(x.form.hidden,false);assert.equal(x.lock.hidden,false);
 assert.equal(x.input.value,'');
 assert.deepEqual(x.requests.map(r=>r.url),['/api/task-editor','/api/summary']);
});
