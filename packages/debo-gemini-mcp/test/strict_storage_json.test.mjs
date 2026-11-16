// GB-034/035/055: storage JSON must reject duplicate keys even when the
// repeated values leave the canonical SHA unchanged. Synthetic/local D1 only.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { D1ExecutionGate } from '../src/durable_execution_gate.mjs';
import { executionD1, executionInput, executionContext } from './helpers/execution-fixtures.mjs';

const result = { interaction_id:'synthetic-completed', model:'gemini-3.8-flash',
  output:{finding:'PASS'}, usage:{total_input_tokens:20,total_output_tokens:5,total_tokens:25},
  provider_requests:1,billing_verified:false };
test('duplicate stored request key cannot pass canonical JSON hash matching',async t=>{
  const local=executionD1();t.after(local.close);
  const gate=new D1ExecutionGate(local.binding,executionContext);
  const input={...executionInput,idempotency_key:'tampered-request-key'};
  const claimed=await gate.claim(input);assert.equal(claimed.status,'CLAIMED');
  const row=local.database.prepare('SELECT request_json FROM bridge_execution_claims').get();
  const original=JSON.parse(row.request_json);
  const matched='"endpoint":'+JSON.stringify(original.endpoint);
  assert.ok(row.request_json.includes(matched));
  const poisoned=row.request_json.replace(matched,matched+','+matched);
  assert.deepEqual(JSON.parse(poisoned),original); // unchanged semantics under ordinary JSON.parse
  local.database.prepare('UPDATE bridge_execution_claims SET request_json=?1').run(poisoned);
  await assert.rejects(gate.claim(input),e=>e?.code==='RECEIPT_INTEGRITY');
  assert.equal(local.database.prepare('SELECT request_json FROM bridge_execution_claims').get().request_json,poisoned);
});
test('duplicate stored immutable receipt key cannot be replayed, edited or redispatched',async t=>{
  const local=executionD1();t.after(local.close);
  const gate=new D1ExecutionGate(local.binding,executionContext);
  const input={...executionInput,idempotency_key:'tampered-receipt-key'};
  const claimed=await gate.claim(input);
  const receipt=await gate.complete(claimed.claim,result);
  assert.equal(receipt.schema,'debo.gemini.transport_receipt.v1');
  const row=local.database.prepare('SELECT receipt_json FROM bridge_execution_claims').get();
  const matched='"schema":"debo.gemini.transport_receipt.v1"';
  assert.ok(row.receipt_json.includes(matched));
  const poisoned=row.receipt_json.replace(matched,matched+','+matched);
  assert.deepEqual(JSON.parse(poisoned),JSON.parse(row.receipt_json));
  local.database.prepare('UPDATE bridge_execution_claims SET receipt_json=?1').run(poisoned);
  await assert.rejects(gate.claim(input),e=>e?.code==='RECEIPT_INTEGRITY');
  assert.equal(local.database.prepare('SELECT receipt_json FROM bridge_execution_claims').get().receipt_json,poisoned);
  assert.equal(local.database.prepare('SELECT state FROM bridge_execution_claims').get().state,'COMPLETED');
});
