# D-194 — Record g19-leftover-join.v3 as G19 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g19-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-193. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-194**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-124.
> **Does not** steal OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED,
> or OBL-MONOTONIC.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G19-FX-AUTHORING.
> **Does not** invent fixture bytes or a grant-journal.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G19, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-193 is ADOPTED at
`b25a0238e9615e91a76152c1bf0caf854d67e561`.
HEAD is `b25a0238e9615e91a76152c1bf0caf854d67e561`.
Last live heading is D-193. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g19-leftover-join.v3.review-independent.claude2.json` | `54be6c2939e237fb5e676e7c5db687266f20b98d501383ff6d62872fd70fad82` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g19-leftover-join.v3.review-independent.codex.json` | `3dbe0329d830378e15b34ba66c0daa75ea54b0fa615a7dabcc6292a6fafc4746` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g19-leftover-join.v3.json | `8b2fe8447cd87025d301afdab885b12dc33e87043623876b849bdae26bfb4748` |
| g19-leftover-join.v3.review-independent.claude2.json | `54be6c2939e237fb5e676e7c5db687266f20b98d501383ff6d62872fd70fad82` |
| g19-leftover-join.v3.review-independent.codex.json | `3dbe0329d830378e15b34ba66c0daa75ea54b0fa615a7dabcc6292a6fafc4746` |
| COORDINATOR-DECISIONS.md | `956a89206259d63a0104baf527e89667d46121f5ec2aa31de8060d483a90319b` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `b25a0238e9615e91a76152c1bf0caf854d67e561` |
| Frozen v2 (historical, not this subject) | `76eaa277171bc82f18d0019eae358bbd0df746f7081fc950f58fc41dfbfa6990` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G19 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, cites
state-class leftover-join.v3 (D-183) as the current
DR-124 remainder, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G19-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v2 stays frozen; do not record it as
current.

## Decision

1. Record `g19-leftover-join.v3.json` as G19 leftover
   remasurement after D-193. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G19 stays `OPEN`. leftover-design of
   OBL-G19-FX-AUTHORING remains. G19 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-124. Does not steal
   OBL-GRANT-JOURNAL, OBL-INHERIT-BLOCKED, or
   OBL-MONOTONIC. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a grant-journal. Does
   not rewrite G19, G31, or G32. Does not edit file 08.
   Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D194. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, or D-193.
