# D-253 — Record g28 leftover-join.v4 as G28 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g28-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249 and D-250 and
> D-251 and D-252. Not a three-limb act. Not a required-now
> successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-253**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G28-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G28.
> **Does not** invent fixture bytes.
> **Does not** invent a D9 code, exit, or HostTermination.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** reopen leftover-design of NT-7 or NT-8.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v4.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record occupancy v3 as current occupancy.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-252 is ADOPTED at
`13395db621abdbb6191526cac9147d49e31b8327`.
HEAD is `13395db621abdbb6191526cac9147d49e31b8327`.
Last live heading is D-252. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g28-leftover-join.v4.review-independent.claude2.json` | `1e58abe49f630cb59a185209673002b442be3546c7d304707d6d763a4937c90a` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g28-leftover-join.v4.review-independent.codex.json` | `070fce7410a8721125b1e0906284a0cd6f88a84e282dbfd5b30b6155ec852c4d` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v4 | none | no observationsNotFindings field; no advisories named |
| Codex leftover-join.v4 observationsNotFindings | none | empty list; zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g28-leftover-join.v4.json | `604dc98dfc4fd6ec2df1c22f2169b5ec921f2f43ab43ef7e0c98b48750dee085` |
| g28-leftover-join.v4.review-independent.claude2.json | `1e58abe49f630cb59a185209673002b442be3546c7d304707d6d763a4937c90a` |
| g28-leftover-join.v4.review-independent.codex.json | `070fce7410a8721125b1e0906284a0cd6f88a84e282dbfd5b30b6155ec852c4d` |
| Frozen leftover-join.v3 (D-203; current G28 leftover-join at draft time; not this subject) | `14f1c34b86245bdf659b0c8e6ef6946a63675dcca2a32febcb00ca214df6d51c` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `94d15934b0bc6d5ea6b7d4643b3e6d2c4af169badd82c389636b7adc534cf958` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `b13389757160deeba10d2c928d515539b13139ca93c74df560af7f7f5902dd30` |
| Frozen occupancy v4 (D-228; current G28 occupancy; not this subject) | `e540ea53b8cfd4e75c05eabfb4c321dca566161b135dc630c2bd1fec5d31ff4d` |
| Frozen occupancy v3 (predecessor occupancy; not current; not this subject) | `d2cceb9f83696ab78618385d7ebb592e16136f562250fa238653e195ad77e41c` |
| COORDINATOR-DECISIONS.md | `c69601f9acda990cc191b704fff4405b7bd2a1744228c5216f06f91d7c7e1ed2` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `13395db621abdbb6191526cac9147d49e31b8327` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4, occupancy v4, occupancy v3, both Stage A
verdicts, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G28 lead
token remains `OPEN`; DR-131 remains `OPEN`. Naming parent is
D-154, not leftover-join.v4. leftover-join.v4 is the G28
leftover-join under review. leftover-join.v3 remains the
current recorded G28 leftover-join at draft time (D-203).
After this successor is recorded, leftover-join.v3 is not
current. Occupancy v4 remains the current G28 occupancy
remasurement. Occupancy v3 is not current. leftoverDesign
remains `[OBL-G28-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v4
leftover remasurement after occupancy v4 (D-228). leftover-join.v3
cited occupancy v3 as the specification. Occupancy v4 remasured
that already-named identifier. leftoverDesign remains
`[OBL-G28-FX-AUTHORING]`. This entry records leftover-join.v4
(G28). It is not SATISFIED-GRADE. Frozen leftover-join.v3 stays
unmoved. leftover-join.v3 remains current at draft time. Do not
invent fixture bytes. Do not invent a D9 code, exit, or
HostTermination. Do not SATISFY DR-131.

## Decision

1. Record
   `g28-leftover-join.v4.json`
   as G28 leftover remasurement after D-252. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v4
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v3 remains
   current at draft time. After this successor is recorded,
   leftover-join.v3 is not current. Occupancy v3 is not recorded
   as current occupancy.
2. DR-G28 stays `OPEN`. leftover-design of
   OBL-G28-FX-AUTHORING remains on leftover-join.v4.
   Remainder of G28 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a D9 code, exit, or HostTermination. Does not
   invent a section 7.1 recipe. Does not reopen leftover-design
   of NT-7 or NT-8. Does not occupy the identifier. Does not
   SATISFY DR-131. Does not SATISFY DR-133. Does not SATISFY
   DR-117. Does not SATISFY DR-114. Does not SATISFY DR-101.
   Gate 1 Class A is not opened. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Naming parent is
   D-154, not leftover-join.v4. naming v6 does not name G28.
   Claude Stage A leftover-join.v4 returned no
   observationsNotFindings field and no advisories. Codex
   Stage A leftover-join.v4 returned an empty
   observationsNotFindings list, zero advisories, and no
   observations. This entry does not invent identifiers and
   does not claim that both reviewers' identifiers are
   preserved. Claude Stage A returned no observation
   identifiers. Codex Stage A returned no observation
   identifiers. Does not execute G28. Does not rewrite
   occupancy v4. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D253.
Does not unwrite D-154, D-203, D-228, or D-252.
