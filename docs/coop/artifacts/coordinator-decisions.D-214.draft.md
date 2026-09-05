# D-214 — Record harness.DR-G15.packaging-adapter-conformance.v9 as G15 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G15.packaging-adapter-conformance.v9.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-213. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-214**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-120.
> **Does not** SATISFY DR-103.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent an adapter implementation.
> **Does not** close leftover-design of OBL-AT-FX-AUTHORING.
> **Does not** steal leftover-design of OBL-ADAPTER-IMPL.
> **Does not** record frozen v7 or v8 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G10, G14, G15, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-213 is ADOPTED at
`1db4edac38e8bdc18d292a4e695a38f99ca5ffd8`.
HEAD is `1db4edac38e8bdc18d292a4e695a38f99ca5ffd8`.
Last live heading is D-213. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G15.packaging-adapter-conformance.v9.review-independent.claude2.json` | `6bc29967192086a46a7a17ac7579dab5ac5841953b7ea87e022784a5c58806ac` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G15.packaging-adapter-conformance.v9.review-independent.codex.json` | `4d19a87ff755fb38309c7682aa5f64a06428084dc8233f65c5a17aa57f064fe5` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G15.packaging-adapter-conformance.v9.json | `d82fac570f952cbc234be682b658cf94d5f7571bf4297e777e4e2c4280f98479` |
| harness.DR-G15.packaging-adapter-conformance.v9.review-independent.claude2.json | `6bc29967192086a46a7a17ac7579dab5ac5841953b7ea87e022784a5c58806ac` |
| harness.DR-G15.packaging-adapter-conformance.v9.review-independent.codex.json | `4d19a87ff755fb38309c7682aa5f64a06428084dc8233f65c5a17aa57f064fe5` |
| COORDINATOR-DECISIONS.md | `c0c7838fa579500085e4a2d063b53b06db19078fde44d6506e5174442d98a17a` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `1db4edac38e8bdc18d292a4e695a38f99ca5ffd8` |
| Frozen v7 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `557b260aff7668c42d62070097d9327531885387ea91c0f813e9a8d611f99e83` |
| Frozen v8 (Codex REJECT CODEX-G15H-V8-SF1, not this subject) | `97a439fcd5f30e2bc32b9b661e7af1123cbc5e120b588e58fd213621e363065f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v9, both
Stage A verdicts, frozen v7/v8, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G15 lead
token remains `OPEN`; DR-120 remains `OPEN`. v9's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G15 (D-086). Frozen v7 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v8 remains a
Codex-REJECT occupancy.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v7 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverJoinV2 as component-manifest leftover-
join.v2. After file 08 cardinality 28, g15-leftover-join.v3
(D-191) is the current G15 leftover-join, packaging leftover-
join.v3 (D-180) is the current DR-120 leftover-join, and
leftover-join.v6 (D-174) is the current DR-103 leftover-join.
v8 remasured occupancy then Codex REJECTED CODEX-G15H-V8-SF1
(EV-5.passProperty offered not-applicable for AT-6). v9 lands
that finding. Dual independent ACCEPT 0/0 now exists. This
entry records v9. It is not SATISFIED-GRADE. v7 and v8 stay
frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G15.packaging-adapter-conformance.v9.json`
   as G15 occupancy remasurement after D-213. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v7 and v8 are not
   recorded as a current occupancy remasurement.
2. DR-G15 stays `OPEN`. leftover-design of OBL-G15-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-191).
   leftover-design of OBL-AT-FX-AUTHORING remains. Remainder
   is G15 execution once AT-ARCHIVE-* fixture implementations
   exist. Does not pin QUALIFIED. Does not invent fixture
   bytes. Does not invent an adapter implementation.
3. Does not SATISFY DR-120. Does not SATISFY DR-103. Does
   not SATISFY DR-117. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories. Codex Stage A
   returned zero advisories. CODEX-G15H-V8-SF1 was landed
   in the occupancy bytes. Does not execute fixtures. Does
   not rewrite G07, G08, G10, G14, G15, G31, or G32. Does
   not edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D214. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, or D-213.
