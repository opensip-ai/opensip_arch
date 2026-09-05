# D-167 — Add DR-G31 as required-now identity-namespace negative-test execution obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Same
> class as D-147 / D-150 / D-157 / D-158. Records
> independent dual ACCEPT 0/0 of frozen
> `g31-three-limb-act.v1.json`.
> (1) D-001 MF-6 file-08 write of one new gate row
> DR-G31 IDENTITY-NAMESPACE-NEGATIVE-TEST-EXECUTION,
> (2) scoped D-002 condition-4 required-gate-set successor:
> prior 26-member set plus G31 (cardinality 27),
> (3) D-086 successor that names
> `harness.DR-G31.identity-namespace-negative-test.preview`
> at
> `docs/coop/artifacts/harness.DR-G31.identity-namespace-negative-test.preview.v2.json`
> in the same act.
> This is coordinator decision **D-167**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-104.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** change the file 08 DR-104 token off
> `DECIDED-V1-NOT-INTEGRATED`.
> **Does not** execute the eleven classes.
> **Does not** invent a twelfth class.
> **Does not** force a ride onto G15.
> **Does not** steal DR-103 leftover.
> **Does not** record G32 or change required-now to 28.
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** invent a D9 code, a section 7.1 recipe, or
> a D-006 unit.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-166 is ADOPTED at
`5d5d77819ae3019d9e6e02f1e66de3d93c060402`.
HEAD is `5d5d77819ae3019d9e6e02f1e66de3d93c060402`
(D-166: remove duplicate D-165 heading). Last live
heading is D-166. No live D-167 heading exists.

Stage A dual independent ACCEPT 0/0 of the frozen
three-limb candidate (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g31-three-limb-act.v1.review-independent.claude2.json` | `0bc2deeb294179005ca668f3d7f2021ba38c51da925bdfc2da9a23c6248e01e9` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g31-three-limb-act.v1.review-independent.codex.json` | `e2a977e7f67ea6604d20644182dc287f52222c7cd90936ac8cc9499eb2c520fc` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g31-three-limb-act.v1.json | `7d5848439b3cca947f1a9c8be730ca21c716559321306778ab7b24876cf28dd7` |
| g31-three-limb-act.v1.review-independent.claude2.json | `0bc2deeb294179005ca668f3d7f2021ba38c51da925bdfc2da9a23c6248e01e9` |
| g31-three-limb-act.v1.review-independent.codex.json | `e2a977e7f67ea6604d20644182dc287f52222c7cd90936ac8cc9499eb2c520fc` |
| identity-nt11-gate-naming.v2.json | `e77756850f39934e41b07c38b6f233dbbeef8a8528c48c816687dff0495a615e` |
| harness.DR-G31.identity-namespace-negative-test.preview.v2.json | `851abb4d5463cc2a3b8a392496f021f2901e64f5266e822be55fdc753292c3f6` |
| identity-namespace-leftover-join.v4.json | `fe337e4db3aa72be80ba35730a643f113491e2fc423197e7a63640e61a9a7eb6` |
| identity-namespace-negative-test-corpus.v1.json | `2c0795cd58e95e56afad46899b3c5d546d4fb520e38e1a8c3f7c132aa69583dd` |
| coordinator-decisions.D-056.turn2.draft.md | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| COORDINATOR-DECISIONS.md | `38297e5b81db4fa3d0b41cd8a4b41d1ab8a7ab3b5aa5396774434a0d8ed8b7b2` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| HEAD | `5d5d77819ae3019d9e6e02f1e66de3d93c060402` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the frozen
three-limb candidate, both Stage A verdicts, naming v2,
G31 v2, leftover-join v4, corpus v1, D-056 turn-2 draft,
and this draft unmoved, re-measure before adoption.
Append-only COORD after this remeasurement, with those
files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a
MUST-FIX. Remeasure live owner / required-name / OPEN
counts at apply time. Do not copy stale snapshot
arithmetic if file 08 has moved.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time (file 08 unmoved at
`3a9442d1…`): 30 gate rows; 30 of 30 owners named; 26 of
26 required names; 27 `OPEN`, 3 `HARD-BLOCKED`; last gate
row is DR-G30; DR-G31 is absent; DR-104 lead token remains
`DECIDED-V1-NOT-INTEGRATED`. Required-now stays 26 until
this entry is adopted.

## Why this entry exists

D-162 recorded leftover-design of DR-104
OBL-NT-11-EXECUTION: no live file-08 DR-G* owns
identity-namespace negative-test execution. D-130 already
authored the eleven classes. Naming v2 and harness v2
already occupy the proposed identifier and v2 path as
CANDIDATE-NOT-APPLIED leftover-design. The frozen
three-limb candidate states the recording that would make
a live condition-4 / DR-G* own that remainder. Same-act
naming is required so condition 4 stays MET.

This entry is that later act. It assigns G31 (file 08's
gate table ends at DR-G30). It assigns no other number.

The candidate assigned no D-* heading. This draft is the
numbered heading. This file existing is not the
recording until CONSENT and apply.

## Decision

1. **Assign DR-G31.** The identifier
   `DR-G31 IDENTITY-NAMESPACE-NEGATIVE-TEST-EXECUTION` is
   assigned. It owns the eleven D-012 / identity-v3
   negative-test classes recorded at D-130, verbatim and
   in order: collision; cycle; shadow; stale-alias;
   parent-linkage collision; reserved-name claim;
   scope-precedence disclosure; ID/version distinctness;
   multi-version coexistence; no-execution-during-admission
   probe; reserved-list/live-grammar CI parity. Class count
   is 11. Namespace-migration doctor-remediation remains a
   DR-114 ride, not a twelfth class.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended through D-158 (requiredNow=26; D-159 did not
   change cardinality), is succeeded by that same
   26-member set plus **DR-G31**. Cardinality becomes 27.
   Other D-018 item-2 sets are unchanged. G17 remains
   inapplicable. G13 remains reserved and not required-now.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G31.identity-namespace-negative-test.preview`.
   Occupancy path is
   `docs/coop/artifacts/harness.DR-G31.identity-namespace-negative-test.preview.v2.json`.
   Naming is not execution. The v2 file is an authored
   harness *specification* (leftover-design authoring). The
   file-08 harness cell still reads not authored; not
   QUALIFIED. Existence of the specification is not
   QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G30 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-104 status cell.
   Do not edit DR-117, DR-131, or DR-133 status cells.

5. **Leftover-design of OBL-NT-11-EXECUTION.** That
   remainder is now named at a live condition-4 / DR-G*
   obligation with owner Product/CLI architecture.
   Remainder after this act is G31 execution of the eleven
   D-130 classes. That is leftover-design closure for
   OBL-NT-11-EXECUTION only.

6. **DR-104 eligibility.** After this act, D-056
   Eligibility gates 2 and 3 hold for DR-104. Gate 1
   Class A is not opened. Class B SATISFIED is not
   recorded. Gates 4 and 5 are not performed. This entry
   is not the dedicated SATISFIED-GRADE cycle. DR-104
   stays `DECIDED-V1-NOT-INTEGRATED`. Not SATISFIED.

7. Does not execute the eleven classes. Does not invent
   a twelfth class. Does not force a ride onto G15.
   Does not steal DR-103 leftover (Windows-path /
   envelope / unicode / OD-1 / OD-2 remain at DR-103).
   Does not record G32. Does not restore G17. Does not
   name G13 into required-now. Does not invent a D9
   code, a section 7.1 recipe, or a D-006 unit. Does
   not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G31 IDENTITY-NAMESPACE-NEGATIVE-TEST-EXECUTION | The eleven D-012 / identity-v3 negative-test classes execute against the already-authored exact-byte fixtures recorded at D-130 | named: harness.DR-G31.identity-namespace-negative-test.preview (D-167; not authored; not QUALIFIED). eleven-class corpus (collision, cycle, shadow, stale-alias, parent-linkage collision, reserved-name claim, scope-precedence disclosure, ID/version distinctness, multi-version coexistence, no-execution-during-admission probe, reserved-list/live-grammar CI parity) | each class primary reproduces its D-130 pinned digest and expected fate; not G15 adapter conformance; not DR-103 leftover Windows-path/envelope/unicode/OD-1/OD-2; not namespace-migration doctor-remediation | Product/CLI architecture | PROPOSED; not QUALIFIED | pass all; no waiver for silent accept of a refuse class | OPEN |
~~~~

The live row cites D-167 in the harness cell because this
entry assigns that number. The frozen candidate assigned
no number and therefore omitted it. All other cells match
`proposedFile08RowIfRecorded` in
`g31-three-limb-act.v1.json` and naming v2 at the
JSON-value level.

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**30 of 30 owners named** at role level; **26 of 26 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154 / D-157 / D-158; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; G29 named under D-157; G30 named under D-158; every assurance stage is below `QUALIFIED`; 27 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**31 of 31 owners named** at role level; **27 of 27 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154 / D-157 / D-158 / D-167; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; G29 named under D-157; G30 named under D-158; G31 named under D-167; every assurance stage is below `QUALIFIED`; 28 `OPEN`, 3 `HARD-BLOCKED`
~~~~

Projected at apply if file 08 is otherwise unmoved: 31
gate rows; last row DR-G31; required-now 27; naming half
stays MET; MET is not QUALIFIED.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26 becomes 27 of 27
in the same act). Condition 5 last. Does not authorize
`docs/v2/implementation/`.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D167, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
26-member required-now set. Does not unwrite D-012,
D-056, D-130, D-158, D-162, or D-166.
