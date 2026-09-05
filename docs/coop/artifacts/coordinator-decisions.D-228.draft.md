# D-228 — Record harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4 as G28 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-227. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-228**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** execute NT-7 or NT-8 by existing.
> **Does not** reopen leftover-design of DR-131 NT-7 and
> NT-8 as unnamed remainders.
> **Does not** invent a D9 code.
> **Does not** treat naming v6 as naming G28.
> **Does not** close leftover-design of OBL-G28-FX-AUTHORING.
> **Does not** record frozen v1, v2, or v3 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27,
> G31, or G32.
> **Does not** rewrite frozen G28 v1, v2, or v3.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-227 is ADOPTED at
`1394645bceee2ce1ebdb69256f0184a0125811b1`.
HEAD is `1394645bceee2ce1ebdb69256f0184a0125811b1`.
Last live heading is D-227. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.review-independent.claude2.json` | `7c1916d16f08c9564cd788749335bd8c945b57818161d5641c1a2e790e6ff1cd` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.review-independent.codex.json` | `308ac423a4548040187dd9304a576f4ac153c6906788f7ef135651f9131eaf54` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json | `e540ea53b8cfd4e75c05eabfb4c321dca566161b135dc630c2bd1fec5d31ff4d` |
| harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.review-independent.claude2.json | `7c1916d16f08c9564cd788749335bd8c945b57818161d5641c1a2e790e6ff1cd` |
| harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.review-independent.codex.json | `308ac423a4548040187dd9304a576f4ac153c6906788f7ef135651f9131eaf54` |
| COORDINATOR-DECISIONS.md | `cc15255b863b1583f0957699ec805817783f1e98e3ce6e10eaf1706a8f2f6442` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `1394645bceee2ce1ebdb69256f0184a0125811b1` |
| Frozen v3 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `d2cceb9f83696ab78618385d7ebb592e16136f562250fa238653e195ad77e41c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, frozen v3, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G28 lead
token remains `OPEN`; DR-131 remains `OPEN`. v4's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G28 (D-154). Frozen v3 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Naming parent is
D-154 dual CONSENT, not naming v6.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v3 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and `Does not change required-now 26.` After
file 08 cardinality 28, g28 leftover-join.v3 (D-203) is the
current G28 leftover-join. leftover-join.v3 leftoverDesign
remains `[OBL-G28-FX-AUTHORING]`. Current INPUT basis as
measured by leftover-join.v3 is g28-input-corpus.v1. Dual
independent ACCEPT 0/0 now exists. This entry records v4.
It is not SATISFIED-GRADE. v3, v2, and v1 stay frozen; do
not record them as current.

## Decision

1. Record
   `harness.DR-G28.preview-analyze-host-must-not-mint.preview.v4.json`
   as G28 occupancy remasurement after D-227. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1, v2, and v3 are not
   recorded as a current occupancy remasurement.
2. DR-G28 stays `OPEN`. leftover-design of OBL-G28-HARNESS-SPEC,
   OBL-G28-NAMED-CORPUS, and OBL-G28-INPUT-CORPUS remains
   measured closed at leftover-join.v3 (D-203). leftover-design
   of OBL-G28-FX-AUTHORING remains. Remainder is G28
   execution once fixture implementations exist. Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   execute NT-7 or NT-8 by existing. Does not reopen
   leftover-design of DR-131 NT-7 and NT-8 as unnamed
   remainders. Does not invent a D9 code. Does not treat
   naming v6 as naming G28.
3. Does not SATISFY DR-131. Does not SATISFY DR-117. Does
   not SATISFY DR-133. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned advisories CLAUDE-G28-V4-A1 and
   CLAUDE-G28-V4-A2. Codex Stage A returned zero advisories
   and no observations. The Claude identifiers A-1 and A-2
   are preserved. Codex Stage A returned no observation
   identifiers. Does not execute fixtures. Does not rewrite
   G07, G08, G09, G10, G12, G14, G15, G16, G18, G19, G20,
   G21, G22, G23, G24, G25, G26, G27, G31, or G32. Does
   not rewrite frozen G28 v1, v2, or v3. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D228. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, D-224, D-225, D-226,
or D-227.
