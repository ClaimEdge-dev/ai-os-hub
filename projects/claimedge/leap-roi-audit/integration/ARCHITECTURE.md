# Leap Integration Architecture

## Recommended production flow

```
Leap CRM
  |  webhooks + REST API v3
  v
Vercel webhook receiver
  |
  +--> durable receipt + deterministic dedupe
  +--> normalize event
  +--> fetch expanded job/customer data when needed
  v
Neon: claimedge-prod / leap_roi
  |
  +--> gap audit
  +--> stage/cycle-time history
  +--> time ledger
  +--> financial-impact ledger
  +--> reconciliation findings
  +--> owner summary views
  v
Owner dashboard / periodic presentation
```

## Verified API facts

Leap's official API documentation currently states:
- REST API version 3.0
- base URL: https://api.jobprogress.com/api/v3
- OAuth 2.0 / bearer access token
- token generated from Leap Settings -> Developer
- admin access required to generate an access token
- list endpoints default to 10 results and can request up to 100
- API rate limit: 60 requests per minute
- webhook notifications are supported

Documented webhook event families:
- customer create
- customer delete
- job create
- job stage change
- job delete
- job lost
- task create
- task complete

Leap documents batching of up to 100 notifications in one webhook request and notes that delivery may be delayed by up to two minutes. The receiver should acknowledge durable receipt quickly rather than perform a full claim audit before responding.

## Ingestion rules

1. Validate request authenticity using the strongest control supported by the configured Leap account and deployment.
2. Return 200 only after durable receipt succeeds.
3. Generate a deterministic payload hash/event key that does not include local receipt time.
4. Store the normalized event and a minimum-necessary payload/audit envelope.
5. Never rely on event order.
6. For job stage changes, store both from-stage and to-stage.
7. Queue an expanded job fetch after create/stage/task events when required fields are not contained in the webhook.
8. Respect API throttling and use bounded retries with exponential backoff for API calls.
9. Never log access tokens, database URLs, or full secrets.
10. Store only the minimum customer information required for claims operations.
11. Keep webhook arrival time, provider/source time when available, and processing time separate.
12. Run reconciliation even when webhooks appear healthy.

## Suggested environment variables

- LEAP_API_BASE=https://api.jobprogress.com/api/v3
- LEAP_ACCESS_TOKEN=[secret]
- DATABASE_URL=[Neon pooled connection string]
- LEAP_WEBHOOK_SECRET=[only if the configured Leap setup supplies one]
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
- Daily reconciliation: Leap jobs vs Neon claims.
- Detect jobs present in one system but absent in the other.
- Refresh financial fields after estimates/supplements are verified.
- Generate weekly owner snapshot.
- Detect repeated missing fields and recommend Leap template changes.

## Financial-data boundary

The Leap event stream proves workflow activity, not financial realization.

For financial-impact events:
- verify carrier/estimate/payment evidence separately;
- use accounting data only when the connected books are authorized and the relevant transaction/account can be matched;
- never infer paid/collected from a Leap stage name.

## Release rule

Future/vendor-announced integrations are not treated as production dependencies until they are released, visible in the connected account, and verified.
