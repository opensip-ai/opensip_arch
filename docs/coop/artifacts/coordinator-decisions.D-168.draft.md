# D-168 — Record preview-product-boundary-successor.v7 as DR-117 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `preview-product-boundary-successor.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-137 / D-159. Not a three-limb act. Not a required-now
> successor.
> This is coordinator decision **D-168**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** open D-056 Class A.
> **Does not** perform SATISFIED-GRADE.
> **Does not** add a DR-G* row or change required-now 27.
> **Does not** rewrite G29, G30, or G31.
> **Does not** record G32.
> **Does not** record v6.
> **Does not** edit file 08.
> **Does not** invent a D9 code, a section 7.1 recipe, or
> a D-006 unit.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-167 is ADOPTED at
`1dcff7649b407728476ee9b0058385daf206a601`.
HEAD is `1dcff7649b407728476ee9b0058385daf206a601`.
Last live heading is D-167. Required-now is 27.

Stage A dual independent ACCEPT 0/0 of the frozen
successor candidate (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/preview-product-boundary-successor.v7.review-independent.claude2.json` | `d154e94a6c3803aab67600b515303b112844f21593b39fe8a8f441b276ed4e87` | ACCEPT 0/0; advisories CLAUDE-PPBS-V7-ADV-1 / CLAUDE-PPBS-V7-ADV-2; standing CLAUDE-PPBS-V3-ADV-1 venue limb |
| Codex | `docs/coop/artifacts/preview-product-boundary-successor.v7.review-independent.codex.json` | `0609c561e50dd50dda81f2c6075deb2e16365e6727d7f1c9f2117efb7c25068c` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| preview-product-boundary-successor.v7.json | `243c12a2389a0f81d059209f5b7050a700498840d036275c7b81eeadc31fe548` |
| preview-product-boundary-successor.v7.review-independent.claude2.json | `d154e94a6c3803aab67600b515303b112844f21593b39fe8a8f441b276ed4e87` |
| preview-product-boundary-successor.v7.review-independent.codex.json | `0609c561e50dd50dda81f2c6075deb2e16365e6727d7f1c9f2117efb7c25068c` |
| preview-product-boundary-successor.v6.json | `b27789492ce2b603ade591a4246fad2b565cfff9106ac05e0b6f674eb5e53bab` |
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| COORDINATOR-DECISIONS.md | `e501239b47a5ba7f86d9c508b1ac3c739719326bdd531f14a312f61d955885cd` |
| file 08 | `9af2bc71adf437c8a138aa6caadd2e6ae55fa9f2165b74e816ef1d45df739b76` |
| D-167 commit / HEAD | `1dcff7649b407728476ee9b0058385daf206a601` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v7, both
Stage A verdicts, v6, v5, and this draft unmoved, re-measure
before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 27 of 27
named; owners 31 of 31; last gate row DR-G31; DR-117 lead
token remains `OPEN`. v7's internal `recordedInputs.HEAD`
and file-08 pin remain the pre-D-167 values
(`5d5d778…` / `3a9442d1…`). Codex remasured on the live
post-D-167 tree and found D-167 changes no DR-117 row,
cited gate row, seven-item source, mapping, or enforcement
ownership. That pin drift is therefore not a DR-117
scope effect. This recording does not rewrite v7.

## Why this entry exists

D-137 recorded v5 as DR-117's preview-scoped successor
candidate and reserved Class A. D-157 / D-158 / D-159
named the leftover EE classes; D-159 recorded that
Eligibility gates 2 and 3 hold. v6 tried to withdraw the
Class A reservation inside an artifact and was REJECT
(CLAUDE-PPBS-V6-B1). v7 restores the Class A refusal,
lands CLAUDE-PPBS-V6-SF1 / ADV-1, and remasures
existingGate after D-157 / D-158 / D-159. Dual
independent ACCEPT 0/0 now exists. This entry records
v7. It is not SATISFIED-GRADE.

v6 stays frozen. Do not record v6.

## Decision

1. Record `preview-product-boundary-successor.v7.json`
   as DR-117 leftover remasurement after D-157 / D-158 /
   D-159. The candidate binds NOTHING. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-117 stays `OPEN`. leftover-design of unnamed EE
   classes remains closed at D-159. Remainder is named-gate
   execution. Naming is not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 continue to hold for
   DR-117 (D-159). Gate 1 Class A remains false under
   D-137's express reservation. v7 does not withdraw that
   reservation. Venue for any later lift is a reviewed
   coordinator act, not an artifact. Gates 4 and 5 are
   not performed. Not eligible in kind. Not SATISFIED.
4. Required-now stays 27. Condition-4 effect is zero.
   Condition 4 stays MET at 27 of 27 required names and
   31 of 31 owners. MET is not QUALIFIED.
5. Advisories CLAUDE-PPBS-V7-ADV-1 and
   CLAUDE-PPBS-V7-ADV-2 travel as honesty work. Standing
   CLAUDE-PPBS-V3-ADV-1 venue limb stands. Does not
   record v6. Does not rewrite G29, G30, or G31. Does
   not record G32. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`. Does not edit
   file 08.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (27 of 27). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D168. Does not unwrite D-137, D-157, D-158, D-159,
or D-167.
