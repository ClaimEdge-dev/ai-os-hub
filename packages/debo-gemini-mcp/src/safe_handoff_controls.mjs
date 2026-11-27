// GB-118 / GB-082: unactivated source and browser-handoff safety primitives.
// No browser session, account, network, provider, storage, or SDK is accessed.
// The caller must verify source independence and draft provenance. These
// functions are not installed in the active host or a replacement for approval.
const SOURCE = /^[A-Za-z][A-Za-z0-9._:-]{2,99}$/;
const MISSION = /^[A-Z][A-Z0-9-]{2,79}$/;
const MAX_READS = 4;
const REFUSED = Object.freeze({ status: 'BLOCKED', code: 'UNVERIFIED_DRAFT_PRESERVED' });
function validSource(value) { return typeof value === 'string' && SOURCE.test(value); }

export async function runIndependentReads(items, { maxConcurrent = 3 } = {}) {
  if (!Array.isArray(items) || items.length > 100 ||
      !Number.isSafeInteger(maxConcurrent) || maxConcurrent < 1 || maxConcurrent > MAX_READS ||
      items.some(x => !x || typeof x !== 'object' || Array.isArray(x) ||
        Object.keys(x).length !== 3 || !validSource(x.source_id) ||
        typeof x.read !== 'function' || x.independent !== true)) {
    throw new TypeError('Bounded independent reads require verified source IDs and read tasks');
  }
  const results = Array(items.length);
  let cursor = 0;
  const runner = async () => {
    for (;;) {
      const i = cursor++;
      if (i >= items.length) return;
      const task = items[i];
      try {
        const value = await task.read();
        results[i] = Object.freeze({ source_id: task.source_id, status: 'FULFILLED', value });
      } catch {
        // Never publish private connector error messages or automatically retry
        // a rate-limited, failed, timed-out or unauthorized source read.
        results[i] = Object.freeze({ source_id: task.source_id, status: 'FAILED', code: 'READ_FAILED' });
      }
    }
  };
  await Promise.all(Array.from({ length: Math.min(maxConcurrent, items.length) }, () => runner()));
  return Object.freeze(results);
}

export function createSerializedSourceWriter() {
  // In-memory queue only. The owning connector must still establish source
  // version/caller authority and durable write idempotency before mutation.
  const tailBySource = new Map();
  const inFlightKeys = new Set();
  return Object.freeze({
    async write({ source_id, mutation_id, run } = {}) {
      if (!validSource(source_id) || typeof mutation_id !== 'string' ||
          !SOURCE.test(mutation_id) || typeof run !== 'function') {
        throw new TypeError('Source, mutation and writer callback required');
      }
      const scopedKey = JSON.stringify([source_id, mutation_id]);
      if (inFlightKeys.has(scopedKey)) throw new Error('DUPLICATE_IN_FLIGHT_WRITE');
      inFlightKeys.add(scopedKey);
      const previous = tailBySource.get(source_id) ?? Promise.resolve();
      // A prior failure must not poison the source queue, but neither is
      // automatically replayed or treated as an accepted write.
      const current = previous.catch(() => {}).then(run);
      tailBySource.set(source_id, current);
      try { return await current; }
      finally {
        inFlightKeys.delete(scopedKey);
        if (tailBySource.get(source_id) === current) tailBySource.delete(source_id);
      }
    }
  });
}

export function prepareDraftReplacement({ mission_id, current_text, next_text, checkpointed_previous_text } = {}) {
  if (!MISSION.test(mission_id ?? '') || typeof current_text !== 'string' ||
      typeof next_text !== 'string' || next_text.length === 0 ||
      !next_text.startsWith('DEBO-HANDOFF ' + mission_id + '\n')) {
    throw new TypeError('Closed handoff mission and explicitly marked next draft required');
  }
  // Empty composer: safe to prepare but this function DOES NOT write it.
  if (current_text === '') {
    return Object.freeze({ status: 'PREPARED_EMPTY_EDITOR', allowed: true, proposed_text: next_text });
  }
  // Same mission alone is not ownership proof. Require exact content that was
  // previously read and checkpointed. Changed, unknown and unrelated drafts
  // are blocked without echoing their contents.
  if (current_text.startsWith('DEBO-HANDOFF ' + mission_id + '\n') &&
      typeof checkpointed_previous_text === 'string' &&
      checkpointed_previous_text === current_text) {
    return Object.freeze({ status: 'PREPARED_VERIFIED_REPLACEMENT', allowed: true, proposed_text: next_text });
  }
  return REFUSED;
}
