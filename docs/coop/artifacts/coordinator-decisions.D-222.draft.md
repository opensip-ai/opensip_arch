# D-222 — Record harness.DR-G19.state-class-authority.preview-classes.v2 as G19 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G19.state-class-authority.preview-classes.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-221. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-222**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-124.
> **Does not** SATISFY DR-117.
> **Does not** apply state-class-contract.v10 or v11.
> **Does not** apply SUP-124-GRANT-JOURNAL.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent a grant-journal.
> **Does not** invent a sealed-Run class.
> **Does not** steal OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED,
> or OBL-MONOTONIC.
> **Does not** close leftover-design of OBL-G19-FX-AUTHORING.
> **Does not** record frozen v1 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G19, G20, G21, G22, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-221 is ADOPTED at
`8b8dc6e4d9cbe8adacac9f9ca82c9220282c5865`.
HEAD is `8b8dc6e4d9cbe8adacac9f9ca82c9220282c5865`.
Last live heading is D-221. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G19.state-class-authority.preview-classes.v2.review-independent.claude2.json` | `236dd38f9ea90a1a7626dc245e820d326974eb4917c810bb18d5f5eede2e139d` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G19.state-class-authority.preview-classes.v2.review-independent.codex.json` | `c6d611d3ee349aea9ef731517310c00077adea5a14ded031a7fa15e962634fe4` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G19.state-class-authority.preview-classes.v2.json | `57f392b2cc30302e3c354781c56c37a30a9241e16e067fda6a281b27ed8691ac` |
| harness.DR-G19.state-class-authority.preview-classes.v2.review-independent.claude2.json | `236dd38f9ea90a1a7626dc245e820d326974eb4917c810bb18d5f5eede2e139d` |
| harness.DR-G19.state-class-authority.preview-classes.v2.review-independent.codex.json | `c6d611d3ee349aea9ef731517310c00077adea5a14ded031a7fa15e962634fe4` |
| COORDINATOR-DECISIONS.md | `063747962b4dfca0daaa95656812ef3f0ef3d08c0409552cd9442294ffb74f12` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `8b8dc6e4d9cbe8adacac9f9ca82c9220282c5865` |
| Frozen v1 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `5ada112a7dada8abb1ffa494154a410fe7ea1718acf68cf229d1322674c18c85` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
Stage A verdicts, frozen v1, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G19 lead
token remains `OPEN`; DR-124 remains `OPEN`. v2's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G19 (D-086). Frozen v1 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, leftoverDesignClosedIfAcceptedAndRecorded
OBL-G19-HARNESS-SPEC, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, g19 leftover-join.v3
(D-194) is the current G19 leftover-join and state-class
leftover-join.v3 (D-183) is the current DR-124 leftover-join.
leftover-join.v3 leftoverDesign remains
`[OBL-G19-FX-AUTHORING]`. Current INPUT basis as measured by
leftover-join.v3 is g19-input-corpus.v2.
`g19-input-corpus.v1` is a superseded INPUT predecessor,
not current. Dual independent ACCEPT 0/0 now exists. This
entry records v2. It is not SATISFIED-GRADE. v1 stays
frozen; do not record it as current.

## Decision

1. Record
   `harness.DR-G19.state-class-authority.preview-classes.v2.json`
   as G19 occupancy remasurement after D-221. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 is not recorded as
   a current occupancy remasurement.
2. DR-G19 stays `OPEN`. leftover-design of OBL-G19-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-194).
   leftover-design of OBL-G19-FX-AUTHORING remains. Remainder
   is G19 execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a grant-journal. Does not invent a sealed-Run
   class. Does not apply state-class-contract.v10 or v11.
   Does not apply SUP-124-GRANT-JOURNAL. Does not steal
   OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, or
   OBL-MONOTONIC.
3. Does not SATISFY DR-124. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories and four unlabeled
   observationsNotFindings. Codex Stage A returned zero
   advisories. The Claude observations carry no identifier.
   Codex Stage A returned no observations. Does not execute
   fixtures. Does not rewrite G07, G08, G09, G10, G12, G14,
   G15, G16, G18, G19, G20, G21, G22, G31, or G32. Does
   not edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D222. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, or D-221.
