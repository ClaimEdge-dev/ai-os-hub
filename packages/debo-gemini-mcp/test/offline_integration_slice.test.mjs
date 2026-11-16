// GB-008: one offline-only integration slice using the existing true R19 Python
// validator. No live Gemini, host, secret manager, deployed D1, or persistent
// task store is contacted. Test-only authorization MUST NOT be promoted.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync, writeFileSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { createUnactivatedSitesAuthorization } from '../src/trusted_sites_authorization.mjs';
import { createUnactivatedFinancialReview } from '../src/financial_authorization_review.mjs';
import { createUnactivatedPrivateWiring } from '../src/private_wiring_plan.mjs';
import { createStagedSyntheticExecutor } from '../src/guarded_interaction.mjs';
import { D1ExecutionGate } from '../src/durable_execution_gate.mjs';
import { sha256 } from '../src/synthetic_contract.mjs';
import { executionD1, executionInput } from './helpers/execution-fixtures.mjs';

const py = fileURLToPath(new URL('../../../tools/debo_r19_continuity.py', import.meta.url));
const clock = Date.parse('2026-11-15T20:00:00Z');
const owner = { principal: 'synthetic-verified-owner', email: 'owner@example.invalid' };
const sourceContext = { principal: owner.principal, projects: ['DEBO-CORE'], providerScope: 'gemini-synthetic-v1' };
const projectBinding = { principal: owner.principal, project_id: 'DEBO-CORE', provider_scope: sourceContext.providerScope, credential_ref: 'managed-secret:synthetic', request_sha256: 'b'.repeat(64) };
const hostEnv = { DEBO_BRIDGE_MODE: 'synthetic_only', DEBO_IDENTITY_BOUNDARY: 'sites_dispatch', DEBO_ENABLE_LIVE_GEMINI: 'false', DEBO_OWNER_EMAIL: owner.email };
const evidence = { schema: 'debo.gemini.financial_evidence.v1', project_id: 'DEBO-CORE', provider_scope: sourceContext.providerScope, credential_ref: projectBinding.credential_ref, source_ref: 'source:synthetic-review', issuer: 'issuer:synthetic-review', issued_at: '2026-11-15T19:59:00Z', expires_at: '2026-11-15T20:01:00Z', eligibility: 'NONBILLABLE_CONFIRMED', max_cost_usd: 0, billing_enabled: false, paid_fallback_enabled: false };
const request = () => new Request('https://synthetic.invalid/mcp', { headers: { 'oai-authenticated-user-id': 'client-spoof', 'x-provider-enabled': 'true' } });
const modelResponse = () => new Response(JSON.stringify({
  id: 'synthetic-integration-only', status: 'completed', model: 'gemini-3.8-flash',
  steps: [{ type: 'model_output', content: [{ type: 'text', text: '{"finding":"PASS"}' }] }],
  usage: { total_input_tokens: 20, total_output_tokens: 5, total_tokens: 25 }
}), { headers: { 'content-type': 'application/json' } });
const credential = 'SYNTHETIC_TEST_CREDENTIAL_NOT_REAL';
const task = { project_id: 'DEBO-CORE', mission_id: 'DEBO-GEMINI-BRIDGE-PR81',
  task_id: 'DEBO-GEMINI-BRIDGE-PR81', objective: 'Verify one offline synthetic Gemini bridge to R19' };
const toCapsule = (receipt, ownerTask, privateReceiptRef) => {
  if (receipt?.schema !== 'debo.gemini.transport_receipt.v1' || receipt.project_id !== ownerTask.project_id ||
      receipt.provider_scope !== sourceContext.providerScope || receipt.idempotency_key !== executionInput.idempotency_key ||
      receipt.result?.billing_verified !== false || typeof privateReceiptRef !== 'string') throw Error('Checked receipt/project mismatch');
  return { schema: 'debo.r19.capsule.v1', project_id: ownerTask.project_id,
    mission_id: ownerTask.mission_id, task_id: ownerTask.task_id, objective: ownerTask.objective,
    status: 'BUILT', checkpoint: 'DEBO-GEMINI-BRIDGE-GB008-OFFLINE',
    evidence: [{ type: 'source_readback', ref: privateReceiptRef }],
    next_action: 'Hosted authenticated and financial acceptance remain unverified; keep API and release disabled.',
    scope: 'private', as_of_utc: '2026-11-15T20:00:00Z' };
};

test('GB-008 trusted preflight and financial review remain denied before any claim', async () => {
  let touched = 0;
  const sites = createUnactivatedSitesAuthorization({ getTrustedSitesCaller: async () => owner });
  assert.deepEqual(await sites.resolveContext(request(), hostEnv), sourceContext);
  const financial = createUnactivatedFinancialReview({
    readServerEvidence: async () => ({ ...evidence }),
    verifyIndependentProof: async () => true, now: () => clock
  });
  const review = await financial.inspect(projectBinding);
  assert.equal(review.status, 'REVIEW_CANDIDATE');
  assert.equal(review.dispatch_authorized, false);
  const wiring = createUnactivatedPrivateWiring({
    getTrustedSitesCaller: async () => owner,
    getServerCredentialRef: async () => projectBinding.credential_ref,
    getServerRequestHash: async () => projectBinding.request_sha256,
    readServerEvidence: async () => ({ ...evidence }),
    verifyIndependentProof: async () => true, now: () => clock
  });
  assert.equal((await wiring.preflight(request(), hostEnv)).code, 'LIVE_RELEASE_BLOCKED');
  assert.equal(await wiring.authorizeRequest(projectBinding), false);
  assert.equal((await wiring.execute(executionInput)).code, 'PROVIDER_DISABLED');
  assert.equal(touched, 0);
});

test('GB-008 offline synthetic authorization -> durable D1 -> injected response -> verified receipt -> real R19 Python save/readback', async t => {
  const sqlite = executionD1(); t.after(() => sqlite.close());
  const directory = mkdtempSync(join(tmpdir(), 'debo-gb008-')); t.after(() => rmSync(directory, { recursive: true, force: true }));
  let dispatches = 0; const phases = [];
  // This is a deliberately synthetic, TEST-ONLY authorization shim. Production
  // Sites and financial adapters above always deny and are NOT used to dispatch.
  const authorizer = async details => {
    phases.push(details.phase);
    return details.principal === owner.principal && details.project_id === 'DEBO-CORE' &&
      details.provider_scope === sourceContext.providerScope &&
      ['before_claim', 'before_dispatch'].includes(details.phase);
  };
  const executor = createStagedSyntheticExecutor({
    enabled: true, binding: sqlite.binding, context: sourceContext,
    authorizeRequest: authorizer,
    transportOptions: { apiKey: credential, fetchImpl: async (_url, init) => {
      dispatches++;
      assert.equal(init.method, 'POST');
      assert.equal(init.redirect, 'error');
      assert.equal(init.credentials, 'omit');
      assert.equal(init.cache, 'no-store');
      assert.equal(init.headers['x-goog-api-key'], credential);
      assert.equal(sqlite.database.prepare('SELECT state FROM bridge_execution_claims').get().state, 'CLAIMED');
      return modelResponse();
    } }
  });
  const first = await executor.execute(executionInput);
  assert.equal(first.status, 'COMPLETED');
  assert.equal(first.replayed, false);
  assert.equal(dispatches, 1);
  assert.deepEqual(phases, ['before_claim', 'before_dispatch']);
  assert.deepEqual(first.receipt.result.output, { finding: 'PASS' });
  assert.equal(first.receipt.result.usage.total_tokens, 25);
  assert.equal(first.receipt.result.billing_verified, false);

  // Independently ask the actual D1 gate to validate/replay the same row.
  const gate = new D1ExecutionGate(sqlite.binding, sourceContext);
  const duplicate = await gate.claim(executionInput);
  assert.equal(duplicate.status, 'COMPLETED');
  assert.deepEqual(duplicate.receipt, first.receipt);
  assert.equal(dispatches, 1);
  const { receipt_sha256: savedHash, ...unsigned } = duplicate.receipt;
  assert.equal(await sha256(unsigned), savedHash);

  // The receipt remains in a PRIVATE temp file; R19 gets a typed reference
  // rather than raw output or usage in a public portable capsule.
  const receiptPath = join(directory, 'synthetic-receipt.json');
  writeFileSync(receiptPath, JSON.stringify(duplicate.receipt));
  const readReceipt = JSON.parse(readFileSync(receiptPath, 'utf8'));
  assert.equal(readReceipt.result.usage.total_tokens, 25);
  assert.equal(readReceipt.result.output.finding, 'PASS');
  const inputPath = join(directory, 'r19-input.json');
  const outputPath = join(directory, 'r19-saved.json');
  const capsule = toCapsule(readReceipt, task, 'file://' + receiptPath);
  assert.equal(JSON.stringify(capsule).includes(credential), false);
  assert.equal(Object.hasOwn(capsule, 'result'), false);
  writeFileSync(inputPath, JSON.stringify(capsule));
  const validated = execFileSync('python3', [py, 'validate', '--input', inputPath], { encoding: 'utf8' });
  assert.match(validated, /PASS/);
  const saved = JSON.parse(execFileSync('python3', [py, 'checkpoint', '--input', inputPath, '--output', outputPath], { encoding: 'utf8' }));
  assert.equal(saved.readback, 'PASS');
  assert.deepEqual(JSON.parse(readFileSync(outputPath, 'utf8')), capsule);
  const replay = JSON.parse(execFileSync('python3', [py, 'checkpoint', '--input', inputPath, '--output', outputPath], { encoding: 'utf8' }));
  assert.equal(replay.unchanged, true);
  assert.equal(dispatches, 1);
  const conflicting = { ...capsule, checkpoint: 'CHANGED-UNAPPROVED' };
  writeFileSync(inputPath, JSON.stringify(conflicting));
  assert.throws(() => execFileSync('python3', [py, 'checkpoint', '--input', inputPath, '--output', outputPath], { stdio: 'pipe' }));
  assert.deepEqual(JSON.parse(readFileSync(outputPath, 'utf8')), capsule);
});

test('GB-008 no unauthorized result projection, no promoted lifecycle and no duplicate dispatch', async t => {
  const sqlite = executionD1(); t.after(() => sqlite.close());
  let calls = 0;
  const executor = createStagedSyntheticExecutor({
    enabled: true, binding: sqlite.binding, context: sourceContext,
    authorizeRequest: async details => details.phase === 'before_claim',
    transportOptions: { apiKey: credential, fetchImpl: async () => { calls++; return modelResponse(); } }
  });
  const r = await executor.execute(executionInput);
  assert.equal(r.status, 'UNCERTAIN');
  assert.equal((await executor.execute(executionInput)).status, 'UNCERTAIN');
  assert.equal(calls, 0);
  assert.throws(() => toCapsule({ ...r, schema: 'fake' }, task, 'file://fake'), /mismatch/);
  assert.throws(() => toCapsule({ schema: 'debo.gemini.transport_receipt.v1', project_id: 'JCT', provider_scope: sourceContext.providerScope }, task, 'file://fake'), /mismatch/);
});

test('GB-008 R19 validator refuses faked TESTED status without test_receipt', () => {
  const directory = mkdtempSync(join(tmpdir(), 'debo-gb008-status-'));
  try {
    const fake = toCapsule({ schema: 'debo.gemini.transport_receipt.v1', project_id: 'DEBO-CORE', provider_scope: sourceContext.providerScope, idempotency_key: executionInput.idempotency_key, result: { billing_verified: false } }, task, 'synthetic://receipt');
    fake.status = 'TESTED';
    writeFileSync(join(directory, 'fake.json'), JSON.stringify(fake));
    assert.throws(() => execFileSync('python3', [py, 'validate', '--input', join(directory, 'fake.json')], { stdio: 'pipe' }));
  } finally { rmSync(directory, { recursive: true, force: true }); }
});
