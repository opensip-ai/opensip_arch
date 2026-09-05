# D-246 — Record g21-leftover-join.v11 as G21 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands D246-S1 and CODEX-D246-SF1.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g21-leftover-join.v11.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245.
> Not a three-limb act. Not a required-now successor. Not
> SATISFIED-GRADE.
> This is coordinator decision **D-246**, not a register
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
> **Does not** author remaining G21 classes.
> **Does not** claim CC-5 fully authored.
> **Does not** author remaining CC-5 injections.
> **Does not** author per-D-002-platform copies of the two
> CC-5 payloads.
> **Does not** take over G23.
> **Does not** invent a finding schema.
> **Does not** invent a D9 code, exit number, or HostTermination.
> **Does not** invent a pack IR.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent a D-002 platform list.
> **Does not** invent observation bytes.
> **Does not** invent a ping body schema.
> **Does not** invent 26214400.
> **Does not** classify non-object top level as CC-5.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v4.
> **Does not** rewrite corpus v1, corpus v2, or corpus v7.
> **Does not** record leftover-join.v4 through v10 as current.
> **Does not** record g21-fixture-corpus.v3 through v6 as current.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-245 is ADOPTED at
`e160bc44ef9f4c9c6b1620e69adda7d489b9ee5f`.
HEAD is `e160bc44ef9f4c9c6b1620e69adda7d489b9ee5f`.
Last live heading is D-245. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g21-leftover-join.v11.review-independent.claude2.json` | `2e45c8ff487421a3ffdea7098fddf7d52da8aae1e83e647c12932d2ba2729856` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g21-leftover-join.v11.review-independent.codex.json` | `f52f947df1bb90013fcc6d546a057225527cd81828d921423d876c0ea0e930fb` | ACCEPT 0/0 |

Stage A observation disposition (no change requested):

| Source | Identifier | Standing |
|---|---|---|
| Claude Stage A | none | no observationsNotFindings field; no advisories named |
| Codex Stage A observations[0] | G21LJ-V11-OBS-1 | object with keys id, observation, and whyNotShouldFix; no change requested |

Measured inputs:

| Path | sha256 |
|---|---|
| g21-leftover-join.v11.json | `ea8d2c52723a46eef3388b93e2a529a5af999d24363a695719d6d7a1bd08224f` |
| g21-leftover-join.v11.review-independent.claude2.json | `2e45c8ff487421a3ffdea7098fddf7d52da8aae1e83e647c12932d2ba2729856` |
| g21-leftover-join.v11.review-independent.codex.json | `f52f947df1bb90013fcc6d546a057225527cd81828d921423d876c0ea0e930fb` |
| Frozen leftover-join.v10 (split G21LJ-V10-SF1; not this subject) | `4b6ca55328a1198a1cb60e2285d1862365ed4029aaa6a81bd75e18e724ca561a` |
| Frozen leftover-join.v9 (D-244; not this subject) | `d0fda8926b5f2e494d1b7c1f3ec716ded3d58ef3b9c498f73d0a3220f893a4de` |
| Frozen leftover-join.v8 (dual REJECT G21LJ-V8-SF1; not this subject) | `fe2a4eff1e143a33addf3f07f7142aa7c2541c8baec644033e7556d64ec6d0e4` |
| Frozen leftover-join.v7 (D-242; not this subject) | `5a48c4626c44c4016390dc5868754da136715b72c76c5de09b89e49aad76eb04` |
| Frozen leftover-join.v6 (split; not this subject) | `edc2d0594bc7719689ca129f0df8fa9dc6f73ed33f0af33cc3143b2624868717` |
| Frozen leftover-join.v5 (split; not this subject) | `92112261207071deec9660b1c854b1096cc8ee510e438ce642e76fd1102c7d1b` |
| Frozen leftover-join.v4 (D-196; not this subject) | `b8696fd134550a9ad15d44a07adcc4030aad3702013cc9de914bbab5b8e74ae4` |
| Frozen corpus v1 (D-241; not this subject) | `861bb4e7d26a80158cc1cc3a0518c5e8e95311bee4d8c8ce63acd1e60d6c906d` |
| Frozen corpus v2 (D-243; not this subject) | `af24c6e7294c5802e02063ad0875907b68e264581f6521325dc6d6b60a97fba1` |
| Frozen corpus v7 (D-245; not this subject) | `20bf75a4b404f54d16b531659af825ef6f86d3721ea10cb3c0c435b0e496c57f` |
| Frozen D-246 turn-1 draft (OBJECT D246-S1 / CODEX-D246-SF1; not this subject) | `b68debe3baf1420b5e9311a7582101ef1d68eb505f9bb0c5b41e3f916809fd91` |
| Frozen D-246 turn-1 Claude OBJECT D246-S1 (not this subject) | `da2ece9cc8f8f5a65970bf8bcfa41b0ce3e6a369394a1764e14924459a8d7934` |
| Frozen D-246 turn-1 Codex OBJECT CODEX-D246-SF1 (not this subject) | `da1c4f8ca296886f2d13e68c0a1d42fd2467b7556348cd7730d30e756d24c1fc` |
| Frozen occupancy v4 (D-218; not this subject) | `13addb3cc70611efe22876f84dbe9e15d9a27529446d7e03841d2b2a3f552e0b` |
| COORDINATOR-DECISIONS.md | `fd74c2f464771f814705b20443cef3e0ba4a797c82cf00b629cc705b99c286b4` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `e160bc44ef9f4c9c6b1620e69adda7d489b9ee5f` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v11, both Stage A verdicts, leftover-join v4 through v10,
occupancy v4, corpus v1, corpus v2, corpus v7, the frozen
turn-1 draft and both turn-1 OBJECT verdicts, and this
draft unmoved,
remasure before adoption. Append-only COORD after this
remasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G21 lead
token remains `OPEN`; DR-114 remains `OPEN`; DR-133 remains
`OPEN`. Naming parent is D-145 / naming v6, not
leftover-join.v9. leftover-join.v9 remains the current recorded
G21 leftover-join. leftover-join.v4 through v8 and split
leftover-join.v10 are not current. leftover-join.v5,
leftover-join.v6, and leftover-join.v10 are split
predecessors. leftover-join.v8 is Dual REJECT 0/1
G21LJ-V8-SF1. Once this entry records leftover-join.v11,
leftover-join.v4 through v10 are not current. Do not record
leftover-join.v11 leftoverDesign as other than
`[OBL-G21-FX-AUTHORING]`. Do not claim CC-5 fully authored.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of v11 leftover
remasurement of G21 after D-245. leftover-design of the two
CC-5 prefix injections is stale as an authoring claim.
leftover-design of NT-1 and NT-2 implementations, and of
per-D-002-platform copies of those implementations, remains
stale as an authoring claim. leftoverDesign remains
`[OBL-G21-FX-AUTHORING]` for remaining unauthored G21
classes, including remaining CC-5 injections and
per-D-002-platform copies of the two CC-5 payloads. Lands
G21LJ-V10-SF1. This entry records v11. It is not
SATISFIED-GRADE. Frozen v4 through v10 are not recorded as
current.

## Decision

1. Record
   `g21-leftover-join.v11.json`
   as G21 leftover remasurement after D-245. Lands
   G21LJ-V10-SF1. The candidate binds NOTHING. Both
   independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v4 through v10 are not recorded as
   current.
2. DR-G21 stays `OPEN`. leftoverDesign remains
   `[OBL-G21-FX-AUTHORING]`. leftover-design of the two
   CC-5 prefix injections is stale as an authoring claim.
   leftover-design of NT-1 and NT-2 implementations, and of
   per-D-002-platform copies of those implementations, is
   stale as an authoring claim. leftover-design of
   per-D-002-platform copies of the two CC-5 payloads
   remains. Remaining CC-5 injections stay unauthored.
   Remaining G21 classes stay unauthored. Remainder of G21
   execution, including candidate-buffer digest,
   subsequent-session view, host-projection goldens, and
   EV-5 diagnostic/audit bytes, remains qualification
   (D-056). Does not pin QUALIFIED. Does not invent a D-002
   platform list. Does not claim CC-5 fully authored. Does
   not classify non-object top level as CC-5. Does not
   invent a ping body schema. Does not invent 26214400.
   Does not invent a finding schema. Does not invent a D9
   code, exit number, or HostTermination. Does not invent a
   pack IR. Does not invent a section 7.1 recipe. Does not
   author NT-6. Does not take over G23. Does not reopen
   DR-102 SATISFIED. Does not SATISFY DR-114. Does not
   SATISFY DR-133. Does not SATISFY DR-117. Does not SATISFY
   DR-131. Does not SATISFY DR-101. Gate 1 Class A is not
   opened. Not SATISFIED. Required-now stays 28.
   Condition-4 effect is zero. Naming parent is D-145 /
   naming v6, not leftover-join.v9. Claude Stage A returned
   no observationsNotFindings. Codex Stage A returned one
   observation object with identifier G21LJ-V11-OBS-1, an
   observation paired with a whyNotShouldFix. This entry
   names that Codex identifier and does not invent
   identifiers. It does not claim that both reviewers'
   identifiers are preserved. Claude returned no observation
   identifiers. Does not execute G21. Does not rewrite
   occupancy v4. Does not rewrite corpus v1, corpus v2, or
   corpus v7. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D246.
Does not unwrite D-145, D-196, D-218, D-241, D-243, D-244,
or D-245.
