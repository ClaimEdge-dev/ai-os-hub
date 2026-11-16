import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createNoRetryAttemptObserver } from '../src/no_retry_attempt_observer.mjs';

test('GB-044 no claim and no dispatch is observed, but never grants retry', () => {
  const trace = createNoRetryAttemptObserver();
  const result = trace.observeFailure();
  assert.equal(result.provider_outcome,'NO_PROVIDER_DISPATCH_OBSERVED_IN_THIS_PROCESS');
  assert.equal(result.storage_assurance,'NO_CLAIM_OBSERVED');
  assert.equal(result.automatic_retry_allowed,false);
  assert.equal(result.claim_replacement_allowed,false);
  assert.equal(result.may_mark_completed,false);
});
test('ambiguous claim acknowledgement remains unknown, even without transport entry', () => {
  const trace=createNoRetryAttemptObserver();
  trace.observeClaimUnknown();
  const r=trace.observeFailure();
  assert.equal(r.phase,'CLAIM_ACK_UNKNOWN');
  assert.equal(r.storage_assurance,'UNKNOWN');
  assert.equal(r.automatic_retry_allowed,false);
  assert.throws(()=>trace.observeProviderEntry(),TypeError);
});
test('acknowledged claim with fresh authorization denial is not a provider call', () => {
  const trace=createNoRetryAttemptObserver();
  trace.observeClaimAcknowledged();
  const r=trace.observeFailure();
  assert.equal(r.phase,'FAILED_BEFORE_PROVIDER_ENTRY');
  assert.equal(r.provider_outcome,'NO_PROVIDER_DISPATCH_OBSERVED_IN_THIS_PROCESS');
  assert.equal(r.storage_assurance,'ACKNOWLEDGED');
  assert.equal(r.claim_replacement_allowed,false);
});
test('network error after transport entry is permanently ambiguous', () => {
  const trace=createNoRetryAttemptObserver();
  trace.observeClaimAcknowledged();
  trace.observeProviderEntry();
  const r=trace.observeFailure();
  assert.equal(r.phase,'FAILED_AFTER_PROVIDER_ENTRY');
  assert.equal(r.provider_outcome,'UNKNOWN_AFTER_PROVIDER_ENTRY');
  assert.equal(r.automatic_retry_allowed,false);
  assert.equal(trace.snapshot().provider_outcome,'UNKNOWN_AFTER_PROVIDER_ENTRY');
});
test('revocation after provider entry cannot reset the trace to never-started', () => {
  const trace=createNoRetryAttemptObserver();
  trace.observeClaimAcknowledged();trace.observeProviderEntry();
  trace.observeFailure();
  assert.throws(()=>trace.observeClaimUnknown(),TypeError);
  assert.throws(()=>trace.observeClaimAcknowledged(),TypeError);
  assert.throws(()=>trace.observeProviderEntry(),TypeError);
  assert.equal(trace.snapshot().provider_outcome,'UNKNOWN_AFTER_PROVIDER_ENTRY');
});
test('invalid transition cannot manufacture an acknowledged claim', () => {
  const trace=createNoRetryAttemptObserver();
  assert.throws(()=>trace.observeProviderEntry(),TypeError);
  trace.observeClaimUnknown();
  assert.throws(()=>trace.observeClaimAcknowledged(),TypeError);
  assert.equal(trace.snapshot().storage_assurance,'UNKNOWN');
});
test('observation is frozen, contains no private IDs and never implies financial authority', () => {
  const trace=createNoRetryAttemptObserver();
  const r=trace.snapshot();
  assert.equal(Object.isFrozen(r),true);
  assert.equal(JSON.stringify(r).includes('credential'),false);
  assert.equal(Object.hasOwn(r,'billing_verified'),false);
  assert.equal(Object.hasOwn(r,'execute'),false);
});
test('observation does not mutate claim storage or invoke transport', () => {
  let transportCalls=0,claimWrites=0;
  const dummy={transport:()=>transportCalls++,claim:()=>claimWrites++};
  const trace=createNoRetryAttemptObserver();
  trace.observeClaimAcknowledged();
  trace.observeProviderEntry();
  assert.equal(trace.observeFailure().automatic_retry_allowed,false);
  assert.equal(transportCalls,0);assert.equal(claimWrites,0);
  void dummy;
});
