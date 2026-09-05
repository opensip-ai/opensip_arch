# D-159 — Record dr117-ee-gate-naming.v3 as D-086 successor

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `dr117-ee-gate-naming.v3.json` (0 blockers, 0
> SHOULD-FIX) as the D-086 / D-145 successor that D-155
> and D-156 deferred. Same no-cell-edit branch as D-145.
> This is coordinator decision **D-159**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** make DR-117 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** rewrite G29 or G30.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-158 is ADOPTED at `0fcf3d358f47d04d8510a02ef6813bb674cd910a`.
HEAD is `0fcf3d358f47d04d8510a02ef6813bb674cd910a`.

Measured inputs:

| Path | sha256 |
|---|---|
| dr117-ee-gate-naming.v3.json | `fb5e928415098c7726bcd91f455327472b6ae7cfe34f65b288ba99cba3ef82c2` |
| Claude 2 v3 verdict | `671c3f1034aeeee4d63778b8bfd0b24c05988e48946f112cf3fa441f71cd45e8` ACCEPT, 0/0 |
| Codex v3 verdict | `c8c6e1d76f0d861a0ceabb6741fb42fd4ed1eaca18a90a94a2d487ba611ecd13` ACCEPT, 0/0 |
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| monorepo-ci-contract.v16.json | `67ca501660a2ba515ce37adc799c5418e4ffd156308189662245e5a5e45a2ddb` |
| COORDINATOR-DECISIONS.md | `d44f6806bfb9954b2151c77c67dcf8d9aeca17c9ae8354d27d066b77a7d8fcf8` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-158 commit | `0fcf3d358f47d04d8510a02ef6813bb674cd910a` |
| HEAD | `0fcf3d358f47d04d8510a02ef6813bb674cd910a` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-156 deferred a D-086 successor that may name EE-6b at
G09, EE-7c at G14, and EE-7e at G16. D-157 and D-158
closed leftover-design of the ten D-155 leftover classes
and left those three riders unnamed. Naming v3 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX.
This entry records that naming. Naming is not execution.

## Decision

1. Record `dr117-ee-gate-naming.v3.json` as the D-086 /
   D-145 successor that names DR-117 EE-6b at G09,
   EE-7c at G14, and EE-7e at G16. The candidate binds
   NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX.
2. Naming is not execution. Not authored. Not QUALIFIED.
   Required-now stays 26. Condition-4 effect is zero.
   Condition 4 stays MET at 26 of 26 required names and
   30 of 30 owners. MET is not QUALIFIED.
3. After this recording, D-056 Eligibility gates 2 and 3
   hold for DR-117: the ten leftover classes are named
   at G29/G30, EE-3a is discharged by named DR-133
   classes, and EE-6b/EE-7c/EE-7e are named at
   G09/G14/G16. Gate 1 Class A remains false under
   D-137's express reservation on
   preview-product-boundary-successor.v5. Gates 4 and 5
   are not performed. Not eligible in kind. Not
   SATISFIED. Class A is not opened. No D-096 (A) grant.
4. DR-117 stays `OPEN`. Does not rewrite G29 or G30.
   Does not convert EE-6b honesty into confinement.
   Demonstrated prevention remains DR-128.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D159. Does not unwrite D-137, D-145, D-157,
or D-158.
