import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createUnactivatedPrivateWiring, validateClosedServerContext } from '../src/private_wiring_plan.mjs';
const now = Date.parse('2026-11-15T20:00:00Z');
const request = () => new Request('https://synthetic.invalid/mcp', { headers: { 'oai-authenticated-user-id': 'fake-client', 'x-enable-live': 'true' } });
const env = () => ({ DEBO_BRIDGE_MODE: 'synthetic_only', DEBO_IDENTITY_BOUNDARY: 'sites_dispatch', DEBO_ENABLE_LIVE_GEMINI: 'false', DEBO_OWNER_EMAIL: 'owner@example.invalid' });
const evidence = { schema: 'debo.gemini.financial_evidence.v1', project_id: 'DEBO-CORE', provider_scope: 'gemini-synthetic-v1', credential_ref: 'managed-secret:existing', source_ref: 'source:independent-proof', issuer: 'issuer:trusted-server', issued_at: '2026-11-15T19:59:00Z', expires_at: '2026-11-15T20:01:00Z', eligibility: 'NONBILLABLE_CONFIRMED', max_cost_usd: 0, billing_enabled: false, paid_fallback_enabled: false };
const config = () => ({ getTrustedSitesCaller: async () => ({ principal: 'server-owned-id', email: 'owner@example.invalid' }), getServerCredentialRef: async () => 'managed-secret:existing', getServerRequestHash: async () => 'b'.repeat(64), readServerEvidence: async () => evidence, verifyIndependentProof: async () => true, now: () => now });

test('no trusted resolver refuses preflight with no network', async () => {
  const r = await createUnactivatedPrivateWiring().preflight(request(), env());
  assert.equal(r.code, 'TRUSTED_HOST_UNAVAILABLE'); assert.equal(r.dispatch_authorized, false);
});
test('host resolution does not accept spoofed caller or client flags', async () => {
  const a = createUnactivatedPrivateWiring(config());
  const r = await a.preflight(request(), env());
  assert.deepEqual(r, { status: 'HOLD', code: 'LIVE_RELEASE_BLOCKED', financial_review: 'REVIEW_CANDIDATE', dispatch_authorized: false });
  assert.equal(await a.authorizeRequest({ authenticated: true }), false);
  assert.equal((await a.execute({ enabled: true })).code, 'PROVIDER_DISABLED');
});
test('credential binding missing or untrusted blocks review', async () => {
  const c = config(); delete c.getServerCredentialRef;
  assert.equal((await createUnactivatedPrivateWiring(c).preflight(request(), env())).code, 'SERVER_BINDING_UNAVAILABLE');
  c.getServerCredentialRef = async () => 'bad';
  assert.equal((await createUnactivatedPrivateWiring(c).preflight(request(), env())).code, 'CONTEXT_NOT_TRUSTED');
});
test('financial check refuses paid fallback and still holds', async () => {
  const c = config(); c.readServerEvidence = async () => ({ ...evidence, paid_fallback_enabled: true });
  const r = await createUnactivatedPrivateWiring(c).preflight(request(), env());
  assert.equal(r.status, 'HOLD'); assert.equal(r.financial_review, 'BLOCKED'); assert.equal(r.dispatch_authorized, false);
});
test('closed server context rejects extra authority fields, wrong project and ref', () => {
  const clean = { principal: 'server-owned-id', project_id: 'DEBO-CORE', provider_scope: 'gemini-synthetic-v1', credential_ref: 'managed-secret:existing', request_sha256: 'b'.repeat(64) };
  assert.deepEqual(validateClosedServerContext(clean), clean);
  for (const patch of [{ authenticated: true }, { billing_verified: true }, { project_id: 'JCT' }, { credential_ref: 'unbound' }, { request_sha256: 'bad' }]) assert.equal(validateClosedServerContext({ ...clean, ...patch }), null);
});
test('host and server binding failures do not propagate private exceptions', async () => {
  const c = config(); c.getServerRequestHash = async () => { throw Error('secret:never'); };
  const r = await createUnactivatedPrivateWiring(c).preflight(request(), env());
  assert.equal(r.code, 'SERVER_BINDING_UNAVAILABLE'); assert.equal(JSON.stringify(r).includes('secret:'), false);
});
