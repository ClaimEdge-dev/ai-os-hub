// GB-003/011: unactivated wiring candidate. Not imported by Worker entrypoints.
// Only host-owned resolvers may supply caller, secret reference or request hash.
// No D1 migration, credential read, provider request or release is performed.
import { createUnactivatedSitesAuthorization } from './trusted_sites_authorization.mjs';
import { createUnactivatedFinancialReview } from './financial_authorization_review.mjs';

const REF = /^[A-Za-z0-9._:-]{8,128}$/;
const SHA = /^[a-f0-9]{64}$/;
const FIELDS = new Set(['principal', 'project_id', 'provider_scope', 'credential_ref', 'request_sha256']);
const deny = code => Object.freeze({ status: 'BLOCKED', code, dispatch_authorized: false });
export function validateClosedServerContext(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw) ||
      Object.keys(raw).length !== FIELDS.size ||
      Object.keys(raw).some(key => !FIELDS.has(key)) ||
      typeof raw.principal !== 'string' || raw.principal.length < 1 || raw.principal.length > 256 || /[\x00-\x1f\x7f]/.test(raw.principal) ||
      raw.project_id !== 'DEBO-CORE' || raw.provider_scope !== 'gemini-synthetic-v1' ||
      typeof raw.credential_ref !== 'string' || !REF.test(raw.credential_ref) ||
      typeof raw.request_sha256 !== 'string' || !SHA.test(raw.request_sha256)) return null;
  return Object.freeze({ ...raw });
}
export function createUnactivatedPrivateWiring({ getTrustedSitesCaller, getServerCredentialRef, getServerRequestHash, readServerEvidence, verifyIndependentProof, now } = {}) {
  const sites = createUnactivatedSitesAuthorization({ getTrustedSitesCaller });
  const financial = createUnactivatedFinancialReview({ readServerEvidence, verifyIndependentProof, ...(now ? { now } : {}) });
  return Object.freeze({
    async preflight(request, env) {
      const owner = await sites.resolveContext(request, env);
      if (!owner) return deny('TRUSTED_HOST_UNAVAILABLE');
      if (typeof getServerCredentialRef !== 'function' || typeof getServerRequestHash !== 'function') return deny('SERVER_BINDING_UNAVAILABLE');
      let credential_ref, request_sha256;
      try {
        credential_ref = await getServerCredentialRef(owner);
        request_sha256 = await getServerRequestHash(owner);
      } catch { return deny('SERVER_BINDING_UNAVAILABLE'); }
      const context = validateClosedServerContext({ principal: owner.principal, project_id: 'DEBO-CORE', provider_scope: owner.providerScope, credential_ref, request_sha256 });
      if (!context) return deny('CONTEXT_NOT_TRUSTED');
      const review = await financial.inspect(context);
      // No synthetic review result can authorize or create a durable claim.
      return Object.freeze({ status: 'HOLD', code: 'LIVE_RELEASE_BLOCKED', financial_review: review.status, dispatch_authorized: false });
    },
    authorizeRequest: async () => false,
    execute: async () => deny('PROVIDER_DISABLED')
  });
}
