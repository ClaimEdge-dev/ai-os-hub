// GB-014/015/018 staged, unactivated capability separation. Not in Worker.
// The host identity resolver and fixture-reader authorization are independent
// server-owned dependencies. This is NOT a hosted identity proof, permission
// grant, provider billing verification, or live receipt read.
import { createUnactivatedSitesAuthorization } from './trusted_sites_authorization.mjs';

const KEY = /^[A-Za-z0-9._:-]{8,128}$/;
const HASH = /^[a-f0-9]{64}$/;
const PROJECT = 'DEBO-CORE';
const DENIED = Object.freeze({ status: 'NOT_FOUND_OR_DENIED' });
const DISABLED = Object.freeze({ status: 'BLOCKED', code: 'PROVIDER_DISABLED' });
const RECONCILIATION_DISABLED = Object.freeze({ status: 'BLOCKED', code: 'RECONCILIATION_DISABLED' });

export function createUnactivatedCapabilityBoundary({ getTrustedSitesCaller, authorizeFixtureRead, readCheckedFixture } = {}) {
  if (authorizeFixtureRead !== undefined && typeof authorizeFixtureRead !== 'function' ||
      readCheckedFixture !== undefined && typeof readCheckedFixture !== 'function') {
    throw new TypeError('Fixture read dependencies must be server-owned functions');
  }
  const sites = createUnactivatedSitesAuthorization({ getTrustedSitesCaller });
  return Object.freeze({
    async readFixture(request, env, input) {
      // Generic denial for invalid, missing, revoked, inaccessible and
      // cross-project items: no owner or existence metadata in an error.
      if (!input || typeof input !== 'object' || Array.isArray(input) ||
          Object.keys(input).length !== 2 || input.project_id !== PROJECT ||
          typeof input.idempotency_key !== 'string' || !KEY.test(input.idempotency_key)) return DENIED;
      const context = await sites.resolveContext(request, env);
      if (!context || !context.projects.includes(PROJECT) ||
          typeof authorizeFixtureRead !== 'function' || typeof readCheckedFixture !== 'function') return DENIED;
      const scope = Object.freeze({ principal: context.principal, project_id: PROJECT, idempotency_key: input.idempotency_key });
      try {
        // MUST resolve host and grant afresh for EACH read. No successful
        // previous lookup, cookie, client role field, or cached context suffices.
        if (await authorizeFixtureRead(scope) !== true) return DENIED;
        const receipt = await readCheckedFixture(scope);
        // The injected reader must verify the complete checksum and actual
        // ownership. These shape guards do not independently prove that.
        if (!receipt || typeof receipt !== 'object' || Array.isArray(receipt) ||
            receipt.schema !== 'debo.gemini.fixture_receipt.v1' ||
            receipt.project_id !== PROJECT || receipt.idempotency_key !== input.idempotency_key ||
            receipt.provider !== 'synthetic_fixture_only' ||
            typeof receipt.receipt_sha256 !== 'string' || !HASH.test(receipt.receipt_sha256)) return DENIED;
        return Object.freeze({ status: 'FIXTURE_READ_ONLY', receipt_sha256: receipt.receipt_sha256 });
      } catch { return DENIED; }
    },
    // No read permission can turn into a durable claim or reconciliation.
    claimExecution: async () => DISABLED,
    reconcileExecution: async () => RECONCILIATION_DISABLED,
    authorizeExecution: async () => false,
    authorizeReconciliation: async () => false
  });
}
