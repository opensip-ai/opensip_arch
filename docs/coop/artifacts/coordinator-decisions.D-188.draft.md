# D-188 — Record g08-leftover-join.v3 as G08 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g08-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-187. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-188**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-112.
> **Does not** steal OBL-RESERVED-NUMBERS.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G08-FX-AUTHORING.
> **Does not** invent fixture bytes or reserved numbers.
> **Does not** record frozen v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G08, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-187 is ADOPTED at
`5ba5d1691198b92d1f64bb821fa483020180704a`.
HEAD is `5ba5d1691198b92d1f64bb821fa483020180704a`.
Last live heading is D-187. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g08-leftover-join.v3.review-independent.claude2.json` | `3f117380bccc934bbd089fa17950fab150a6d76460623d2816b6a617a0af4747` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g08-leftover-join.v3.review-independent.codex.json` | `74796baf9629620e6cc4a8dea1ab8238cb0d28add3a3f643a180175bf1b6cd72` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g08-leftover-join.v3.json | `d7a194c5bc743a6dfd01a6196377d8e63b4dc7aea61f4d48dc40d79e90013e87` |
| g08-leftover-join.v3.review-independent.claude2.json | `3f117380bccc934bbd089fa17950fab150a6d76460623d2816b6a617a0af4747` |
| g08-leftover-join.v3.review-independent.codex.json | `74796baf9629620e6cc4a8dea1ab8238cb0d28add3a3f643a180175bf1b6cd72` |
| COORDINATOR-DECISIONS.md | `a996596caf8fffe3a8dd91bd607e38140e30b6d30e932d122f64c38c0f612530` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `5ba5d1691198b92d1f64bb821fa483020180704a` |
| Frozen v2 (historical, not this subject) | `d78c0f9b365a60fe58b77c53f57665092b2db0c78bb7956649fbc5bfe5f3dbae` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G08 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, lands the
generic predecessor form, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G08-FX-AUTHORING remains. Dual independent ACCEPT 0/0
now exists. This entry records v3. It is not
SATISFIED-GRADE. v2 stays frozen; do not record it as
current.

## Decision

1. Record `g08-leftover-join.v3.json` as G08 leftover
   remasurement after D-187. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v2 is not recorded as a current
   remasurement.
2. DR-G08 stays `OPEN`. leftover-design of
   OBL-G08-FX-AUTHORING remains. G08 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-112. Does not steal
   OBL-RESERVED-NUMBERS. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or reserved numbers. Does
   not rewrite G08, G31, or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D188. Does not unwrite D-105, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, D-176, D-177,
D-178, D-179, D-180, D-181, D-182, D-183, D-184, D-185,
D-186, or D-187.
