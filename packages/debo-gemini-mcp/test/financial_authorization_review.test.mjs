import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createUnactivatedFinancialReview } from '../src/financial_authorization_review.mjs';

const clock = Date.parse('2026-11-15T20:00:00Z');
const context = Object.freeze({ principal: 'owner-validated', project_id: 'DEBO-CORE', provider_scope: 'gemini-synthetic-v1', credential_ref: 'managed-secret:existing', request_sha256: 'a'.repeat(64) });
const evidence = Object.freeze({ schema: 'debo.gemini.financial_evidence.v1', project_id: context.project_id, provider_scope: context.provider_scope, credential_ref: context.credential_ref, source_ref: 'source:independent-proof', issuer: 'issuer:trusted-server', issued_at: '2026-11-15T19:59:00Z', expires_at: '2026-11-15T20:01:00Z', eligibility: 'NONBILLABLE_CONFIRMED', max_cost_usd: 0, billing_enabled: false, paid_fallback_enabled: false });
const make = (patch = {}, proof = async () => true) => createUnactivatedFinancialReview({ now: () => clock, readServerEvidence: async () => ({ ...evidence, ...patch }), verifyIndependentProof: proof });

test('missing server evidence dependencies fail closed with no dispatch', async () => {
  const auth = createUnactivatedFinancialReview({ now: () => clock });
  assert.equal((await auth.inspect(context)).code, 'EVIDENCE_SOURCE_UNAVAILABLE');
  assert.equal(await auth.authorizeRequest({ authenticated: true, free_tier: true }), false);
  assert.deepEqual(await auth.execute({ enabled: true }), { status: 'BLOCKED', code: 'PROVIDER_DISABLED', dispatch_authorized: false });
});
test('self-asserted caller authority and context extension fail before evidence read', async () => {
  let calls = 0;
  const auth = createUnactivatedFinancialReview({ now: () => clock, readServerEvidence: async () => { calls++; return evidence; }, verifyIndependentProof: async () => true });
  for (const patch of [{ authenticated: true }, { billing_verified: true }, { cost_ceiling_usd: 0 }, { project_id: 'JCT' }, { credential_ref: 'other:credential' }, { request_sha256: 'bad' }]) {
    const result = await auth.inspect({ ...context, ...patch });
    if ('credential_ref' in patch) assert.equal(result.code, 'EVIDENCE_INVALID');
    else assert.equal(result.code, 'CONTEXT_NOT_TRUSTED');
  }
  assert.equal(calls, 1);
});
test('paid, fallback, mismatched scope and extra evidence fields are rejected', async () => {
  for (const patch of [{ max_cost_usd: 0.01 }, { billing_enabled: true }, { paid_fallback_enabled: true }, { project_id: 'JCT' }, { credential_ref: 'different:credential' }, { source_ref: '' }, { issuer: 'bad' }, { client_claim: true }, { eligibility: 'FREE_TIER_UI_ONLY' }]) {
    assert.equal((await make(patch).inspect(context)).code, 'EVIDENCE_INVALID');
  }
});
test('expired, future and overlong evidence windows are rejected', async () => {
  for (const patch of [{ expires_at: '2026-11-15T19:59:30Z' }, { issued_at: '2026-11-15T20:00:01Z' }, { issued_at: '2026-11-15T19:53:00Z' }, { expires_at: '2026-11-15T20:10:00Z' }]) {
    assert.equal((await make(patch).inspect(context)).code, 'EVIDENCE_STALE');
  }
});
test('no independent verification, false, exception and malformed verifier fail closed', async () => {
  assert.equal((await createUnactivatedFinancialReview({ now: () => clock, readServerEvidence: async () => evidence }).inspect(context)).code, 'EVIDENCE_SOURCE_UNAVAILABLE');
  for (const cb of [async () => false, async () => ({ verified: true }), async () => { throw Error('private'); }]) {
    assert.equal((await make({}, cb).inspect(context)).code, 'EVIDENCE_UNVERIFIED');
  }
});
test('synthetic verified evidence is a review candidate but still never authorization', async () => {
  const auth = make();
  const result = await auth.inspect(context);
  assert.deepEqual(result, { status: 'REVIEW_CANDIDATE', code: 'RELEASE_AND_HOST_PROOF_PENDING', dispatch_authorized: false });
  assert.equal(await auth.authorizeRequest(result), false);
  assert.equal((await auth.execute(result)).code, 'PROVIDER_DISABLED');
  assert.equal(Object.isFrozen(result), true);
});
test('source error is not surfaced and never authorizes', async () => {
  const auth = createUnactivatedFinancialReview({ now: () => clock, readServerEvidence: async () => { throw Error('secret:unavailable'); }, verifyIndependentProof: async () => true });
  const result = await auth.inspect(context);
  assert.equal(result.code, 'EVIDENCE_SOURCE_UNAVAILABLE');
  assert.equal(JSON.stringify(result).includes('secret:'), false);
});
test('invalid constructor config does not create a review interface', () => {
  for (const patch of [{ verifyIndependentProof: true }, { readServerEvidence: {} }, { now: 1 }, { maxEvidenceAgeMs: 0 }, { maxEvidenceAgeMs: 400000 }]) {
    assert.throws(() => createUnactivatedFinancialReview(patch), TypeError);
  }
});
