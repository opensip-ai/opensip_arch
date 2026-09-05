# D-249 — Record g25 leftover-join.v5 as G25 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-23
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `g25-leftover-join.v5.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 and D-238 and D-239 and
> D-240 and D-241 and D-242 and D-243 and D-244 and D-245
> and D-246 and D-247 and D-248. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE.
> This is coordinator decision **D-249**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-101.
> **Does not** close leftover-design of OBL-G25-FX-AUTHORING.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** execute G25.
> **Does not** invent fixture bytes.
> **Does not** collapse the two NT-3 readings.
> **Does not** take over G23.
> **Does not** invent a pack IR.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent observation bytes.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** rewrite occupancy v3.
> **Does not** rewrite leftover-join.v8.
> **Does not** record leftover-join.v4 as current.
> **Does not** record leftover-join.v3 as current after this successor is recorded.
> **Does not** record leftover-join.v4 (G23) as current G23 leftover-join.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-248 is ADOPTED at
`825616145ea768a3394965f2e21129396e188e78`.
HEAD is `825616145ea768a3394965f2e21129396e188e78`.
Last live heading is D-248. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g25-leftover-join.v5.review-independent.claude2.json` | `de346fc88b4a99f11184a0b9ebf490f00135686d437de714f25bb48ba920772c` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g25-leftover-join.v5.review-independent.codex.json` | `6f4e28dda440c89f34e67a42cb64fdccf5bcbdc2befc10f80e4c42c05edbd2c2` | ACCEPT 0/0 |

leftover-join.v4 Stage A split (not Dual REJECT; not Dual ACCEPT):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g25-leftover-join.v4.review-independent.claude2.json` | `8fcf9b86a04d6587d89ad8adb071a4d01cc3b0d3d95a39a13dfa441f4dc4322f` | REJECT 0/2 G25LJ-V4-CL-SF1, G25LJ-V4-CL-SF2 |
| Codex | `docs/coop/artifacts/g25-leftover-join.v4.review-independent.codex.json` | `9bbc5b5d388c9fa362fe996fe4b149e100293be25f60f670be902d6a6f5dcd1d` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifier | Standing |
|---|---|---|
| Claude leftover-join.v5 observationsNotFindings[0] | none | unlabeled string; no change requested |
| Claude leftover-join.v5 observationsNotFindings[1] | none | unlabeled string; no change requested |
| Claude leftover-join.v5 observationsNotFindings[2] | none | unlabeled string; no change requested |
| Claude leftover-join.v5 observationsNotFindings[3] | none | unlabeled string; no change requested |
| Claude leftover-join.v5 observationsNotFindings[4] | none | unlabeled string; no change requested |
| Claude leftover-join.v5 observationsNotFindings[5] | none | unlabeled string; no change requested |
| Codex leftover-join.v5 | none | zero advisories; no observations |
| Claude leftover-join.v4 findings | G25LJ-V4-CL-SF1, G25LJ-V4-CL-SF2 | landed at leftover-join.v5 |
| Codex leftover-join.v4 | none | ACCEPT 0/0; no findings |

Measured inputs:

| Path | sha256 |
|---|---|
| g25-leftover-join.v5.json | `9f2b137fe0b01830b4113ef26c8283214a75982f588f164391d61c5510f67aa3` |
| g25-leftover-join.v5.review-independent.claude2.json | `de346fc88b4a99f11184a0b9ebf490f00135686d437de714f25bb48ba920772c` |
| g25-leftover-join.v5.review-independent.codex.json | `6f4e28dda440c89f34e67a42cb64fdccf5bcbdc2befc10f80e4c42c05edbd2c2` |
| Frozen leftover-join.v4 (G25; split; not current; not this subject) | `441fd35afc9c6bd13bec54271a5bcd5e4feb0e263aee391aa1d0dd41b5086e15` |
| Frozen leftover-join.v3 (D-200; not current; not this subject) | `df038663c9911cf13a3c1b078eabf54863fe18a1f85d956668ae3ac08662f4db` |
| Frozen occupancy v3 (D-225; not this subject) | `4f124cd763974b603fb307e13830cc7f79bc559c3b05ab7d39c59194d2f5dfde` |
| Frozen leftover-join.v8 (D-240; current G23 leftover-join; not this subject) | `498324e5e456562317c7681b44cdac9138ca1e947aa363dad5a331caa3eef812` |
| Frozen leftover-join.v4 (G23; D-198; not current; not this subject) | `a542dc6b023d07cf8657c76909ded1641efd29277760308d52574fa706fad56e` |
| COORDINATOR-DECISIONS.md | `334c18e93a35e5fab341ce3fbaa60c39c3a9a156d64c08c4c10838ce3c8c9c55` |
| file 08 | `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e` |
| HEAD | `825616145ea768a3394965f2e21129396e188e78` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, leftover-join
v3, leftover-join.v4 (G25), leftover-join.v5, occupancy v3,
leftover-join.v8, leftover-join.v4 (G23), both Stage A
verdicts, and this draft unmoved, remasure before adoption.
Append-only COORD after this remasurement, with those files
unmoved, is **PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G25 lead
token remains `OPEN`; DR-131 remains `OPEN`; DR-133 remains
`OPEN`. Naming parent is D-151, not leftover-join.v5.
leftover-join.v5 is the G25 leftover-join under review.
leftover-join.v4 (G25) is split and not current.
leftover-join.v3 is not current. leftover-join.v8 remains
the current G23 leftover-join leftoverDesign `[]`.
leftover-join.v4 (G23) is not current. leftoverDesign
remains `[OBL-G25-FX-AUTHORING]`.

This is a leftover remasurement COORD draft. It does not
claim that D-056 gates 2 and 3 do not hold.

## Why this entry exists

Dual independent ACCEPT 0/0 now exists of leftover-join.v5
leftover remasurement after leftover-join.v4 split. Lands
G25LJ-V4-CL-SF1 and G25LJ-V4-CL-SF2. leftover-join.v3 cited
leftover-join.v4 (G23) as current G23 leftover-join and
occupancy v2. leftover-join.v4 (G25) remasured those stale
after occupancy v3 (D-225) and leftover-join.v8 leftoverDesign
`[]` (D-240). leftover-join.v5 pins predecessorV3.recording
D-200 and deletes unfounded Landed in this lineage at v3.
leftoverDesign remains `[OBL-G25-FX-AUTHORING]`. This entry
records leftover-join.v5. It is not SATISFIED-GRADE. Frozen
leftover-join.v4 stays unmoved. Do not invent G25 fixture
bytes. Do not take over G23. Do not SATISFY DR-131.

## Decision

1. Record
   `g25-leftover-join.v5.json`
   as G25 leftover remasurement after D-248. Lands
   G25LJ-V4-CL-SF1 and G25LJ-V4-CL-SF2. The candidate binds
   NOTHING. Both independent Stage A reviewers of leftover-join.v5
   returned 0 blockers and 0 SHOULD-FIX. leftover-join.v4
   remains split. leftover-join.v3 is not current after this
   successor is recorded. leftover-join.v4 (G23) is not
   recorded as current.
2. DR-G25 stays `OPEN`. leftover-design of
   OBL-G25-FX-AUTHORING remains on leftover-join.v5.
   leftover-join.v8 leftoverDesign `[]` is the current G23
   leftover-join. Remainder of G25 execution remains
   qualification (D-056). Does not pin QUALIFIED. Does not
   invent fixture bytes. Does not collapse the two NT-3
   readings. Does not take over G23. Does not invent a pack
   IR. Does not invent a D9 code. Does not invent a section
   7.1 recipe. Does not SATISFY DR-131. Does not SATISFY
   DR-133. Does not SATISFY DR-117. Does not SATISFY DR-114.
   Does not SATISFY DR-101. Gate 1 Class A is not opened.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Naming parent is D-151, not leftover-join.v5.
   Claude Stage A leftover-join.v5 returned six unlabeled
   observationsNotFindings strings. They carry no
   identifiers. Codex Stage A leftover-join.v5 returned zero
   advisories and no observations. This entry does not
   invent identifiers and does not claim that both
   reviewers' identifiers are preserved. Claude Stage A
   returned no observation identifiers. Codex Stage A
   returned no observation identifiers. Does not execute
   G25. Does not rewrite occupancy v3. Does not rewrite
   leftover-join.v8. Does not edit file 08. Does not
   authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays
MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D249.
Does not unwrite D-151, D-200, D-225, D-240, or D-248.
