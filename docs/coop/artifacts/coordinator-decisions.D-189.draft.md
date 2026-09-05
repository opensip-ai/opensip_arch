# D-189 — Record g09-leftover-join.v10 as G09 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g09-leftover-join.v10.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-188. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-189**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-105.
> **Does not** steal DR-114 leftover.
> **Does not** fold R-10 or R-6 into the fourteen FX.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-FX-AUTHORING.
> **Does not** invent fixture bytes or a decision-record envelope.
> **Does not** record frozen v3 through v9 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G09, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-188 is ADOPTED at
`bd67a3b791c89e7a5b2f7dd0a5e9a8c1f4f54329`.
HEAD is `bd67a3b791c89e7a5b2f7dd0a5e9a8c1f4f54329`.
Last live heading is D-188. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g09-leftover-join.v10.review-independent.claude2.json` | `d4119330bf528b191f953583fb19ac59bfe03b58cd7a5a7b3b123af51db3b91b` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g09-leftover-join.v10.review-independent.codex.json` | `2064220bdc2ece2450a4234b671ed56593fd862f2d06d3cec5b31f19dd0cf9fa` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g09-leftover-join.v10.json | `98cf4849da2aad1f700c4a8ba39b76a505f86a82137ce28f3469c4ffbe16b8c9` |
| g09-leftover-join.v10.review-independent.claude2.json | `d4119330bf528b191f953583fb19ac59bfe03b58cd7a5a7b3b123af51db3b91b` |
| g09-leftover-join.v10.review-independent.codex.json | `2064220bdc2ece2450a4234b671ed56593fd862f2d06d3cec5b31f19dd0cf9fa` |
| COORDINATOR-DECISIONS.md | `1705e1e1c33a8528d70018fae9b1b7f4e34ee0cad9ba3c6170662bd08d1bf27a` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `bd67a3b791c89e7a5b2f7dd0a5e9a8c1f4f54329` |
| Frozen v3 (historical, not this subject) | `63c67b1e5a07ec16b7d5e4eafe094ad250275f286d0257401744c01c38d2877f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v10, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G09 lead
token remains `OPEN`. v10's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v3 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v3 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v10 remasures live pins, cites
permission leftover-join.v9 (D-171) as the current DR-105
ROW leftover-join and doctor-actor leftover-join.v11
(D-170) as the current DR-114 remainder, and lands
G09LJ-V4-B1, G09LJ-V4-B2, G09-V4-SF1, G09LJ-V5-B1,
G09LJ-V5-SF1, G09LJ-V6-SF1, G09LJ-V7-SF1, G09LJ-V8-SF1,
and G09LJ-V9-SF1. leftover-design of OBL-FX-AUTHORING
remains. Dual independent ACCEPT 0/0 now exists. This
entry records v10. It is not SATISFIED-GRADE. v3 through
v9 stay frozen; do not record them as current.

## Decision

1. Record `g09-leftover-join.v10.json` as G09 leftover
   remasurement after D-188. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v3 through v9 are not recorded as a
   current remasurement.
2. DR-G09 stays `OPEN`. leftover-design of
   OBL-FX-AUTHORING remains. G09 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-105. Does not steal DR-114 leftover.
   Does not fold R-10 or R-6 into the fourteen FX. Gate 1
   Class A is not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a decision-record
   envelope. Does not rewrite G09, G31, or G32. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D189. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, or D-188.
