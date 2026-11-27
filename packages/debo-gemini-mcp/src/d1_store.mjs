import { PolicyError } from './contracts.mjs';
import { verifyReceipt } from './synthetic_contract.mjs';

// Only fixed synthetic results are inserted. This does NOT implement pre-call
// ownership or exactly-once execution for any future paid provider adapter.
export class D1FixtureStore {
  constructor(binding) {
    try {
      if (typeof binding?.withSession !== 'function') throw new Error();
      this.session = binding.withSession('first-primary');
    } catch { throw new PolicyError('STORE_UNAVAILABLE', 'Persistent receipt store is unavailable'); }
  }
  async query(sql, values) {
    let timer;
    try {
      return await Promise.race([
        this.session.prepare(sql).bind(...values).first(),
        new Promise((_, reject) => { timer = setTimeout(() => reject(new Error('deadline')), 1500); })
      ]);
    } catch { throw new PolicyError('STORE_UNAVAILABLE', 'Receipt store request failed; replay only the same request key'); }
    finally { clearTimeout(timer); }
  }
  readRow(args) {
    return this.query('SELECT owner_id, input_sha256, receipt_json FROM bridge_fixture_receipts WHERE project_id = ?1 AND idempotency_key = ?2', [args.project_id, args.idempotency_key]);
  }
  async read(principal, args) {
    const row = await this.readRow(args);
    if (!row || row.owner_id !== principal) return null;
    return verifyReceipt(row, principal, args);
  }
  async put(principal, args, candidate) {
    const inserted = await this.query(
      'INSERT INTO bridge_fixture_receipts (project_id, idempotency_key, owner_id, input_sha256, receipt_json) VALUES (?1, ?2, ?3, ?4, ?5) ON CONFLICT(project_id, idempotency_key) DO NOTHING RETURNING owner_id',
      [args.project_id, args.idempotency_key, principal, candidate.input_sha256, JSON.stringify(candidate)]
    );
    const row = await this.readRow(args);
    if (!row) throw new PolicyError('STORE_UNAVAILABLE', 'Receipt write could not be independently read back');
    if (row.owner_id !== principal) throw new PolicyError('IDEMPOTENCY_CONFLICT', 'Receipt key is already in use');
    const receipt = await verifyReceipt(row, principal, args);
    if (receipt.input_sha256 !== candidate.input_sha256) throw new PolicyError('IDEMPOTENCY_CONFLICT', 'Receipt key is already in use');
    return { receipt, deduplicated: inserted === null };
  }
}
