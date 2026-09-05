# D-238 — Record g23-leftover-join.v7 as G23 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Frozen
> turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g23-leftover-join.v7.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-238**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G23-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G23.
> **Does not** invent fixture bytes, observation bytes,
> per-platform copies, or a D-002 platform list.
> **Does not** reopen leftover-design of NT-3 or NT-5.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v2.
> **Does not** rewrite corpus v3.
> **Does not** record frozen v4, v5, or v6 as current.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

Turn-1 subject `coordinator-decisions.D-238.draft.md`
`128488c62f75a1f99843c02eedc708a4ae3e685cd130245ccd50b7cae5c5899c`
held frozen. Claude 2 OBJECT, 1 MUST-FIX CLAUDE-D238-M1.
Codex OBJECT, 1 SHOULD-FIX D238-SF-1.

| ID | Sev | Disposition |
|---|---|---|
| CLAUDE-D238-M1 | MUST-FIX | ACCEPTED. Decision-type limb now says the no-cell-edit branch is D-170 through D-235 and D-237. The range does not span D-236. |
| D238-SF-1 | SHOULD-FIX | ACCEPTED. Same repair as CLAUDE-D238-M1. Shared class; both identifiers are preserved. |
| CLAUDE-D238-O1 | OBSERVATION | EXAMINED. remasurement clause omits occupancy v2; no change requested. Codex returned no counterpart identifier. This entry does not invent one. |

D-237 is ADOPTED at
`0a814f9fdf7abc206fd172f7b1ecc11ba35ed116`.
HEAD is `0a814f9fdf7abc206fd172f7b1ecc11ba35ed116`.
Last live heading is D-237. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g23-leftover-join.v7.review-independent.claude2.json` | `14817c408761d3c6c8e537431c654d55a92e6674e7881352fca9af6d7000452b` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g23-leftover-join.v7.review-independent.codex.json` | `5e1bd98eaf5d11688a61963907afb927f71cea36527614e37227056c8cb216b8` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g23-leftover-join.v7.json | `22a52b01a58a44e6162999d1b18bd76945086e3563724106ca05d62eeba90c5b` |
| g23-leftover-join.v7.review-independent.claude2.json | `14817c408761d3c6c8e537431c654d55a92e6674e7881352fca9af6d7000452b` |
| g23-leftover-join.v7.review-independent.codex.json | `5e1bd98eaf5d11688a61963907afb927f71cea36527614e37227056c8cb216b8` |
| COORDINATOR-DECISIONS.md | `5a06c1c95031d4aaeea150228e8e8f11d2cdfab24b8ee93bbe8b9ad99ab0e66b` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `0a814f9fdf7abc206fd172f7b1ecc11ba35ed116` |
| Frozen v6 (split; not this subject) | `5ce314b7bc526376b5995d492c31427be75e037302feb775650f46e519dec887` |
| Frozen v5 (split; not this subject) | `d7a8daf64f8179843068f44b11c0299558ad381b33baec75eb97de9ae1247f08` |
| Frozen v4 (historical D-198; not this subject) | `a542dc6b023d07cf8657c76909ded1641efd29277760308d52574fa706fad56e` |
| Frozen corpus v3 (D-237; not this subject) | `3576e2e606b3eed68feced5b83a34247263d3b563274ef3fd9054c8b2a2ba6a7` |
| Turn-1 subject | `128488c62f75a1f99843c02eedc708a4ae3e685cd130245ccd50b7cae5c5899c` |
| Claude 2 turn 1 | `4f78b0e00ec3a2a1966a829551c0a35d3535de66410180cb46dc4fcd769a4f0a` |
| Codex turn 1 | `3b34bd4464e2823a5bb3d367ffa5e761a6e85963730f157b3a12327090f39266` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v7, both Stage A verdicts, frozen v4, frozen v5, frozen v6,
corpus v3, frozen turn-1 subject, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G23 lead
token remains `OPEN`; DR-133 remains `OPEN`. Naming parent
is D-147. Frozen v4 remains a historical measurement as of
D-198. Frozen v5 remains a historical split (Codex REJECT
G23LJ-V5-M1/S1; Claude ACCEPT 0/0). Frozen v6 remains a
historical split (Codex ACCEPT 0/0; Claude REJECT
CLAUDE-G23LJ-V6-M1/S1). Do not record v4, v5, or v6 as
current.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v7.
v5 and v6 are frozen historical splits. leftover-join.v4
(D-198) is not recordable as the current leftover
remasurement after D-237 recorded corpus v3. v7 remasures
leftover-design of OBL-G23-FX-AUTHORING against those four
implementations and occupancy v2: leftover-design of the
four implementations is stale; leftover-design of
per-D-002-platform copies remains; host-refusal observation
and subsequent-session view ride G23 execution. This entry
records v7. It is not SATISFIED-GRADE. It does not close
leftover-design of OBL-G23-FX-AUTHORING. v4, v5, and v6 stay
frozen; do not record them as current.

## Decision

1. Record
   `g23-leftover-join.v7.json`
   as G23 leftover remasurement after D-237. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v4, v5, and v6 are not
   recorded as current.
2. DR-G23 stays `OPEN`. leftoverDesign remains
   `[OBL-G23-FX-AUTHORING]`, scoped to per-D-002-platform
   copies of the four D-237 implementations. leftover-design
   of those four implementations is stale as an authoring
   claim. Host-refusal observation and subsequent-session
   view remain qualification at OBL-G23-EXECUTION (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes,
   observation bytes, per-platform copies, or a D-002
   platform list. Does not reopen leftover-design of NT-3
   or NT-5. Does not SATISFY DR-133. Does not SATISFY
   DR-117. Does not SATISFY DR-131. Does not SATISFY DR-101.
   Gate 1 Class A is not opened. Not SATISFIED.
   Required-now stays 28. Condition-4 effect is zero.
   Naming parent is D-147. Claude Stage A returned
   observation CLAUDE-G23LJ-V7-O1: `namedCorpusNotAuthored`
   stays `[]` on OBL-G23-FX-AUTHORING; no change requested.
   Codex Stage A returned zero advisories and no
   observations. This entry names CLAUDE-G23LJ-V7-O1. It
   does not invent a Codex identifier. It does not claim
   that both reviewers' identifiers are preserved. Codex
   returned no observation identifiers. Does not execute
   G23. Does not rewrite occupancy v2. Does not rewrite
   corpus v3. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D238.
Does not unwrite D-147, D-198, D-223, D-236, or D-237.
