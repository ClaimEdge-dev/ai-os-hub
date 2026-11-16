import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createUnactivatedCapabilityBoundary } from '../src/unactivated_capability_boundary.mjs';
const request = (headers={}) => new Request('https://synthetic.invalid/mcp', { headers });
const env = { DEBO_BRIDGE_MODE:'synthetic_only', DEBO_IDENTITY_BOUNDARY:'sites_dispatch', DEBO_ENABLE_LIVE_GEMINI:'false', DEBO_OWNER_EMAIL:'owner@example.invalid' };
const input = { project_id:'DEBO-CORE',idempotency_key:'fixture-receipt-001' };
const receipt = { schema:'debo.gemini.fixture_receipt.v1',project_id:'DEBO-CORE',idempotency_key:input.idempotency_key,
  provider:'synthetic_fixture_only', receipt_sha256:'a'.repeat(64), output:{ finding:'SYNTHETIC_HEALTH_OK' } };
const config = () => ({ getTrustedSitesCaller:async()=>({ principal:'host-owner',email:'owner@example.invalid' }),
  authorizeFixtureRead:async()=>true,readCheckedFixture:async()=>receipt });
test('absent host or reader defaults to uniform denial, with no execution',async()=>{
  const b=createUnactivatedCapabilityBoundary();
  assert.deepEqual(await b.readFixture(request({'oai-authenticated-user-id':'host-owner'}),env,input),{status:'NOT_FOUND_OR_DENIED'});
  assert.equal((await b.claimExecution()).code,'PROVIDER_DISABLED');
  assert.equal((await b.reconcileExecution()).code,'RECONCILIATION_DISABLED');
  assert.equal(await b.authorizeExecution(),false);
  assert.equal(await b.authorizeReconciliation(),false);
});
test('identity, ACL and checked fixture are required together, extra client claims ignored',async()=>{
  const b=createUnactivatedCapabilityBoundary(config());
  const r=await b.readFixture(request({'oai-authenticated-user-id':'attacker','x-role':'reconciler'}),env,input);
  assert.deepEqual(r,{status:'FIXTURE_READ_ONLY',receipt_sha256:'a'.repeat(64)});
  assert.equal(Object.isFrozen(r),true);
  assert.equal(JSON.stringify(r).includes('SYNTHETIC_HEALTH_OK'),false);
  assert.equal((await b.claimExecution({project_id:'DEBO-CORE',role:'admin'})).code,'PROVIDER_DISABLED');
});
test('revocation after first read denies same key and does not invoke reader again',async()=>{
  let active=true,calls=0,readCalls=0,hostCalls=0;
  const c=config();
  c.getTrustedSitesCaller=async()=>{hostCalls++;return {principal:'host-owner',email:'owner@example.invalid'};};
  c.authorizeFixtureRead=async()=>{calls++;return active;};
  c.readCheckedFixture=async()=>{readCalls++;return receipt;};
  const b=createUnactivatedCapabilityBoundary(c);
  assert.equal((await b.readFixture(request(),env,input)).status,'FIXTURE_READ_ONLY');
  active=false;
  assert.deepEqual(await b.readFixture(request(),env,input),{status:'NOT_FOUND_OR_DENIED'});
  assert.equal(hostCalls,2);assert.equal(calls,2);assert.equal(readCalls,1);
});
test('unprivileged caller cannot distinguish missing, pending, completed or uncertain fixtures',async()=>{
  for(const r of [null,{state:'CLAIMED'},{state:'COMPLETED'},{state:'UNCERTAIN'}, { ...receipt, project_id:'JCT' },
    { ...receipt, idempotency_key:'other-key' },{...receipt,receipt_sha256:'invalid'}]){
    const c=config(); c.readCheckedFixture=async()=>r;
    assert.deepEqual(await createUnactivatedCapabilityBoundary(c).readFixture(request(),env,input),{status:'NOT_FOUND_OR_DENIED'});
  }
  const c=config(); c.authorizeFixtureRead=async()=>false;
  assert.deepEqual(await createUnactivatedCapabilityBoundary(c).readFixture(request(),env,input),{status:'NOT_FOUND_OR_DENIED'});
});
test('wrong project, extra fields, bad key and header-only authority never touch reader',async()=>{
  let touched=0;const c=config();c.readCheckedFixture=async()=>{touched++;return receipt;};
  const b=createUnactivatedCapabilityBoundary(c);
  for(const change of [{project_id:'JCT'},{verified:true},{idempotency_key:'short'}, {idempotency_key:'a'.repeat(129)}]) {
    assert.deepEqual(await b.readFixture(request(),env,{...input,...change}),{status:'NOT_FOUND_OR_DENIED'});
  }
  assert.equal(touched,0);
});
test('revoked host or unsupported mode fails before reader and leaks no private exception',async()=>{
  const c=config();let called=0;
  c.getTrustedSitesCaller=async()=>{throw Error('secret:host');};
  c.readCheckedFixture=async()=>{called++;throw Error('secret:receipt');};
  const b=createUnactivatedCapabilityBoundary(c);
  const denied=await b.readFixture(request(),env,input);
  assert.deepEqual(denied,{status:'NOT_FOUND_OR_DENIED'});
  assert.equal(JSON.stringify(denied).includes('secret:'),false);
  assert.equal(called,0);
});
test('authorized reader failure fails closed with no ownership or existence disclosure',async()=>{
  const c=config();c.readCheckedFixture=async()=>{throw Error('private:ownerToken');};
  const denied=await createUnactivatedCapabilityBoundary(c).readFixture(request(),env,input);
  assert.deepEqual(denied,{status:'NOT_FOUND_OR_DENIED'});
  assert.equal(JSON.stringify(denied).includes('ownerToken'),false);
});
test('invalid injected dependencies are refused',()=>{
  for(const p of [{authorizeFixtureRead:true},{readCheckedFixture:{authenticated:true}},{getTrustedSitesCaller:'self'}]) {
    assert.throws(()=>createUnactivatedCapabilityBoundary(p),TypeError);
  }
});
