import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {handleEditor} from '../src/api/task-editor.js';
const secret = 'A'.repeat(48);
const env = {
  DEBO_TASK_EDITOR_ENABLED:'true',
  DEBO_EDITOR_ALLOWED_ORIGIN:'https://debo-private-command-r55-claimedge.vercel.app',
  DEBO_EDITOR_KEY_SHA256: createHash('sha256').update(secret).digest('hex'),
  DEBO_NEON_EDITOR_DSN:'REDACTED-TEST-ONLY',
  DEBO_EDITOR_ACTOR:'DEBO_OWNER'
};
function makeReq(overrides={}) {
 return {method:'POST',headers:{origin:env.DEBO_EDITOR_ALLOWED_ORIGIN,'sec-fetch-site':'same-origin','x-debo-editor-key':secret,'content-type':'application/json','idempotency-key':'3fddbd83-1b3e-40b2-bf55-312b2f0967b6'},body:{task_id:'DEBO-LOCAL-TEST-001',fields:{title:'Demo Task',status:'Backlog',priority:'P2',assignee_role:'Mack',pillar:'DEBO'}},...overrides};
}
function makeRes(){return{code:0,body:null,headers:{},setHeader(k,v){this.headers[k]=v;return this},status(n){this.code=n;return this},json(obj){this.body=obj;return obj}}}
async function run(overrides={},opts={}){const res=makeRes();let calls=0;const sql=async()=>{calls++;return[{result:{task_id:'DEBO-LOCAL-TEST-001',revision:0,archived:false}}]};await handleEditor(makeReq(overrides),res,{env:{...env,...(opts.env||{})},sql:opts.sql||sql});return {...res,calls}}
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
