# D-177 — Record compatibility-leftover-join.v2 as DR-111 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `compatibility-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-176. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-177**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-111.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-NUMERIC-WINDOWS
> or OBL-LOCK-JOIN.
> **Does not** invent numeric windows.
> **Does not** produce a lock.
> **Does not** record frozen v1 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-176 is ADOPTED at
`f76aa872d91e071c83bd7b03dd650402518eda64`.
HEAD is `f76aa872d91e071c83bd7b03dd650402518eda64`.
Last live heading is D-176. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/compatibility-leftover-join.v2.review-independent.claude2.json` | `a0cef800e46fa394a4cbbf28d4742cfcd494b9f0bbad39a611f5cf263c6ed9ed` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/compatibility-leftover-join.v2.review-independent.codex.json` | `ba6c178ba1e1c3d951d9e4c58c66e9d37b8a49ff15aaf27f2fc83a2878492fdc` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| compatibility-leftover-join.v2.json | `33e4299d7f65bf37c2f5d54193e004c69d542d3f5da99417e1360efc2f8b7259` |
| compatibility-leftover-join.v2.review-independent.claude2.json | `a0cef800e46fa394a4cbbf28d4742cfcd494b9f0bbad39a611f5cf263c6ed9ed` |
| compatibility-leftover-join.v2.review-independent.codex.json | `ba6c178ba1e1c3d951d9e4c58c66e9d37b8a49ff15aaf27f2fc83a2878492fdc` |
| COORDINATOR-DECISIONS.md | `cac12d00438b78198c6a48f8e57d242a7a36d83c2103b02584ef4df0ce5f3c14` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `f76aa872d91e071c83bd7b03dd650402518eda64` |
| Frozen v1 (historical, not this subject) | `bd63d1548dd04bc31937c81efb3849d05e0a2c70e2b19a6fd8b596b010cb2298` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-111 lead
token remains `OPEN`. v2's top-level head, recordedInputs.HEAD,
file08Pin, and both requiredNowUnchanged fields equal those
live values. Frozen v1 remains a historical measurement as
of HEAD `5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v1 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v2 remasures live pins.
leftover-design of OBL-NUMERIC-WINDOWS and OBL-LOCK-JOIN
remains. Dual independent ACCEPT 0/0 now exists. This
entry records v2. It is not SATISFIED-GRADE. v1 stays
frozen; do not record it as current.

## Decision

1. Record `compatibility-leftover-join.v2.json` as DR-111
   leftover remasurement after D-176. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX. Frozen v1 is not recorded as a current
   remasurement.
2. DR-111 stays `OPEN`. leftover-design of
   OBL-NUMERIC-WINDOWS and OBL-LOCK-JOIN remains. Naming is
   not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-111. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent numeric windows. Does not produce a
   lock. Does not edit file 08. Does not invent a D9 code.
   Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D177. Does not unwrite D-103, D-167, D-168, D-169,
D-170, D-171, D-172, D-173, D-174, D-175, or D-176.
