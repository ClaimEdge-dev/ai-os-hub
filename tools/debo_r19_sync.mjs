/** Read-only R19 synchronization planner. No network, no external writes. */
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const types = new Set(['TASK_VERIFIED','SOURCE_SAVED','TEST_FAILED','BLOCKER_RESOLVED','VERSION_APPROVED','CHECKPOINT_ADVANCED']);
const goodStates = new Set(['UNKNOWN','PROPOSED','BUILT','TESTED','APPROVED','DEPLOYED','LIVE','BLOCKED']);
const evidenceByStatus = {TESTED:'test_receipt',APPROVED:'owner_approval',DEPLOYED:'deployment_receipt',LIVE:'runtime_probe'};

export function planSync(event, seenEventIds = new Set()) {
  if (!event || event.schema !== 'debo.r19.event.v1' || !types.has(event.event_type)) throw new Error('invalid event');
  for (const key of ['event_id','project_id','task_id','checkpoint','source_revision']) {
    if (typeof event[key] !== 'string' || !event[key].trim()) throw new Error('invalid ' + key);
  }
  if (!goodStates.has(event.status)) throw new Error('invalid state');
  if (!Array.isArray(event.evidence)) throw new Error('invalid evidence');
  const needed = evidenceByStatus[event.status];
  if (needed && !event.evidence.some(p => p && p.type === needed && typeof p.ref === 'string' && p.ref.trim())) {
    throw new Error('missing proof: ' + needed);
  }
  if (event.event_type === 'TASK_VERIFIED' && !needed) throw new Error('no verified completion evidence');
  if (!['private','public_metadata'].includes(event.scope)) throw new Error('scope is required');
  if (seenEventIds.has(event.event_id)) return {event_id:event.event_id, result:'SKIP_DUPLICATE', writes:0};
  // Read-only planning; public feed may receive only metadata events already explicitly scoped for publication.
  const destinations = ['OWNING_PROJECT_CHECKPOINT','DEBO_CORE_INDEX'];
  if (event.scope === 'public_metadata') destinations.push('PUBLIC_SOURCE_HEALTH_FEED_REVIEW');
  return {event_id:event.event_id, result:'DRY_RUN', writes:0,
          project_id:event.project_id, destinations, external_write_permitted:false};
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const event = JSON.parse(readFileSync(process.argv[2], 'utf8'));
    const seen = process.argv[3] ? new Set(JSON.parse(readFileSync(process.argv[3], 'utf8'))) : new Set();
    process.stdout.write(JSON.stringify(planSync(event, seen), null, 2)+'\n');
  } catch (err) { process.stderr.write(String(err)+'\n'); process.exitCode=1; }
}
