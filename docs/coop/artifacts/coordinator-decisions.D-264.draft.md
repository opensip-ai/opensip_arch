# D-264 — Record g20 leftover-join.v4 as G20 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-24
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g20-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249 and D-250 and
> D-251 and D-252 and D-253 and D-254 and D-255 and D-256
> and D-257 and D-258 and D-259 and D-260 and D-261 and
> D-262 and D-263. Not a three-limb act. Not a required-now
> successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-264**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-125.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G20-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G20.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** invent reserved SDK APIs.
> **Does not** steal OBL-SDK-API-RESERVED.
> **Does not** close OBL-DR125-ACTIVATION.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v2.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record occupancy v1 as current occupancy.
> **Does not** record sdk leftover-join.v4 as current DR-125 leftover-join.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-263 is ADOPTED at
`b7d11873d34c5a2eb44734026742b5030803baea`.
HEAD is `b7d11873d34c5a2eb44734026742b5030803baea`.
Last live heading is D-263. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g20-leftover-join.v4.review-independent.claude2.json` | `859b0d965544fddb5a9918033b59a24b0bb85860fbd30c186f82f67f7ba9d07a` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g20-leftover-join.v4.review-independent.codex.json` | `5548f330e95a35cf70f9603cb78a9414a2d7d371085ffa297999304a59cb7802` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v4 advisories | ADV-1, ADV-2, ADV-3, ADV-4 | four named advisories; no observationsNotFindings field |
| Codex leftover-join.v4 observationsNotFindings | none | empty list; zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g20-leftover-join.v4.json | `9de955ea25b2e896f1fc31e2c7b10f507a99157acfa7711dbbbb844cd16b5ff2` |
| g20-leftover-join.v4.review-independent.claude2.json | `859b0d965544fddb5a9918033b59a24b0bb85860fbd30c186f82f67f7ba9d07a` |
| g20-leftover-join.v4.review-independent.codex.json | `5548f330e95a35cf70f9603cb78a9414a2d7d371085ffa297999304a59cb7802` |
| Frozen leftover-join.v3 (D-195; current G20 leftover-join at draft time; not this subject) | `1a04325f648b2cede73e932fb5083867dea4de57c1484b89ece8a983225f2617` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `2b54e9adfaebd9aa68c2071f9ea7d33f01bb3ba6a196248fb45492a09dd4acaa` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `0741dece8c2d103cb01ba7f9ce5c7512639c03fd08f87416ea7b81c1bdfb810e` |
| Frozen occupancy v2 (D-217; current G20 occupancy; not this subject) | `2c4823b7c5feb04afb739602397f81dc34333617c284bff21e82657fa289bb37` |
| Frozen occupancy v1 (predecessor occupancy; not current; not this subject) | `2f35a2e0b042788d2cf327393cb314d0d46e913dd20f49b992ba304298778055` |
| Frozen sdk leftover-join.v5 (D-184; current DR-125 leftover-join; not this subject) | `6f73376e93e7e84849ff6bc2de26c9fc88a53438ad2929dbe427b87f3125d187` |
| Frozen sdk leftover-join.v4 (predecessor DR-125 leftover-join; not current; not this subject) | `930e352765bf15f427ea33c7407349a7c36cc2d4b9f6d10d024cec14c46aac96` |
| COORDINATOR-DECISIONS.md | `95d305dd9993b26a0a32f163b26b2ad79307ea160aceb9812e2d0d24bb45883d` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `b7d11873d34c5a2eb44734026742b5030803baea` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4, occupancy v2, occupancy v1, sdk leftover-join.v5,
sdk leftover-join.v4, both Stage A verdicts, and this draft
unmoved, remasure before adoption. Append-only COORD after
this remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G20 lead
token remains `OPEN`; DR-125 remains `OPEN`. Naming parent
is naming v6 (D-145), not leftover-join.v4. D-086 named the
identifier. leftover-join.v4 is the G20 leftover-join under
review. leftover-join.v3 remains the current recorded G20
leftover-join at draft time (D-195). After this successor is
recorded, leftover-join.v3 is not current. Occupancy v2
remains the current G20 occupancy remasurement. Occupancy v1
is not current. sdk leftover-join.v5 remains the current
DR-125 leftover-join. leftoverDesign remains
`[OBL-G20-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v4
leftover remasurement after occupancy v2 (D-217). leftover-join.v3
cited occupancy v1 as the specification. Occupancy v2 remasured
that already-named identifier. leftoverDesign remains
`[OBL-G20-FX-AUTHORING]`. This entry records leftover-join.v4
(G20). It is not SATISFIED-GRADE. Frozen leftover-join.v3
stays unmoved. leftover-join.v3 remains current at draft
time. Do not invent fixture bytes. Do not SATISFY DR-125.

## Decision

1. Record
   `g20-leftover-join.v4.json`
   as G20 leftover remasurement after D-263. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v4
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v3 remains
   current at draft time. After this successor is recorded,
   leftover-join.v3 is not current. Occupancy v2 is the current
   G20 occupancy remasurement. Occupancy v1 is not recorded as
   current occupancy. sdk leftover-join.v5 remains the current
   DR-125 leftover-join. sdk leftover-join.v4 is not recorded as
   current DR-125 leftover-join.
2. DR-G20 stays `OPEN`. leftover-design of
   OBL-G20-FX-AUTHORING remains on leftover-join.v4.
   Remainder of G20 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a D9 code. Does not invent a section 7.1 recipe.
   Does not invent reserved SDK APIs. Does not steal
   OBL-SDK-API-RESERVED. Does not close OBL-DR125-ACTIVATION.
   Does not occupy the identifier. Does not SATISFY DR-125.
   Does not SATISFY DR-117. Does not SATISFY DR-131. Does not
   SATISFY DR-133. Does not SATISFY DR-114. Does not SATISFY
   DR-101. Gate 1 Class A is not opened. Not SATISFIED.
   Required-now stays 28. Condition-4 effect is zero. Naming
   parent is naming v6 (D-145), not leftover-join.v4. D-086
   named the identifier. Claude Stage A leftover-join.v4
   returned four named advisories ADV-1, ADV-2, ADV-3, and
   ADV-4. No change requested. They carry those identifiers.
   Codex Stage A leftover-join.v4 returned an empty
   observationsNotFindings list, zero advisories, and no
   observations. This entry names those Claude identifiers.
   It does not invent a Codex identifier. It does not claim
   that both reviewers' identifiers are preserved. Codex
   Stage A returned no observation identifiers. Does not
   execute G20. Does not rewrite occupancy v2. Does not edit
   file 08. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D264.
Does not unwrite D-086, D-195, D-217, or D-263.
