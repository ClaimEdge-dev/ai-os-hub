// GB-111/025: offline route *recommendation* only. It never dispatches,
// authorizes a payment, opens a browser, uploads data or reissues an attempt.
// Capabilities are caller-supplied observations, not authenticated proof.
const TASK_KINDS = new Set(['public_research', 'synthetic_coding', 'synthetic_schema']);
const CAP_KINDS = new Set(['connected_read', 'public_browser', 'gemini_api']);
const ACCESS = new Set(['AVAILABLE', 'UNAVAILABLE', 'UNKNOWN']);
const PRICE = new Set(['VERIFIED_ZERO_NEW_SPEND', 'PAID', 'UNKNOWN']);
const MISSION = /^[A-Z][A-Z0-9-]{3,95}$/;
const BARRIER = Object.freeze({ status: 'HOLD', reason: 'UNCERTAIN_ATTEMPT_NO_ROUTE_SWITCH', dispatch_authorized: false, selected_route: null, automatic_fallback: false });
const deny = reason => Object.freeze({ status: 'HOLD', reason, dispatch_authorized: false, selected_route: null, automatic_fallback: false });

export function proposeNoSpendRoute({ task, capabilities, existing_attempt = null } = {}) {
  if (!task || typeof task !== 'object' || Array.isArray(task) ||
      Object.keys(task).sort().join('|') !== 'classification|kind|mission_id|project_id' ||
      task.project_id !== 'DEBO-CORE' || typeof task.mission_id !== 'string' || !MISSION.test(task.mission_id) ||
      !TASK_KINDS.has(task.kind) || !['PUBLIC', 'SYNTHETIC'].includes(task.classification) ||
      !Array.isArray(capabilities) || capabilities.length > 20 ||
      capabilities.some(x => !x || typeof x !== 'object' || Array.isArray(x) ||
        Object.keys(x).sort().join('|') !== 'access|kind|pricing|project_id|supports' ||
        !CAP_KINDS.has(x.kind) || !ACCESS.has(x.access) || !PRICE.has(x.pricing) ||
        x.project_id !== 'DEBO-CORE' || !Array.isArray(x.supports) || !x.supports.length ||
        x.supports.length > 3 || x.supports.some(k=>!TASK_KINDS.has(k)))) {
    return deny('CLOSED_ROUTE_INPUT_REQUIRED');
  }
  if (existing_attempt !== null) {
    if (typeof existing_attempt !== 'object' || Array.isArray(existing_attempt) ||
        Object.keys(existing_attempt).sort().join('|') !== 'mission_id|state' ||
        existing_attempt.mission_id !== task.mission_id ||
        !['NOT_STARTED', 'CLAIMED', 'UNCERTAIN', 'COMPLETED'].includes(existing_attempt.state)) {
      return deny('EXISTING_ATTEMPT_UNVERIFIED');
    }
    // A failed/unknown task may not dodge the original idempotency barrier by
    // switching routes, renaming providers, or using a free website.
    if (existing_attempt.state !== 'NOT_STARTED') return BARRIER;
  }
  // This recommendation is not an execution authority. A connected adapter,
  // private browser and provider have different independent approval gates.
  const eligible = capabilities.filter(c =>
    c.access === 'AVAILABLE' &&
    c.pricing === 'VERIFIED_ZERO_NEW_SPEND' &&
    c.supports.includes(task.kind) &&
    c.kind !== 'gemini_api');
  const route = eligible.find(c=>c.kind==='connected_read') ??
    eligible.find(c=>c.kind==='public_browser');
  if (!route) return deny('NO_VERIFIED_NO_SPEND_ROUTE');
  return Object.freeze({
    status: 'CANDIDATE_REQUIRES_OWN_AUTHORIZATION',
    selected_route: route.kind,
    reason: 'SCOPE_BOUNDED_NO_NEW_SPEND_CANDIDATE',
    project_id: task.project_id,
    mission_id: task.mission_id,
    dispatch_authorized: false,
    automatic_fallback: false,
    price_observed: 'VERIFIED_ZERO_NEW_SPEND'
  });
}
