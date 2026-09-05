# D-173 — Record distribution-core-leftover-join.v7 as DR-101 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `distribution-core-leftover-join.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 / D-171 / D-172. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-173**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-101.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of the D-006 unit limb,
> OD-101-1, or OD-101-2.
> **Does not** invent a D-006 unit.
> **Does not** mint Rust-as-core.
> **Does not** record frozen v5 or v6 as a current
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G01–G05, G31, or G32.
> **Does not** invent fixture bytes.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-172 is ADOPTED at
`f4d0606553286672ac8586b8f0d8049a096f65de`.
HEAD is `f4d0606553286672ac8586b8f0d8049a096f65de`.
Last live heading is D-172. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/distribution-core-leftover-join.v7.review-independent.claude2.json` | `9500da512b7235e0b5d407c6df35bf13806ce608967969797a9f5809df9165db` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/distribution-core-leftover-join.v7.review-independent.codex.json` | `63d24a385858b959ee3fc6de77b0625a7d993a7fa8d44ff6b8dc71c4e65c8f5c` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| distribution-core-leftover-join.v7.json | `ccdae033f09dfa3655003d69bf30d29de28c712943f9d0eefb78eb93dac27ad6` |
| distribution-core-leftover-join.v7.review-independent.claude2.json | `9500da512b7235e0b5d407c6df35bf13806ce608967969797a9f5809df9165db` |
| distribution-core-leftover-join.v7.review-independent.codex.json | `63d24a385858b959ee3fc6de77b0625a7d993a7fa8d44ff6b8dc71c4e65c8f5c` |
| COORDINATOR-DECISIONS.md | `19d9094f65a3765732777dc76fc5d6edbbb6488863c316a56c86404902620719` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `f4d0606553286672ac8586b8f0d8049a096f65de` |
| Frozen v6 (not this subject) | `653c6637c78f32200a39b986e717c983f06d7d5ad932bca297730113ca19cf73` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v7, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-101 lead
token remains `OPEN`. v7's top-level head, recordedInputs.HEAD,
file08Pin, and summary.requiredNowUnchanged equal those live
values. Frozen v5 remains a historical measurement as of
HEAD `5d5d778` / required-now 26. Frozen v6 stays unmoved
and is not recorded.

## Why this entry exists

Wave 2. Frozen v5 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v6 remasured live pins and received
Claude REJECT CLAUDE-DCLJ-V6-SF1 (stale `This vN`
self-version claims in predecessor roles). v7 lands that
finding with the generic form and keeps the live pins.
leftover-design of the D-006 unit limb, OD-101-1, and
OD-101-2 remains. Dual independent ACCEPT 0/0 now exists.
This entry records v7. It is not SATISFIED-GRADE. v5/v6
stay frozen; do not record them as current.

## Decision

1. Record `distribution-core-leftover-join.v7.json` as
   DR-101 leftover remasurement after D-172. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v5 and v6 are not
   recorded as a current remasurement.
2. DR-101 stays `OPEN`. leftover-design of the D-006 unit
   limb, OD-101-1, and OD-101-2 remains. G01–G05 harness
   specifications are measured authored and not QUALIFIED.
   Naming is not execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-101. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent a D-006 unit. Does not mint
   Rust-as-core. Does not invent fixture bytes. Does not
   rewrite G01–G05, G31, or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D173. Does not unwrite D-114, D-160, D-169, D-170,
D-171, or D-172.
