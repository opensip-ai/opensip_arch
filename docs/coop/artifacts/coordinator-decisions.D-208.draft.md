# D-208 — Record harness.DR-G31.identity-namespace-negative-test.preview.v5 as G31 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G31.identity-namespace-negative-test.preview.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-207. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-208**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-104.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute the eleven classes.
> **Does not** reopen leftover-design of unnamed NT-11
> execution remainder.
> **Does not** record frozen v2, v3, or v4 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G31 or G32.
> **Does not** edit file 08.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-207 is ADOPTED at
`aa19af228bcf180901ce696ff1a7a88d828b0ff1`.
HEAD is `aa19af228bcf180901ce696ff1a7a88d828b0ff1`.
Last live heading is D-207. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G31.identity-namespace-negative-test.preview.v5.review-independent.claude2.json` | `edae073303d893901c7ec7ff7dc6632a86ca8c8c31dbdac290939d56abce44e0` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G31.identity-namespace-negative-test.preview.v5.review-independent.codex.json` | `6caae191cf1d844e3afb6e1255efd8a6d7f14b40996103b29ea6704fbddbd16d` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G31.identity-namespace-negative-test.preview.v5.json | `4cc42b86cf74b95c88c8efc9b85e48b894759712d30fbc1aaee079f301ca00a4` |
| harness.DR-G31.identity-namespace-negative-test.preview.v5.review-independent.claude2.json | `edae073303d893901c7ec7ff7dc6632a86ca8c8c31dbdac290939d56abce44e0` |
| harness.DR-G31.identity-namespace-negative-test.preview.v5.review-independent.codex.json | `6caae191cf1d844e3afb6e1255efd8a6d7f14b40996103b29ea6704fbddbd16d` |
| COORDINATOR-DECISIONS.md | `35bee0a9af237c25503e74e3157a247e31af5e0fe49707b626edb5441e60cb12` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `aa19af228bcf180901ce696ff1a7a88d828b0ff1` |
| Frozen v2 (historical, not this subject) | `851abb4d5463cc2a3b8a392496f021f2901e64f5266e822be55fdc753292c3f6` |
| Frozen v4 (dual REJECT, not this subject) | `af23c1b29c956d9941541d4eb337542700ad9e91300348295df5bf61f81bf272` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v5, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G31 lead
token remains `OPEN`; DR-104 remains
`DECIDED-V1-NOT-INTEGRATED`. v5's top-level head,
recordedInputs.HEAD, file08Pin, and requiredNowUnchanged
equal those live values. File 08 carries G31 (D-167). Frozen
v2 remains a historical occupancy as of HEAD `5d5d778` /
required-now 26. Frozen v3 and v4 remain dual-REJECT
occupancies.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v2 asserted required-now 26, file08DoesNotCarryG31,
and HEAD `5d5d778`. After D-167, G31 is live and required-now
is 28. v3 and v4 dual REJECTED for stale live-state contracts
and stale self-references. v5 remasures occupancy at live
pins, cites identity leftover-join.v6 (D-175) as the current
DR-104 leftover-join, and lands those findings. Dual
independent ACCEPT 0/0 now exists. This entry records v5.
It is not SATISFIED-GRADE. v2, v3, and v4 stay frozen; do
not record them as current.

## Decision

1. Record
   `harness.DR-G31.identity-namespace-negative-test.preview.v5.json`
   as G31 occupancy remasurement after D-207. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v2, v3, and v4 are not
   recorded as a current occupancy remasurement.
2. DR-G31 stays `OPEN`. leftover-design of unnamed NT-11
   execution remainder remains closed at D-175. Remainder is
   G31 execution. Does not pin QUALIFIED.
3. Does not SATISFY DR-104. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Advisory CODEX-G31-V5-ADV-1 travels as honesty work.
   Does not execute the eleven classes. Does not invent
   fixture bytes. Does not rewrite G31 or G32. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D208. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, or D-207.
