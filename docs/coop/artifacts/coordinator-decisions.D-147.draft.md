# D-147 — Add DR-G23 as required-now well-formed admission obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> the later work D-146 proposed: (1) D-001 MF-6 file-08
> write of one new gate row, (2) scoped D-002 condition-4
> required-gate-set successor, (3) D-086 successor that
> names the harness identifier in the same act.
> Performing the proposed later work is this cycle's
> choice, not a mandate inherited from D-146's heading
> (CLAUDE-D146-ADV1).
> This is coordinator decision **D-147**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** apply or seal provider-only-output-contract.v3.
> **Does not** make DR-133 eligible in kind (Class A does
> not hold: the contract remains CANDIDATE-NOT-APPLIED).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145 naming of NT-1/2/4/6/7.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-146 is ADOPTED at `94250a83e8917872a088f65ab578e13cbe6e11f6`.

Measured inputs:

| Path | sha256 |
|---|---|
| provider-only-admission-leftover.v1.json | `eae27692b4d799df2bd6b2d16497b0cbe3378166b6b541bc77df1989b3181865` |
| provider-only-output-contract.v3.json | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| provider-only-nt-gate-join.v6.json | `93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3` |
| gate-harness-naming.v6.json | `b74e30092cf1f5aad55434d2f12465fa31111923c1b2c0c5ddc8a78445b5ffba` |
| COORDINATOR-DECISIONS.md | `ef26728ddf7229cb561172669a5f35aa82b961cb8adfaf9f5296f168637b263c` |
| file 08 | `7128f62ecea3d8121b670359fa0ca0bce4ec2df8a8f4680bb3edba09f42b865f` |
| D-146 commit | `94250a83e8917872a088f65ab578e13cbe6e11f6` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the leftover
candidate, v3, join v6, naming v6, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-144 / D-145 left NT-3 and NT-5 as leftover-design. D-146
recorded `provider-only-admission-leftover.v1.json` as the
measurement and a candidate-not-adopted later DR-G*
obligation. Leftover.v1 and its dual ACCEPT said the later
act that adds the row is three limbs at once: MF-6, D-002
required-gate-set successor, and D-086 successor.
CLAUDE-PONAL-V1-ADV1: adding a nineteenth required row
without naming its identifier in the same act would flip
condition 4 from MET to not MET.

This entry is that later act. It assigns the number G23
(file 08's gate table ends at DR-G22; the unadopted D-143
G23 draft concerned DR-131 and is not a live row).

## Decision

1. **Assign DR-G23.** The identifier
   `DR-G23 PROVIDER-WELL-FORMED-ADMISSION` is assigned.
   It owns DR-133 NT-3 and NT-5 only. It does not own
   NT-1, NT-2, NT-4, NT-6, or NT-7.

2. **Limb A — scoped D-002 successor.** D-002's
   condition-4 required-gate set, as amended by D-077
   (G17 inapplicable) and recorded as requiredNow=18 at
   D-086 / D-145, is succeeded by that same 18-member
   set plus **DR-G23**. Cardinality becomes 19. This is
   one of D-018 item-2's six sets. This entry does not
   change the other five. G06/G11 remain not
   slice-1-required. G13 remains reserved behind DR-118.
   G17 remains inapplicable. Commands, platforms,
   deferrals, identity rides, and the SATISFIED-requiring
   row set are unchanged.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G23.provider-well-formed-admission.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.
   D-145 naming of NT-1/2/6 at G21 and NT-4/7 at G20
   stands and is not rewritten.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G22 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell:
   replace
   `**22 of 22 owners named** at role level; **18 of 18 required gates name a recorded identifier** (D-086 / D-088 / D-102; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); every assurance stage is below \`QUALIFIED\`; 19 \`OPEN\`, 3 \`HARD-BLOCKED\``
   with
   `**23 of 23 owners named** at role level; **19 of 19 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; every assurance stage is below \`QUALIFIED\`; 20 \`OPEN\`, 3 \`HARD-BLOCKED\``.
   Do not change the 65-row preamble (gates are excluded
   from that figure). Do not change conditions 1, 2, 3,
   or 5. Do not change condition 4 standing (`MET`).
   Do not edit the DR-133 status cell.

5. **Leftover-design of NT-3 and NT-5.** Those two
   classes are now named at a condition-4 / DR-G*
   obligation with owner Protocol + semantic owners.
   Their remainder is harness execution at G23, not
   further design. That is leftover-design closure for
   NT-3 and NT-5. Product-law ownership remains DR-133 /
   provider-only-output-contract.v3 (PAL-V1-A1: this
   owner is the execution-obligation owner).

6. **DR-133 leftover-design of the seven NT classes.**
   NT-1/2/6 remain named at G21; NT-4/7 at G20; NT-3/5
   at G23. All seven remainders are execution. This
   entry does not open Class A. The v3 contract remains
   CANDIDATE-NOT-APPLIED and binds NOTHING, so
   Eligibility gate 1 does not hold. Not eligible in
   kind. Not SATISFIED.

7. Advisories CLAUDE-PONAL-V1-ADV1 (landed by same-act
   naming), PAL-V1-A1, and CLAUDE-D146-ADV1 travel as
   honesty work.

8. Does not authorize `docs/v2/implementation/`.
   Does not mint a D-096 (A) grant.

### Exact new row

Insert this one markdown table row:

`| DR-G23 PROVIDER-WELL-FORMED-ADMISSION | Host admission of well-formed TypeScript-provider FactCandidate and Coverage payloads refuses finding-masquerade and Coverage-domain mutation | named: harness.DR-G23.provider-well-formed-admission.preview (D-147; not authored; not QUALIFIED). hostile-but-well-formed admission corpus (DR-133 NT-3, NT-5) | FactCandidate relation-registry refusal before fact admission; Coverage-domain mutation refusal; no unknown-to-covered conversion | Protocol + semantic owners | PROPOSED; not QUALIFIED | pass all; no waiver for silent admission | OPEN |`

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (18 of 18 becomes 19 of 19
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D147, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
18-member required-now set. Does not unwrite D-136,
D-144, D-145, or D-146.
