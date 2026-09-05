# D-163 — Record permission-leftover-join.v2 as DR-105 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1.
> Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `permission-leftover-join.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-162 / D-161. This is coordinator decision **D-163**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-105.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** execute fixtures.
> **Does not** record FC-C1.
> **Does not** apply D-042, D-093, D-126, or D-128.
> **Does not** admit CA-1 IN_PROCESS or mint the later CA-2 gate.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** invent a D9 code.
> **Does not** invent a section 7.1 recipe.
> **Does not** invent a G09 harness specification or FX fixture bytes.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

Turn-1 subject `coordinator-decisions.D-163.draft.md`
`8641e75e3551e3c11c1e246e78d5f81dd308cb6b14c6523374e5edc557b2bfdb`
held frozen. Claude 2 CONSENT, 0 MUST-FIX, 0 SHOULD-FIX.
Codex OBJECT, 0 MUST-FIX, 1 SHOULD-FIX CODEX-D163-SF1.

| ID | Sev | Disposition |
|---|---|---|
| CODEX-D163-SF1 | SHOULD-FIX | ACCEPTED. Both cited join verdicts are now mode 0444 at the same digests they had at turn 1. This turn-2 draft recites that custody. No operative decision change. |

Join-verdict custody (turn-2 recital):

| Path | sha256 | mode |
|---|---|---|
| permission-leftover-join.v2.review-independent.claude2.json | `dba7c23c8dc4a938f4b1d1b6dfec4c0a1e507d1848bcb5041d0d22e28b12fccb` | 0444 |
| permission-leftover-join.v2.review-independent.codex.json | `247705987130171c187b6afcf53e1f3d6d23be1c4e472db1969abcf04575c917` | 0444 |

D-162 is ADOPTED at `8fd376d6a3fb3fde829f4c9ca932358c688580cf`.
HEAD is `8fd376d6a3fb3fde829f4c9ca932358c688580cf`.

Measured inputs:

| Path | sha256 |
|---|---|
| permission-leftover-join.v2.json | `68ea10e052ae6a2eb6a35fd021be7e72418157a47fa07493ad2f4d927aeb9558` |
| Claude 2 join verdict | `dba7c23c8dc4a938f4b1d1b6dfec4c0a1e507d1848bcb5041d0d22e28b12fccb` ACCEPT, 0/0; mode 0444 |
| Codex join verdict | `247705987130171c187b6afcf53e1f3d6d23be1c4e472db1969abcf04575c917` ACCEPT, 0/0; mode 0444 |
| permission-truth-tables.v9.json | `05d559647d103a47c18ed5177b71900a1d9dfcdea6b9a1255aefcec5f09eaccb` |
| host-effect-authorization.v25.json | `b91b9f739b10b1bd30eb56b9d68feac81c483ad86f50e11ed33b95e98ae2d9b9` |
| COORDINATOR-DECISIONS.md | `f323e639b26209fc5ee859d9f5ce142fea41f56afc88db383de36a7b08702903` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-162 commit | `8fd376d6a3fb3fde829f4c9ca932358c688580cf` |
| HEAD | `8fd376d6a3fb3fde829f4c9ca932358c688580cf` |
| Turn-1 subject (frozen) | `8641e75e3551e3c11c1e246e78d5f81dd308cb6b14c6523374e5edc557b2bfdb` |
| Claude 2 turn-1 verdict | `1b199e69e2cb2252921276c5ced9c742876b7c18785316384bb576c27cc660a1` CONSENT 0/0 |
| Codex turn-1 verdict | `fe69b0ff03916b8bb0f2413c37913a5626eb126d246fefb2e9b9f4aeca85e99b` OBJECT 0/1 CODEX-D163-SF1 |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
join verdicts, the frozen turn-1 subject, both turn-1
verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-139 L names DR-105 leftover: the D-056 ineligible table
and the D-042 / D-093 remaining-unmet list. Join v2
received independent dual ACCEPT at 0 blockers and 0
SHOULD-FIX after Claude REJECT of v1 (CLAUDE-PLJ-V1-SF1)
and Codex REJECT of v1 (PLJ-V1-SF1, PLJ-V1-SF2). This
entry records that measurement. It does not add a row
and does not SATISFY DR-105.

## Decision

1. Record `permission-leftover-join.v2.json` as DR-105
   leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-105 stays `OPEN`. leftover-design/OPEN is the token,
   not a finding. Leftover-design is not closed. Remaining
   leftover-design: OBL-G09-HARNESS-SPEC, OBL-FX-AUTHORING,
   OBL-FC-C1, and OBL-BLK-1..4. D-032 actor scope and the
   recorded v2/v9/v8/v25 candidates are not leftover-
   authoring. OBL-ACTOR-JOIN rides DR-114; D-129's recorded
   candidate binds NOTHING and SATISFIES no row.
3. D-056 Class A is not opened. Gates 2 and 3 do not hold
   for DR-105. No SATISFIED. Required-now stays 26. This
   entry does not execute fixtures, does not record FC-C1,
   does not apply D-042, D-093, D-126, or D-128, does not
   admit CA-1 IN_PROCESS, and does not mint the later CA-2
   gate.
4. **Proposed later work, not performed here:** a later
   D-000 cycle may author the G09 harness specification
   and independently pin the fourteen FX implementations;
   a later joint-owner act may record FC-C1; a later
   D-139 L cycle on DR-114 may measure actor-join leftover.
   Each later act that adds a required-now row is a scoped
   D-002 successor and a D-086 successor in the same act.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, FC-C1 recording, or SATISFIED cycle.
Overturn: C-D163. Does not unwrite D-032, D-042, D-093,
D-126, D-128, D-129, or D-162.
