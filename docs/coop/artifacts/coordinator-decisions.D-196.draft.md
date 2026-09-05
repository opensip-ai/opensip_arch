# D-196 — Record g21-leftover-join.v4 as G21 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g21-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-195. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-196**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** reopen DR-102 SATISFIED.
> **Does not** steal OBL-DOCTOR-FX-AUTHORING,
> OBL-JOIN-FX-AUTHORING, OBL-JOIN-FX-EXECUTION, OBL-FC-C1,
> or OBL-BLK-1..4.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G21-FX-AUTHORING.
> **Does not** invent fixture bytes or a D9 code.
> **Does not** record frozen v1, v2, or v3 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G21, G31, or G32.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-195 is ADOPTED at
`784a4851147e13f2eb05bfc27e353eb8f108a5ac`.
HEAD is `784a4851147e13f2eb05bfc27e353eb8f108a5ac`.
Last live heading is D-195. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g21-leftover-join.v4.review-independent.claude2.json` | `24fce2ddcb885b56323e27af767ba9a628713384aef8dc3149d94e64344726bb` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g21-leftover-join.v4.review-independent.codex.json` | `406337e883ee6d66817849204bf616a988101724f8a4edcfad308004f8e0b59f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g21-leftover-join.v4.json | `b8696fd134550a9ad15d44a07adcc4030aad3702013cc9de914bbab5b8e74ae4` |
| g21-leftover-join.v4.review-independent.claude2.json | `24fce2ddcb885b56323e27af767ba9a628713384aef8dc3149d94e64344726bb` |
| g21-leftover-join.v4.review-independent.codex.json | `406337e883ee6d66817849204bf616a988101724f8a4edcfad308004f8e0b59f` |
| COORDINATOR-DECISIONS.md | `644851983e51375aba4933ce50ece006184000193ac5e64a6e08ffa2aed52e9a` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `784a4851147e13f2eb05bfc27e353eb8f108a5ac` |
| Frozen v3 (not this subject; dual REJECT G21LJ-V3-SF1) | `bce392d488ae70810c989953c663936048874491f92ddff74913f4938ac3f955` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G21 lead
token remains `OPEN`. v4's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26. Frozen v3 remains dual
REJECT 0/1 G21LJ-V3-SF1 and is not this subject.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. Frozen v3 remasured live pins at HEAD
`784a485` but dual REJECT 0/1 G21LJ-V3-SF1 left
leftoverDesignOpenStanding resting on doctor-actor
leftover-join.v6. v4 lands G21LJ-V3-SF1, cites
doctor-actor leftover-join.v11 (D-170) as the current
DR-114 ROW leftover-join, and states OBL-JOIN-FX-EXECUTION
is leftoverDesign false on v11. leftover-design of
OBL-G21-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v4. It is not
SATISFIED-GRADE. v1, v2, and v3 stay frozen; do not
record them as current.

## Decision

1. Record `g21-leftover-join.v4.json` as G21 leftover
   remasurement after D-195. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1, v2, and v3 are not recorded as a
   current remasurement.
2. DR-G21 stays `OPEN`. leftover-design of
   OBL-G21-FX-AUTHORING remains. G21 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-114. Does not reopen DR-102
   SATISFIED. Does not steal OBL-DOCTOR-FX-AUTHORING,
   OBL-JOIN-FX-AUTHORING, OBL-JOIN-FX-EXECUTION, OBL-FC-C1,
   or OBL-BLK-1..4. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a D9 code. Does not
   rewrite G21, G31, or G32. Does not edit file 08. Does
   not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D196. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
or D-195.
