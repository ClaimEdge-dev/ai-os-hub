-- STAGED ONLY. No live migration or provider activation is authorized here.
-- Separate from the existing immutable fixture table; never drops/replaces it.
CREATE TABLE IF NOT EXISTS bridge_execution_claims (
  project_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  provider_scope TEXT NOT NULL,
  request_sha256 TEXT NOT NULL CHECK(length(request_sha256) = 64),
  request_json TEXT NOT NULL CHECK(length(request_json) <= 48000),
  owner_token TEXT NOT NULL,
  state TEXT NOT NULL CHECK(state IN ('CLAIMED', 'COMPLETED', 'UNCERTAIN')),
  receipt_json TEXT CHECK(receipt_json IS NULL OR length(receipt_json) <= 48000),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY(project_id, idempotency_key),
  CHECK((state = 'COMPLETED' AND receipt_json IS NOT NULL) OR (state != 'COMPLETED' AND receipt_json IS NULL))
);
