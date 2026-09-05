# D-162 — Record identity-namespace-leftover-join.v2 as DR-104 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `identity-namespace-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-161 / D-160. This is coordinator decision **D-162**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-104.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** execute fixtures.
> **Does not** apply D-130 or D-131.
> **Does not** change the file 08 token off
> DECIDED-V1-NOT-INTEGRATED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-161 is ADOPTED at `23fe6d92facc7ac5d5f8b2b82754308a99821bee`.
HEAD is `23fe6d92facc7ac5d5f8b2b82754308a99821bee`.

Measured inputs:

| Path | sha256 |
|---|---|
| identity-namespace-leftover-join.v2.json | `cdb3003bfd2a823730833c05f8cbacb13c98555170ea57d150e0acb055597df3` |
| Claude 2 join verdict | `e80779634f7d64ffa3e4c19d46f12b704979f0a8eb9799596df960a148062694` ACCEPT, 0/0, advisory CLAUDE-INLJ-V2-ADV1 |
| Codex join verdict | `b3efb3a18cb84f061d5955eb9a5ed5fa6e9fb860eef1a047349a8977af6925c0` ACCEPT, 0/0 |
| identity-namespace-negative-test-corpus.v1.json | `2c0795cd58e95e56afad46899b3c5d546d4fb520e38e1a8c3f7c132aa69583dd` |
| identity-namespace-integration-contract.v4.json | `cd7ff948d95cf595ed1b7654c7ea2a458540f417cf13922373fcf8af8b280e62` |
| COORDINATOR-DECISIONS.md | `d47ccdcd18d87b1b208c32a05d934788d9a011fee8c282174ae3f23e8586b091` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-161 commit | `23fe6d92facc7ac5d5f8b2b82754308a99821bee` |
| HEAD | `23fe6d92facc7ac5d5f8b2b82754308a99821bee` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-139 L names DR-104 leftover: D-056 ineligible table and
the D-130 / D-131 leftover T2-02 recordings. Join v2
received independent dual ACCEPT at 0 blockers and 0
SHOULD-FIX after Claude REJECT of v1 (CLAUDE-INLJ-V1-SF1).
This entry records that measurement. It does not add a
row and does not SATISFY DR-104.

## Decision

1. Record `identity-namespace-leftover-join.v2.json` as
   DR-104 leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-104 stays `DECIDED-V1-NOT-INTEGRATED`. leftover-
   design/OPEN is a finding against that token. Leftover-
   design is not closed. Remaining leftover-design:
   OBL-NT-11-EXECUTION (no live DR-G* owns identity-
   namespace negative-test execution). D-012 policy and
   the eleven authored classes are not leftover-authoring.
   D-012 deferrals to DR-117 / DR-116 and rides to DR-111
   / DR-114 remain off this row.
3. D-056 Class A is not opened. Class B SATISFIED is not
   recorded. Gates 2 and 3 do not hold for DR-104. No
   SATISFIED. Required-now stays 26. This entry does not
   execute fixtures and does not apply D-130 or D-131.
4. Advisory CLAUDE-INLJ-V2-ADV1 travels as honesty work.
   **Proposed later work, not performed here:** a later
   D-000 cycle may name the eleven-class execution
   remainder at a condition-4 / DR-G* obligation whose
   live claim owns that property, or add a new row. Each
   later act that adds a required-now row is a scoped
   D-002 successor and a D-086 successor in the same act.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, or SATISFIED cycle. Overturn: C-D162.
Does not unwrite D-012, D-130, D-131, or D-161.
