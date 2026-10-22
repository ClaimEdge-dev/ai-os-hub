// Reference-only Leap webhook normalization.
// Keep secrets in environment variables. Do not deploy until Leap + Neon credentials are configured.
// This file intentionally avoids binding to a specific web framework version.

import { createHash } from "node:crypto";

type LeapEvent = {
  action?: string;
  operation?: string;
  id?: number | string;
  stage_moved_from?: { name?: string; code?: string; removed?: boolean };
  stage_moved_to?: { name?: string; code?: string; removed?: boolean };
  details?: Record<string, unknown>;
};

export type NormalizedLeapEvent = {
  eventKey: string;
  payloadHash: string;
  action: string | null;
  operation: string | null;
  externalId: string | null;
  jobId: string | null;
  jobNumber: string | null;
  customerId: string | null;
  stageFrom: string | null;
  stageTo: string | null;
  sourceEventAt: string | null;
  details: Record<string, unknown>;
  receivedAt: string;
};

function str(v: unknown): string | null {
  return v === undefined || v === null || v === "" ? null : String(v);
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    return Object.keys(value as Record<string, unknown>)
      .sort()
      .reduce<Record<string, unknown>>((acc, key) => {
        acc[key] = canonicalize((value as Record<string, unknown>)[key]);
        return acc;
      }, {});
  }
  return value;
}

function sha256Canonical(value: unknown): string {
  const canonical = JSON.stringify(canonicalize(value));
  return createHash("sha256").update(canonical).digest("hex");
}

export function normalizeLeapEvent(e: LeapEvent): NormalizedLeapEvent {
  const details = (e.details ?? {}) as Record<string, unknown>;
  const receivedAt = new Date().toISOString();

  const action = str(e.action);
  const operation = str(e.operation);
  const externalId = str(e.id);
  const jobId = str(details.job_id ?? (action === "jobs" ? e.id : null));
  const jobNumber = str(details.job_number);
  const customerId = str(details.customer_id);
  const stageFrom = str(e.stage_moved_from?.name);
  const stageTo = str(e.stage_moved_to?.name);

  // Leap's documented task-complete payload may include completed_at.
  // Other event families do not always provide a source timestamp.
  const sourceEventAt = str(details.completed_at);

  // Critical: the key MUST NOT include receipt time.
  // Leap can retry the same notification; retries must collapse to the same key.
  const payloadHash = sha256Canonical(e);
  const eventKey = payloadHash;

  return {
    eventKey,
    payloadHash,
    action,
    operation,
    externalId,
    jobId,
    jobNumber,
    customerId,
    stageFrom,
    stageTo,
    sourceEventAt,
    details,
    receivedAt
  };
}

export function shouldRunGapAudit(e: NormalizedLeapEvent): boolean {
  if (e.action === "jobs" && ["create", "stage_change"].includes(e.operation ?? "")) return true;
  if (e.action === "tasks" && ["created", "completed"].includes(e.operation ?? "")) return true;
  return false;
}

/*
Production handler outline:

1. Parse request body as LeapEvent[].
2. Validate request authenticity using the strongest control available in the configured Leap account.
3. For each event:
   - normalize
   - INSERT webhook event with event_key UNIQUE and ON CONFLICT DO NOTHING
   - upsert job shell when job identity is present
   - append stage/work event with its own deterministic event key
   - trigger the gap audit when shouldRunGapAudit(...) is true
4. Commit durable receipt quickly and return HTTP 200 within the provider timeout.
5. Separately call Leap API v3 to refresh full job/customer data when needed.
6. Reconciliation remains mandatory because webhook delivery can be delayed or fail.

Do NOT:
- commit LEAP_ACCESS_TOKEN
- log DATABASE_URL
- use receivedAt as a dedupe key
- treat webhook details as complete financial truth
- infer payment from stage names
- overwrite verified values with weaker-source values
*/
