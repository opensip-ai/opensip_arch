# D-241 — Record g21-fixture-corpus.v1 as G21 leftover-design NT-1/NT-2 fixture implementations

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g21-fixture-corpus.v1.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240. Not a three-limb act. Not a required-now successor.
> Not SATISFIED-GRADE.
> This is coordinator decision **D-241**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-101.
> **Does not** reopen DR-102 SATISFIED.
> **Does not** close leftover-design of OBL-G21-FX-AUTHORING.
> **Does not** remasure leftover-join.v4.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G21.
> **Does not** author NT-6.
> **Does not** take over G23.
> **Does not** invent a finding schema.
> **Does not** invent a D9 code, exit number, or HostTermination.
> **Does not** invent a pack IR.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent a D-002 platform list.
> **Does not** invent observation bytes.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v4.
> **Does not** rewrite leftover-join.v4.
> **Does not** rewrite leftover-join.v8.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-240 is ADOPTED at
`7e2284d0bc89bb0995c96c8bc4f52f1fae2de6c6`.
HEAD is `7e2284d0bc89bb0995c96c8bc4f52f1fae2de6c6`.
Last live heading is D-240. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
fixture corpus (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g21-fixture-corpus.v1.review-independent.claude2.json` | `ad9234df10c7952cd21b63945fceffea76509eb8a3d261951efd2e4575c20de1` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g21-fixture-corpus.v1.review-independent.codex.json` | `5b547afdad83c46e83e608c26f59a693994f6a11a5bd10eaa94c26f269dc6368` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude Stage A observationsNotFindings[0] | none | observation; no change requested |
| Claude Stage A observationsNotFindings[1] | none | observation; no change requested |
| Claude Stage A observationsNotFindings[2] | none | observation; no change requested |
| Claude Stage A observationsNotFindings[3] | none | observation; no change requested |
| Codex Stage A | none | zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g21-fixture-corpus.v1.json | `861bb4e7d26a80158cc1cc3a0518c5e8e95311bee4d8c8ce63acd1e60d6c906d` |
| g21-fixture-corpus.v1.review-independent.claude2.json | `ad9234df10c7952cd21b63945fceffea76509eb8a3d261951efd2e4575c20de1` |
| g21-fixture-corpus.v1.review-independent.codex.json | `5b547afdad83c46e83e608c26f59a693994f6a11a5bd10eaa94c26f269dc6368` |
| g21-fixture-corpus.v1.review-prompt.md | `1b163a6a869634ca4bba20b9d4937441e472bee04161e370b1122f677021c9fa` |
| fixtures/g21.v1/G21.nt1.unknown-Finding-frame.json | `b9ff9338d6a8a13142ed073e2543c48cd7790e38df8585ee90e130b212151c8c` |
| fixtures/g21.v1/G21.nt2.extra-finding-member-on-closed-payload.json | `bc264fc7d0cad17bd269be42cd5f06579c2a50340d68d3abbe19c895b4b06dc8` |
| g21-leftover-join.v4.json (current G21 leftover-join; not this subject) | `b8696fd134550a9ad15d44a07adcc4030aad3702013cc9de914bbab5b8e74ae4` |
| harness.DR-G21.component-failure-containment.v4.json (current occupancy; not this subject) | `13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b` |
| g21-input-corpus.v1.json (not this subject) | `247e69a6118a7af5e4ea139e0b2be60029cc0f8e024497d149da9ada68bd0429` |
| g23-leftover-join.v8.json (current G23 leftover-join; not this subject) | `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` |
| delivery.v2.json (not this subject) | `47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3` |
| provider-only-output-contract.v3.json (not this subject) | `ef2a7416700cc8197486c6e29450673c60e3b94512be3ad278d1995f7d281309` |
| provider-only-nt-gate-join.v6.json (not this subject) | `93bc62d43751d8037aa2a696209eccbdee0ae3b3f11292d9a05be2bc245082a3` |
| coordinator-decisions.D-056.turn2.draft.md (not this subject) | `dfb0c2af39ff31df9bf3609c131f03ee2d87a585dcd684abd633d47ffb11ed82` |
| COORDINATOR-DECISIONS.md | `c6399c74a7892d6687beda854d3ab26661695a11b807833332129b459bd7d330` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `7e2284d0bc89bb0995c96c8bc4f52f1fae2de6c6` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v1, both
Stage A verdicts, leftover-join.v4, occupancy v4,
leftover-join.v8, the two v1 fixture files, and this draft
unmoved, remasure before adoption. Append-only COORD after
this remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G21 lead
token remains `OPEN`; DR-114 remains `OPEN`; DR-133 remains
`OPEN`. Naming parent is D-145 / naming v6, not
leftover-join.v4. leftover-join.v4 remains the current G21
leftover-join. leftover-join.v8 remains the current G23
leftover-join. There is no predecessor G21 fixture corpus.
Do not record leftover-join.v4 as closed. Do not record
leftover-join.v8 leftoverDesign as other than `[]`.

This is a leftover-design COORD draft. It does not claim
that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of v1 leftover-design
fixture implementations for two live G21 INPUT-corpus
initial states: NT-1 unknown-Finding-frame and NT-2
extra-finding-member-on-closed-payload. Types are quoted
from delivery.v2 and provider-only-output-contract.v3.
leftover-join.v4 (D-196) leftoverDesign remains
`[OBL-G21-FX-AUTHORING]`. This entry records v1. It is not
SATISFIED-GRADE. It does not close leftover-design of
OBL-G21-FX-AUTHORING. Remaining G21 classes stay unauthored.
A later leftover-join remasurement may measure leftover-design
of these two NT implementations as stale as an authoring
claim while leftoverDesign of OBL-G21-FX-AUTHORING remains
for the unauthored classes. Candidate-buffer digest and
subsequent-session view remain qualification.

## Decision

1. Record
   `g21-fixture-corpus.v1.json`
   as G21 leftover-design NT-1/NT-2 fixture implementations
   after D-240. The candidate binds NOTHING. Both independent
   reviewers returned 0 blockers and 0 SHOULD-FIX. There is
   no predecessor G21 fixture corpus.
2. DR-G21 stays `OPEN`. leftover-design of
   OBL-G21-FX-AUTHORING remains on leftover-join.v4 (D-196).
   Remainder of G21 execution, including candidate-buffer
   digest and subsequent-session view, remains qualification
   (D-056). Does not pin QUALIFIED. Does not invent a finding
   schema. Does not invent a D9 code, exit number, or
   HostTermination. Does not invent a pack IR. Does not
   invent a section 7.1 recipe. Does not invent a D-002
   platform list. Does not author NT-6. Does not take over
   G23. Does not reopen DR-102 SATISFIED. Does not SATISFY
   DR-114. Does not SATISFY DR-133. Does not SATISFY DR-117.
   Does not SATISFY DR-131. Does not SATISFY DR-101. Gate 1
   Class A is not opened. Not SATISFIED. Required-now stays
   28. Condition-4 effect is zero. Naming parent is D-145 /
   naming v6, not leftover-join.v4. Claude Stage A returned
   four observationsNotFindings strings. They carry no
   identifiers. Codex Stage A returned zero advisories and
   no observations. This entry does not invent identifiers
   for those observations and does not claim that both
   reviewers' identifiers are preserved. Codex returned no
   observation identifiers. Does not execute G21. Does not
   rewrite leftover-join.v4. Does not rewrite occupancy v4.
   Does not rewrite leftover-join.v8. Does not edit file 08.
   Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D241.
Does not unwrite D-086, D-145, D-196, D-218, or D-240.
