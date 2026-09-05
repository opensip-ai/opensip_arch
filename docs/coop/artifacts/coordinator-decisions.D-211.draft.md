# D-211 — Record harness.DR-G08.trust-recovery.install-surfaces.v3 as G08 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G08.trust-recovery.install-surfaces.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-210. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-211**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-112.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** mint OD-112-1..4.
> **Does not** invent TR-ROOT.
> **Does not** name a repair-media harness.
> **Does not** close leftover-design of OBL-G08-FX-AUTHORING.
> **Does not** steal leftover-design of OBL-RESERVED-NUMBERS.
> **Does not** record frozen v1 or v2 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-210 is ADOPTED at
`100c46ea67bfdd0c88adc67eb2598cacba7b0000`.
HEAD is `100c46ea67bfdd0c88adc67eb2598cacba7b0000`.
Last live heading is D-210. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G08.trust-recovery.install-surfaces.v3.review-independent.claude2.json` | `f78c4b0e68f0a080e43133d4f1ab8f231e13479a32fa60077293093774064ab8` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G08.trust-recovery.install-surfaces.v3.review-independent.codex.json` | `92390c354363e254852787efeb38a3b74ba76e4563b08b3dd9767d2885694e9f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G08.trust-recovery.install-surfaces.v3.json | `13076be20e4eef0dfe352786b705de09304a69f583529502388e5086f6f098c0` |
| harness.DR-G08.trust-recovery.install-surfaces.v3.review-independent.claude2.json | `f78c4b0e68f0a080e43133d4f1ab8f231e13479a32fa60077293093774064ab8` |
| harness.DR-G08.trust-recovery.install-surfaces.v3.review-independent.codex.json | `92390c354363e254852787efeb38a3b74ba76e4563b08b3dd9767d2885694e9f` |
| COORDINATOR-DECISIONS.md | `97ceb11b6858849af713e6368dd2d92fb90049f35beb9eb57367edebc2eb1fa1` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `100c46ea67bfdd0c88adc67eb2598cacba7b0000` |
| Frozen v1 (historical, not this subject) | `526a9707e6312b0f6f08cf73ed88d69947de2464748ff977391e440eb383e714` |
| Frozen v2 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `01b71359572597e28abca0e10a487c7782ecdf18b6e22ed44dea9af86859d14e` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, frozen v1/v2, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G08 lead
token remains `OPEN`; DR-112 remains `OPEN`. v3's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G08 (D-086). Frozen v2 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v1 remains a
Claude-REJECT occupancy.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v2 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, g08-leftover-join.v3
(D-188) is the current G08 leftover-join and signed-index
leftover-join.v3 (D-178) is the current DR-112 leftover-join.
v3 remasures occupancy at live pins and cites those current
leftover-joins. Dual independent ACCEPT 0/0 now exists.
This entry records v3. It is not SATISFIED-GRADE. v1 and v2
stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G08.trust-recovery.install-surfaces.v3.json`
   as G08 occupancy remasurement after D-210. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 and v2 are not
   recorded as a current occupancy remasurement.
2. DR-G08 stays `OPEN`. leftover-design of OBL-G08-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-188).
   leftover-design of OBL-G08-FX-AUTHORING remains. Remainder
   is G08 execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes. Does
   not mint OD-112-1..4. Does not invent TR-ROOT. Does not
   name a repair-media harness.
3. Does not SATISFY DR-112. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories. Codex Stage A
   returned zero advisories. Does not execute fixtures. Does
   not rewrite G07, G08, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D211. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, or D-210.
