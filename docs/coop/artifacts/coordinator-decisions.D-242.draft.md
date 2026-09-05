# D-242 — Record g21-leftover-join.v7 as G21 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g21-leftover-join.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241. Not a three-limb act. Not a required-now
> successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-242**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-101.
> **Does not** reopen DR-102 SATISFIED.
> **Does not** close leftover-design of OBL-G21-FX-AUTHORING.
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
> **Does not** author per-D-002-platform copies.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v4.
> **Does not** rewrite corpus v1.
> **Does not** record leftover-join.v4, v5, or v6 as current.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-241 is ADOPTED at
`e6d26a73e13d85caf13bb3ca61c09a6e5c64da67`.
HEAD is `e6d26a73e13d85caf13bb3ca61c09a6e5c64da67`.
Last live heading is D-241. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g21-leftover-join.v7.review-independent.claude2.json` | `15710285e149c89e8fa9a01396a893769555dab41b283d66954dc278033741cd` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g21-leftover-join.v7.review-independent.codex.json` | `2b15089ad1ed9bddbdef7c5fdce612bbd77884d13412c2ee8f3d29e0ce48ec33` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude Stage A observationsNotFindings[0] | none | unlabeled object; no change requested |
| Claude Stage A observationsNotFindings[1] | none | unlabeled object; no change requested |
| Claude Stage A observationsNotFindings[2] | none | unlabeled object; no change requested |
| Claude Stage A observationsNotFindings[3] | none | unlabeled object; no change requested |
| Claude Stage A observationsNotFindings[4] | none | unlabeled object; no change requested |
| Codex Stage A | none | zero advisories; no observations |

Measured inputs:

| Path | sha256 |
|---|---|
| g21-leftover-join.v7.json | `5a48c4626c44c4016390dc5868754da136715b72c76c5de09b89e49aad76eb04` |
| g21-leftover-join.v7.review-independent.claude2.json | `15710285e149c89e8fa9a01396a893769555dab41b283d66954dc278033741cd` |
| g21-leftover-join.v7.review-independent.codex.json | `2b15089ad1ed9bddbdef7c5fdce612bbd77884d13412c2ee8f3d29e0ce48ec33` |
| Frozen leftover-join.v6 (split; not this subject) | `edc2d0594bc7719689ca129f0df8fa9dc6f73ed33f0af33cc3143b2624868717` |
| Frozen leftover-join.v5 (split; not this subject) | `92112261207071deec9660b1c854b1096cc8ee510e438ce642e76fd1102c7d1b` |
| Frozen leftover-join.v4 (D-196; not this subject) | `b8696fd134550a9ad15d44a07adcc4030aad3702013cc9de914bbab5b8e74ae4` |
| Frozen corpus v1 (D-241; not this subject) | `861bb4e7d26a80158cc1cc3a0518c5e8e95311bee4d8c8ce63acd1e60d6c906d` |
| Frozen occupancy v4 (D-218; not this subject) | `13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b` |
| fixtures/g21.v1 NT-1 (not this subject) | `b9ff9338d6a8a13142ed073e2543c48cd7790e38df8585ee90e130b212151c8c` |
| fixtures/g21.v1 NT-2 (not this subject) | `bc264fc7d0cad17bd269be42cd5f06579c2a50340d68d3abbe19c895b4b06dc8` |
| COORDINATOR-DECISIONS.md | `c8472832ecbe70714ccef576d54d4f5fb8a1044b643eb929a8896a002dd71eda` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `e6d26a73e13d85caf13bb3ca61c09a6e5c64da67` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v7, both Stage A verdicts, leftover-join v4/v5/v6, occupancy
v4, corpus v1, the two v1 fixture files, and this draft
unmoved, remasure before adoption. Append-only COORD after
this remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G21 lead
token remains `OPEN`; DR-114 remains `OPEN`; DR-133 remains
`OPEN`. Naming parent is D-145 / naming v6, not
leftover-join.v4. leftover-join.v4, v5, and v6 are not
current. leftover-join.v5 and leftover-join.v6 are split
predecessors, not Dual REJECT. Do not record leftover-join.v7
leftoverDesign as other than `[OBL-G21-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of v7 leftover
remasurement of G21 after D-241. leftover-design of NT-1
and NT-2 implementations is stale as an authoring claim.
leftover-design of per-D-002-platform copies of those
implementations remains. Remaining G21 classes stay
unauthored. leftoverDesign remains
`[OBL-G21-FX-AUTHORING]`. This entry records v7. It is not
SATISFIED-GRADE. It does not close leftover-design of
OBL-G21-FX-AUTHORING. It does not invent a D-002 platform
list. Frozen v4 remains D-196. Frozen v5 and v6 remain
split. Do not record v4, v5, or v6 as current.

## Decision

1. Record
   `g21-leftover-join.v7.json`
   as G21 leftover remasurement after D-241. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v4, v5, and v6 are not
   recorded as current.
2. DR-G21 stays `OPEN`. leftoverDesign remains
   `[OBL-G21-FX-AUTHORING]`. leftover-design of NT-1 and
   NT-2 implementations is stale as an authoring claim.
   leftover-design of per-D-002-platform copies of those
   implementations remains. Remaining G21 classes stay
   unauthored. Remainder of G21 execution, including
   candidate-buffer digest, subsequent-session view, and
   host-projection goldens, remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent a D-002 platform
   list. Does not author those copies. Does not invent a
   finding schema. Does not invent a D9 code, exit number,
   or HostTermination. Does not invent a pack IR. Does not
   invent a section 7.1 recipe. Does not author NT-6. Does
   not take over G23. Does not reopen DR-102 SATISFIED.
   Does not SATISFY DR-114. Does not SATISFY DR-133. Does
   not SATISFY DR-117. Does not SATISFY DR-131. Does not
   SATISFY DR-101. Gate 1 Class A is not opened. Not
   SATISFIED. Required-now stays 28. Condition-4 effect is
   zero. Naming parent is D-145 / naming v6, not
   leftover-join.v4. Claude Stage A returned five unlabeled
   observationsNotFindings objects, each an observation
   paired with a whyNotAFinding. They carry no identifiers.
   Codex Stage A returned zero advisories and no
   observations. This entry does not invent identifiers
   for those observations and does not claim that both
   reviewers' identifiers are preserved. Codex returned no
   observation identifiers. Does not execute G21. Does not
   rewrite occupancy v4. Does not rewrite corpus v1. Does
   not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D242.
Does not unwrite D-086, D-145, D-196, D-218, or D-241.
