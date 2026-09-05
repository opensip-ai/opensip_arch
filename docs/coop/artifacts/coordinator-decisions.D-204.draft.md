# D-204 — Record g29-leftover-join.v3 as G29 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g29-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-203. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-204**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-117.
> **Does not** take over G21, G23, G24, or G30.
> **Does not** reopen leftover-design of EE-1, EE-2, EE-3b,
> EE-4, EE-5a, EE-5b, or EE-6a.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G29-FX-AUTHORING.
> **Does not** invent fixture bytes or a section 7.1 recipe.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G29, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-203 is ADOPTED at
`634a5cf034511bfd7b24693a1c770446970f9090`.
HEAD is `634a5cf034511bfd7b24693a1c770446970f9090`.
Last live heading is D-203. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g29-leftover-join.v3.review-independent.claude2.json` | `32b2f6a2423f716d05e8a3b4d364df342c8b15f6f84fa34e5499475f63c0b506` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g29-leftover-join.v3.review-independent.codex.json` | `71647f678b8dcd3e3910c48d572d096c8372808e34e332830e5f199e2edbc8a0` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g29-leftover-join.v3.json | `4ab44caebced258a4ba2ef795879bf3afc9427cb5ae547c1138bf1c0e9f7ec5f` |
| g29-leftover-join.v3.review-independent.claude2.json | `32b2f6a2423f716d05e8a3b4d364df342c8b15f6f84fa34e5499475f63c0b506` |
| g29-leftover-join.v3.review-independent.codex.json | `71647f678b8dcd3e3910c48d572d096c8372808e34e332830e5f199e2edbc8a0` |
| COORDINATOR-DECISIONS.md | `8c928ab30dda3dce6b782b52f56e958506a9661db97c6a1c42bc5625612ca8fa` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `634a5cf034511bfd7b24693a1c770446970f9090` |
| Frozen v2 (historical, not this subject) | `a757e718d8cd1c3d530a71e4f23ad57c80d6e833071f56a42b0f6cac355c6302` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G29 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins and replaces
D-167 placeholder sentences with carry-safe phrasing.
leftover-design of OBL-G29-FX-AUTHORING remains. Dual
independent ACCEPT 0/0 now exists. This entry records v3.
It is not SATISFIED-GRADE. v1 and v2 stay frozen; do not
record them as current.

## Decision

1. Record `g29-leftover-join.v3.json` as G29 leftover
   remasurement after D-203. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G29 stays `OPEN`. leftover-design of
   OBL-G29-FX-AUTHORING remains. G29 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-117. Does not take over G21, G23,
   G24, or G30. Does not reopen leftover-design of EE-1,
   EE-2, EE-3b, EE-4, EE-5a, EE-5b, or EE-6a. Gate 1 Class
   A is not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a section 7.1 recipe.
   Does not rewrite G29, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D204. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
or D-203.
