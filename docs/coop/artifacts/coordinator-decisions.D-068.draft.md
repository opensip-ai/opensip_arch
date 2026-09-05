# D-068 — Product-owner record of product-boundary-preview.v2 for DR-010

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** PREFERENCE-LADEN. Product-owner recording
> under D-000 (product-authority grant). Not D-054 (D-054 is
> preview Route B only).
> **Does** owner-record DR-010, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** close DR-117 or DR-011-R16.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `281bd81d2ca509c4fb36278dfbfb5c47a9ab8c112503dff5dd6d8893d665fefa` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| candidate | `docs/coop/artifacts/product-boundary-preview.v2.json` `ff7a09130a2b5b409b02725a839f9d7b5fb88e945d7f9bbb63c0d0154c627b85` |
| Claude 2 | `docs/coop/artifacts/product-boundary-preview.v2.review-independent.claude2.json` `d5c1eccd7a6fa6cf1bf364563e1b47aa66252913a06b2cc0c8dc8c6d666ec273` ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/product-boundary-preview.v2.review-independent.codex.json` `8b64732cfd1b87fedd6a78104b5cf19be87f58815b97f516cd41017f57fc9ce1` ACCEPT 0/0 |
| D-066 commit | `c2d7f7704be9e89dac8859f15e086b3694c3227b` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority

- Product owner (file 08 DR-010). D-000 authorizes
  coordinator/product-authority decisions on the user's behalf.
  This entry is that product-owner recording.
- D-066 already recorded v2 as the accepted candidate. This
  entry is the later owner act D-066 left owed.
- D-054 does not apply. This is Route C, not Route B.

## Decision

1. As product owner, record
   `docs/coop/artifacts/product-boundary-preview.v2.json` as the
   preview-scope product disposition of file 02's seven binding
   items: PB-1..PB-6 EXCLUDED, PB-7 NOT REPLACED. P-1, P-2, and
   G3-SUBSTRATE are preserved. CD-RT-5 is untouched.
2. This may discharge condition 1 for DR-010 within
   architecture-preview scope only.
3. Does not mark DR-010 SATISFIED. Does not close DR-117 or
   DR-011-R16. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.

## Alternatives

- Wait for a human product-owner act. Rejected: D-000 already
  delegates product-authority decisions.
- Also close DR-117 / R16 here. Rejected: independently
  required; would bundle.

## Readiness effect

Condition 1 for DR-010 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D068, plus reconciliation of any later
MF-6 note. Does not overturn D-066.
