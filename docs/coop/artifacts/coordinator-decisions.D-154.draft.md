# D-154 — Add DR-G28 as required-now preview-analyze host-must-not-mint obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> D-149's fifth and last proposed later work:
> PREVIEW-ANALYZE-HOST-MUST-NOT-MINT for NT-7 and NT-8.
> (1) D-001 MF-6 file-08 write of one new gate row,
> (2) scoped D-002 condition-4 required-gate-set successor,
> (3) D-086 successor that names the harness identifier in
> the same act.
> This is coordinator decision **D-154**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** make DR-131 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145, D-147, D-148, D-150, D-151,
> D-152, or D-153.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-153 is ADOPTED at `b07763345adebbdfda8c1966a9afe6b40382348c`.

Measured inputs:

| Path | sha256 |
|---|---|
| preview-analyze-admission-leftover.v1.json | `1222501032917790832a3ffa8f3953ceb7a73907942a5ea30442346bf59935a5` |
| preview-analyze-contract.v2.json | `081ff7fb529b34a3db3ac9f4c7505848e2253be12b5a867d39b49b3a26d56970` |
| COORDINATOR-DECISIONS.md | `18e62a1e642bce301d26a936b87e90f229f845d34416e1e8c48af42bf344f6c5` |
| file 08 | `7bf1c2e35fdba5afe80e97a9803a492f5a99c884fa7541bfe92b7773b1056206` |
| D-153 commit | `b07763345adebbdfda8c1966a9afe6b40382348c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover.v1,
v2 contract, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-149's fifth proposed kind owns NT-7 and NT-8: the host
must not mint fail/warn other than core policyOutcome, and
must not mint a D9 class, exit number, or HostTermination
from the pack threshold or policyOutcome. Host maps only
existing D9 v1.14 classes. This entry invents no D9 code.
Same-act naming is required so condition 4 stays MET.

This entry is that later act for the fifth kind only.
It assigns G28 (file 08's gate table ends at DR-G27).

## Decision

1. **Assign DR-G28.** The identifier
   `DR-G28 PREVIEW-ANALYZE-HOST-MUST-NOT-MINT` is assigned.
   It owns DR-131 NT-7 and NT-8 only.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended through D-153 (requiredNow=23), is succeeded
   by that same 23-member set plus **DR-G28**. Cardinality
   becomes 24. Other D-018 item-2 sets are unchanged.
   G17 remains inapplicable.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G28.preview-analyze-host-must-not-mint.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G27 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-131 or DR-133
   status cells.

5. **Leftover-design of NT-7 and NT-8.** Those two
   classes are now named at a condition-4 / DR-G*
   obligation with owner Product + CLI / output.
   Remainder is G28 execution. That is leftover-design
   closure for NT-7 and NT-8. This artifact invents no
   D9 code.

6. **DR-131 leftover as a whole.** After this act, every
   D-149 leftover class (NT-1/2/3/5/6/7/8) is named at a
   condition-4 / DR-G* obligation, and NT-4 remains
   discharged by named DR-133 classes. After this act,
   D-056 Eligibility gates 2 and 3 hold for those eight
   NT classes. This entry does not open Class A and does
   not record SATISFIED. Gate 1's application-grade /
   no-express-reservation limb is not established here.
   Gate 4 reserves eligibility to a later dedicated
   SATISFIED-GRADE cycle. This entry is not that cycle.
   Not eligible in kind. Not SATISFIED.
   CANDIDATE-NOT-APPLIED / binds NOTHING is not itself
   a Class A bar (D-085).

7. Does not invent a D9 code. Does not restore G17.
   Does not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G28 PREVIEW-ANALYZE-HOST-MUST-NOT-MINT | Host must not mint fail/warn other than core policyOutcome, and must not mint a D9 class, exit, or HostTermination from the pack threshold or policyOutcome | named: harness.DR-G28.preview-analyze-host-must-not-mint.preview (D-154; not authored; not QUALIFIED). host-must-not-mint corpus (DR-131 NT-7, NT-8) | host maps only existing D9 v1.14 classes; policyOutcome is not HostTermination; invents no D9 code | Product + CLI / output | PROPOSED; not QUALIFIED | pass all; no waiver by host-minted D9 | OPEN |
~~~~

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**27 of 27 owners named** at role level; **23 of 23 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; every assurance stage is below `QUALIFIED`; 24 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**28 of 28 owners named** at role level; **24 of 24 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; every assurance stage is below `QUALIFIED`; 25 `OPEN`, 3 `HARD-BLOCKED`
~~~~

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (23 of 23 becomes 24 of 24
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D154, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
23-member required-now set. Does not unwrite D-138,
D-147, D-149, D-150, D-151, D-152, or D-153.
