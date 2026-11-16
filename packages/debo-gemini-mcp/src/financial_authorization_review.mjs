// GB-002: server-only financial-evidence interface, NOT a financial authorization.
// Never exported by either live Worker. Neither a test double, quota display,
// client flag nor a passing review may authorize Gemini dispatch or spending.
const BLOCK = Object.freeze({ status: 'BLOCKED', dispatch_authorized: false });
const FIELDS = new Set(['schema', 'project_id', 'provider_scope', 'credential_ref', 'source_ref', 'issuer', 'issued_at', 'expires_at', 'eligibility', 'max_cost_usd', 'billing_enabled', 'paid_fallback_enabled']);
const CONTEXT_FIELDS = new Set(['principal', 'project_id', 'provider_scope', 'credential_ref', 'request_sha256']);
const ID = /^[A-Za-z0-9._:-]{8,128}$/;
const SHA = /^[a-f0-9]{64}$/;
const UTC = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/;
const record = x => x && typeof x === 'object' && !Array.isArray(x);
const exact = (x, expected) => Object.keys(x).every(k => expected.has(k)) && Object.keys(x).length === expected.size;
const denial = code => Object.freeze({ ...BLOCK, code });
const finiteTime = s => typeof s === 'string' && UTC.test(s) && Number.isFinite(Date.parse(s));

export function createUnactivatedFinancialReview({ readServerEvidence, verifyIndependentProof, now = Date.now, maxEvidenceAgeMs = 300000 } = {}) {
  // There is intentionally no 'enabled' or client-provided override.
  if (readServerEvidence !== undefined && typeof readServerEvidence !== 'function' ||
      verifyIndependentProof !== undefined && typeof verifyIndependentProof !== 'function' ||
      typeof now !== 'function' || !Number.isSafeInteger(maxEvidenceAgeMs) || maxEvidenceAgeMs < 1000 || maxEvidenceAgeMs > 300000) {
    throw new TypeError('Invalid server financial-review dependency');
  }
  return Object.freeze({
    async inspect(rawContext) {
      if (!record(rawContext) || !exact(rawContext, CONTEXT_FIELDS) ||
          typeof rawContext.principal !== 'string' || !ID.test(rawContext.principal) ||
          rawContext.project_id !== 'DEBO-CORE' || !ID.test(rawContext.provider_scope) ||
          typeof rawContext.credential_ref !== 'string' || !ID.test(rawContext.credential_ref) ||
          typeof rawContext.request_sha256 !== 'string' || !SHA.test(rawContext.request_sha256)) return denial('CONTEXT_NOT_TRUSTED');
      if (typeof readServerEvidence !== 'function' || typeof verifyIndependentProof !== 'function') return denial('EVIDENCE_SOURCE_UNAVAILABLE');
      const context = Object.freeze({ ...rawContext });
      let evidence, current;
      try {
        // This is a server-owned read contract. Any eventual integration must
        // additionally authenticate these dependencies and their source scope.
        current = now();
        evidence = await readServerEvidence(context);
      } catch { return denial('EVIDENCE_SOURCE_UNAVAILABLE'); }
      if (!Number.isSafeInteger(current) || !record(evidence) || !exact(evidence, FIELDS) ||
          evidence.schema !== 'debo.gemini.financial_evidence.v1' ||
          evidence.project_id !== context.project_id ||
          evidence.provider_scope !== context.provider_scope ||
          evidence.credential_ref !== context.credential_ref ||
          typeof evidence.source_ref !== 'string' || !ID.test(evidence.source_ref) ||
          typeof evidence.issuer !== 'string' || !ID.test(evidence.issuer) ||
          evidence.eligibility !== 'NONBILLABLE_CONFIRMED' ||
          evidence.max_cost_usd !== 0 || evidence.billing_enabled !== false ||
          evidence.paid_fallback_enabled !== false ||
          !finiteTime(evidence.issued_at) || !finiteTime(evidence.expires_at)) return denial('EVIDENCE_INVALID');
      const issued = Date.parse(evidence.issued_at), expires = Date.parse(evidence.expires_at);
      if (issued > current || current >= expires || current - issued > maxEvidenceAgeMs || expires - issued > maxEvidenceAgeMs) return denial('EVIDENCE_STALE');
      try {
        // A returned boolean is only a review signal from a separately vetted
        // server authority. It is NOT permission to send an API call.
        if (await verifyIndependentProof(Object.freeze({ ...evidence }), context) !== true) return denial('EVIDENCE_UNVERIFIED');
      } catch { return denial('EVIDENCE_UNVERIFIED'); }
      return Object.freeze({ status: 'REVIEW_CANDIDATE', code: 'RELEASE_AND_HOST_PROOF_PENDING', dispatch_authorized: false });
    },
    authorizeRequest: async () => false,
    execute: async () => denial('PROVIDER_DISABLED')
  });
}
