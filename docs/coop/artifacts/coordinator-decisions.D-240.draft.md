# D-240 — Record g23-leftover-join.v8 as G23 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g23-leftover-join.v8.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239. Not a
> three-limb act. Not a required-now successor. Not
> SATISFIED-GRADE.
> This is coordinator decision **D-240**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-101.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G23.
> **Does not** invent observation bytes.
> **Does not** invent a D-002 platform list.
> **Does not** copy onto Windows.
> **Does not** reopen leftover-design of NT-3 or NT-5.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v2.
> **Does not** rewrite corpus v4.
> **Does not** record frozen v4, v5, v6, or v7 as current.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-239 is ADOPTED at
`0c58fe1ed10d4e0c50f8d36290d7952e77bff4a4`.
HEAD is `0c58fe1ed10d4e0c50f8d36290d7952e77bff4a4`.
Last live heading is D-239. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g23-leftover-join.v8.review-independent.claude2.json` | `269d49e231f347e5220c6010e0f806737951ea2ecc2fef6b560dbd2f40c71a61` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g23-leftover-join.v8.review-independent.codex.json` | `a6809f658b9f78b5ab1fd32556c0227d3b8899c2a3734e1c697548c0e54a9f08` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g23-leftover-join.v8.json | `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` |
| g23-leftover-join.v8.review-independent.claude2.json | `269d49e231f347e5220c6010e0f806737951ea2ecc2fef6b560dbd2f40c71a61` |
| g23-leftover-join.v8.review-independent.codex.json | `a6809f658b9f78b5ab1fd32556c0227d3b8899c2a3734e1c697548c0e54a9f08` |
| COORDINATOR-DECISIONS.md | `49811b2c770a36c891adffc33653a79e87f32d50a10409457b98c23d63d4460f` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `0c58fe1ed10d4e0c50f8d36290d7952e77bff4a4` |
| Frozen leftover-join.v7 (D-238; not this subject) | `22a52b01a58a44e6162999d1b18bd76945086e3563724106ca05d62eeba90c5b` |
| Frozen corpus v4 (D-239; not this subject) | `b3fce9f5bab6764919f5dc43c28a43f3d9c3b6be310e45c2c1bd08a617c755c5` |
| Frozen occupancy v2 (D-223; not this subject) | `f48ba637bdf193785c05906a1686ce268b27b6ce7355de07fa5effefdd84fb0b` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v8, both Stage A verdicts, leftover-join v7, corpus v4,
occupancy v2, and this draft unmoved, remasure before
adoption. Append-only COORD after this remasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G23 lead
token remains `OPEN`; DR-133 remains `OPEN`. Naming parent
is D-147. Frozen v7 remains a historical measurement as of
D-238. Frozen v4, v5, and v6 remain historical. Do not
record v4, v5, v6, or v7 as current.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v8.
leftover-join.v7 (D-238) leftoverDesign remained
`[OBL-G23-FX-AUTHORING]` scoped to per-D-002-platform
copies. D-239 recorded those copies. v8 remasures that
leftover-design stale. leftoverDesign is `[]`. Remainder is
G23 execution. This entry records v8. It is not
SATISFIED-GRADE. It does not SATISFY DR-133. v4, v5, v6,
and v7 stay frozen; do not record them as current.

## Decision

1. Record
   `g23-leftover-join.v8.json`
   as G23 leftover remasurement after D-239. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v4, v5, v6, and v7 are
   not recorded as current.
2. DR-G23 stays `OPEN`. leftoverDesign is `[]`.
   leftover-design of the four D-237 implementations is
   stale as an authoring claim. leftover-design of
   per-D-002-platform copies is stale as an authoring claim
   after D-239. Host-refusal observation and
   subsequent-session view remain qualification at
   OBL-G23-EXECUTION (D-056). Does not pin QUALIFIED. Does
   not invent observation bytes. Does not invent a D-002
   platform list. Does not copy onto Windows. Does not
   reopen leftover-design of NT-3 or NT-5. Does not SATISFY
   DR-133. Does not SATISFY DR-117. Does not SATISFY
   DR-131. Does not SATISFY DR-101. Gate 1 Class A is not
   opened. Not SATISFIED. Required-now stays 28.
   Condition-4 effect is zero. Naming parent is D-147.
   Claude Stage A returned observations CLAUDE-G23LJ-V8-O1,
   CLAUDE-G23LJ-V8-O2, and CLAUDE-G23LJ-V8-O3. No change
   requested. Codex Stage A returned zero advisories and no
   observations. This entry names those Claude identifiers.
   It does not invent a Codex identifier. It does not claim
   that both reviewers' identifiers are preserved. Codex
   returned no observation identifiers. Does not execute
   G23. Does not rewrite occupancy v2. Does not rewrite
   corpus v4. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D240.
Does not unwrite D-147, D-223, D-237, D-238, or D-239.
