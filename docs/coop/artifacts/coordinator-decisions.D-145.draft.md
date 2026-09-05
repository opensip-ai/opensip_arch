# D-145 — Record gate-harness-naming.v6 as D-086 successor

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT (0 blockers, 0 SHOULD-FIX). Performs the D-086
> successor owed by D-144 Decision 3. Same no-cell-edit
> branch as D-086 / D-144. This is coordinator decision
> **D-145**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or change requiredNow (18).
> **Does not** name NT-3 or NT-5 at any gate.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.

D-144 is ADOPTED at `13b07f4c35647558f7ebc586bdcf02d0ef051cb0`.
HEAD is `1ac85c76bc8418d785c308dcdbbd8ea10fe9081f` (D-144
heading hygiene).

Measured inputs:

| Path | sha256 |
|---|---|
| gate-harness-naming.v6.json | `b74e30092cf1f5aad55434d2f12465fa31111923c1b2c0c5ddc8a78445b5ffba` |
| Claude 2 verdict | `a01ad74029cbe52bc82c83ab6f4ad9b2c752e34b5528cc5942ff2482434ed2b8` ACCEPT, 0/0 |
| Codex verdict | `908c416b07509a56f2aa89adfcf5a311319a488c4bfa174c12b967bbd9451dcc` ACCEPT, 0/0, advisories GHN-V6-A1/A2/A3 |
| gate-harness-naming.v3.json (D-086) | `b5236612394a3d24259f3b11b99e9928b530a4be3d147d2007d00c3ee96c3ccd` |
| provider-only-nt-gate-join.v6.json | `93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3` |
| COORDINATOR-DECISIONS.md | `e838775b3c47f4347b7bf5935711bbfa87e94fd5423317100d58cb78c6276341` |
| file 08 | `7128f62ecea3d8121b670359fa0ca0bce4ec2df8a8f4680bb3edba09f42b865f` |
| D-144 hygiene HEAD | `1ac85c76bc8418d785c308dcdbbd8ea10fe9081f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD duplicate-heading hygiene, with file 08, v6,
both v6 verdicts, v3, and this draft unmoved, re-measure
before adoption. Append-only COORD or heading hygiene after
this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Decision

1. Record `gate-harness-naming.v6.json` as the D-086
   successor candidate owed by D-144. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-G21 now names DR-133 NT-1, NT-2, NT-6 as executing
   there. DR-G20 now names DR-133 NT-4, NT-7 as executing
   there. Naming is not execution. Not QUALIFIED.
3. DR-133 stays `OPEN`. Leftover-design is not closed.
   NT-3 and NT-5 remain leftover-design. D-056 gates 2
   and 3 do not hold. Class A is not opened. No SATISFIED.
4. Condition-4 effect is zero. G20 and G21 were already
   named. Condition 4 stays MET on the naming half and
   below QUALIFIED.
5. Codex advisories GHN-V6-A1, GHN-V6-A2, GHN-V6-A3
   travel as honesty work.
6. Does not edit file 08. Does not add DR-G23. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half. Condition 5 last.

### Reversibility

Total only before a dependent leftover-design closure,
SATISFIED cycle, or file-08 harness-cell rewrite.
Pre-dependent overturn: C-D145.
