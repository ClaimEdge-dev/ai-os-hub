// GB-044 integrated phase evidence, staged executor only; no outbound Gemini.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createStagedSyntheticExecutor } from '../src/guarded_interaction.mjs';
import { executionD1, executionInput, executionContext } from './helpers/execution-fixtures.mjs';
const credential='SYNTHETIC_TEST_CREDENTIAL_NOT_REAL';
const fake=()=>new Response('{}',{headers:{'content-type':'application/json'}});
function build(local, extras={}) {
  return createStagedSyntheticExecutor({enabled:true,binding:local.binding,context:executionContext,
    authorizeRequest:async()=>true,transportOptions:{apiKey:credential,fetchImpl:async()=>fake()},...extras});
}
const uncertain={status:'UNCERTAIN',code:'EXECUTION_UNCERTAIN'};
test('pre-dispatch denied after durable claim records NEVER_DISPATCHED, still UNCERTAIN',async t=>{
  const d=executionD1();t.after(d.close);
  let calls=0;const observed=[];
  const ex=build(d,{authorizeRequest:async x=>x.phase==='before_claim',
    recordAttemptEvidence:o=>observed.push(o),
    transportOptions:{apiKey:credential,fetchImpl:async()=>{calls++;return fake();}}});
  assert.deepEqual(await ex.execute(executionInput),uncertain);
  assert.equal(calls,0);
  assert.equal(observed.length,1);
  assert.equal(observed[0].phase,'FAILED_BEFORE_PROVIDER_ENTRY');
  assert.equal(observed[0].provider_outcome,'NO_PROVIDER_DISPATCH_OBSERVED_IN_THIS_PROCESS');
  assert.equal(observed[0].storage_assurance,'ACKNOWLEDGED');
  assert.equal(observed[0].automatic_retry_allowed,false);
  assert.equal(d.database.prepare('SELECT state FROM bridge_execution_claims').get().state,'UNCERTAIN');
});
test('provider fetch entry before thrown transport error remains UNKNOWN and no automatic retry',async t=>{
  const d=executionD1();t.after(d.close);
  let calls=0;const observed=[];
  const ex=build(d,{recordAttemptEvidence:o=>observed.push(o),
    transportOptions:{apiKey:credential,fetchImpl:async()=>{calls++;throw Error('synthetic network');}}});
  assert.deepEqual(await ex.execute(executionInput),uncertain);
  assert.equal(calls,1);
  assert.equal(observed[0]?.provider_outcome,'UNKNOWN_AFTER_PROVIDER_ENTRY');
  assert.equal(observed[0]?.phase,'FAILED_AFTER_PROVIDER_ENTRY');
  assert.equal(observed[0]?.claim_replacement_allowed,false);
  assert.equal((await ex.execute(executionInput)).status,'UNCERTAIN');
  assert.equal(calls,1);
});
test('lost claim acknowledgement remains UNKNOWN storage even without provider dispatch',async t=>{
  const d=executionD1();t.after(d.close);
  let calls=0;const observed=[];
  const binding={withSession(constraint) {
    const real=d.binding.withSession(constraint);
    return {prepare(sql) {
      const stmt=real.prepare(sql);
      if(!sql.startsWith('INSERT INTO bridge_execution_claims'))return stmt;
      return {bind(...values){
        const q=stmt.bind(...values);return {first:async()=>{await q.first();throw Error('lost DB ack');}};
      }};
    }};
  }};
  const ex=build(d,{binding,recordAttemptEvidence:o=>observed.push(o),
    transportOptions:{apiKey:credential,fetchImpl:async()=>{calls++;return fake();}}});
  assert.deepEqual(await ex.execute(executionInput),uncertain);
  assert.equal(calls,0);
  assert.equal(observed[0]?.storage_assurance,'UNKNOWN');
  assert.equal(observed[0]?.automatic_retry_allowed,false);
});
test('diagnostic callback failure cannot alter claim, retry, or redact errors improperly',async t=>{
  const d=executionD1();t.after(d.close);
  let calls=0;
  const ex=build(d,{recordAttemptEvidence:()=>{throw Error('private:diagnostics');},
    authorizeRequest:async x=>x.phase==='before_claim',
    transportOptions:{apiKey:credential,fetchImpl:async()=>{calls++;return fake();}}});
  const result=await ex.execute(executionInput);
  assert.deepEqual(result,uncertain);
  assert.equal(JSON.stringify(result).includes('private:'),false);
  assert.equal(calls,0);
});
test('invalid diagnostic injection cannot enable transport',t=>{
  const d=executionD1();t.after(d.close);
  assert.throws(()=>build(d,{recordAttemptEvidence:{allow:true}}),e=>e?.code==='CONFIGURATION_REQUIRED');
});
