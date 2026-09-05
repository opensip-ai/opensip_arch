# D-230 — Record harness.DR-G30.preview-boundary-install-shape.preview.v2 as G30 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G30.preview-boundary-install-shape.preview.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-229. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-230**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** execute EE-7a, EE-7b, or EE-7d by existing.
> **Does not** reopen leftover-design of those EE classes
> as unnamed remainders.
> **Does not** invent a D9 code.
> **Does not** invent a PlanIntent schema.
> **Does not** invent a section 7.1 recipe.
> **Does not** treat naming v6 as naming G30.
> **Does not** close leftover-design of OBL-G30-FX-AUTHORING.
> **Does not** record frozen v1 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27,
> G28, G29, G31, or G32.
> **Does not** rewrite frozen G30 v1.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-229 is ADOPTED at
`9ba7576ed3ace40120f574b3c45f341de48a74ff`.
HEAD is `9ba7576ed3ace40120f574b3c45f341de48a74ff`.
Last live heading is D-229. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G30.preview-boundary-install-shape.preview.v2.review-independent.claude2.json` | `43d6b2c576ba745686b2c4a7004722d7a8eecbf6da556b00bde86401c7398003` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G30.preview-boundary-install-shape.preview.v2.review-independent.codex.json` | `e968cbeee48a8f8a402c60c6fbd57263ff06c73030cfb68c4bb06a1e0924d897` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G30.preview-boundary-install-shape.preview.v2.json | `371695b8fc7b5cf61e016508da69436fbe6146683979f0c2468f52757a16cfda` |
| harness.DR-G30.preview-boundary-install-shape.preview.v2.review-independent.claude2.json | `43d6b2c576ba745686b2c4a7004722d7a8eecbf6da556b00bde86401c7398003` |
| harness.DR-G30.preview-boundary-install-shape.preview.v2.review-independent.codex.json | `e968cbeee48a8f8a402c60c6fbd57263ff06c73030cfb68c4bb06a1e0924d897` |
| COORDINATOR-DECISIONS.md | `2b461c5657016c94ae41af0f06678db902ecd3bcff3161e1638bf64e390f85ba` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `9ba7576ed3ace40120f574b3c45f341de48a74ff` |
| Frozen v1 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `74934fe15c06d92dad98c19be47ff9b50af0eb1441de02dd016617cb862ae0ee` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
Stage A verdicts, frozen v1, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G30 lead
token remains `OPEN`; DR-117 remains `OPEN`. v2's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G30 (D-158). Frozen v1 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Naming parent is
D-158 turn-2 dual CONSENT, not naming v6, and not D-158
turn-1 Claude OBJECT.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, `Does not change required-now 26.`, and a
leftoverNameNote that no leftover-join artifact for this
gate exists. After file 08 cardinality 28, g30 leftover-join.v3
(D-205) is the current G30 leftover-join. leftover-join.v3
leftoverDesign remains `[OBL-G30-FX-AUTHORING]`. Current
INPUT basis as measured by leftover-join.v3 is
g30-input-corpus.v1. Dual independent ACCEPT 0/0 now exists.
This entry records v2. It is not SATISFIED-GRADE. v1 stays
frozen; do not record it as current.

## Decision

1. Record
   `harness.DR-G30.preview-boundary-install-shape.preview.v2.json`
   as G30 occupancy remasurement after D-229. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 is not recorded as
   a current occupancy remasurement.
2. DR-G30 stays `OPEN`. leftover-design of OBL-G30-HARNESS-SPEC,
   OBL-G30-NAMED-CORPUS, and OBL-G30-INPUT-CORPUS remains
   measured closed at leftover-join.v3 (D-205). leftover-design
   of OBL-G30-FX-AUTHORING remains. Remainder is G30
   execution once fixture implementations exist. Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   execute EE-7a, EE-7b, or EE-7d by existing. Does not
   reopen leftover-design of those EE classes as unnamed
   remainders. Does not invent a D9 code. Does not invent
   a PlanIntent schema. Does not invent a section 7.1 recipe.
   Does not treat naming v6 as naming G30.
3. Does not SATISFY DR-117. Does not SATISFY DR-131. Does
   not SATISFY DR-133. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned seven `observationsNotFindings`
   strings. They carry no identifiers. Codex Stage A
   returned zero advisories and no observations. This entry
   does not invent identifiers for those Claude observations
   and does not claim that both reviewers' identifiers are
   preserved. Codex Stage A returned no observation
   identifiers. Does not execute fixtures. Does not rewrite
   G07, G08, G09, G10, G12, G14, G15, G16, G18, G19, G20,
   G21, G22, G23, G24, G25, G26, G27, G28, G29, G31, or
   G32. Does not rewrite frozen G30 v1. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D230. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
D-227, D-228, or D-229.
