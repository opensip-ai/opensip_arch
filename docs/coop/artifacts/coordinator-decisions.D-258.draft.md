# D-258 — Record g12 leftover-join.v4 as G12 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-24
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g12-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249 and D-250 and
> D-251 and D-252 and D-253 and D-254 and D-255 and D-256
> and D-257. Not a three-limb act. Not a required-now
> successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-258**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-105.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-DOCTOR-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G12.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** steal OBL-JOIN-FX-AUTHORING,
> OBL-JOIN-FX-EXECUTION, OBL-FC-C1, or OBL-BLK-1..4.
> **Does not** take over G21.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v6.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record occupancy v4 as current occupancy.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-257 is ADOPTED at
`2b4e1fb1943c8df1f1da455f2f90062bd55a1d2e`.
HEAD is `2b4e1fb1943c8df1f1da455f2f90062bd55a1d2e`.
Last live heading is D-257. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g12-leftover-join.v4.review-independent.claude2.json` | `b40f29217a891627df5eca7ac2d58ccee84d1bac5117070bb875285d77867eb8` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g12-leftover-join.v4.review-independent.codex.json` | `5581d18f79e640075010f466b0d67e9afcb2d751b08783ab85bb4c7bb8ec9d5d` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v4 observationsNotFindings | none | four unlabeled objects, each an observation paired with a whyNotAFinding; no advisories named |
| Codex leftover-join.v4 observationsNotFindings | none | empty list; zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g12-leftover-join.v4.json | `60eed5d42ec4c52ed042d6c069abddbadf055cf97cf6c151c3d35952ee4a481c` |
| g12-leftover-join.v4.review-independent.claude2.json | `b40f29217a891627df5eca7ac2d58ccee84d1bac5117070bb875285d77867eb8` |
| g12-leftover-join.v4.review-independent.codex.json | `5581d18f79e640075010f466b0d67e9afcb2d751b08783ab85bb4c7bb8ec9d5d` |
| Frozen leftover-join.v3 (D-190; current G12 leftover-join at draft time; not this subject) | `11ebaf973b57ebf9d4b8da931ef0f66a0f299732c13a42e524d0f1f8a609a50a` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `0b68c98b5bb6fc07018a754e1dd5fd06120f3234e3460a84b14a69694deff93d` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `5c354f68ddce867764f84f0eeb3f88fcc31aa831fc3bc044eaf22a742b8cc9ac` |
| Frozen occupancy v6 (D-221; current G12 occupancy; not this subject) | `e6b72a9e0cc7053c991c51c510531c6ecd263bb895c70a3e9ab84bd6b6256735` |
| Frozen occupancy v4 (predecessor occupancy; not current; not this subject) | `6ad74892e5e9f48beba8d411d9c354613d08abb666a717a9b49fdd3aeab840c8` |
| Frozen doctor-actor leftover-join.v11 (D-170; current DR-114 ROW leftover-join; not this subject) | `3943a7bb2813324f1df0960b216fc2703139754283f72b3add307967caa0d950` |
| COORDINATOR-DECISIONS.md | `65caba56859e183df139caeaac1f74f127606ddfc2a1ee138c1c6c908011660b` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `2b4e1fb1943c8df1f1da455f2f90062bd55a1d2e` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4, occupancy v6, occupancy v4, doctor-actor
leftover-join.v11, both Stage A verdicts, and this draft
unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G12 lead
token remains `OPEN`; DR-114 remains `OPEN`. Naming parent is
naming v6 (D-145), not leftover-join.v4. D-086 named the
identifier. leftover-join.v4 is the G12 leftover-join under
review. leftover-join.v3 remains the current recorded G12
leftover-join at draft time (D-190). After this successor is
recorded, leftover-join.v3 is not current. Occupancy v6
remains the current G12 occupancy remasurement. Occupancy v4
is not current. doctor-actor leftover-join.v11 remains the
current DR-114 ROW leftover-join. leftoverDesign remains
`[OBL-DOCTOR-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v4
leftover remasurement after occupancy v6 (D-221). leftover-join.v3
cited occupancy v4 as the specification. Occupancy v6 remasured
that already-named identifier. leftoverDesign remains
`[OBL-DOCTOR-FX-AUTHORING]`. This entry records leftover-join.v4
(G12). It is not SATISFIED-GRADE. Frozen leftover-join.v3 stays
unmoved. leftover-join.v3 remains current at draft time. Do not
invent fixture bytes. Do not SATISFY DR-114.

## Decision

1. Record
   `g12-leftover-join.v4.json`
   as G12 leftover remasurement after D-257. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v4
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v3 remains
   current at draft time. After this successor is recorded,
   leftover-join.v3 is not current. Occupancy v6 is the current
   G12 occupancy remasurement. Occupancy v4 is not recorded as
   current occupancy.
2. DR-G12 stays `OPEN`. leftover-design of
   OBL-DOCTOR-FX-AUTHORING remains on leftover-join.v4.
   Remainder of G12 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a D9 code. Does not invent a section 7.1 recipe.
   Does not steal OBL-JOIN-FX-AUTHORING, OBL-JOIN-FX-EXECUTION,
   OBL-FC-C1, or OBL-BLK-1..4. Does not take over G21. Does not
   occupy the identifier. Does not SATISFY DR-114. Does not
   SATISFY DR-117. Does not SATISFY DR-131. Does not SATISFY
   DR-133. Does not SATISFY DR-105. Does not SATISFY DR-101.
   Gate 1 Class A is not opened. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Naming parent is
   naming v6 (D-145), not leftover-join.v4. D-086 named the
   identifier. Claude Stage A leftover-join.v4 returned four
   unlabeled observationsNotFindings objects, each an
   observation paired with a whyNotAFinding. They carry no
   identifiers. Codex Stage A leftover-join.v4 returned an
   empty observationsNotFindings list, zero advisories, and
   no observations. This entry does not invent identifiers
   and does not claim that both reviewers' identifiers are
   preserved. Claude Stage A returned no observation
   identifiers. Codex Stage A returned no observation
   identifiers. Does not execute G12. Does not rewrite
   occupancy v6. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D258.
Does not unwrite D-086, D-190, D-221, or D-257.
