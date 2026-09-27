# Leap Integration Architecture

## Recommended production flow

```
Leap CRM
  |  webhooks + REST API v3
  v
Vercel webhook receiver
  |
  +--> normalize/dedupe event
  +--> fetch expanded job/customer data when needed
  v
Neon: claimedge-prod / leap_roi
  |
  +--> gap audit
  +--> time ledger
  +--> financial-impact ledger
  +--> owner summary views
  v
Owner dashboard / periodic presentation
```

## Why this path

Use Leap's supported API instead of browser scraping whenever possible.

Current official contractor-Leap API documentation indicates:
- API v3
- base URL: https://api.jobprogress.com/api/v3
- OAuth 2.0 / bearer access token generated from Leap Settings -> Developer
- admin access is required to generate the token
- list endpoints are paginated and commonly support includes[]
- rate limit is 60 requests/minute
- webhook notifications are supported

Webhook event families currently documented include:
- customer create
- customer delete
- job create
- job stage change
- job delete
- job lost
- task create
- task complete

Notifications may be batched and should be treated as event triggers, not as the complete canonical job record. Fetch the current job after material events when a fresh full snapshot is required.

## Ingestion rules

1. Verify webhook authenticity using the supported mechanism available in the Leap account/configuration.
2. Return 2xx quickly after durable receipt.
3. Store an immutable raw-event envelope or hash for deduplication.
4. Never rely on event order.
5. For job stage changes, store both from-stage and to-stage.
6. Queue an expanded job fetch after create/stage/task events when required fields are not contained in the webhook.
7. Respect API throttling and use exponential backoff.
8. Never log access tokens or full secrets.
9. Store only the minimum personal/customer information needed for claims operations.
10. Separate webhook arrival time, source event time when available, and processing time.

## Suggested environment variables

- LEAP_API_BASE=https://api.jobprogress.com/api/v3
- LEAP_ACCESS_TOKEN=[secret]
- DATABASE_URL=[Neon pooled connection string]
- LEAP_WEBHOOK_SECRET=[only if supported/configured]
- AUDIT_OPERATOR=DEBO

Do not commit actual secret values.

## Automation opportunities

### Immediate
- Auto-create/update job shell in Neon on Leap job create.
- Auto-log stage movement.
- Auto-log task created/completed.
- Trigger missing-field audit after job creation and important stage changes.
- Calculate cycle time between stages.
- Flag stage transitions where critical required fields are still missing.

### Next
- Periodic reconciliation: Leap jobs vs Neon claims.
- Detect jobs present in one system but absent in the other.
- Refresh financial fields after estimates/supplements are uploaded.
- Generate weekly owner snapshot.
- Detect repeated missing fields and recommend Leap template changes.

## Financial-data boundary

The Leap event stream proves workflow activity, not financial realization.

For financial-impact events:
- verify carrier/estimate/payment source separately;
- use QuickBooks only when the company's connected books are authorized and the relevant transaction/account can be matched;
- never infer paid/collected from a Leap stage name.

## Xactimate note

Leap announced on 2026-09-25 that it is developing a direct Xactimate integration targeted for winter 2026. Treat it as FUTURE until actually released and verified in the account.
