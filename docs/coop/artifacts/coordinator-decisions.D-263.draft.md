# D-263 — Record g18 leftover-join.v5 as G18 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-24
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g18-leftover-join.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249 and D-250 and
> D-251 and D-252 and D-253 and D-254 and D-255 and D-256
> and D-257 and D-258 and D-259 and D-260 and D-261 and
> D-262. Not a three-limb act. Not a required-now successor.
> Not SATISFIED-GRADE.
> This is coordinator decision **D-263**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-107.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G18-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G18.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** invent a journal.
> **Does not** steal OBL-ENCODING-RESERVED.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v4.
> **Does not** record leftover-join.v4 as current after this successor is recorded.
> **Does not** record occupancy v2 as current occupancy.
> **Does not** record lifecycle leftover-join.v2 as current DR-107 leftover-join.
> **Does not** flatten DR-107 `PROPOSED-CLOSED-FOR-REVIEW` to `OPEN`.
> **Does not** re-land CLAUDE-G18LJ-V2-SF1.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-262 is ADOPTED at
`0f718aa57a99a280bff3a0665d20981db4bad235`.
HEAD is `0f718aa57a99a280bff3a0665d20981db4bad235`.
Last live heading is D-262. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g18-leftover-join.v5.review-independent.claude2.json` | `1d00171ff3ebbfe2de8d831792e36613b6664cde23da111b75a52d061823a4dd` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g18-leftover-join.v5.review-independent.codex.json` | `70584f28506b5cb38d583f59d3ad8b80ad5a7dab97a1219d009e767aa1a4279b` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v5 | none | no observationsNotFindings field; no advisories named |
| Codex leftover-join.v5 observationsNotFindings | none | empty list; zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g18-leftover-join.v5.json | `3d9aa52369c53d4a22667bf7616afe0bb2c6da2af4d22ed6a6b9f10ac1073c8a` |
| g18-leftover-join.v5.review-independent.claude2.json | `1d00171ff3ebbfe2de8d831792e36613b6664cde23da111b75a52d061823a4dd` |
| g18-leftover-join.v5.review-independent.codex.json | `70584f28506b5cb38d583f59d3ad8b80ad5a7dab97a1219d009e767aa1a4279b` |
| Frozen leftover-join.v4 (D-193; current G18 leftover-join at draft time; not this subject) | `f18f08bcb360a68b76e08330b716129a69193a3d91a8e2623f0a396ecba33228` |
| Frozen leftover-join.v3 (historical; not current; not this subject) | `fa24a22d4967575fa8d2eb77f7525947a4c83da467b217564974fe8220e53010` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `189e73191ee4c7b8016211621a9bcf977870662bc77d833d11010355e1ef562b` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `f79711ccd7e8a53086e5099b43b72d727990e6758ca6372c08738d18d72daff9` |
| Frozen occupancy v4 (D-216; current G18 occupancy; not this subject) | `2ce9aa522bf014af27b088d3bd50885a271e5e321ba6c372af527552cb6660cc` |
| Frozen occupancy v2 (predecessor occupancy; not current; not this subject) | `5a762661b0c91ac6dc54015fa3803e66eca2dce111030a57931f6748ee50a462` |
| Frozen lifecycle leftover-join.v3 (D-176; current DR-107 leftover-join; not this subject) | `9ca8bdb03af8e6e00f970364e5a1958f0fe88dcd12f0f8948d0d29069dd7042d` |
| Frozen lifecycle leftover-join.v2 (predecessor DR-107 leftover-join; not current; not this subject) | `ae27ed0a5d824fe131976069f12f87828862d540ad36168831fb5dcc9ce6e2dd` |
| COORDINATOR-DECISIONS.md | `a9b8328a8f3f33b5144c8430fb4ccf5519caa79b3b7306bc01e14f4fe05fa385` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `0f718aa57a99a280bff3a0665d20981db4bad235` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v4, leftover-join.v5, occupancy v4, occupancy v2, lifecycle
leftover-join.v3, lifecycle leftover-join.v2, both Stage A
verdicts, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G18 lead
token remains `OPEN`; DR-107 remains
`PROPOSED-CLOSED-FOR-REVIEW`. Naming parent is naming v6
(D-145), not leftover-join.v5. D-086 named the identifier.
leftover-join.v5 is the G18 leftover-join under review.
leftover-join.v4 remains the current recorded G18 leftover-join
at draft time (D-193). After this successor is recorded,
leftover-join.v4 is not current. Occupancy v4 remains the
current G18 occupancy remasurement. Occupancy v2 is not
current. lifecycle leftover-join.v3 remains the current
DR-107 leftover-join. leftoverDesign remains
`[OBL-G18-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v5
leftover remasurement after occupancy v4 (D-216). leftover-join.v4
cited occupancy v2 as the specification. Occupancy v4 remasured
that already-named identifier. leftoverDesign remains
`[OBL-G18-FX-AUTHORING]`. This entry records leftover-join.v5
(G18). It is not SATISFIED-GRADE. Frozen leftover-join.v4
stays unmoved. leftover-join.v4 remains current at draft
time. Live remasurement recites DR-107 as
`PROPOSED-CLOSED-FOR-REVIEW`, not `OPEN`. Do not invent
fixture bytes. Do not SATISFY DR-107. Do not re-land
CLAUDE-G18LJ-V2-SF1.

## Decision

1. Record
   `g18-leftover-join.v5.json`
   as G18 leftover remasurement after D-262. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v5
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v4 remains
   current at draft time. After this successor is recorded,
   leftover-join.v4 is not current. Occupancy v4 is the current
   G18 occupancy remasurement. Occupancy v2 is not recorded as
   current occupancy. lifecycle leftover-join.v3 remains the
   current DR-107 leftover-join. lifecycle leftover-join.v2 is
   not recorded as current DR-107 leftover-join.
2. DR-G18 stays `OPEN`. leftover-design of
   OBL-G18-FX-AUTHORING remains on leftover-join.v5.
   Remainder of G18 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a D9 code. Does not invent a section 7.1 recipe.
   Does not invent a journal. Does not steal
   OBL-ENCODING-RESERVED. Does not occupy the identifier. Does
   not SATISFY DR-107. Live remasurement recites DR-107 as
   `PROPOSED-CLOSED-FOR-REVIEW`, not `OPEN`. Does not SATISFY
   DR-117. Does not SATISFY DR-131. Does not SATISFY DR-133.
   Does not SATISFY DR-114. Does not SATISFY DR-101. Gate 1
   Class A is not opened. Not SATISFIED. Required-now stays
   28. Condition-4 effect is zero. Naming parent is naming
   v6 (D-145), not leftover-join.v5. D-086 named the
   identifier. Claude Stage A leftover-join.v5 returned no
   observationsNotFindings field and no advisories. Codex
   Stage A leftover-join.v5 returned an empty
   observationsNotFindings list, zero advisories, and no
   observations. This entry does not invent identifiers and
   does not claim that both reviewers' identifiers are
   preserved. Claude Stage A returned no observation
   identifiers. Codex Stage A returned no observation
   identifiers. CLAUDE-G18LJ-V2-SF1 already landed in this
   lineage at leftover-join.v4. This entry does not re-land
   it. Does not execute G18. Does not rewrite occupancy v4.
   Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D263.
Does not unwrite D-086, D-193, D-216, or D-262.
