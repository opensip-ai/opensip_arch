# D-146 — Record provider-only-admission-leftover.v1 as DR-133 NT-3/NT-5 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `provider-only-admission-leftover.v1.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-144. This is coordinator decision **D-146**, not a
> register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold.
> **Does not** add a DR-G* row or change requiredNow (18).
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-145 is ADOPTED at `95bab60a886439b927afe6ba15e1b0f2b3596cd1`.

Measured inputs:

| Path | sha256 |
|---|---|
| provider-only-admission-leftover.v1.json | `eae27692b4d799df2bd6b2d16497b0cbe3378166b6b541bc77df1989b3181865` |
| Claude 2 leftover verdict | `9c7124091197e9b41bdb57d276cfb74c44bdf577f59f035806c535d135df3a9b` ACCEPT, 0/0, advisory CLAUDE-PONAL-V1-ADV1 |
| Codex leftover verdict | `ec912264027686d6ad0b81fdbaf72c40912e30ade9b660aecf153a41eccea106` ACCEPT, 0/0, advisory PAL-V1-A1 |
| provider-only-output-contract.v3.json | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| provider-only-nt-gate-join.v6.json | `93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3` |
| COORDINATOR-DECISIONS.md | `8ad552bbb4c4b8f521b18bb5c2150631d4cd9b23d69915b2f5825491fcdbf915` |
| file 08 | `7128f62ecea3d8121b670359fa0ca0bce4ec2df8a8f4680bb3edba09f42b865f` |
| D-145 commit | `95bab60a886439b927afe6ba15e1b0f2b3596cd1` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the v1
candidate, both leftover verdicts, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

## Why this entry exists

D-144 / D-145 left NT-3 and NT-5 as leftover-design.
`provider-only-admission-leftover.v1.json` received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX.
This entry records that leftover-design measurement and
its candidate-not-adopted later DR-G* obligation. It does
not add the row and does not SATISFY DR-133.

## Decision

1. Record `provider-only-admission-leftover.v1.json` as
   DR-133's leftover-design measurement for NT-3 and
   NT-5. The candidate binds NOTHING. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX.
2. DR-133 stays `OPEN`. Leftover-design is not closed.
   NT-3 and NT-5 remain leftover-design. D-056 Class A
   is not opened. Gates 2 and 3 do not hold. No SATISFIED.
3. The proposed DR-G23 identifier is candidate-not-adopted.
   This entry does not add a DR-G* row and does not change
   required-now 18.
4. **Owed later work, not performed here:** a later D-000
   MF-6, its own cycle, may add one DR-G* row with owner
   Protocol + semantic owners whose corpus is
   hostile-but-well-formed admission inputs covering NT-3
   and NT-5. That act assigns the number and is a scoped
   D-002 / D-086 required-now successor if it adds the
   row to the required-now set. Not performed here.
5. Advisories CLAUDE-PONAL-V1-ADV1 and PAL-V1-A1 travel
   as honesty work.
6. Does not edit file 08. Does not retarget D-145. Does
   not authorize `docs/v2/implementation/`.
7. Does not edit COORD except the append-only adoption
   of this entry after CONSENT.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 5 last.

### Reversibility

Total only before a later dependent MF-6, leftover rewrite,
or SATISFIED cycle. Overturn: C-D146. Does not unwrite
D-136, D-144, or D-145.
