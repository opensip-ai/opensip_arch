# D-170 — Record doctor-actor-leftover-join.v11 as DR-114 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `doctor-actor-leftover-join.v11.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-164 / D-168. Not a three-limb act. Not a required-now
> successor.
> This is coordinator decision **D-170**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** open D-056 Class A.
> **Does not** perform SATISFIED-GRADE.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G31 or G32.
> **Does not** invent fixture bytes.
> **Does not** record FC-C1 or mint BLK-1..4.
> **Does not** force a ride onto G09.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-169 is ADOPTED at
`892236a1ccaad33178480880f4915f8bf52de703`.
HEAD is `892236a1ccaad33178480880f4915f8bf52de703`.
Last live heading is D-169. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/doctor-actor-leftover-join.v11.review-independent.claude2.json` | `5ce64f13f3c4ef3001a7c42045fa7887a610bd9322c866b2195c02e5fa21b25b` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/doctor-actor-leftover-join.v11.review-independent.codex.json` | `9e645f447cb083179c6046e8a27b8f24472daee48967a8ff6038d3b71d1ecb3a` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| doctor-actor-leftover-join.v11.json | `3943a7bb2813324f1df0960b216fc2703139754283f72b3add307967caa0d950` |
| doctor-actor-leftover-join.v11.review-independent.claude2.json | `5ce64f13f3c4ef3001a7c42045fa7887a610bd9322c866b2195c02e5fa21b25b` |
| doctor-actor-leftover-join.v11.review-independent.codex.json | `9e645f447cb083179c6046e8a27b8f24472daee48967a8ff6038d3b71d1ecb3a` |
| COORDINATOR-DECISIONS.md | `d06cac9a780d963d8b8bf6240a509d55945829cf6a58e2e9746d9833c3d9e1c1` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `892236a1ccaad33178480880f4915f8bf52de703` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v11, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-114 lead
token remains `OPEN`.

## Why this entry exists

D-164 recorded leftover-design of DR-114 including
OBL-JOIN-FX-EXECUTION as unnamed remainder. D-169 recorded
DR-G32. v11 remasures that unnamed remainder closed:
remainder is G32 execution (qualification). leftover-design
of OBL-JOIN-FX-AUTHORING, OBL-DOCTOR-FX-AUTHORING,
OBL-FC-C1, and OBL-BLK-1..4 remains. Dual independent
ACCEPT 0/0 now exists. This entry records v11. It is not
SATISFIED-GRADE. v8/v9/v10 stay frozen; do not record them.

## Decision

1. Record `doctor-actor-leftover-join.v11.json` as DR-114
   leftover remasurement after D-169. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-114 stays `OPEN`. leftover-design of unnamed
   JOIN-FX execution remainder is closed. Remainder of that
   obligation is G32 execution. leftover-design of
   OBL-JOIN-FX-AUTHORING, OBL-DOCTOR-FX-AUTHORING,
   OBL-FC-C1, and OBL-BLK-1..4 remains. Naming is not
   execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-114. Gate 1 Class A is not opened. Gates 4 and 5 are
   not performed. Not eligible in kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes. Does not record FC-C1.
   Does not mint BLK-1..4. Does not force a ride onto G09.
   Does not rewrite G31 or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D170. Does not unwrite D-032, D-164, D-167, D-168, or
D-169.
