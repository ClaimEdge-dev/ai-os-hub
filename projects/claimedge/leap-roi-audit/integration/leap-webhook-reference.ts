// Reference-only Vercel-style webhook receiver.
// Keep secrets in environment variables. Do not deploy until Leap + Neon credentials are configured.
// This file intentionally avoids binding to a specific web framework version.

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
  action: string | null;
  operation: string | null;
  externalId: string | null;
  jobId: string | null;
  jobNumber: string | null;
  customerId: string | null;
  stageFrom: string | null;
  stageTo: string | null;
  details: Record<string, unknown>;
  receivedAt: string;
};

function str(v: unknown): string | null {
  return v === undefined || v === null || v === "" ? null : String(v);
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

  // Replace with a stronger provider event ID if Leap exposes one in the configured webhook payload.
  const eventKey = [
    action ?? "unknown",
    operation ?? "unknown",
    externalId ?? "none",
    jobId ?? "none",
    jobNumber ?? "none",
    stageFrom ?? "none",
    stageTo ?? "none",
    receivedAt.slice(0, 16)
  ].join(":");

  return {
    eventKey,
    action,
    operation,
    externalId,
    jobId,
    jobNumber,
    customerId,
    stageFrom,
    stageTo,
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
2. Validate request authenticity based on the supported Leap webhook configuration.
3. For each event:
   - normalize
   - insert raw/normalized envelope with ON CONFLICT DO NOTHING
   - upsert job shell when job identity is present
   - append work/stage event
   - enqueue/trigger gap audit when shouldRunGapAudit(...) is true
4. Commit transaction.
5. Return HTTP 200 quickly.
6. Separately call Leap API v3 to refresh full job/customer data where needed.

Do NOT:
- commit LEAP_ACCESS_TOKEN
- log DATABASE_URL
- treat webhook details as complete financial truth
- infer payment from stage names
- overwrite verified values with weaker-source values
*/
