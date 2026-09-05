# D-152 — Add DR-G26 as required-now preview-analyze SARIF-not-advertised obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> D-149's third proposed later work:
> PREVIEW-ANALYZE-SARIF-NOT-ADVERTISED for NT-5 only.
> (1) D-001 MF-6 file-08 write of one new gate row,
> (2) scoped D-002 condition-4 required-gate-set successor,
> (3) D-086 successor that names the harness identifier in
> the same act. This cycle's choice, not a mandate to
> perform the remaining two D-149 kinds.
> This is coordinator decision **D-152**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design for NT-6, NT-7, or
> NT-8.
> **Does not** make DR-131 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145, D-147, D-148, D-150, or
> D-151.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-151 is ADOPTED at `3c8dafbc6e95b72b40ccbe550cd973e7be35860d`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-admission-leftover.v1.json | `1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `2d04c8a668e717af59240821acc3672d79dd2bbeebed1e9ffd3b59f16fa65865` |
| file 08 | `1e442bca4be229653d010a4b4477b1decd844d8df5f5f63a61e77cb5b771b583` |
| D-151 commit | `3c8dafbc6e95b72b40ccbe550cd973e7be35860d` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover.v1,
v2 contract, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-149's third proposed kind owns NT-5: preview analyze
refuses or does not offer SARIF 2.1.0. G17 remains
inapplicable and is not this obligation. Same-act naming
is required so condition 4 stays MET.

This entry is that later act for the third kind only.
It assigns G26 (file 08's gate table ends at DR-G25).

## Decision

1. **Assign DR-G26.** The identifier
   `DR-G26 PREVIEW-ANALYZE-SARIF-NOT-ADVERTISED` is
   assigned. It owns DR-131 NT-5 only. It does not
   restore G17.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended by D-077, D-147, D-150, and D-151
   (requiredNow=21), is succeeded by that same
   21-member set plus **DR-G26**. Cardinality becomes
   22. Other D-018 item-2 sets are unchanged. G17
   remains inapplicable.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G26.preview-analyze-sarif-not-advertised.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G25 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-131 or DR-133
   status cells.

5. **Leftover-design of NT-5.** NT-5 is now named at a
   condition-4 / DR-G* obligation with owner
   Output/operability + CLI/product owners. Remainder is
   G26 execution. That is leftover-design closure for
   NT-5 only. Product-law ownership remains DR-131 /
   preview-analyze-contract.v2 citing D-077.

6. **DR-131 leftover as a whole.** NT-6, NT-7, and NT-8
   remain leftover-design. After this act, D-056
   Eligibility gates 2 and 3 do **not** hold for DR-131,
   because three leftover classes remain. Class A is not
   opened. Not eligible in kind. Not SATISFIED.

7. Does not invent a D9 code. Does not restore G17.
   Does not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G26 PREVIEW-ANALYZE-SARIF-NOT-ADVERTISED | Preview analyze refuses or does not offer SARIF 2.1.0; D-077 drop stands | named: harness.DR-G26.preview-analyze-sarif-not-advertised.preview (D-152; not authored; not QUALIFIED). refuse-or-not-offer corpus (DR-131 NT-5) | request or flag advertising SARIF is refused or not offered; G17 remains inapplicable | Output/operability + CLI/product owners | PROPOSED; not QUALIFIED | pass all; no waiver by silent advertisement | OPEN |
~~~~

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**25 of 25 owners named** at role level; **21 of 21 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; every assurance stage is below `QUALIFIED`; 22 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**26 of 26 owners named** at role level; **22 of 22 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; every assurance stage is below `QUALIFIED`; 23 `OPEN`, 3 `HARD-BLOCKED`
~~~~

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (21 of 21 becomes 22 of 22
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D152, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
21-member required-now set. Does not unwrite D-138,
D-147, D-149, D-150, or D-151.
