# D-066 — Record product-boundary-preview.v2 as DR-010's accepted Route C candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records an independent ACCEPT.
> Same form as D-035 / D-038 / D-042.
> **Does not** owner-record.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `d0284aab3259731cb2d694350cb7f66956022d3e1f380f0278ab44142e60e4dc` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| candidate | `docs/coop/artifacts/product-boundary-preview.v2.json` `ff7a09130a2b5b409b02725a839f9d7b5fb88e945d7f9bbb63c0d0154c627b85` |
| Claude 2 | `docs/coop/artifacts/product-boundary-preview.v2.review-independent.claude2.json` `d5c1eccd7a6fa6cf1bf364563e1b47aa66252913a06b2cc0c8dc8c6d666ec273` ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/product-boundary-preview.v2.review-independent.codex.json` `8b64732cfd1b87fedd6a78104b5cf19be87f58815b97f516cd41017f57fc9ce1` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Decision

1. Record `product-boundary-preview.v2.json` as DR-010's accepted
   Route C design-candidate for architecture-preview scope. The
   seven file-02 items are EXCLUDED or NOT REPLACED. P-1, P-2,
   and G3-SUBSTRATE are preserved. CD-RT-5 is untouched.
2. This is not owner recording. An ACCEPT verdict is not owner
   recording. DR-010 stays HARD-BLOCKED. Condition 1 does not
   discharge until the product owner records. DR-117 and
   DR-011-R16 stay independently required.
3. Does not mark SATISFIED. Does not edit file 08. Conditions
   2–5 remain. Condition 5 remains the only implementation
   authorization.

## Alternatives

- Treat ACCEPT as owner recording. Rejected.
- Also close DR-117 / R16 here. Rejected: bundling; those remain
  independently required.

## Readiness effect

Zero.

## Reversibility

Total. Overturn: C-D066.
