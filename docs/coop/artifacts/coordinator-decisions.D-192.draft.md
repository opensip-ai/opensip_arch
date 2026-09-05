# D-192 — Record g16-leftover-join.v3 as G16 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g16-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-191. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-192**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-121.
> **Does not** steal OBL-CI-ENCODING-RESERVED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G16-FX-AUTHORING.
> **Does not** invent fixture bytes or reserved CI encodings.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G16, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-191 is ADOPTED at
`04afe24ad64d5cead4505beca76dbbc9f2cf7d29`.
HEAD is `04afe24ad64d5cead4505beca76dbbc9f2cf7d29`.
Last live heading is D-191. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g16-leftover-join.v3.review-independent.claude2.json` | `cda15f7d914a1781fdf4afb227871bba8b9d49156e09a5b0b6211b6ec7dbca75` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g16-leftover-join.v3.review-independent.codex.json` | `9bf5f0c04107c06e59850f1fd8d965289af24dfa8b0d8efeb47d6e28004a99c7` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g16-leftover-join.v3.json | `bc87c6b342195a29bd582aa0b48973e5e8e1f76f4bca717d13578c2b2fc181f6` |
| g16-leftover-join.v3.review-independent.claude2.json | `cda15f7d914a1781fdf4afb227871bba8b9d49156e09a5b0b6211b6ec7dbca75` |
| g16-leftover-join.v3.review-independent.codex.json | `9bf5f0c04107c06e59850f1fd8d965289af24dfa8b0d8efeb47d6e28004a99c7` |
| COORDINATOR-DECISIONS.md | `9d24e4e052208d4295db5ba9571322eadfe5ea09a3dc6e78bae5ed8889a85658` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `04afe24ad64d5cead4505beca76dbbc9f2cf7d29` |
| Frozen v2 (historical, not this subject) | `1937b334739701210a06ac16530dec7983897af57d610464c3ba1dbc171c280e` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G16 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, cites
monorepo leftover-join.v3 (D-181) as the current DR-121
ROW leftover-join, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G16-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v2 stays frozen; do not record it as
current.

## Decision

1. Record `g16-leftover-join.v3.json` as G16 leftover
   remasurement after D-191. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G16 stays `OPEN`. leftover-design of
   OBL-G16-FX-AUTHORING remains. G16 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-121. Does not steal
   OBL-CI-ENCODING-RESERVED. Gate 1 Class A is not opened.
   Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or reserved CI encodings.
   Does not rewrite G16, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D192. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, or D-191.
