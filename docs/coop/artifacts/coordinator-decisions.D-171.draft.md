# D-171 — Record permission-leftover-join.v9 as DR-105 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `permission-leftover-join.v9.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-163 / D-170. Not a three-limb act. Not a required-now
> successor.
> This is coordinator decision **D-171**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-105.
> **Does not** open D-056 Class A.
> **Does not** close OBL-FX-AUTHORING, OBL-R10-AUTHORING,
> OBL-R6-AUTHORING, OBL-FC-C1, or OBL-BLK-1..4.
> **Does not** fold R-10 or R-6 into the fourteen FX classes.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G31 or G32.
> **Does not** invent fixture bytes or a leftover ID.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-170 is ADOPTED at
`81e706b0306b79574cc1924a2965d541ea7f2c76`.
HEAD is `81e706b0306b79574cc1924a2965d541ea7f2c76`.
Last live heading is D-170. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/permission-leftover-join.v9.review-independent.claude2.json` | `aa50c430a1efe2b4f099464dd004432319afe523927ece06b5631edbe9b9b390` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/permission-leftover-join.v9.review-independent.codex.json` | `832242100056ffcb3c8cc648ed5cdf47a53c18e2fa64d1feb01206ab0a774a80` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| permission-leftover-join.v9.json | `71c0b80bfd11fe9ae1601cc390d76e01aa67621b550a04e1ad8b8359ce2b97fe` |
| permission-leftover-join.v9.review-independent.claude2.json | `aa50c430a1efe2b4f099464dd004432319afe523927ece06b5631edbe9b9b390` |
| permission-leftover-join.v9.review-independent.codex.json | `832242100056ffcb3c8cc648ed5cdf47a53c18e2fa64d1feb01206ab0a774a80` |
| COORDINATOR-DECISIONS.md | `86d4f2af011f784edd8e59205dc3d3e17db4ec749b56e699b9a269abc5d386f9` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `81e706b0306b79574cc1924a2965d541ea7f2c76` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v9, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-105 lead
token remains `OPEN`.

## Why this entry exists

Wave 2 sample. Frozen v7 was REJECT PLJ-V7-SF1 after
D-169/D-170. v9 remasures actor-join: execution is
qualification at live DR-G32; authoring/integration still
rides DR-114. leftover-design of OBL-FX-AUTHORING,
OBL-R10-AUTHORING, OBL-R6-AUTHORING, OBL-FC-C1, and
OBL-BLK-1..4 remains. Dual independent ACCEPT 0/0 now
exists. This entry records v9. It is not SATISFIED-GRADE.
v7/v8 stay frozen; do not record them.

## Decision

1. Record `permission-leftover-join.v9.json` as DR-105
   leftover remasurement after D-169 / D-170. The
   candidate binds NOTHING. Both independent reviewers
   returned 0 blockers and 0 SHOULD-FIX.
2. DR-105 stays `OPEN`. Actor-join fixture execution is
   qualification at DR-G32. leftover-design of
   OBL-FX-AUTHORING, OBL-R10-AUTHORING, OBL-R6-AUTHORING,
   OBL-FC-C1, and OBL-BLK-1..4 remains. Naming is not
   execution. Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-105. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not fold R-10 or R-6 into the fourteen. Does not
   invent a leftover ID, fixture bytes, or a
   decision-record envelope. Does not rewrite G31 or G32.
   Does not edit file 08. Does not invent a D9 code. Does
   not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D171. Does not unwrite D-032, D-042, D-163, D-169, or
D-170.
