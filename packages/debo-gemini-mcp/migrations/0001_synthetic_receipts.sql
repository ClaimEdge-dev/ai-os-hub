-- Candidate schema for isolated synthetic receipts only. No canonical R19 data.
-- Apply through an approved migration workflow, never inside request handling.
CREATE TABLE bridge_fixture_receipts (
  project_id TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  input_sha256 TEXT NOT NULL CHECK (length(input_sha256) = 64),
  receipt_json TEXT NOT NULL CHECK (json_valid(receipt_json) AND length(receipt_json) <= 8192),
  PRIMARY KEY (project_id, idempotency_key)
);
