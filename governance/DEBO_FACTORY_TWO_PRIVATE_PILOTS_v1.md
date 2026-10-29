# DEBO Business Build Factory — two private contract pilots

Branch: `debo-factory-private-pilots-2026-10-29`

Status: PRIVATE SYNTHETIC TESTS. These files do **not** mutate the live JCT or Morgan's CRM, website, ownership, published content, rates or payments.

Use existing `DEBO Core → Industry Blueprint → Project Adapter → Local Brand/Data → Verified Build` rule. These artifacts are a first executable contract layer, **not** an operational deployment or proof of live ingestion.

## Source-first recovery
- JCT: existing JCT-OPS, Google Sheets operations pack (Dispatch Log, Billing Lines, Evidence QA, Rate Sources and Payments AR); Higgsfield V2 owner-review site and Lovable CRM migration source remain separate from this test.
- Morgan's: existing MOL Sister Brain and owner command source, BTF-001 Brand & Template Forge, protected Site/editor source and brand proofs. Never replace or publish site or invent NAP/menu/event details.
- No shadow CRM or duplicate document factory is created.

## Acceptance contract
1. Test only synthetic cases, never real customer data.
2. Validate the correct industry-specific adapter and module classification.
3. JCT: synthetic request → draft dispatch record → evidence gate → rate-authority gate → QA HOLD when authorization/evidence/rate missing. No actual bill, financial claim or live CRM write.
4. Morgan's: synthetic inquiry → private CRM candidate → approved-source brand gate → owner/public-truth gate → HOLD pending approvals. No public design or live submission.
5. Generate receipts, linking to `BusinessAudit` and `GAP-JCT-FACTORY-PILOT` / `GAP-MOL-FACTORY-PILOT`.
6. Test outcomes are **contract tests** only. Next gate requires real adapter integration and authenticated write/readback in an authorized sandbox before calling E2E or deployed.

## Run
```
python -m unittest discover -s tests -p 'test_debo_factory_pilot.py'
python tools/debo_factory_pilot.py projects/jcs-towing/factory-adapter.json projects/jcs-towing/factory-pilot-case.json
python tools/debo_factory_pilot.py projects/morgans/factory-adapter.json projects/morgans/factory-pilot-case.json
```

## QA gates
No public send, publish, payment, domain/ownership change or production write. Missing rates remain null, never zero or guessed. Missing approved brand source keeps Morgan's creative output a placeholder, not a claimed usable asset. Do not log synthetic records as real jobs or bookings.
