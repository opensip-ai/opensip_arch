# D-254 — Record g29 leftover-join.v4 as G29 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-24
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g29-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249 and D-250 and
> D-251 and D-252 and D-253. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-254**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G29-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G29.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** reopen leftover-design of EE-1 through EE-6a.
> **Does not** take over G21, G23, G24, or G30.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v3.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record occupancy v2 as current occupancy.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-253 is ADOPTED at
`cbe471bfc0de4b49791d40c9d795b57dbb2a298c`.
HEAD is `cbe471bfc0de4b49791d40c9d795b57dbb2a298c`.
Last live heading is D-253. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g29-leftover-join.v4.review-independent.claude2.json` | `9c900fe4294b154c3b81c3d2df66676fe8ea22bfd975513f6f9016cfdb4d731a` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g29-leftover-join.v4.review-independent.codex.json` | `39e4509b542588b15f3fe2bdc4be028a15b75c3fac73a1b21b82c49e9b3b53f4` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v4 | none | no observationsNotFindings field; no advisories named; one unlabeled disclosure in attacksNotChargedWithDisclosure, not a finding |
| Codex leftover-join.v4 observationsNotFindings | none | empty list; zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g29-leftover-join.v4.json | `9e1af4ba3b21e483154825fa2c6d275f7ee805d1fb455f01c9d35e48411c3f64` |
| g29-leftover-join.v4.review-independent.claude2.json | `9c900fe4294b154c3b81c3d2df66676fe8ea22bfd975513f6f9016cfdb4d731a` |
| g29-leftover-join.v4.review-independent.codex.json | `39e4509b542588b15f3fe2bdc4be028a15b75c3fac73a1b21b82c49e9b3b53f4` |
| Frozen leftover-join.v3 (D-204; current G29 leftover-join at draft time; not this subject) | `4ab44caebced258a4ba2ef795879bf3afc9427cb5ae547c1138bf1c0e9f7ec5f` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `a757e718d8cd1c3d530a71e4f23ad57c80d6e833071f56a42b0f6cac355c6302` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `163fd2280ec3898dcc7db3d6ea233bd7203424a5c43f2a5e63854e7b05c098bb` |
| Frozen occupancy v3 (D-229; current G29 occupancy; not this subject) | `94a40de95097afbf51e50461bac54f5fc95326215cf94e89a2f3655c731be96d` |
| Frozen occupancy v2 (predecessor occupancy; not current; not this subject) | `e9f17dbbef3ace3f97171bf750fd10816174b7a363395e910677a07a33dfa232` |
| COORDINATOR-DECISIONS.md | `3219c6ba0e510ac0a00402272f02d4518f645ce5744c9f81c5fa774b217ad098` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `cbe471bfc0de4b49791d40c9d795b57dbb2a298c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4, occupancy v3, occupancy v2, both Stage A
verdicts, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G29 lead
token remains `OPEN`; DR-117 remains `OPEN`. Naming parent is
D-157, not leftover-join.v4. leftover-join.v4 is the G29
leftover-join under review. leftover-join.v3 remains the
current recorded G29 leftover-join at draft time (D-204).
After this successor is recorded, leftover-join.v3 is not
current. Occupancy v3 remains the current G29 occupancy
remasurement. Occupancy v2 is not current. leftoverDesign
remains `[OBL-G29-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v4
leftover remasurement after occupancy v3 (D-229). leftover-join.v3
cited occupancy v2 as the specification. Occupancy v3 remasured
that already-named identifier. leftoverDesign remains
`[OBL-G29-FX-AUTHORING]`. This entry records leftover-join.v4
(G29). It is not SATISFIED-GRADE. Frozen leftover-join.v3 stays
unmoved. leftover-join.v3 remains current at draft time. Do not
invent fixture bytes. Do not SATISFY DR-117.

## Decision

1. Record
   `g29-leftover-join.v4.json`
   as G29 leftover remasurement after D-253. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v4
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v3 remains
   current at draft time. After this successor is recorded,
   leftover-join.v3 is not current. Occupancy v2 is not recorded
   as current occupancy.
2. DR-G29 stays `OPEN`. leftover-design of
   OBL-G29-FX-AUTHORING remains on leftover-join.v4.
   Remainder of G29 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a D9 code. Does not invent a section 7.1 recipe.
   Does not reopen leftover-design of EE-1 through EE-6a. Does
   not take over G21, G23, G24, or G30. Does not occupy the
   identifier. Does not SATISFY DR-117. Does not SATISFY
   DR-131. Does not SATISFY DR-133. Does not SATISFY DR-114.
   Does not SATISFY DR-101. Gate 1 Class A is not opened.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Naming parent is D-157, not leftover-join.v4.
   naming v6 does not name G29. Claude Stage A leftover-join.v4
   returned no observationsNotFindings field and no
   advisories. Codex Stage A leftover-join.v4 returned an
   empty observationsNotFindings list, zero advisories, and
   no observations. This entry does not invent identifiers
   and does not claim that both reviewers' identifiers are
   preserved. Claude Stage A returned no observation
   identifiers. Codex Stage A returned no observation
   identifiers. Does not execute G29. Does not rewrite
   occupancy v3. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D254.
Does not unwrite D-157, D-204, D-229, or D-253.
