# D-233 — Record harness.DR-G03.core-startup.v5 as G03 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G03.core-startup.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-232. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-233**, not a register
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
> **Does not** invent FC-G03-COMPONENT-PRESENT or
> FC-G03-PROJECT-PRESENT bytes.
> **Does not** invent a D-006 unit.
> **Does not** invent G02 tree-accounting.
> **Does not** amend D-102.
> **Does not** invent a machine identifier outside D-102.
> **Does not** treat warm p50 as a fail-qualification bound.
> **Does not** mint Rust-as-core.
> **Does not** close leftover-design of OBL-2, OBL-D1, or
> OBL-D2.
> **Does not** take over G01, G02, G04, G05, G07, G14, or
> G22.
> **Does not** treat naming v6 as not naming G03.
> **Does not** treat leftover-join.v7 as parentReview.
> **Does not** occupy the G01 or G02 identifier.
> **Does not** record frozen v1, v2, v3, or v4 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G01, G02, G04, G05, G07, G08, G09,
> G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G23,
> G24, G25, G26, G27, G28, G29, G30, G31, or G32.
> **Does not** rewrite frozen G03 v1 through v4.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-232 is ADOPTED at
`8a6da81468e8bd3c230b2f516c1ae9dfaaf1ff42`.
HEAD is `8a6da81468e8bd3c230b2f516c1ae9dfaaf1ff42`.
Last live heading is D-232. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G03.core-startup.v5.review-independent.claude2.json` | `59ecb89a05d252aaf12f7dd8a2e836a78a6f1c45fd9d36906f19f65bb202237d` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G03.core-startup.v5.review-independent.codex.json` | `b4830b00e1fa69e731c477af43aa19b3fc931e65f9a4cbd99c706be67003df4c` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G03.core-startup.v5.json | `398ec6474eacbc4b873488dd07bce0e6295c2149d9d2794a177d13a96ebb8324` |
| harness.DR-G03.core-startup.v5.review-independent.claude2.json | `59ecb89a05d252aaf12f7dd8a2e836a78a6f1c45fd9d36906f19f65bb202237d` |
| harness.DR-G03.core-startup.v5.review-independent.codex.json | `b4830b00e1fa69e731c477af43aa19b3fc931e65f9a4cbd99c706be67003df4c` |
| COORDINATOR-DECISIONS.md | `816ff23c43819b89fd40d7b780e64fd47ab97d5ae9deabf0c99922366a81d985` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `8a6da81468e8bd3c230b2f516c1ae9dfaaf1ff42` |
| Frozen v1 (historical; Claude REJECT 0/1 CLAUDE-G03-V1-SF1; not this subject) | `d2d0727ba9e9613770e10768a241cdecea6088d387e150dd36bc730a331d85db` |
| Frozen v2 (historical thin-extraction occupancy; not this subject) | `8a2d3b10ed6199a8dd44a6d39b1dad4d302734ef6d298ddd2fe51a7889f3eaf6` |
| Frozen v3 (historical thin-extraction occupancy; Claude ACCEPT 0/0; not this subject) | `b0f75fcc11c5181d82a358e64e6a7bda72fcad5153f45bbb2d75762e1299eb04` |
| Frozen v4 (CGHS promised-path occupancy; Claude ACCEPT 0/0; Codex not reviewed; not this subject) | `1e135703fb0202bf2cac8ed733c158119673e7335a78edf9bcc3a05397d69af7` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v5, both
Stage A verdicts, frozen v1 through v4, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G03 lead
token remains `OPEN`; DR-101 remains `OPEN`. v5's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G03. Naming parent is naming v6 (D-145) dual
ACCEPT 0/0, not leftover-join.v7. Frozen v4 remains the
CGHS promised-path occupancy. Frozen v1 remains a
historical occupancy that was Claude REJECT 0/1
CLAUDE-G03-V1-SF1. Do not record v1 through v4 as current.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 through v4 are occupancies without live-HEAD house
form. Frozen v4 occupies CGHS v4's artifactPathWhenAuthored
and landed CLAUDE-G03-V1-SF1. After file 08 cardinality 28,
distribution-core leftover-join.v7 (D-173) is the current
DR-101 leftover-join. leftover-join.v7 leftoverDesign
remains `[OBL-2, OBL-D1, OBL-D2]`. Dual independent ACCEPT
0/0 now exists of v5 occupancy remasurement at live HEAD.
This entry records v5. It is not SATISFIED-GRADE. v1 through
v4 stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G03.core-startup.v5.json`
   as G03 occupancy remasurement after D-232. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 through v4 are not
   recorded as a current occupancy remasurement.
2. DR-G03 stays `OPEN`. leftover-design of the G03
   specification-authoring limb of OBL-2 remains measured
   stale at leftover-join.v7 (D-173). leftover-design of
   OBL-2, OBL-D1, and OBL-D2 remains. Remainder of OBL-2
   is (a) D-006 unit and G02 tree-accounting UNDECIDED, so
   size comparison cannot be scored, and (b) G01-G05
   execution, which remains qualification (D-056). Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   invent a D-006 unit. Does not amend D-102. Does not
   invent a machine identifier outside D-102. Does not
   treat warm p50 as a fail-qualification bound. Does not
   take over G01, G02, G04, G05, G07, G14, or G22.
3. Does not SATISFY DR-101. Does not SATISFY DR-117. Does
   not SATISFY DR-131. Does not SATISFY DR-133. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
   Naming parent is naming v6 (D-145) dual ACCEPT 0/0.
   leftover-join.v7 is not parentReview. This occupancy
   does not occupy the G01 or G02 identifier. Frozen v4
   remains the CGHS promised-path occupancy.
4. Claude Stage A returned three `observationsNotFindings`
   strings. They carry no identifiers. Codex Stage A
   returned zero advisories and no observations. This entry
   does not invent identifiers for those Claude observations
   and does not claim that both reviewers' identifiers are
   preserved. Codex Stage A returned no observation
   identifiers. Does not execute fixtures. Does not rewrite
   G01, G02, G04, G05, G07, G08, G09, G10, G12, G14, G15,
   G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27,
   G28, G29, G30, G31, or G32. Does not rewrite frozen G03
   v1 through v4. Does not edit file 08. Does not invent a
   D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D233. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
D-227, D-228, D-229, D-230, D-231, or D-232.
