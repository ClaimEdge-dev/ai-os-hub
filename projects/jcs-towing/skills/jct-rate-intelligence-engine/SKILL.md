---
name: jct-rate-intelligence-engine
description: Build and maintain JC's Towing's source-verified towing-rate intelligence across Illinois/Chicagoland municipalities, insurers, commercial accounts, police rotations, relocation limits, historical JC billing, and market benchmarks.
---

# JCT Rate Intelligence Engine

## Trigger
Use for JCT RATE research, rate comparisons, rate-source registers, insurer-rate claims, municipal benchmarks, proposed list rates, or rate expiration/review.

## Rules
- Recover existing JCT rate work before researching or creating new schedules.
- Separate LEGAL MAXIMUM / CONTRACT RATE / MUNICIPAL RATE / MARKET BENCHMARK / INSURANCE PAYMENT EXPERIENCE / JC LIST RATE / NEGOTIATED RATE.
- Never apply a rate from one towing lane to another without authority.
- Never claim an insurer pays a rate without actual carrier/payment/contract evidence.
- Current-rate findings use VERIFIED / LIKELY / UNRESOLVED.
- Every proposed JC rate must cite one or more rate-source IDs.
- Public/customer use remains approval-gated.

## Core record
Rate ID; service; vehicle/equipment class; payer/jurisdiction; amount; unit; source type; source organization; source URL/file; effective date; verified date; legal cap; contract flag; market benchmark; insurance-payment evidence; notes; status.

## Output
Updated rate-source register, benchmark matrix, proposed-rate delta, conflicts/gaps, and next verification action.
