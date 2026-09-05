# D-169 — Add DR-G32 as required-now actor-join fixture-execution obligation

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED three-limb act. Same
> class as D-147 / D-150 / D-157 / D-158 / D-167. Records
> independent dual ACCEPT 0/0 of frozen
> `g32-three-limb-act.v2.json`.
> (1) D-001 MF-6 file-08 write of one new gate row
> DR-G32 ACTOR-JOIN-FIXTURE-EXECUTION,
> (2) scoped D-002 condition-4 required-gate-set successor:
> live 27-member set plus G32 (cardinality 28),
> (3) D-086 successor that names
> `harness.DR-G32.actor-join-fixture-execution.preview`
> at
> `docs/coop/artifacts/harness.DR-G32.actor-join-fixture-execution.preview.v1.json`
> in the same act.
> This is coordinator decision **D-169**, not a register
> row other than the one gate cell it adds.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** change the file 08 DR-114 token off `OPEN`.
> **Does not** execute the thirteen classes.
> **Does not** author join-fixture bytes.
> **Does not** invent a fourteenth class.
> **Does not** force a ride onto G09.
> **Does not** steal DR-105 leftover.
> **Does not** record FC-C1, mint a CA-2 decision, or
> admit CA-1 IN_PROCESS.
> **Does not** record join-fx-gate-naming.v1.
> **Does not** unwrite D-167.
> **Does not** restore G17 or name G13 into required-now.
> **Does not** change D-002 commands, platforms, deferrals,
> identity rides, or the SATISFIED-requiring row set.
> **Does not** invent a D9 code, a section 7.1 recipe, or
> a D-006 unit.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-168 is ADOPTED at
`c983aa272569a780674d04cb912f0b2797606201`.
HEAD is `c983aa272569a780674d04cb912f0b2797606201`.
Last live heading is D-168. No live D-169 heading exists.
Required-now is 27. G31 is live. G32 is not.

Stage A dual independent ACCEPT 0/0 of the frozen
three-limb candidate (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g32-three-limb-act.v2.review-independent.claude2.json` | `61dbbf6c22b49cc4c89795ffb7d23507d7b6ed8b4defc6ee239f5b8f28436d40` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g32-three-limb-act.v2.review-independent.codex.json` | `93e040fe110c21b7202f94072df3723f5f1e428a422faa427125fa4d48f959d2` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g32-three-limb-act.v2.json | `8a64123830a95bd7774f171531f7872a34e35aeaf865383311c29dbb7ed5fc31` |
| g32-three-limb-act.v2.review-independent.claude2.json | `61dbbf6c22b49cc4c89795ffb7d23507d7b6ed8b4defc6ee239f5b8f28436d40` |
| g32-three-limb-act.v2.review-independent.codex.json | `93e040fe110c21b7202f94072df3723f5f1e428a422faa427125fa4d48f959d2` |
| join-fx-gate-naming.v2.json | `533031752975425e95fc1aa1bfee8a8413c7368152d4c5b5d1e3ce2d2895119d` |
| harness.DR-G32.actor-join-fixture-execution.preview.v1.json | `a5a5f163f408062e86052f8b095f938a96d36f26407f9dcc30cb8040ca199c28` |
| doctor-actor-join-integration-contract.v8.json | `c830f954605a4a1d47c5643230439340994a0c42c4a487359541c578d00bc662` |
| coordinator-decisions.D-056.turn2.draft.md | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| COORDINATOR-DECISIONS.md | `8a061a672fd6035ed144782c38def089c5200389d6bb0f354db6d3ab94b2b681` |
| file 08 | `9af2bc71adf437c8a138aa6caadd2e6ae55fa9f2165b74e816ef1d45df739b76` |
| HEAD | `c983aa272569a780674d04cb912f0b2797606201` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, the frozen
three-limb candidate, both Stage A verdicts, naming v2,
G32 spec v1, actor-join v8, D-056 turn-2 draft, and this
draft unmoved, re-measure before adoption. Append-only
COORD after this remeasurement, with those files unmoved,
is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.
Remeasure live owner / required-name / OPEN counts at
apply time. Do not copy stale snapshot arithmetic if
file 08 has moved.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time (file 08 unmoved at
`9af2bc71…`): 31 gate rows; 31 of 31 owners named; 27 of
27 required names; 28 `OPEN`, 3 `HARD-BLOCKED`; last gate
row is DR-G31; DR-G32 is absent; DR-114 lead token remains
`OPEN`. Required-now stays 27 until this entry is adopted.

## Why this entry exists

D-164 recorded leftover-design of DR-114
OBL-JOIN-FX-EXECUTION: no live file-08 DR-G* owns
actor-join fixture execution. join-fx-gate-naming.v1
was REJECT JFXG-V1-B1. Naming v2 remasured occupancy
and received dual ACCEPT 0/0. The G32 v1 specification
occupies the named path and received dual ACCEPT 0/0.
The frozen three-limb candidate states the recording
that would make a live condition-4 / DR-G* own that
remainder. Same-act naming is required so condition 4
stays MET. G31 is already live, so this identifier is
eligible as G32.

This entry is that later act. It assigns G32 (file 08's
gate table ends at DR-G31). It assigns no other number.
join-fx-gate-naming.v1 is not recorded.

The candidate assigned no D-* heading. This draft is the
numbered heading. This file existing is not the
recording until CONSENT and apply.

## Decision

1. **Assign DR-G32.** The identifier
   `DR-G32 ACTOR-JOIN-FIXTURE-EXECUTION` is assigned. It
   owns the thirteen already-named actor-join v8 fixture
   classes, verbatim and in order. Class count is 13.
   Doctor FC implementations remain OBL-DOCTOR-FX-AUTHORING
   on DR-114, not a fourteenth class. G09 owns permission
   truth, not this property.

2. **Limb A — scoped D-002 successor.** Required-now,
   as amended through D-167 (requiredNow=27; D-168 did not
   change cardinality), is succeeded by that same
   27-member set plus **DR-G32**. Cardinality becomes 28.
   Other D-018 item-2 sets are unchanged. G17 remains
   inapplicable. G13 remains reserved and not required-now.

3. **Limb B — D-086 successor, same act.** The harness
   identifier is
   `harness.DR-G32.actor-join-fixture-execution.preview`.
   Occupancy path is
   `docs/coop/artifacts/harness.DR-G32.actor-join-fixture-execution.preview.v1.json`.
   Naming is not execution. The v1 file is an authored
   harness *specification* (leftover-design authoring).
   Fixture bytes remain NOT-AUTHORED. The file-08 harness
   cell still reads not authored; not QUALIFIED.

4. **Limb C — MF-6 file-08 write, same act.** After
   CONSENT, insert exactly one new gate-table row
   immediately after the live DR-G31 row and immediately
   before the heading `## Blueprint-readiness decision`.
   The row is the exact markdown line in §Exact new row.
   Rewrite only the condition-4 "Measured now" cell using
   the fenced operands in §Exact condition-4 operands.
   Do not change the 65-row preamble. Do not change
   conditions 1, 2, 3, or 5. Do not change condition 4
   standing (`MET`). Do not edit the DR-114 status cell.
   Do not edit DR-104, DR-117, DR-131, or DR-133 status
   cells.

5. **Leftover-design of OBL-JOIN-FX-EXECUTION.** That
   remainder is now named at a live condition-4 / DR-G*
   obligation with owner Operability + security.
   Remainder after this act is G32 execution of the
   thirteen classes once fixture implementations exist.
   leftover-design of OBL-JOIN-FX-AUTHORING,
   OBL-DOCTOR-FX-AUTHORING, OBL-FC-C1, and OBL-BLK-1..4
   remains.

6. **DR-114 eligibility.** After this act, D-056
   Eligibility gates 2 and 3 do **not** hold for DR-114:
   leftover-design of fixture-authoring, FC-C1, and
   BLK-1..4 remains. Gate 1 Class A is not opened.
   Class B SATISFIED is not recorded. Gates 4 and 5 are
   not performed. This entry is not the dedicated
   SATISFIED-GRADE cycle. DR-114 stays `OPEN`. Not
   SATISFIED.

7. Does not execute the thirteen classes. Does not
   author fixture bytes. Does not invent a fourteenth
   class. Does not force a ride onto G09. Does not
   steal DR-105 leftover. Does not record FC-C1. Does
   not mint a CA-2 decision. Does not admit CA-1
   IN_PROCESS. Does not record naming v1. Does not
   unwrite D-167. Does not restore G17. Does not name
   G13 into required-now. Does not invent a D9 code.
   Does not authorize `docs/v2/implementation/`.

### Exact new row

Insert this one markdown table row:

~~~~
| DR-G32 ACTOR-JOIN-FIXTURE-EXECUTION | The thirteen already-named actor-join fixture classes execute against independently pinned fixture implementations of those classes. Naming is not execution. G09 owns permission truth, not this property | named: harness.DR-G32.actor-join-fixture-execution.preview (D-169; not authored; not QUALIFIED). thirteen-class corpus (FC-JOIN-HOST-OUTSIDE-DR105, FC-JOIN-HOST-DEFAULT-AND-OPMETA, FC-JOIN-DOCTOR-CONSENT-NOT-GRANT, FC-JOIN-COMPONENT-TAIL, FC-JOIN-CA2-TAIL, FC-JOIN-FAIL-CLOSED-UNRECORDED, FC-JOIN-PERMISSIONREF-RESERVED, FC-JOIN-CA2-UNEXERCISABLE, FC-JOIN-CA2-D000-GATE, FC-JOIN-CA1-INPROCESS-UNEXERCISABLE, FC-JOIN-CA3-KEYCHAIN-UNEXERCISABLE, FC-JOIN-INHERITED-PERM-RECITAL, FC-JOIN-BLK-STILL-ROUTED) | each class reproduces its actor-join v8 definition and specified refuse/pass fate once fixture implementations exist; unexercisable classes remain refuse; not G09 permission truth; not doctor FC implementations; not FC-C1 recording; not CA-2 mint; not CA-1 IN_PROCESS admission | Operability + security | PROPOSED; not QUALIFIED | pass all; no waiver for silent accept of a refuse class; no waiver that admits an unexercisable class | OPEN |
~~~~

The live row cites D-169 in the harness cell because this
entry assigns that number. The frozen candidate assigned
no number and therefore omitted it. All other cells match
`proposedFile08RowIfRecorded` in
`g32-three-limb-act.v2.json` and naming v2 at the
JSON-value level.

### Exact condition-4 operands

Before (live file 08 Measured-now cell; occurs exactly once;
no backslash bytes):

~~~~
**31 of 31 owners named** at role level; **27 of 27 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154 / D-157 / D-158 / D-167; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; G29 named under D-157; G30 named under D-158; G31 named under D-167; every assurance stage is below `QUALIFIED`; 28 `OPEN`, 3 `HARD-BLOCKED`
~~~~

After:

~~~~
**32 of 32 owners named** at role level; **28 of 28 required gates name a recorded identifier** (D-086 / D-088 / D-102 / D-147 / D-150 / D-151 / D-152 / D-153 / D-154 / D-157 / D-158 / D-167 / D-169; not authored; not QUALIFIED); G03/G04 named under D-102 hosted-fleet-class contract; G17 is inapplicable (D-077); G23 named under D-147; G24 named under D-150; G25 named under D-151; G26 named under D-152; G27 named under D-153; G28 named under D-154; G29 named under D-157; G30 named under D-158; G31 named under D-167; G32 named under D-169; every assurance stage is below `QUALIFIED`; 29 `OPEN`, 3 `HARD-BLOCKED`
~~~~

Projected at apply if file 08 is otherwise unmoved: 32
gate rows; last row DR-G32; required-now 28; naming half
stays MET; MET is not QUALIFIED.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (27 of 27 becomes 28 of 28
in the same act). Condition 5 last. Does not authorize
`docs/v2/implementation/`.

### Reversibility

Total only before a later dependent SATISFIED cycle,
leftover rewrite, or file-08 harness-cell rewrite.
Overturn: C-D169, plus restore of the prior gate table,
the prior condition-4 measured cell, and the prior
27-member required-now set. Does not unwrite D-032,
D-129, D-164, D-167, or D-168.
