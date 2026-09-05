# D-151 — Add DR-G25 as required-now preview-analyze missing-rung obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> D-149's second proposed later work:
> PREVIEW-ANALYZE-MISSING-RUNG for NT-3 only.
> (1) D-001 MF-6 file-08 write of one new gate row,
> (2) scoped D-002 condition-4 required-gate-set successor,
> (3) D-086 successor that names the harness identifier in
> the same act. This cycle's choice, not a mandate to
> perform the remaining three D-149 kinds.
> This is coordinator decision **D-151**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design for NT-5, NT-6, NT-7,
> or NT-8.
> **Does not** make DR-131 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145, D-147, D-148, or D-150.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-150 is ADOPTED at `6516d8cb34f0cac6d3d00d3562193ce4a03a676c`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-admission-leftover.v1.json | `1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `f526e94b7fd07611fde2b684e55e65dd8c985ebf8b9aba726484a79336dfe2a9` |
| file 08 | `bb5e7e94b46d08673c84db451230b7186b230ada76a2b04a32b99fcbd4a14276` |
| D-150 commit | `6516d8cb34f0cac6d3d00d3562193ce4a03a676c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover.v1,
v2 contract, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-149's second proposed kind owns NT-3: a missing required
TypeScript semantic rung is typed Coverage-indeterminate.
No live gate owns that corpus (G21 Coverage goldens are
post-fault; G23 Coverage class is domain mutation).
Same-act naming is required so condition 4 stays MET.

This entry is that later act for the second kind only.
It assigns G25 (file 08's gate table ends at DR-G24).

## Decision

1. **Assign DR-G25.** The identifier
   `DR-G25 PREVIEW-ANALYZE-MISSING-RUNG` is assigned.
   It owns DR-131 NT-3 only.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended by D-077, D-147, and D-150 (requiredNow=20),
   is succeeded by that same 20-member set plus **DR-G25**.
   Cardinality becomes 21. Other D-018 item-2 sets are
   unchanged. G06/G11 remain not slice-1-required. G13
   remains reserved. G17 remains inapplicable.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G25.preview-analyze-missing-rung.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G24 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-131 or DR-133
   status cells.

5. **Leftover-design of NT-3.** NT-3 is now named at a
   condition-4 / DR-G* obligation with owner Product +
   CLI / output + semantic owners. Remainder is G25
   execution. That is leftover-design closure for NT-3
   only. Product-law ownership remains DR-131 /
   preview-analyze-contract.v2.

6. **DR-131 leftover as a whole.** NT-5, NT-6, NT-7, and
   NT-8 remain leftover-design. NT-1/NT-2 remain named
   at G24. NT-4 remains discharged by named DR-133
   classes. After this act, D-056 Eligibility gates 2
   and 3 do **not** hold for DR-131, because four leftover
   classes remain. Class A is not opened. Not eligible
   in kind. Not SATISFIED. Gate 4 reserves eligibility
   to a later dedicated SATISFIED-GRADE cycle.

7. Does not invent a D9 code. Does not restore G17.
   Does not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G25 PREVIEW-ANALYZE-MISSING-RUNG | A missing required TypeScript semantic rung is typed Coverage-indeterminate; silent syntax fallback fails | named: harness.DR-G25.preview-analyze-missing-rung.preview (D-151; not authored; not QUALIFIED). missing-required-rung corpus (DR-131 NT-3) | typed Coverage-indeterminate; no silent syntax fallback; not authoritative success | Product + CLI / output + semantic owners | PROPOSED; not QUALIFIED | pass all; no waiver for silent fallback | OPEN |
~~~~

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**24 of 24 owners named** at role level; **20 of 20 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; every assurance stage is below `QUALIFIED`; 21 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**25 of 25 owners named** at role level; **21 of 21 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; every assurance stage is below `QUALIFIED`; 22 `OPEN`, 3 `HARD-BLOCKED`
~~~~

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (20 of 20 becomes 21 of 21
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D151, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
20-member required-now set. Does not unwrite D-138,
D-147, D-148, D-149, or D-150.
