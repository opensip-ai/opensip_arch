# D-198 — Record g23-leftover-join.v4 as G23 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g23-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-197. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-198**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-133.
> **Does not** reopen leftover-design of NT-3 or NT-5.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G23-FX-AUTHORING.
> **Does not** invent fixture bytes or NT-1/2/4/6/7/8 as
> G23 classes.
> **Does not** record frozen v1, v2, or v3 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G23, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-197 is ADOPTED at
`9bffa4258cd67e3b8906b567557de606be4d39c6`.
HEAD is `9bffa4258cd67e3b8906b567557de606be4d39c6`.
Last live heading is D-197. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g23-leftover-join.v4.review-independent.claude2.json` | `fde540a9658c750ed5868146258771a79108e18359f3847695a95d76bba6dac8` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g23-leftover-join.v4.review-independent.codex.json` | `5c0e12686215c30d229db438ae300373b477772808629bedf91c46fe73050fa6` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g23-leftover-join.v4.json | `a542dc6b023d07cf8657c76909ded1641efd29277760308d52574fa706fad56e` |
| g23-leftover-join.v4.review-independent.claude2.json | `fde540a9658c750ed5868146258771a79108e18359f3847695a95d76bba6dac8` |
| g23-leftover-join.v4.review-independent.codex.json | `5c0e12686215c30d229db438ae300373b477772808629bedf91c46fe73050fa6` |
| COORDINATOR-DECISIONS.md | `c3aa8e7fee2d391d0d26be3f63dae2067ac402674fbee4f2415073c3921c6b79` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `9bffa4258cd67e3b8906b567557de606be4d39c6` |
| Frozen v3 (historical, not this subject) | `88eb22347eea9e34d7c1988a3da4f5181f5e628d68523a906a53a9e26035b143` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G23 lead
token remains `OPEN`. v4's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v3 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v3 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v4 remasures live pins and replaces
D-167 placeholder sentences with carry-safe phrasing.
leftover-design of OBL-G23-FX-AUTHORING remains. NT-3/NT-5
unnamed remainder remains closed at D-147.
provider-only-admission leftover-join.v1 remains the D-146
measurement of that NT leftover-design grouping. Dual
independent ACCEPT 0/0 now exists. This entry records v4.
It is not SATISFIED-GRADE. v1, v2, and v3 stay frozen; do
not record them as current.

## Decision

1. Record `g23-leftover-join.v4.json` as G23 leftover
   remasurement after D-197. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1, v2, and v3 are not recorded as a
   current remasurement.
2. DR-G23 stays `OPEN`. leftover-design of
   OBL-G23-FX-AUTHORING remains. G23 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-133. Does not reopen leftover-design
   of NT-3 or NT-5. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or NT-1/2/4/6/7/8 as G23
   classes. Does not rewrite G23, G31, or G32. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D198. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, or D-197.
