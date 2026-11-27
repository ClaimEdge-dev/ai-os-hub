// GB-039/057: regression for UTF-8 byte envelope, not JS string length.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { D1ExecutionGate } from '../src/durable_execution_gate.mjs';
import { executionD1, executionInput, executionContext } from './helpers/execution-fixtures.mjs';
const bytes = x => new TextEncoder().encode(x).byteLength;
test('multibyte synthetic request over 48KB is refused before claim', async t => {
  const d = executionD1(); t.after(d.close);
  const input = { ...executionInput, idempotency_key: 'multibyte-request', payload: 'SYNTHETIC:' + '界'.repeat(20000) };
  assert.ok(input.payload.length < 32000 && bytes(input.payload) > 48000);
  await assert.rejects(new D1ExecutionGate(d.binding, executionContext).claim(input), e => e?.code === 'BAD_REQUEST');
  assert.equal(d.database.prepare('SELECT COUNT(*) AS n FROM bridge_execution_claims').get().n, 0);
});
test('multibyte synthetic receipt over 48KB cannot persist completed', async t => {
  const d = executionD1(); t.after(d.close);
  const gate = new D1ExecutionGate(d.binding, executionContext);
  const names = ['a','b','c','d','e','f','g','h'];
  const input = { ...executionInput, idempotency_key: 'multibyte-receipt', expected_output_keys: names };
  const claim = await gate.claim(input);
  assert.equal(claim.status, 'CLAIMED');
  const output = Object.fromEntries(names.map(name => [name, '界'.repeat(3800)]));
  assert.ok(JSON.stringify(output).length < 32000 && bytes(JSON.stringify(output)) > 48000);
  await assert.rejects(gate.complete(claim.claim, { interaction_id:'synthetic-utf8',model:'gemini-3.8-flash',
    output,usage:{total_input_tokens:20,total_output_tokens:5,total_tokens:25},
    provider_requests:1,billing_verified:false }), e => e?.code === 'RECEIPT_LIMIT');
  const row = d.database.prepare('SELECT state,receipt_json FROM bridge_execution_claims').get();
  assert.equal(row.state, 'CLAIMED'); assert.equal(row.receipt_json, null);
  assert.equal((await gate.claim(input)).status, 'UNCERTAIN');
});
test('ordinary ASCII receipt remains validated and replayable', async t => {
  const d = executionD1(); t.after(d.close);
  const gate = new D1ExecutionGate(d.binding, executionContext);
  const input = { ...executionInput, idempotency_key: 'small-ascii-replay' };
  const claim = await gate.claim(input);
  const receipt = await gate.complete(claim.claim,{interaction_id:'synthetic-small',model:'gemini-3.8-flash',
    output:{finding:'PASS'},usage:{total_input_tokens:20,total_output_tokens:5,total_tokens:25},
    provider_requests:1,billing_verified:false});
  assert.equal((await gate.claim(input)).receipt.receipt_sha256, receipt.receipt_sha256);
});
