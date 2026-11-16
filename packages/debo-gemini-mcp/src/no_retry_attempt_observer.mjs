// GB-044: review-only trusted phase observation for staged synthetic work.
// This module never contacts an API, claims work, changes storage, or enables
// a retry. The caller MUST link observations to its actual durable claim;
// these in-process observations are not independently authenticated audit proof.
const outcome = (phase, providerEntered, storageAssurance) => Object.freeze({
  schema: 'debo.gemini.attempt_observation.v1',
  phase,
  provider_outcome: providerEntered
    ? 'UNKNOWN_AFTER_PROVIDER_ENTRY'
    : 'NO_PROVIDER_DISPATCH_OBSERVED_IN_THIS_PROCESS',
  storage_assurance: storageAssurance,
  automatic_retry_allowed: false,
  claim_replacement_allowed: false,
  may_mark_completed: false
});
export function createNoRetryAttemptObserver() {
  let phase = 'BEFORE_CLAIM';
  let entered = false;
  let storage = 'NO_CLAIM_OBSERVED';
  return Object.freeze({
    observeClaimUnknown() {
      if (phase !== 'BEFORE_CLAIM') throw new TypeError('Invalid attempt phase transition');
      phase = 'CLAIM_ACK_UNKNOWN';
      storage = 'UNKNOWN';
    },
    observeClaimAcknowledged() {
      if (phase !== 'BEFORE_CLAIM') throw new TypeError('Invalid attempt phase transition');
      phase = 'CLAIM_ACKNOWLEDGED';
      storage = 'ACKNOWLEDGED';
    },
    // Call at the exact trusted transport invocation boundary, not before
    // policy/validation checks. Once set, errors and timeouts cannot undo it.
    observeProviderEntry() {
      if (phase !== 'CLAIM_ACKNOWLEDGED') throw new TypeError('No acknowledged claim');
      entered = true;
      phase = 'PROVIDER_ENTRY_OBSERVED';
    },
    observeFailure() {
      if (phase === 'BEFORE_CLAIM') phase = 'BLOCKED_BEFORE_CLAIM';
      else if (phase === 'CLAIM_ACKNOWLEDGED') phase = 'FAILED_BEFORE_PROVIDER_ENTRY';
      else if (phase === 'PROVIDER_ENTRY_OBSERVED') phase = 'FAILED_AFTER_PROVIDER_ENTRY';
      return outcome(phase, entered, storage);
    },
    snapshot() { return outcome(phase, entered, storage); }
  });
}
