# D-190 — Record g12-leftover-join.v3 as G12 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g12-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-189. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-190**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** steal DR-114 leftover.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-DOCTOR-FX-AUTHORING.
> **Does not** invent fixture bytes or a D9 code.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G12, G31, or G32.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-189 is ADOPTED at
`991f0e58436804a03357c1ae434a96246be25067`.
HEAD is `991f0e58436804a03357c1ae434a96246be25067`.
Last live heading is D-189. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g12-leftover-join.v3.review-independent.claude2.json` | `7f7b60f0b4c7b0ec760decd04429aa046fd2adeb3f4b9290e5478b3c1f74b7c7` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g12-leftover-join.v3.review-independent.codex.json` | `7eb99fe6a92927dfeaf3a0446bd7eecc888d1805eb433be6be694a56659dd0ef` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g12-leftover-join.v3.json | `11ebaf973b57ebf9d4b8da931ef0f66a0f299732c13a42e524d0f1f8a609a50a` |
| g12-leftover-join.v3.review-independent.claude2.json | `7f7b60f0b4c7b0ec760decd04429aa046fd2adeb3f4b9290e5478b3c1f74b7c7` |
| g12-leftover-join.v3.review-independent.codex.json | `7eb99fe6a92927dfeaf3a0446bd7eecc888d1805eb433be6be694a56659dd0ef` |
| COORDINATOR-DECISIONS.md | `03327319f668366c79709c67d072cf0c0e224af9a66ddda4f932c87e03f239c1` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `991f0e58436804a03357c1ae434a96246be25067` |
| Frozen v2 (historical, not this subject) | `0b68c98b5bb6fc07018a754e1dd5fd06120f3234e3460a84b14a69694deff93d` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G12 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, cites
doctor-actor leftover-join.v11 (D-170) as the current
DR-114 remainder, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-DOCTOR-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v2 stays frozen; do not record it as
current.

## Decision

1. Record `g12-leftover-join.v3.json` as G12 leftover
   remasurement after D-189. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G12 stays `OPEN`. leftover-design of
   OBL-DOCTOR-FX-AUTHORING remains. G12 harness
   specification is measured authored and not QUALIFIED.
   Not QUALIFIED.
3. Does not SATISFY DR-114. Does not steal DR-114 leftover.
   Gate 1 Class A is not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a D9 code. Does not
   rewrite G12, G31, or G32. Does not edit file 08. Does
   not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D190. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, or D-189.
