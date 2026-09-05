# D-155 — Record preview-product-boundary-ee-gate-join.v1 as DR-117 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `preview-product-boundary-ee-gate-join.v1.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-148. This is coordinator decision **D-155**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or change requiredNow (24).
> **Does not** name EE-6b/EE-7c/EE-7e at G09/G14/G16.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-154 is ADOPTED at `a6081c692b2d8bbf38a21789a50b0db10fe41a97`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-product-boundary-ee-gate-join.v1.json | `ae20b25fcb908a19fcd38dbb8e7c5963eee983b566132936c4bd1e7af34b3de0` |
| Claude 2 join verdict | `7d30f21792ccb47653f4ea32191e3cd804d7553e260d734f2c92061ab49376cd` ACCEPT, 0/0, advisory CLAUDE-PPBEEJ-V1-ADV1 |
| Codex join verdict | `164e828fc49a6c34bff5e15be82c80cdb56f33aff61c59e513cebb820272cd44` ACCEPT, 0/0 |
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| COORDINATOR-DECISIONS.md | `20a8f69b3782838ec95329c4cdd82859627547e079cfc104b986040b2fd5fc73` |
| file 08 | `6d593a11880f2063376bd8760f7779822a167b52e4d8299cf9e75e2cbb97133f` |
| D-154 commit | `a6081c692b2d8bbf38a21789a50b0db10fe41a97` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the v1
candidate, both join verdicts, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-137 recorded preview-product-boundary-successor.v5 and
left most enforcement classes candidate-owned. D-139 L
authorizes drafting that leftover-design closure. Join v1
received independent dual ACCEPT at 0 blockers and 0
SHOULD-FIX. This entry records that measurement. It does
not add a row and does not SATISFY DR-117.

## Decision

1. Record `preview-product-boundary-ee-gate-join.v1.json`
   as DR-117 leftover-design measurement. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX.
2. DR-117 stays `OPEN`. Leftover-design is not closed.
   EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a, EE-7a,
   EE-7b, and EE-7d remain leftover-design. EE-3a is not
   leftover-design: its pass is already named as DR-133
   execution at G21 and G23. EE-6b / EE-7c / EE-7e are
   capable-of-riding G09 / G14 / G16 and are not named
   at those gates by this entry.
3. D-056 Class A is not opened. Gates 2 and 3 do not
   hold. No SATISFIED. Required-now stays 24.
4. **Proposed later work, not performed here:** later
   D-000 cycles may (a) name the riding EE classes at
   G09/G14/G16 by a D-086 successor, and/or (b) close
   the ten leftover classes by naming them at one or
   more condition-4 / DR-G* obligations. Not performed
   here.
5. Advisory CLAUDE-PPBEEJ-V1-ADV1 travels as honesty
   work.
6. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (24 of 24). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, or SATISFIED cycle. Overturn: C-D155.
Does not unwrite D-137 or D-154.
