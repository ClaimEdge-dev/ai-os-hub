// GB-001: unactivated, server-internal Sites context candidate.
// A trusted host must supply getTrustedSitesCaller. Request headers, browser
// payloads, environment mode flags and this module are NOT independent
// authentication or financial authorization. Provider dispatch always denies.
const DENIED = Object.freeze({ status: 'BLOCKED', code: 'PROVIDER_DISABLED' });
const PRINCIPAL = /^[^\x00-\x1f\x7f]{1,256}$/;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PROJECT = 'DEBO-CORE';
const PROVIDER_SCOPE = 'gemini-synthetic-v1';

export function createUnactivatedSitesAuthorization({ getTrustedSitesCaller } = {}) {
  if (getTrustedSitesCaller !== undefined && typeof getTrustedSitesCaller !== 'function') {
    throw new TypeError('Trusted Sites caller resolver must be a server-owned function');
  }
  return Object.freeze({
    async resolveContext(request, env) {
      // The resolver is deliberately absent unless supplied by reviewed host
      // wiring. No fallback to headers or client-supplied claims is permitted.
      if (typeof getTrustedSitesCaller !== 'function' || !(request instanceof Request) ||
          env?.DEBO_BRIDGE_MODE !== 'synthetic_only' ||
          env?.DEBO_IDENTITY_BOUNDARY !== 'sites_dispatch' ||
          env?.DEBO_ENABLE_LIVE_GEMINI !== 'false' ||
          typeof env.DEBO_OWNER_EMAIL !== 'string' ||
          !EMAIL.test(env.DEBO_OWNER_EMAIL.trim())) return null;
      let caller;
      try { caller = await getTrustedSitesCaller(request); }
      catch { return null; }
      if (!caller || typeof caller !== 'object' || Array.isArray(caller) ||
          typeof caller.principal !== 'string' || !PRINCIPAL.test(caller.principal) ||
          typeof caller.email !== 'string' || !EMAIL.test(caller.email.trim()) ||
          caller.email.trim().toLowerCase() !== env.DEBO_OWNER_EMAIL.trim().toLowerCase()) return null;
      // No client project selection or provider config can widen this context.
      return Object.freeze({
        principal: caller.principal,
        projects: Object.freeze([PROJECT]),
        providerScope: PROVIDER_SCOPE
      });
    },
    // GB-002 financial evidence, GB-003 wiring and owner release remain HOLD.
    // No caller, environment flag or successful identity resolution enables API.
    authorizeRequest: async () => false,
    execute: async () => DENIED
  });
}
