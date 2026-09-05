# D-137 — Record preview-product-boundary-successor.v5 as DR-117's preview-scoped successor candidate

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX from both reviewers). Same
> no-cell-edit branch as D-116 / D-131 / D-136. DR-117's live
> cell is a bare `OPEN` and does not become false on adoption.
> **Subject:** `docs/coop/artifacts/preview-product-boundary-successor.v5.json`
> only.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> This is coordinator decision **D-137**, not a register row.

D-136 is ADOPTED at `d204ba095da7f91da1ca99b39ea89478b7cc4805`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| Claude 2 verdict | `51289f8efe15123d18f548507090bfa8b6990b94ec491fa2e4b6940b68e23b45` ACCEPT, 0/0, advisories CLAUDE-PPBS-V5-ADV-1 / CLAUDE-PPBS-V5-ADV-2 |
| Codex verdict | `ec1517dc4fade8a43dfaa9f1b174be5c6058a326cc203e392d5f9a8673453dd1` ACCEPT, 0/0, advisory PPBSV4-ADV-1 |
| product-boundary-successor-contract.v8.json (D-116; unmoved) | `52c70f7715fb869bae70bc588043dc5b4d731b73408d2d451e868b8de963f362` |
| product-boundary-preview.v2.json (D-068; unmoved) | `ff7a09130a2b5b409b02725a839f9d7b5fb88e945d7f9bbb63c0d0154c627b85` |
| COORDINATOR-DECISIONS.md | `d3d8db1713b0a92182088b23c4c5e8931522a02c2d875850eac4e47eba7f9fd4` |
| file 08 | `7585325d73a678739b74309700680e6b7663bf017c6d5a6796eee4cc1441d94e` |
| D-136 commit | `d204ba095da7f91da1ca99b39ea89478b7cc4805` |

If a cited file moves in a way that is not append-only COORD
growth with file 08, the v5 subject, both v5 verdicts, recorded
v8, recorded preview.v2, and this draft unmoved, re-measure
before adoption. Append-only COORD after this remeasurement,
with those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is
not a MUST-FIX.

## Decision

1. Record `preview-product-boundary-successor.v5.json` as
   DR-117's preview-scoped successor **candidate**, authorized
   by D-132. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-117 stays `OPEN`. No `SATISFIED`. No `QUALIFIED`. The
   candidate binds NOTHING. D-056 Class A is not opened.
   This recording is not a SATISFIED re-record.
3. product-boundary-successor-contract.v8 remains the D-116
   leftover T2-02 candidate and is not replaced. D-068 remains
   the owner recording of product-boundary-preview.v2 for
   DR-010 / condition 1 and does not close DR-117.
4. Advisories CLAUDE-PPBS-V5-ADV-1, CLAUDE-PPBS-V5-ADV-2, and
   Codex PPBSV4-ADV-1 travel as honesty work. They are not
   SHOULD-FIX and do not block this recording.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`. Does not mint a D-096 (A)
   grant.
6. Does not SATISFY DR-131, DR-133, or any other row. Does
   not overturn D-116, D-068, D-066, or D-136.

### Readiness effect

Zero. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total. Overturn: C-D137.
