# D-231 — Record harness.DR-G01.core-download.v9 as G01 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G01.core-download.v9.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-230. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-231**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-101.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent a D-006 unit or authorize 26214400
> as the bound.
> **Does not** mint Rust-as-core.
> **Does not** close leftover-design of OBL-2, OBL-D1, or
> OBL-D2.
> **Does not** take over G02, G03, G04, G05, G07, G14, or
> G22.
> **Does not** treat naming v6 as not naming G01.
> **Does not** treat leftover-join.v7 as parentReview.
> **Does not** occupy the G30 identifier.
> **Does not** record frozen v1, v2, v3, v4, v5, v6, v7,
> or v8 as a current occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G02, G03, G04, G05, G07, G08, G09,
> G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G23,
> G24, G25, G26, G27, G28, G29, G30, G31, or G32.
> **Does not** rewrite frozen G01 v1 through v8.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-230 is ADOPTED at
`c51cb86e1b38375f8120d0a1594e22d2094aa1b7`.
HEAD is `c51cb86e1b38375f8120d0a1594e22d2094aa1b7`.
Last live heading is D-230. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G01.core-download.v9.review-independent.claude2.json` | `6f697ee39f5cb170693f1f23f6daf36b56ee63ad37aef8685e004f73bfab7a01` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G01.core-download.v9.review-independent.codex.json` | `b9755e1ea407c25da1acb43e66264467da397603c7f87e2591935d80ecfc213f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G01.core-download.v9.json | `f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b` |
| harness.DR-G01.core-download.v9.review-independent.claude2.json | `6f697ee39f5cb170693f1f23f6daf36b56ee63ad37aef8685e004f73bfab7a01` |
| harness.DR-G01.core-download.v9.review-independent.codex.json | `b9755e1ea407c25da1acb43e66264467da397603c7f87e2591935d80ecfc213f` |
| COORDINATOR-DECISIONS.md | `9f7cc6107b047429f9a4539138f1428e995c0064394c977874396e2aac472755` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `c51cb86e1b38375f8120d0a1594e22d2094aa1b7` |
| Frozen v1 (CGHS promised-path occupancy; Claude ACCEPT 0/0; Codex not reviewed; not this subject) | `0ddb58cf77f7647927aae2c993f01900b600e9c209ebe8cb96468b7160f8993f` |
| Frozen v2 (historical, not this subject) | `e2c7ec832e197ccd252a4f318c75a3266c370bd7476e76466ecd321c3e84e677` |
| Frozen v3 (historical thin-extraction occupancy; Claude REJECT 0/1 CLAUDE-G01H-V3-SF1; not this subject) | `cb386936782808d463eb96ee8bd9202b19397d1a9a4a96acbe3f5f67eafb7284` |
| Frozen v4 (historical occupancy; dual not 0/0; not this subject) | `0496bfdb866f4b5e1e502c33095413b7a50bf88a4f193e683271b2d11c3483eb` |
| Frozen v5 (historical occupancy; dual not 0/0; not this subject) | `9dc0c1aef2aa962b3b638e4d1c5d41b415b3952b14051c0ddae72fd32258a2a3` |
| Frozen v6 (historical occupancy; dual REJECT; not this subject) | `76816c1c10758a8c47c474a286951671219d5c02d6035a9b8a6b4f42f494df88` |
| Frozen v7 (historical occupancy; dual REJECT; not this subject) | `ec0bda18aa4ccd169135a2e920bec37e368b9969fd5dd645ce72e305f5c6effa` |
| Frozen v8 (historical occupancy; dual REJECT; not this subject) | `53b7e5cb7627cbff6a3f9cb85e8868cbca02a46acea12f47495f9bbe7c0bc110` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v9, both
Stage A verdicts, frozen v1 through v8, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G01 lead
token remains `OPEN`; DR-101 remains `OPEN`. v9's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G01 (D-086). Naming parent is naming v6 (D-145)
dual ACCEPT 0/0, not leftover-join.v7. Frozen v1 remains
the CGHS promised-path occupancy. Frozen v3 remains a
historical thin-extraction occupancy as of HEAD `5d5d778`
/ required-now 26. Frozen v4 through v8 remain historical
reject-cycle occupancies. Do not record v1 through v8 as
current.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 through v3 are thin occupancies without live-HEAD
house form. Frozen v3 asserted no requiredNowUnchanged and
no live HEAD pin. After file 08 cardinality 28,
distribution-core leftover-join.v7 (D-173) is the current
DR-101 leftover-join. leftover-join.v7 leftoverDesign
remains `[OBL-2, OBL-D1, OBL-D2]`. leftover-join.v7
measured harnessSpecificationsNotAuthored false: the
authoring-of-specifications limb of OBL-2 is stale as an
authoring claim. Dual independent ACCEPT 0/0 now exists of
v9 occupancy remasurement at live HEAD. This entry records
v9. It is not SATISFIED-GRADE. v1 through v8 stay frozen;
do not record them as current.

## Decision

1. Record
   `harness.DR-G01.core-download.v9.json`
   as G01 occupancy remasurement after D-230. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 through v8 are not
   recorded as a current occupancy remasurement.
2. DR-G01 stays `OPEN`. leftover-design of the G01
   specification-authoring limb of OBL-2 remains measured
   stale at leftover-join.v7 (D-173). leftover-design of
   OBL-2, OBL-D1, and OBL-D2 remains. Remainder of OBL-2
   is (a) D-006 unit and G02 tree-accounting UNDECIDED, so
   size comparison cannot be scored, and (b) G01-G05
   execution, which remains qualification (D-056). Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   invent a D-006 unit or authorize 26214400 as the bound.
   Does not mint Rust-as-core. Does not take over G02, G03,
   G04, G05, G07, G14, or G22.
3. Does not SATISFY DR-101. Does not SATISFY DR-117. Does
   not SATISFY DR-131. Does not SATISFY DR-133. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
   Naming parent is naming v6 (D-145) dual ACCEPT 0/0.
   leftover-join.v7 is not parentReview. This occupancy
   does not occupy the G30 identifier.
4. Advisory CLAUDE-G01H-V9-ADV1 travels as honesty work.
   Three occupancy fields gloss the OBL-2 remainder without
   the G02 tree-accounting half of leftover-join.v7 limb
   (a). authorityClaim carries the unabbreviated remainder.
   No successor is required on that advisory's account.
   Codex Stage A returned zero advisories and no
   observations. This entry does not invent identifiers for
   Codex Stage A observations and does not claim that both
   reviewers' identifiers are preserved. Codex Stage A
   returned no observation identifiers. Does not execute
   fixtures. Does not rewrite G02, G03, G04, G05, G07, G08,
   G09, G10, G12, G14, G15, G16, G18, G19, G20, G21, G22,
   G23, G24, G25, G26, G27, G28, G29, G30, G31, or G32.
   Does not rewrite frozen G01 v1 through v8. Does not edit
   file 08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D231. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
D-227, D-228, D-229, or D-230.
