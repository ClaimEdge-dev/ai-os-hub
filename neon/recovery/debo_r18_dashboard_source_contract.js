'use strict';
// Pure source/readiness projection; not an authorization or deployment mechanism.
// All checks fail closed unless explicit boolean true is provided.
function sourceHealth({
  sourceReadVerified = false,
  taskReadsVerified = false,
  latestReadAt = null,
  acceptedCount = 0,
  importReadbackVerified = false,
  mobileQAPassed = false,
  securityQAPassed = false,
  ownerReleaseApproved = false,
  sourceFreshnessVerified = false
} = {}) {
  const hasAccepted = Number.isSafeInteger(acceptedCount) && acceptedCount > 0;
  const sourceOK = sourceReadVerified === true;
  const readsOK = taskReadsVerified === true;
  const importOK = importReadbackVerified === true;
  const freshnessOK = sourceFreshnessVerified === true;
  const mobileOK = mobileQAPassed === true;
  const securityOK = securityQAPassed === true;
  const ownerOK = ownerReleaseApproved === true;
  const synchronized = sourceOK && readsOK && importOK && hasAccepted;
  const eligible = synchronized && freshnessOK && mobileOK && securityOK && ownerOK;
  let reason = 'ACCEPTED';
  if (!sourceOK) reason = 'SOURCE_NOT_VERIFIED';
  else if (!readsOK) reason = 'CORE_READBACK_MISSING';
  else if (!importOK || !hasAccepted) reason = 'SYNC_NOT_VERIFIED';
  else if (!freshnessOK) reason = 'FRESHNESS_NOT_VERIFIED';
  else if (!mobileOK) reason = 'MOBILE_QA_OPEN';
  else if (!securityOK) reason = 'SECURITY_QA_OPEN';
  else if (!ownerOK) reason = 'OWNER_RELEASE_HOLD';
  return Object.freeze({
    source: 'DEBO Core',
    health: synchronized ? 'VERIFIED' : 'UNKNOWN',
    read_at: latestReadAt,
    eligible_for_release: eligible,
    reason
  });
}
module.exports = { sourceHealth };
