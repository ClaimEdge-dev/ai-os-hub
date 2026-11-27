import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createUnactivatedSitesAuthorization } from '../src/trusted_sites_authorization.mjs';

const request = (headers = {}) => new Request('https://synthetic.invalid/mcp', { headers });
const env = () => ({ DEBO_BRIDGE_MODE: 'synthetic_only', DEBO_IDENTITY_BOUNDARY: 'sites_dispatch', DEBO_ENABLE_LIVE_GEMINI: 'false', DEBO_OWNER_EMAIL: 'owner@example.invalid' });
const host = () => ({ principal: 'verified-owner-id', email: 'OWNER@example.invalid' });

test('no host resolver fails closed regardless of client identity claims', async () => {
  const auth = createUnactivatedSitesAuthorization();
  const r = request({ 'oai-authenticated-user-id': 'verified-owner-id', 'oai-authenticated-user-email': 'owner@example.invalid', 'x-authorized': 'true' });
  assert.equal(await auth.resolveContext(r, env()), null);
  assert.equal(await auth.authorizeRequest({ authenticated: true, billing_verified: true }), false);
  assert.deepEqual(await auth.execute({ enabled: true }), { status: 'BLOCKED', code: 'PROVIDER_DISABLED' });
});

test('context comes only from host resolver, never spoofed caller headers or project flags', async () => {
  const auth = createUnactivatedSitesAuthorization({ getTrustedSitesCaller: async () => host() });
  const r = request({ 'oai-authenticated-user-id': 'attacker', 'oai-authenticated-user-email': 'attacker@example.invalid', 'x-project-id': 'JCT' });
  const context = await auth.resolveContext(r, { ...env(), DEBO_CALLER_PROJECT_ACL: '{"attacker":["JCT"]}' });
  assert.deepEqual(context, { principal: 'verified-owner-id', projects: ['DEBO-CORE'], providerScope: 'gemini-synthetic-v1' });
  assert.equal(Object.isFrozen(context), true);
  assert.equal(Object.isFrozen(context.projects), true);
  assert.equal(await auth.authorizeRequest({ ...context, project_id: 'DEBO-CORE' }), false);
});

test('runtime modes never enable provider calls', async () => {
  const auth = createUnactivatedSitesAuthorization({ getTrustedSitesCaller: async () => host() });
  for (const patch of [{ DEBO_ENABLE_LIVE_GEMINI: 'true' }, { DEBO_IDENTITY_BOUNDARY: 'client_headers' }, { DEBO_BRIDGE_MODE: 'live' }, { DEBO_OWNER_EMAIL: '' }, { DEBO_OWNER_EMAIL: 'other@example.invalid' }]) {
    assert.equal(await auth.resolveContext(request(), { ...env(), ...patch }), null);
  }
  assert.equal(await auth.authorizeRequest({ billing_verified: true }), false);
  assert.deepEqual(await auth.execute(), { status: 'BLOCKED', code: 'PROVIDER_DISABLED' });
});

test('invalid and cross-owner identities are rejected', async () => {
  for (const identity of [null, {}, { principal: 'caller', email: 'wrong@example.invalid' }, { principal: '\nattacker', email: 'owner@example.invalid' }, { principal: 'a'.repeat(257), email: 'owner@example.invalid' }, { principal: 'caller', email: null }]) {
    const auth = createUnactivatedSitesAuthorization({ getTrustedSitesCaller: async () => identity });
    assert.equal(await auth.resolveContext(request(), env()), null);
  }
});

test('host resolver failures fail closed; no request headers consulted as fallback', async () => {
  const auth = createUnactivatedSitesAuthorization({ getTrustedSitesCaller: async () => { throw Error('private host error'); } });
  assert.equal(await auth.resolveContext(request({ 'oai-authenticated-user-id': 'fallback' }), env()), null);
  assert.equal(await auth.authorizeRequest(), false);
});

test('bad injection setup fails rather than converting a flag into authority', () => {
  assert.throws(() => createUnactivatedSitesAuthorization({ getTrustedSitesCaller: { authenticated: true } }), TypeError);
});
