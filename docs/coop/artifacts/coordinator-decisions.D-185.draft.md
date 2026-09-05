# D-185 — Record platform-tcb-leftover-join.v6 as DR-126 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `platform-tcb-leftover-join.v6.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-184. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-185**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-126.
> **Does not** apply platform-tcb-contract.v45.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G22-FX-AUTHORING
> or OBL-RESERVED-TABLES.
> **Does not** populate a TCB table.
> **Does not** invent fixture bytes.
> **Does not** record frozen v5 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G22, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-184 is ADOPTED at
`d9059b949b426a4a4044ab0d20120111b474fd3b`.
HEAD is `d9059b949b426a4a4044ab0d20120111b474fd3b`.
Last live heading is D-184. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/platform-tcb-leftover-join.v6.review-independent.claude2.json` | `c5bb993040a68e7ed772f061453ca75ffad0d94b440f32399f0c9864cc3f3a01` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/platform-tcb-leftover-join.v6.review-independent.codex.json` | `997d5654bc3cbb09cffbcd0d4724934f457e2aff617cff91f44d64d6086d56da` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| platform-tcb-leftover-join.v6.json | `c799f4d7f4dc5206b777e82da934ef8812bc11c87f3edc10d234ceaf8fba79b4` |
| platform-tcb-leftover-join.v6.review-independent.claude2.json | `c5bb993040a68e7ed772f061453ca75ffad0d94b440f32399f0c9864cc3f3a01` |
| platform-tcb-leftover-join.v6.review-independent.codex.json | `997d5654bc3cbb09cffbcd0d4724934f457e2aff617cff91f44d64d6086d56da` |
| COORDINATOR-DECISIONS.md | `e4a58d3516622df1c4c3f099ca0f672179fbc703fc4b9d5e3f1b3567c7b68394` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `d9059b949b426a4a4044ab0d20120111b474fd3b` |
| Frozen v5 (historical, not this subject) | `fa559ccc815cc6e6d4beace3b613f520d91c0473dd521a2a81e646db42af173e` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v6, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-126 lead
token remains `OPEN`. v6's top-level head, recordedInputs.HEAD,
file08Pin, and both requiredNowUnchanged fields equal those
live values. Frozen v5 remains a historical measurement as
of HEAD `5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v5 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v6 remasures live pins, lands the
generic predecessor form, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G22-FX-AUTHORING and OBL-RESERVED-TABLES remains. Dual
independent ACCEPT 0/0 now exists. This entry records
v6. It is not SATISFIED-GRADE. v5 stays frozen; do not
record it as current.

## Decision

1. Record `platform-tcb-leftover-join.v6.json` as DR-126
   leftover remasurement after D-184. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX. Frozen v5 is not recorded as a current
   remasurement.
2. DR-126 stays `OPEN`. leftover-design of
   OBL-G22-FX-AUTHORING and OBL-RESERVED-TABLES remains.
   G22 harness specification is measured authored and not
   QUALIFIED. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-126. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not apply platform-tcb-contract.v45. Does not
   populate a TCB table. Does not invent fixture bytes.
   Does not rewrite G22, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D185. Does not unwrite D-125, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, D-176, D-177,
D-178, D-179, D-180, D-181, D-182, D-183, or D-184.
