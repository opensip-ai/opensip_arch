# D-219 — Record harness.DR-G22.platform-abi-loader.v2 as G22 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G22.platform-abi-loader.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-218. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-219**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-126.
> **Does not** SATISFY DR-117.
> **Does not** apply platform-tcb-contract.v45.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** populate reserved TCB tables.
> **Does not** invent Rosetta.
> **Does not** steal platform-tcb leftover-join.v6 leftoverDesign.
> **Does not** steal OBL-RESERVED-TABLES.
> **Does not** close leftover-design of OBL-G22-FX-AUTHORING.
> **Does not** record frozen v1 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G10, G14, G15, G16, G18,
> G20, G21, G22, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-218 is ADOPTED at
`01b4dab7d9169128ccf3d3fa944fb5fac5b61e96`.
HEAD is `01b4dab7d9169128ccf3d3fa944fb5fac5b61e96`.
Last live heading is D-218. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G22.platform-abi-loader.v2.review-independent.claude2.json` | `8f0444b7f859f7b276ac7f61ffa56c2b79d35596ed2fcb945e81b9cf7b2fa345` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G22.platform-abi-loader.v2.review-independent.codex.json` | `c7f43e3dcf90c4ca5565a0524f17e0143a3e57c9cb981445eb269ee68ea3c416` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G22.platform-abi-loader.v2.json | `2973cda2adac1b612c084b64606e4fc5b5ed5b78317fc64780a7311172ff1307` |
| harness.DR-G22.platform-abi-loader.v2.review-independent.claude2.json | `8f0444b7f859f7b276ac7f61ffa56c2b79d35596ed2fcb945e81b9cf7b2fa345` |
| harness.DR-G22.platform-abi-loader.v2.review-independent.codex.json | `c7f43e3dcf90c4ca5565a0524f17e0143a3e57c9cb981445eb269ee68ea3c416` |
| COORDINATOR-DECISIONS.md | `269f72d4fe5b836ac7fb9700b5cbb2763bba14a779a7ed13c7c3449f9a8ebaef` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `01b4dab7d9169128ccf3d3fa944fb5fac5b61e96` |
| Frozen v1 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `35b5fa0efe03ac1baea075983e604bbb00eb34de47e68e3a0cf063e7cd4aea5c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
Stage A verdicts, frozen v1, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G22 lead
token remains `OPEN`; DR-126 remains `OPEN`. v2's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G22 (D-086). Frozen v1 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, g22 leftover-join.v3
(D-197) is the current G22 leftover-join and platform-tcb
leftover-join.v6 (D-185) is the current DR-126 leftover-join.
leftover-join.v3 leftoverDesign remains
`[OBL-G22-FX-AUTHORING]`. Current INPUT basis as measured by
leftover-join.v3 is g22-input-corpus.v2.
`g22-input-corpus.v1` is a superseded INPUT predecessor,
not current. Dual independent ACCEPT 0/0 now exists. This
entry records v2. It is not SATISFIED-GRADE. v1 stays
frozen; do not record it as current.

## Decision

1. Record
   `harness.DR-G22.platform-abi-loader.v2.json`
   as G22 occupancy remasurement after D-218. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 is not recorded as
   a current occupancy remasurement.
2. DR-G22 stays `OPEN`. leftover-design of OBL-G22-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-197).
   leftover-design of OBL-G22-FX-AUTHORING remains. Remainder
   is G22 execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes. Does
   not populate reserved TCB tables. Does not invent Rosetta.
   Does not apply platform-tcb-contract.v45. Does not steal
   platform-tcb leftover-join.v6 leftoverDesign. Does not
   steal OBL-RESERVED-TABLES.
3. Does not SATISFY DR-126. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories. Codex Stage A
   returned zero advisories. Does not execute fixtures. Does
   not rewrite G07, G08, G10, G14, G15, G16, G18, G20, G21,
   G22, G31, or G32. Does not edit file 08. Does not invent
   a D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D219. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, or
D-218.
