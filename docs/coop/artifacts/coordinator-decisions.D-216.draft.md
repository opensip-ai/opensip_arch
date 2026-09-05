# D-216 — Record harness.DR-G18.lifecycle-generation-recovery.v4 as G18 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G18.lifecycle-generation-recovery.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-215. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-216**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-107.
> **Does not** SATISFY DR-117.
> **Does not** apply lifecycle-generation-contract.v2.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent a journal.
> **Does not** steal leftover-design of OBL-ENCODING-RESERVED.
> **Does not** close leftover-design of OBL-G18-FX-AUTHORING.
> **Does not** record frozen v1, v2, or v3 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G10, G14, G15, G16, G18,
> G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-215 is ADOPTED at
`443d951390d4e8b4e513e02c391f31dee8d81559`.
HEAD is `443d951390d4e8b4e513e02c391f31dee8d81559`.
Last live heading is D-215. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G18.lifecycle-generation-recovery.v4.review-independent.claude2.json` | `ac8da15d81e9e1ebc8e0939960bf0ba6ac8f9eb7636c7bda0d1e282e41caa781` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G18.lifecycle-generation-recovery.v4.review-independent.codex.json` | `c086314313fa0315b976039d29078b4060d83a7aeea4e5506277354aafbcdf5e` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G18.lifecycle-generation-recovery.v4.json | `2ce9aa522bf014af27b088d3bd50885a271e5e321ba6c372af527552cb6660cc` |
| harness.DR-G18.lifecycle-generation-recovery.v4.review-independent.claude2.json | `ac8da15d81e9e1ebc8e0939960bf0ba6ac8f9eb7636c7bda0d1e282e41caa781` |
| harness.DR-G18.lifecycle-generation-recovery.v4.review-independent.codex.json | `c086314313fa0315b976039d29078b4060d83a7aeea4e5506277354aafbcdf5e` |
| COORDINATOR-DECISIONS.md | `67d3184cb46c7e913f54c6cf37f43df7ae441e19af6624cceec91717ca54b16f` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `443d951390d4e8b4e513e02c391f31dee8d81559` |
| Frozen v1 (Claude REJECT CLAUDE-G18-V1-B1, not this subject) | `a9d80e799028d7b16056d0c6339747b1879fc4df4707442ba9150a65a9d10bf7` |
| Frozen v2 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `5a762661b0c91ac6dc54015fa3803e66eca2dce111030a57931f6748ee50a462` |
| Frozen v3 (dual REJECT CLAUDE-G18-V3-B1 / CODEX-G18-V3-SF1, not this subject) | `fe9815a431642bdfb3c1c5a5c5fa836e1559411f012b45a9050b2ed6491bd7d3` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, frozen v1/v2/v3, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G18 lead
token remains `OPEN`; DR-107 remains
`PROPOSED-CLOSED-FOR-REVIEW`. v4's top-level head,
recordedInputs.HEAD, file08Pin, and requiredNowUnchanged
equal those live values. File 08 carries G18 (D-086). Frozen
v2 remains a historical occupancy as of HEAD `5d5d778` /
required-now 26. Frozen v1 remains a Claude-REJECT occupancy.
Frozen v3 remains a dual-REJECT occupancy.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v2 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, g18 leftover-join.v4
(D-193) is the current G18 leftover-join and lifecycle
leftover-join.v3 (D-176) is the current DR-107 leftover-join.
v3 remasured occupancy then dual REJECTED CLAUDE-G18-V3-B1 /
CODEX-G18-V3-SF1 (one shared class: current INPUT basis was
g18-input-corpus.v1, described with v2's exactByteIntent
property, while leftover-join.v4 measured
OBL-G18-INPUT-CORPUS against v2). v4 lands that shared class
by pinning g18-input-corpus.v2 as the current INPUT basis
and retaining v1 only as the superseded empty-state
predecessor. Dual independent ACCEPT 0/0 now exists. This
entry records v4. It is not SATISFIED-GRADE. v1, v2, and v3
stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G18.lifecycle-generation-recovery.v4.json`
   as G18 occupancy remasurement after D-215. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1, v2, and v3 are not
   recorded as a current occupancy remasurement.
2. DR-G18 stays `OPEN`. leftover-design of OBL-G18-HARNESS-SPEC
   remains measured closed at leftover-join.v4 (D-193).
   leftover-design of OBL-G18-FX-AUTHORING remains. Remainder
   is G18 execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a journal. Does not apply
   lifecycle-generation-contract.v2. Does not steal
   OBL-ENCODING-RESERVED.
3. Does not SATISFY DR-107. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories and three unlabeled
   observations. Codex Stage A returned zero advisories.
   CLAUDE-G18-V3-B1 and CODEX-G18-V3-SF1 (one shared class;
   both identifiers preserved) were landed in the occupancy
   bytes. CLAUDE-G18-V1-B1 remains retained. Does not execute
   fixtures. Does not rewrite G07, G08, G10, G14, G15, G16,
   G18, G31, or G32. Does not edit file 08. Does not invent
   a D9 code. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D216. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, or D-215.
