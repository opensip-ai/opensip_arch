# D-232 — Record harness.DR-G02.core-installed.v4 as G02 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G02.core-installed.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-231. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-232**, not a register
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
> **Does not** invent a D-006 unit or authorize 83886080
> as the bound.
> **Does not** invent G02 tree-accounting.
> **Does not** mint Rust-as-core.
> **Does not** decide L-TCB identity.
> **Does not** populate the per-OS TCB table.
> **Does not** retarget DR-126.
> **Does not** close leftover-design of OBL-2, OBL-D1, or
> OBL-D2.
> **Does not** take over G01, G03, G04, G05, G07, G14, or
> G22.
> **Does not** treat naming v6 as not naming G02.
> **Does not** treat leftover-join.v7 as parentReview.
> **Does not** occupy the G01 identifier.
> **Does not** record frozen v1, v2, or v3 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G01, G03, G04, G05, G07, G08, G09,
> G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G23,
> G24, G25, G26, G27, G28, G29, G30, G31, or G32.
> **Does not** rewrite frozen G02 v1 through v3.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-231 is ADOPTED at
`daba63b7e10bf871d140b3c235d27dcaf2efb002`.
HEAD is `daba63b7e10bf871d140b3c235d27dcaf2efb002`.
Last live heading is D-231. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G02.core-installed.v4.review-independent.claude2.json` | `e5d6d9aacbc090381ae85ef792f0c1beb8cf510f4dfd5020873ca32b7de18a1b` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G02.core-installed.v4.review-independent.codex.json` | `dad3667f6c92b514822d1222428b5ef7d9aba51b49b01c3fefdb9d20a9eb309f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G02.core-installed.v4.json | `1bc247f779fa980ecde7d7a244effa6116f02a79be4a0ee74e0cedb168ccf360` |
| harness.DR-G02.core-installed.v4.review-independent.claude2.json | `e5d6d9aacbc090381ae85ef792f0c1beb8cf510f4dfd5020873ca32b7de18a1b` |
| harness.DR-G02.core-installed.v4.review-independent.codex.json | `dad3667f6c92b514822d1222428b5ef7d9aba51b49b01c3fefdb9d20a9eb309f` |
| COORDINATOR-DECISIONS.md | `0d97de4a2bf8a9764fdf2ed78d8cc0831ff384897080e2c203f230e63beca380` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `daba63b7e10bf871d140b3c235d27dcaf2efb002` |
| Frozen v1 (CGHS promised-path occupancy; Claude ACCEPT 0/0; Codex not reviewed; not this subject) | `f806f76b5c972948e034b7ceb80520630c33846b75a48086811cdd7fdc6849e8` |
| Frozen v2 (historical thin-extraction occupancy; not this subject) | `92126a00e901301405cbb29fe1fb220b481c86f6f388dedfbbd3ee26520bdeed` |
| Frozen v3 (historical thin-extraction occupancy; Claude ACCEPT 0/0; Codex not reviewed; not this subject) | `de43b11d6c3901a0d0d7fa3b16a810ec22863b2bf4388c15247fae1456868f4d` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, frozen v1 through v3, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G02 lead
token remains `OPEN`; DR-101 remains `OPEN`. v4's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G02 (D-086). Naming parent is naming v6 (D-145)
dual ACCEPT 0/0, not leftover-join.v7. Frozen v1 remains
the CGHS promised-path occupancy. Frozen v3 remains a
historical thin-extraction occupancy as of HEAD `5d5d778`
/ required-now 26. Frozen v2 remains a historical
thin-extraction occupancy. Do not record v1 through v3 as
current.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 through v3 are thin occupancies without live-HEAD
house form. After file 08 cardinality 28, distribution-core
leftover-join.v7 (D-173) is the current DR-101 leftover-join.
leftover-join.v7 leftoverDesign remains
`[OBL-2, OBL-D1, OBL-D2]`. leftover-join.v7 measured
harnessSpecificationsNotAuthored false: the
authoring-of-specifications limb of OBL-2 is stale as an
authoring claim. Dual independent ACCEPT 0/0 now exists of
v4 occupancy remasurement at live HEAD. This entry records
v4. It is not SATISFIED-GRADE. v1 through v3 stay frozen;
do not record them as current.

## Decision

1. Record
   `harness.DR-G02.core-installed.v4.json`
   as G02 occupancy remasurement after D-231. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 through v3 are not
   recorded as a current occupancy remasurement.
2. DR-G02 stays `OPEN`. leftover-design of the G02
   specification-authoring limb of OBL-2 remains measured
   stale at leftover-join.v7 (D-173). leftover-design of
   OBL-2, OBL-D1, and OBL-D2 remains. Remainder of OBL-2
   is (a) D-006 unit and G02 tree-accounting UNDECIDED, so
   size comparison cannot be scored, and (b) G01-G05
   execution, which remains qualification (D-056). Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   invent a D-006 unit or authorize 83886080 as the bound.
   Does not invent G02 tree-accounting. Does not mint
   Rust-as-core. Does not decide L-TCB identity. Does not
   populate the per-OS TCB table. Does not retarget DR-126.
   Does not take over G01, G03, G04, G05, G07, G14, or G22.
3. Does not SATISFY DR-101. Does not SATISFY DR-117. Does
   not SATISFY DR-131. Does not SATISFY DR-133. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
   Naming parent is naming v6 (D-145) dual ACCEPT 0/0.
   leftover-join.v7 is not parentReview. This occupancy
   does not occupy the G01 identifier.
4. Claude Stage A returned three `observationsNotFindings`
   strings. They carry no identifiers. Codex Stage A
   returned zero advisories and no observations. This entry
   does not invent identifiers for those Claude observations
   and does not claim that both reviewers' identifiers are
   preserved. Codex Stage A returned no observation
   identifiers. Does not execute fixtures. Does not rewrite
   G01, G03, G04, G05, G07, G08, G09, G10, G12, G14, G15,
   G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27,
   G28, G29, G30, G31, or G32. Does not rewrite frozen G02
   v1 through v3. Does not edit file 08. Does not invent a
   D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D232. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
D-227, D-228, D-229, D-230, or D-231.
