# D-150 — Add DR-G24 as required-now preview-analyze admission obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> the first of D-149's five proposed later works:
> PREVIEW-ANALYZE-WELL-FORMED-ADMISSION for NT-1 and NT-2.
> (1) D-001 MF-6 file-08 write of one new gate row,
> (2) scoped D-002 condition-4 required-gate-set successor,
> (3) D-086 successor that names the harness identifier in
> the same act. Performing this first proposed later work
> is this cycle's choice, not a mandate to perform all five.
> This is coordinator decision **D-150**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design for NT-3, NT-5, NT-6,
> NT-7, or NT-8.
> **Does not** make DR-131 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145, D-147, or D-148.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-149 is ADOPTED at `6b5f4c8012f13a9336a053d55f562c0bcc67770f`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-admission-leftover.v1.json | `1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5` |
| preview-analyze-nt-gate-join.v2.json | `4081c7400b3b9eae61089bb807140b4f75f5dd512b664c1f6657553a7da03813` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `264f0235cd000f44c2ac0afd228111155a6185c07f325525d0185925d342b181` |
| file 08 | `23cdf039452d38007d1ccca20139767e627e1ec0948192e532d6fb9b4a5df243` |
| D-149 commit | `6b5f4c8012f13a9336a053d55f562c0bcc67770f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover.v1,
join v2, v2 contract, and this draft unmoved, re-measure
before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-149 recorded five candidate-not-adopted later kinds.
The first kind owns NT-1 and NT-2: hostile-but-well-formed
preview-analyze pack-identity and imperative-pack admission.
No live gate owns that corpus (G23 owns provider
FactCandidate/Coverage only). CLAUDE-PONAL-V1-ADV1 still
applies: adding a twentieth required row without naming
its identifier in the same act would flip condition 4.

This entry is that later act for the first kind only.
It assigns G24 (file 08's gate table ends at DR-G23).

## Decision

1. **Assign DR-G24.** The identifier
   `DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION` is
   assigned. It owns DR-131 NT-1 and NT-2 only. It does
   not own NT-3, NT-4, NT-5, NT-6, NT-7, or NT-8.

2. **Limb A — scoped D-002 successor.** D-002's
   condition-4 required-gate set, as amended by D-077
   and D-147 (requiredNow=19), is succeeded by that
   same 19-member set plus **DR-G24**. Cardinality
   becomes 20. This is one of D-018 item-2's six sets.
   This entry does not change the other five. G06/G11
   remain not slice-1-required. G13 remains reserved
   behind DR-118. G17 remains inapplicable. Commands,
   platforms, deferrals, identity rides, and the
   SATISFIED-requiring row set are unchanged.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G24.preview-analyze-well-formed-admission.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.
   D-145 / D-147 / D-148 namings stand and are not
   rewritten.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G23 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell.
   The before and after operands are the fenced blocks
   in §Exact condition-4 operands. Do not change the
   65-row preamble. Do not change conditions 1, 2, 3,
   or 5. Do not change condition 4 standing (`MET`).
   Do not edit the DR-131 or DR-133 status cells.

5. **Leftover-design of NT-1 and NT-2.** Those two
   classes are now named at a condition-4 / DR-G*
   obligation with owner Product + CLI / output.
   Their remainder is harness execution at G24. That
   is leftover-design closure for NT-1 and NT-2 only.
   Product-law ownership remains DR-131 /
   preview-analyze-contract.v2.

6. **DR-131 leftover as a whole.** NT-3, NT-5, NT-6,
   NT-7, and NT-8 remain leftover-design. NT-4 remains
   discharged by named DR-133 classes and is not named
   here. After this act, D-056 Eligibility gates 2 and
   3 do **not** hold for DR-131, because five leftover
   classes remain. This entry does not open Class A
   and does not record SATISFIED. Gate 4 reserves the
   eligibility determination to a later dedicated
   D-000 cycle with independent SATISFIED-GRADE review.
   This entry is not that cycle. Not eligible in kind.
   Not SATISFIED.

7. Does not invent a D9 code. Does not restore G17.
   Does not authorize `docs/v2/implementation/`.
   Does not mint a D-096 (A) grant.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION | Host admission of preview analyze requests refuses a non-bundled pack identity and a non-declarative pack or contribution | named: harness.DR-G24.preview-analyze-well-formed-admission.preview (D-150; not authored; not QUALIFIED). hostile-but-well-formed admission corpus (DR-131 NT-1, NT-2) | pack-identity refusal before evaluation; imperative-pack refusal; no user or third-party pack | Product + CLI / output | PROPOSED; not QUALIFIED | pass all; no waiver for silent admission | OPEN |
~~~~

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**23 of 23 owners named** at role level; **19 of 19 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; every assurance stage is below `QUALIFIED`; 20 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**24 of 24 owners named** at role level; **20 of 20 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; every assurance stage is below `QUALIFIED`; 21 `OPEN`, 3 `HARD-BLOCKED`
~~~~

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (19 of 19 becomes 20 of 20
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D150, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
19-member required-now set. Does not unwrite D-138,
D-147, D-148, or D-149.
