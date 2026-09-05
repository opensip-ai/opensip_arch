# D-149 — Record preview-analyze-admission-leftover.v1 as DR-131 leftover grouping

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `preview-analyze-admission-leftover.v1.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-146 / D-148. This is coordinator decision **D-149**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or assign G24 or any later
> identifier.
> **Does not** change requiredNow (19).
> **Does not** restore G17.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** invent a D9 code.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-148 is ADOPTED at `fb6ba1f07a487970e83a13b91562af6d73257ff7`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-admission-leftover.v1.json | `1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5` |
| Claude 2 leftover verdict | `d2772fb5fa1d4a7c975b4be040869b54801c1ce4764a215a54f9bc85fa88e213` ACCEPT, 0/0 |
| Codex leftover verdict | `725c239cc4d4dc61765c944cac8bd9c583822fde57b4b594e7cb18e05fc770ff` ACCEPT, 0/0 |
| preview-analyze-nt-gate-join.v2.json | `4081c7400b3b9eae61089bb807140b4f75f5dd512b664c1f6657553a7da03813` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `e4ec0f6cba2db570952a8a5fd846cc4f2b65976daa9b4683c668e761355a2f24` |
| file 08 | `23cdf039452d38007d1ccca20139767e627e1ec0948192e532d6fb9b4a5df243` |
| D-148 commit | `fb6ba1f07a487970e83a13b91562af6d73257ff7` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the leftover
candidate, both leftover verdicts, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-148 recorded that seven DR-131 NT classes remain
leftover-design. Leftover.v1 received independent dual
ACCEPT at 0 blockers and 0 SHOULD-FIX. This entry records
that grouping and its five candidate-not-adopted later
obligations. It does not add a row.

## Decision

1. Record `preview-analyze-admission-leftover.v1.json` as
   DR-131 leftover-design grouping for NT-1, NT-2, NT-3,
   NT-5, NT-6, NT-7, and NT-8. The candidate binds
   NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX.
2. DR-131 stays `OPEN`. Leftover-design is not closed.
   Those seven classes remain leftover-design. NT-4
   standing from D-148 is not retargeted. Class A is
   not opened. Gates 2 and 3 do not hold. No SATISFIED.
3. The five proposed kinds
   (PREVIEW-ANALYZE-WELL-FORMED-ADMISSION,
   PREVIEW-ANALYZE-MISSING-RUNG,
   PREVIEW-ANALYZE-SARIF-NOT-ADVERTISED,
   PREVIEW-ANALYZE-NOT-SEALED-RUN,
   PREVIEW-ANALYZE-HOST-MUST-NOT-MINT) are
   candidate-not-adopted. This entry does not add a
   DR-G* row, does not assign G24 or any later
   identifier, and does not change required-now 19.
4. **Proposed later work, not performed here:** later
   D-000 MF-6 cycles, each its own cycle, may add one
   or more DR-G* rows whose owners and corpora match
   those proposed kinds. Each such act assigns or remints
   the number and is a scoped D-002 / D-086 required-now
   successor if it adds a row to the required-now set.
   Not performed here.
5. Does not restore G17. Does not invent a D9 code.
   Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.
6. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (19 of 19). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
MF-6, or SATISFIED cycle. Overturn: C-D149. Does not
unwrite D-138, D-147, or D-148.
