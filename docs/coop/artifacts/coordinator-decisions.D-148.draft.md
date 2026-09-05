# D-148 — Record preview-analyze-nt-gate-join.v2 as DR-131 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `preview-analyze-nt-gate-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-144 / D-146. This is coordinator decision **D-148**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or change requiredNow (19).
> **Does not** name DR-131 NT-4 at G21 or G23.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-147 is ADOPTED at `e68cc88415b3e9f947c4e1800c766e61a108bedf`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-nt-gate-join.v2.json | `4081c7400b3b9eae61089bb807140b4f75f5dd512b664c1f6657553a7da03813` |
| Claude 2 join verdict | `6a897dc7f93a2eb4815b290db429e1fc99f3292ef643802fd8ecbf1ccba0ebab` ACCEPT, 0/0 |
| Codex join verdict | `6a3378d380e2f4bebd81d2bdd760cbf6f07dc0a645e739db5d75acd055ddf66a` ACCEPT, 0/0 |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `0c85e7bba4899eec30a5a1ef25603facd9bff620d6eed947957a7590c1b657e5` |
| file 08 | `23cdf039452d38007d1ccca20139767e627e1ec0948192e532d6fb9b4a5df243` |
| D-147 commit | `e68cc88415b3e9f947c4e1800c766e61a108bedf` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the v2
candidate, both join verdicts, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-138 recorded preview-analyze-contract.v2 and left
NT-1..NT-8 without owner/gate/harness. D-139 L authorizes
drafting that leftover-design closure. Join v2 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX.
This entry records that measurement. It does not add a
row and does not SATISFY DR-131.

## Decision

1. Record `preview-analyze-nt-gate-join.v2.json` as
   DR-131 leftover-design measurement. The candidate
   binds NOTHING. Both independent reviewers returned
   0 blockers and 0 SHOULD-FIX.
2. DR-131 stays `OPEN`. Leftover-design is not closed.
   NT-1, NT-2, NT-3, NT-5, NT-6, NT-7, and NT-8 remain
   leftover-design. NT-4 is not leftover-design: its
   pass is already named as DR-133 execution at G21
   (D-145) and G23 (D-147). This entry does not name
   DR-131 NT-4 at those gates.
3. D-056 Class A is not opened. Gates 2 and 3 do not
   hold. No SATISFIED. Required-now stays 19.
4. **Proposed later work, not performed here:** a later
   D-000 cycle may close the seven leftover classes by
   naming them at one or more condition-4 / DR-G*
   obligations with owners. That later act assigns any
   new number and is a scoped D-002 / D-086 successor
   if it adds a row to the required-now set. Not
   performed here.
5. Does not edit file 08. Does not retarget D-145 or
   D-147. Does not authorize `docs/v2/implementation/`.
6. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (19 of 19). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, or SATISFIED cycle. Overturn: C-D148.
Does not unwrite D-138, D-145, D-146, or D-147.
