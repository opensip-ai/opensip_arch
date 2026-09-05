# D-235 — Record harness.DR-G05.component-delta.v4 as G05 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G05.component-delta.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-234. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-235**, not a register
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
> **Does not** invent a D-006 unit.
> **Does not** invent a numeric cap.
> **Does not** invent G02 tree-accounting.
> **Does not** mint Rust-as-core.
> **Does not** close leftover-design of OBL-2, OBL-D1, or
> OBL-D2.
> **Does not** take over G01, G02, G03, G04, G07, G14, or
> G22.
> **Does not** treat naming v6 as not naming G05.
> **Does not** treat leftover-join.v7 as parentReview.
> **Does not** occupy the G04 identifier.
> **Does not** occupy CGHS artifactPathWhenAuthored (that
> path remains v1).
> **Does not** record frozen v1, v2, or v3 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G01, G02, G03, G04, G07, G08, G09,
> G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G23,
> G24, G25, G26, G27, G28, G29, G30, G31, or G32.
> **Does not** rewrite frozen G05 v1 through v3.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-234 is ADOPTED at
`2988629e64b5d5ad0319926c9a1151c73d935c27`.
HEAD is `2988629e64b5d5ad0319926c9a1151c73d935c27`.
Last live heading is D-234. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G05.component-delta.v4.review-independent.claude2.json` | `104794547ae7cf489faf06f797d8ce2ce05c4810ef77d76696ed7d90da6f5877` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G05.component-delta.v4.review-independent.codex.json` | `54ab5290aee27b0d8eef5bc7173f40754ef81f83c56c809a513507e522098839` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G05.component-delta.v4.json | `fb1b2158f16d07814a6c5f67166faadb12d122353f26d23e804060f7687b7875` |
| harness.DR-G05.component-delta.v4.review-independent.claude2.json | `104794547ae7cf489faf06f797d8ce2ce05c4810ef77d76696ed7d90da6f5877` |
| harness.DR-G05.component-delta.v4.review-independent.codex.json | `54ab5290aee27b0d8eef5bc7173f40754ef81f83c56c809a513507e522098839` |
| COORDINATOR-DECISIONS.md | `4bf0376ac759239eab10b6eb3f140f2cb220e293b9800c65d2b8fa5ab9e42926` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `2988629e64b5d5ad0319926c9a1151c73d935c27` |
| Frozen v1 (CGHS promised-path occupancy; Claude ACCEPT 0/0; Codex not reviewed; not this subject) | `1294bdf907cbefb8039813468f8aebe9bb474d68f53f889b9fa5b2cf1e0f7dc4` |
| Frozen v2 (historical thin-extraction occupancy; not this subject) | `7cb529166b0b982d1bd7223d87ed72e597c7c0f9269ca2abb283abde2380e6a7` |
| Frozen v3 (historical thin-extraction occupancy; Claude ACCEPT 0/0; not this subject) | `d97adad436b479ca8e1f84a1b87678bc67de7a997b40b2f7e4bd62fc3322103a` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, frozen v1 through v3, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G05 lead
token remains `OPEN`; DR-101 remains `OPEN`. v4's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G05 (D-086). Naming parent is naming v6 (D-145)
dual ACCEPT 0/0, not leftover-join.v7. Frozen v1 remains
the CGHS promised-path occupancy. Frozen v3 remains a
historical thin-extraction occupancy. Do not record v1
through v3 as current.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 through v3 are occupancies without live-HEAD house
form. Frozen v1 occupies CGHS v4's artifactPathWhenAuthored.
After file 08 cardinality 28, distribution-core leftover-join.v7
(D-173) is the current DR-101 leftover-join. leftover-join.v7
leftoverDesign remains `[OBL-2, OBL-D1, OBL-D2]`. Dual
independent ACCEPT 0/0 now exists of v4 occupancy remasurement
at live HEAD. This entry records v4. It is not SATISFIED-GRADE.
v1 through v3 stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G05.component-delta.v4.json`
   as G05 occupancy remasurement after D-234. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 through v3 are not
   recorded as a current occupancy remasurement.
2. DR-G05 stays `OPEN`. leftover-design of the G05
   specification-authoring limb of OBL-2 remains measured
   stale at leftover-join.v7 (D-173). leftover-design of
   OBL-2, OBL-D1, and OBL-D2 remains. Remainder of OBL-2
   is (a) D-006 unit and G02 tree-accounting UNDECIDED, so
   size comparison cannot be scored, and (b) G01-G05
   execution, which remains qualification (D-056). Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   invent a D-006 unit. Does not invent a numeric cap. Does
   not invent G02 tree-accounting. Does not take over G01,
   G02, G03, G04, G07, G14, or G22.
3. Does not SATISFY DR-101. Does not SATISFY DR-117. Does
   not SATISFY DR-131. Does not SATISFY DR-133. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
   Naming parent is naming v6 (D-145) dual ACCEPT 0/0.
   leftover-join.v7 is not parentReview. This occupancy
   does not occupy the G04 identifier. Frozen v1 remains
   the CGHS promised-path occupancy.
4. Advisory CLAUDE-G05H-V4-ADV1 travels as honesty work.
   EV-1 collapses the pairedWorkload.deltaFormula start and
   RSS operands; passProperty still binds computation to
   pairedWorkload.deltaFormula in the pinned parents. No
   successor is required on that advisory's account. Claude
   Stage A also returned four `observationsNotFindings`
   strings. They carry no identifiers. Codex Stage A
   returned zero advisories and no observations. This entry
   does not invent identifiers for those Claude observations
   and does not claim that both reviewers' identifiers are
   preserved. Codex Stage A returned no observation
   identifiers. Does not execute fixtures. Does not rewrite
   G01, G02, G03, G04, G07, G08, G09, G10, G12, G14, G15,
   G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27,
   G28, G29, G30, G31, or G32. Does not rewrite frozen G05
   v1 through v3. Does not edit file 08. Does not invent a
   D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D235. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
D-227, D-228, D-229, D-230, D-231, D-232, D-233, or
D-234.
