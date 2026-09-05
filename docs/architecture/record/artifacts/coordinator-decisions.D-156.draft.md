# D-156 — Record preview-product-boundary-admission-leftover.v1 as DR-117 leftover grouping

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `preview-product-boundary-admission-leftover.v1.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-149. This is coordinator decision **D-156**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or assign G29 or any later
> identifier.
> **Does not** change requiredNow (24).
> **Does not** name EE-6b/EE-7c/EE-7e at G09/G14/G16.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** invent a D9 code.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-155 is ADOPTED at `a7d98c25234de7290efffa93f7b89bd085afd189`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-product-boundary-admission-leftover.v1.json | `6280d64867433a963a4ce0bcc44521c57c485b0eea19404b4740c36c94ef4cce` |
| Claude 2 leftover verdict | `c4e0384d1edcbd4a7a900e69fa5421c2c38e87ab22940f453cb3c00e5d037eba` ACCEPT, 0/0, advisory CLAUDE-PPBAL-V1-ADV1 |
| Codex leftover verdict | `e6cfd756853d8be8ff6c94815150412b4406c70d38974db1e015f7aacfd3c8c5` ACCEPT, 0/0 |
| preview-product-boundary-ee-gate-join.v1.json | `ae20b25fcb908a19fcd38dbb8e7c5963eee983b566132936c4bd1e7af34b3de0` |
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| COORDINATOR-DECISIONS.md | `2f733c3987075ca6903ba0d6790938ee216fff342f744ba06f184fa09e44ded0` |
| file 08 | `6d593a11880f2063376bd8760f7779822a167b52e4d8299cf9e75e2cbb97133f` |
| D-155 commit | `a7d98c25234de7290efffa93f7b89bd085afd189` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the leftover
candidate, both leftover verdicts, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-155 recorded that ten DR-117 EE classes remain leftover-
design. Leftover.v1 received independent dual ACCEPT at 0
blockers and 0 SHOULD-FIX. This entry records that grouping
and its two candidate-not-adopted later obligations. It
does not add a row.

## Decision

1. Record `preview-product-boundary-admission-leftover.v1.json`
   as DR-117 leftover-design grouping for EE-1, EE-2, EE-3b,
   EE-4, EE-5a, EE-5b, EE-6a, EE-7a, EE-7b, and EE-7d. The
   candidate binds NOTHING. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. DR-117 stays `OPEN`. Leftover-design is not closed.
   Those ten classes remain leftover-design. EE-3a and
   EE-6b/EE-7c/EE-7e standing from D-155 is not retargeted.
   Class A is not opened. Gates 2 and 3 do not hold. No
   SATISFIED.
3. The two proposed kinds
   (PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION and
   PREVIEW-BOUNDARY-INSTALL-SHAPE) are candidate-not-
   adopted. This entry does not add a DR-G* row, does
   not assign G29 or any later identifier, and does not
   change required-now 24.
4. **Proposed later work, not performed here:** later
   D-000 MF-6 cycles, each its own cycle, may add one
   or more DR-G* rows whose owners and corpora match
   those proposed kinds. Each such act assigns or remints
   the number and is a scoped D-002 / D-086 required-now
   successor if it adds a row to the required-now set.
   Not performed here. A later D-086 successor may name
   EE-6b/EE-7c/EE-7e at G09/G14/G16. Not performed here.
5. Advisory CLAUDE-PPBAL-V1-ADV1 travels as honesty
   work: the install-shape claim still needs an inline
   corpus characterisation and not-that-gate distinctions
   when that later act is drafted.
6. Does not invent a D9 code. Does not edit file 08.
   Does not authorize `docs/v2/implementation/`.
7. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (24 of 24). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
MF-6, naming successor, or SATISFIED cycle. Overturn:
C-D156. Does not unwrite D-137, D-154, or D-155.
