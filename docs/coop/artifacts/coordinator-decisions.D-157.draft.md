# D-157 — Add DR-G29 as required-now preview-boundary excluded-form admission obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-15
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Performs
> D-156's first proposed later work:
> PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION for EE-1, EE-2,
> EE-3b, EE-4, EE-5a, EE-5b, and EE-6a.
> (1) D-001 MF-6 file-08 write of one new gate row,
> (2) scoped D-002 condition-4 required-gate-set successor,
> (3) D-086 successor that names the harness identifier in
> the same act. This cycle's choice, not a mandate to
> perform the last D-156 kind (install-shape).
> This is coordinator decision **D-157**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design for EE-7a, EE-7b, or
> EE-7d.
> **Does not** name EE-6b at G09, EE-7c at G14, or EE-7e
> at G16.
> **Does not** make DR-117 eligible in kind. This entry is
> not the dedicated SATISFIED-GRADE cycle (Eligibility
> gate 4).
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** retarget D-145, D-147, D-154, D-155, or
> D-156.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-156 is ADOPTED at `f58071ac402b907e01f22eaa6d488a4caea8a5cd`.
HEAD is `2a90e79cc21c57e6ce472886912b83c2761fb28a` (D-156
heading hygiene).

Measured inputs:

| Path | sha256 |
|---|---|
| preview-product-boundary-admission-leftover.v1.json | `6280d64867433a963a4ce0bcc44521c57c485b0eea19404b4740c36c94ef4cce` |
| preview-product-boundary-ee-gate-join.v1.json | `ae20b25fcb908a19fcd38dbb8e7c5963eee983b566132936c4bd1e7af34b3de0` |
| preview-product-boundary-successor.v5.json | `5face6a97b311117569044c0214452571e6d3f051e1ab9b38f46abf442ce1262` |
| COORDINATOR-DECISIONS.md | `f87934e24a6efc6428068c8050c6c07fd337c3cd56a8bcddbbc3d20cdba5b8c2` |
| file 08 | `6d593a11880f2063376bd8760f7779822a167b52e4d8299cf9e75e2cbb97133f` |
| D-156 commit | `f58071ac402b907e01f22eaa6d488a4caea8a5cd` |
| HEAD | `2a90e79cc21c57e6ce472886912b83c2761fb28a` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover.v1,
join v1, v5, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-156's first proposed kind owns EE-1, EE-2, EE-3b, EE-4,
EE-5a, EE-5b, and EE-6a: preview admission refuses those
well-formed excluded forms. Same-act naming is required so
condition 4 stays MET.

This entry is that later act for the first kind only.
It assigns G29 (file 08's gate table ends at DR-G28).

## Decision

1. **Assign DR-G29.** The identifier
   `DR-G29 PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION` is
   assigned. It owns DR-117 EE-1, EE-2, EE-3b, EE-4,
   EE-5a, EE-5b, and EE-6a only.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended through D-154 (requiredNow=24), is succeeded
   by that same 24-member set plus **DR-G29**. Cardinality
   becomes 25. Other D-018 item-2 sets are unchanged.
   G17 remains inapplicable.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G29.preview-boundary-excluded-form-admission.preview`.
   Naming is not execution. Not authored. Not QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G28 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-117, DR-131, or
   DR-133 status cells.

5. **Leftover-design of EE-1, EE-2, EE-3b, EE-4, EE-5a,
   EE-5b, and EE-6a.** Those seven classes are now named
   at a condition-4 / DR-G* obligation with owner Product
   owner. Remainder is G29 execution. That is leftover-
   design closure for those seven only.

6. **DR-117 leftover as a whole.** EE-7a, EE-7b, and
   EE-7d remain leftover-design. EE-6b, EE-7c, and EE-7e
   remain capable-of-riding and unnamed at G09/G14/G16.
   After this act, D-056 Eligibility gates 2 and 3 do
   **not** hold for DR-117. Class A is not opened. Not
   eligible in kind. Not SATISFIED.

7. Does not invent a D9 code. Does not restore G17.
   Does not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G29 PREVIEW-BOUNDARY-EXCLUDED-FORM-ADMISSION | Preview admission refuses well-formed excluded forms: non-first-party/untrusted publisher, public-lifecycle/discovery, contributor authority claims, untrusted native/WASM, contribution hooks/roots/probes, pre-stage imperative substitution, and network-granted analysis | named: harness.DR-G29.preview-boundary-excluded-form-admission.preview (D-157; not authored; not QUALIFIED). hostile-but-well-formed excluded-form admission corpus (DR-117 EE-1, EE-2, EE-3b, EE-4, EE-5a, EE-5b, EE-6a) | refused at admission; no ExecutionId; v1-slice §7 item 8; not G21 sandbox; not G23 provider FactCandidate/Coverage | Product owner | PROPOSED; not QUALIFIED | pass all; no waiver for silent admission | OPEN |
~~~~

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**28 of 28 owners named** at role level; **24 of 24 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; every assurance stage is below `QUALIFIED`; 25 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**29 of 29 owners named** at role level; **25 of 25 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154 / D-157; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; G29 named under D-157; every assurance stage is below `QUALIFIED`; 26 `OPEN`, 3 `HARD-BLOCKED`
~~~~

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (24 of 24 becomes 25 of 25
in the same act). Condition 5 last.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D157, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
24-member required-now set. Does not unwrite D-137,
D-154, D-155, or D-156.
