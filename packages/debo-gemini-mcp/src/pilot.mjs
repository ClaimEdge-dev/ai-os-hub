import { randomUUID } from 'node:crypto';
import { assertCaller,validateInput, validateOutput,hashJson,PolicyError } from './policy.mjs';
export async function executeFixture({rawInput, token, expectedToken, store, syntheticExecutor}) {
  assertCaller(token,expectedToken);
  const input=validateInput(rawInput);
  if(typeof syntheticExecutor!=='function') throw new PolicyError('NO_FIXTURE_EXECUTOR','This pilot has no live Gemini adapter');
  const fingerprint=hashJson(input);
  return store.withRequestLock(input.project_id,input.idempotency_key,async()=>{
    const old=await store.read(input.project_id,input.idempotency_key);
    if(old){if(old.input_sha256!==fingerprint)throw new PolicyError('IDEMPOTENCY_CONFLICT','Key reused with different input');return {receipt:old,deduplicated:true};}
    const output=validateOutput(await syntheticExecutor(structuredClone(input)),input.expected_output_keys);
    const receipt={schema:'debo.gemini.fixture_receipt.v1',receipt_id:'FIXTURE-'+randomUUID(),project_id:input.project_id,idempotency_key:input.idempotency_key,provider:'synthetic_fixture_only',status:'TESTED_OFFLINE',input_sha256:fingerprint,output_sha256:hashJson(output),output,network_calls:0,actual_cost_usd:0,executed_at:new Date().toISOString()};
    const stored=await store.put(input.project_id,input.idempotency_key,receipt);
    if(!stored || hashJson(stored.output)!==stored.output_sha256)throw new PolicyError('RECEIPT_INTEGRITY','Readback checksum mismatch');
    return {receipt:stored,deduplicated:false};
  });
}
export async function readFixtureReceipt({project,key,token,expectedToken,store}) {
  assertCaller(token,expectedToken);
  // Project is scoped by stored path; project auth must be bound to caller in later remote transport.
  const receipt=await store.read(project,key);
  if(!receipt)return null;
  if(receipt.project_id!==project || hashJson(receipt.output)!==receipt.output_sha256)throw new PolicyError('RECEIPT_INTEGRITY','Invalid receipt checksum/scope');
  return receipt;
}
