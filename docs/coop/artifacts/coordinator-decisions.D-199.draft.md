# D-199 — Record g24-leftover-join.v3 as G24 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g24-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-198. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-199**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** reopen leftover-design of NT-1 or NT-2.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G24-FX-AUTHORING.
> **Does not** invent fixture bytes, a pack IR, or a
> section 7.1 recipe.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G24, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-198 is ADOPTED at
`73ac9b4e6ec720431f9c01b637f885cd77199699`.
HEAD is `73ac9b4e6ec720431f9c01b637f885cd77199699`.
Last live heading is D-198. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g24-leftover-join.v3.review-independent.claude2.json` | `f677748458a17b9906bce118dd57e86fbef71b28a551e80b76df670063b2ca9c` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g24-leftover-join.v3.review-independent.codex.json` | `a8ec79ad4789ea126229f00e5d1eaabe34a6462ac2e7c0517884ba0722c4734f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g24-leftover-join.v3.json | `c4fa464802f6075de8054a93f10fbc0b80e2bade6d04e510c2fecc52cf8b0f72` |
| g24-leftover-join.v3.review-independent.claude2.json | `f677748458a17b9906bce118dd57e86fbef71b28a551e80b76df670063b2ca9c` |
| g24-leftover-join.v3.review-independent.codex.json | `a8ec79ad4789ea126229f00e5d1eaabe34a6462ac2e7c0517884ba0722c4734f` |
| COORDINATOR-DECISIONS.md | `d8d6312bfbb731d64e5a0ff8e8fba208896310a4d0988059d3684b095ea76f8a` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `73ac9b4e6ec720431f9c01b637f885cd77199699` |
| Frozen v2 (historical, not this subject) | `fd944ea7d1f915463784d292bc280388138a1dea41a49c2add748fff8a791701` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G24 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins and replaces
D-167 placeholder sentences with carry-safe phrasing.
leftover-design of OBL-G24-FX-AUTHORING remains. NT-1/NT-2
unnamed remainder remains closed at D-150. Dual independent
ACCEPT 0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v1 and v2 stay frozen; do not record them
as current.

## Decision

1. Record `g24-leftover-join.v3.json` as G24 leftover
   remasurement after D-198. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G24 stays `OPEN`. leftover-design of
   OBL-G24-FX-AUTHORING remains. G24 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-131. Does not reopen leftover-design
   of NT-1 or NT-2. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes, a pack IR, or a section
   7.1 recipe. Does not rewrite G24, G31, or G32. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D199. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, or D-198.
