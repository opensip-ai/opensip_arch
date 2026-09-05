# D-250 — Record g24 leftover-join.v4 as G24 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 2 of 3. Lands CLAUDE-D250-SF1
> and CLAUDE-D250-SF2.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g24-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248 and D-249. Not a three-limb
> act. Not a required-now successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-250**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G24-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G24.
> **Does not** invent fixture bytes.
> **Does not** invent a pack IR.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** reopen leftover-design of NT-1 or NT-2.
> **Does not** occupy the identifier.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v3.
> **Does not** rewrite leftover-join.v8.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record occupancy v1 as current occupancy.
> **Does not** record leftover-join.v4 (G23) as current G23 leftover-join.
> **Does not** record leftover-join.v4 (G25) as current G25 leftover-join.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-249 is ADOPTED at
`1e939c5643fea73a6581f45f1d4067854747271c`.
HEAD is `1e939c5643fea73a6581f45f1d4067854747271c`.
Last live heading is D-249. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g24-leftover-join.v4.review-independent.claude2.json` | `64ae502fbe7d2d267e1d19a990a63de38fdb3961647fc3ca7b5ab63ceda23f8f` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g24-leftover-join.v4.review-independent.codex.json` | `b956658feb003dbb1f5ea2c8d581e1d8b80afb554b870136b58dc8d50a0d99df` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v4 observationsNotFindings[0] | none | unlabeled string; no change requested |
| Claude leftover-join.v4 observationsNotFindings[1] | none | unlabeled string; no change requested |
| Claude leftover-join.v4 observationsNotFindings[2] | none | unlabeled string; no change requested |
| Codex leftover-join.v4 observationsNotFindings | none | empty list; zero advisories; no observations |

Turn 1 split. Claude OBJECT 0/2 CLAUDE-D250-SF1,
CLAUDE-D250-SF2. Codex CONSENT 0/0. Not Dual REJECT.
Not Dual CONSENT.

Stage B turn 1:

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/coordinator-decisions.D-250.review-adversarial.claude2.json` | `48be6bc5536e61932f3788c74fc6cde2e07a302606a1618b7bb291a98d9b5439` | OBJECT 0/2 CLAUDE-D250-SF1, CLAUDE-D250-SF2 |
| Codex | `docs/coop/artifacts/coordinator-decisions.D-250.review-adversarial.codex.json` | `fd95f94ba45f6404d76b194f2e2f2ab3da571716db20e791a67355c2e8e0deb0` | CONSENT 0/0 |

Stage B turn 1 observation disposition (no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude Stage B observations[0] | none | unlabeled object, observation paired with standing; no change requested |
| Claude Stage B observations[1] | none | unlabeled object, observation paired with standing; no change requested |
| Codex Stage B | none | zero advisories; no observations |

Frozen turn 1 draft
`docs/coop/artifacts/coordinator-decisions.D-250.draft.md`
`dadb52620b0c28d1a4f5dfa2067359afce04ac027992eac43615849271f859c6`
stays unmoved.

Measured inputs:

| Path | sha256 |
|---|---|
| g24-leftover-join.v4.json | `c451f7ce20e93442172322ff2fd29a029a9a0ca209538ece7c590d32c72e43d7` |
| g24-leftover-join.v4.review-independent.claude2.json | `64ae502fbe7d2d267e1d19a990a63de38fdb3961647fc3ca7b5ab63ceda23f8f` |
| g24-leftover-join.v4.review-independent.codex.json | `b956658feb003dbb1f5ea2c8d581e1d8b80afb554b870136b58dc8d50a0d99df` |
| Frozen leftover-join.v3 (D-199; current G24 leftover-join at draft time; not this subject) | `c4fa464802f6075de8054a93f10fbc0b80e2bade6d04e510c2fecc52cf8b0f72` |
| Frozen leftover-join.v2 (historical; not current; not this subject) | `fd944ea7d1f915463784d292bc280388138a1dea41a49c2add748fff8a791701` |
| Frozen leftover-join.v1 (historical; not current; not this subject) | `6d4d92287acd3e97861d47be6c87f4e5ba7afe010833218793e916175ff021e5` |
| Frozen occupancy v3 (D-224; current G24 occupancy; not this subject) | `ee41d14c7896ce97ebbf6611054991688ef1755499fbdc9d7f274498ebf9fdd4` |
| Frozen occupancy v1 (predecessor occupancy; not current; not this subject) | `9d8fb91395d683d40093c4e962f1e1e44cd0d0db84fce424e34eceeedb663ef3` |
| Frozen leftover-join.v8 (D-240; current G23 leftover-join leftoverDesign []; not this subject) | `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` |
| Frozen leftover-join.v4 (G23; D-198; not current; not this subject) | `a542dc6b023d07cf8657c76909ded1641efd29277760308d52574fa706fad56e` |
| Frozen leftover-join.v5 (D-249; current G25 leftover-join; not this subject) | `9f2b137fe0b01830b4113ef26c8283214a75982f588f164391d61c5510f67aa3` |
| Frozen leftover-join.v4 (G25; split; not current; not this subject) | `441fd35afc9c6bd13bec54271a5bcd5e4feb0e263aee391aa1d0dd41b5086e15` |
| Frozen turn 1 D-250 draft (not this subject) | `dadb52620b0c28d1a4f5dfa2067359afce04ac027992eac43615849271f859c6` |
| Frozen D-250 turn 1 Claude review (not this subject) | `48be6bc5536e61932f3788c74fc6cde2e07a302606a1618b7bb291a98d9b5439` |
| Frozen D-250 turn 1 Codex review (not this subject) | `fd95f94ba45f6404d76b194f2e2f2ab3da571716db20e791a67355c2e8e0deb0` |
| COORDINATOR-DECISIONS.md | `e289147c18d9b90520692a406e7c2ce4229ad63c163447e8ff7249375f4a450d` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `1e939c5643fea73a6581f45f1d4067854747271c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4 (G24), occupancy v3, occupancy v1,
leftover-join.v8, leftover-join.v4 (G23), leftover-join.v5,
leftover-join.v4 (G25), both Stage A verdicts, frozen turn 1
draft, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G24 lead
token remains `OPEN`; DR-131 remains `OPEN`; DR-133 remains
`OPEN`. Naming parent is D-150, not leftover-join.v4.
leftover-join.v4 is the G24 leftover-join under review.
leftover-join.v3 remains the current recorded G24 leftover-join
at draft time (D-199). After this successor is recorded,
leftover-join.v3 is not current. Occupancy v3 remains the
current G24 occupancy remasurement. Occupancy v1 is not
current. leftoverDesign remains `[OBL-G24-FX-AUTHORING]`.
leftover-join.v8 leftoverDesign `[]` remains the current G23
leftover-join. leftover-join.v4 (G23) is not current.
leftover-join.v5 remains the current G25 leftover-join.
leftover-join.v4 (G25) remains split.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Lands CLAUDE-D250-SF1 and CLAUDE-D250-SF2. Dual independent
ACCEPT 0/0 now exists of leftover-join.v4 leftover remasurement
after occupancy v3 (D-224). leftover-join.v3 cited occupancy v1
as the specification. Occupancy v3 remasured that already-named
identifier. leftoverDesign remains `[OBL-G24-FX-AUTHORING]`.
This entry records leftover-join.v4 (G24). It is not
SATISFIED-GRADE. Frozen leftover-join.v3 stays unmoved.
leftover-join.v3 remains current at draft time. Frozen turn 1
draft stays unmoved. Do not invent a pack IR. Do not invent
fixture bytes. Do not SATISFY DR-131.

## Decision

1. Record
   `g24-leftover-join.v4.json`
   as G24 leftover remasurement after D-249. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v4
   returned 0 blockers and 0 SHOULD-FIX. Lands CLAUDE-D250-SF1
   and CLAUDE-D250-SF2. leftover-join.v3 remains current at
   draft time. After this successor is recorded, leftover-join.v3
   is not current. Occupancy v1 is not recorded as current
   occupancy. leftover-join.v4 (G23) is not recorded as current.
   leftover-join.v4 (G25) is not recorded as current.
2. DR-G24 stays `OPEN`. leftover-design of
   OBL-G24-FX-AUTHORING remains on leftover-join.v4.
   Remainder of G24 execution remains qualification (D-056).
   Does not pin QUALIFIED. Does not invent fixture bytes. Does
   not invent a pack IR. Does not invent a D9 code. Does not
   invent a section 7.1 recipe. Does not reopen leftover-design
   of NT-1 or NT-2. Does not occupy the identifier. Does not
   SATISFY DR-131. Does not SATISFY DR-133. Does not SATISFY
   DR-117. Does not SATISFY DR-114. Does not SATISFY DR-101.
   Gate 1 Class A is not opened. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Naming parent is
   D-150, not leftover-join.v4. naming v6 does not name G24.
   Claude Stage A leftover-join.v4 returned three unlabeled
   observationsNotFindings strings. They carry no identifiers.
   Codex Stage A leftover-join.v4 returned an empty
   observationsNotFindings list, zero advisories, and no
   observations. This entry does not invent identifiers and
   does not claim that both reviewers' identifiers are
   preserved. Claude Stage A returned no observation
   identifiers. Codex Stage A returned no observation
   identifiers. Claude Stage B turn 1 returned two unlabeled
   observations objects, each an observation paired with a
   standing. They carry no identifiers. Codex Stage B turn 1
   returned zero advisories and no observations; its verdict
   is CONSENT 0/0. This entry does not invent identifiers for
   those Stage B observations and does not claim that both
   reviewers' identifiers are preserved. Claude Stage B
   returned no observation identifiers. Codex Stage B
   returned no observation identifiers. Does not execute G24.
   Does not rewrite occupancy v3. Does not rewrite
   leftover-join.v8. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D250.
Does not unwrite D-150, D-199, D-224, D-240, or D-249.
