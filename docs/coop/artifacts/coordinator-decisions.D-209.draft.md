# D-209 — Record harness.DR-G32.actor-join-fixture-execution.preview.v3 as G32 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G32.actor-join-fixture-execution.preview.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-208. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-209**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute the thirteen classes.
> **Does not** author fixture bytes.
> **Does not** close leftover-design of OBL-JOIN-FX-AUTHORING.
> **Does not** record frozen v1 or v2 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G31 or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-208 is ADOPTED at
`629d87c6f2b8e39ee88464d6bd81b32a01dc43eb`.
HEAD is `629d87c6f2b8e39ee88464d6bd81b32a01dc43eb`.
Last live heading is D-208. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G32.actor-join-fixture-execution.preview.v3.review-independent.claude2.json` | `c65fbcc7a8d3e03d2864032a0ff427bf3a10ee1258dcebca537265d194f3b11c` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G32.actor-join-fixture-execution.preview.v3.review-independent.codex.json` | `5cede4b742ad19b150d9889834a200336258191de315e611eb69e263b786315c` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G32.actor-join-fixture-execution.preview.v3.json | `9c782a50fecd45bcec3b8eaa3fa6b8ea09b240d9cda5d530564b9e84fa48df49` |
| harness.DR-G32.actor-join-fixture-execution.preview.v3.review-independent.claude2.json | `c65fbcc7a8d3e03d2864032a0ff427bf3a10ee1258dcebca537265d194f3b11c` |
| harness.DR-G32.actor-join-fixture-execution.preview.v3.review-independent.codex.json | `5cede4b742ad19b150d9889834a200336258191de315e611eb69e263b786315c` |
| COORDINATOR-DECISIONS.md | `8978f2316bb237c86f6c0c1c62bbec8df02760fb9b673f03f682dcf4cec7c109` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `629d87c6f2b8e39ee88464d6bd81b32a01dc43eb` |
| Frozen v1 (historical, not this subject) | `a5a5f163f408062e86052f8b095f938a96d36f26407f9dcc30cb8040ca199c28` |
| Frozen v2 (Codex REJECT, not this subject) | `01ff61cb01765b5d45732d985f4feac9d3924196419c30331b9f60fbd17809fa` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, frozen v1/v2, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G32 lead
token remains `OPEN`; DR-114 remains `OPEN`. v3's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G31 (D-167) and G32 (D-169). Frozen v1 remains a
historical occupancy as of HEAD `5d5d778` / required-now 26.
Frozen v2 remains a Codex-REJECT occupancy.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, file08DoesNotCarryG31,
file08DoesNotCarryG32, and HEAD `5d5d778`. After D-167 and
D-169, G31 and G32 are live and required-now is 28. v2
Codex REJECTED CODEX-G32-V2-B1 (certified rejected naming
v1 as parent and omitted naming v2). v3 remasures occupancy
at live pins, cites leftover-join.v11 (D-170) as the current
DR-114 leftover-join, pins naming v2 as the accepted parent
consumed by D-169, and lands that finding. Dual independent
ACCEPT 0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v1 and v2 stay frozen; do not record them
as current.

## Decision

1. Record
   `harness.DR-G32.actor-join-fixture-execution.preview.v3.json`
   as G32 occupancy remasurement after D-208. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 and v2 are not
   recorded as a current occupancy remasurement.
2. DR-G32 stays `OPEN`. leftover-design of unnamed JOIN-FX-
   EXECUTION remainder remains closed at D-169. Remainder is
   G32 execution once fixture implementations exist.
   leftover-design of OBL-JOIN-FX-AUTHORING remains. Does
   not pin QUALIFIED. Does not invent fixture bytes.
3. Does not SATISFY DR-114. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Advisory CODEX-G32-V3-ADV-1 travels as honesty work.
   Claude Stage A returned zero advisories. Does not execute
   the thirteen classes. Does not rewrite G31 or G32. Does
   not edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D209. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, or D-208.
