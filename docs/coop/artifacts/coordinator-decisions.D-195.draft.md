# D-195 — Record g20-leftover-join.v3 as G20 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g20-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-194. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-195**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-125.
> **Does not** steal OBL-SDK-API-RESERVED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G20-FX-AUTHORING.
> **Does not** invent fixture bytes or reserved SDK APIs.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G20, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-194 is ADOPTED at
`e7070c9e2ed844a1304a75bb47735988c43a3b98`.
HEAD is `e7070c9e2ed844a1304a75bb47735988c43a3b98`.
Last live heading is D-194. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g20-leftover-join.v3.review-independent.claude2.json` | `18ade8fa5f6d757612c166e9be6360551a1c335eb5d6ae7fd5d1ac6aab4df614` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g20-leftover-join.v3.review-independent.codex.json` | `6160f479d17a5e6d5f06ea7b174c1913aa8f5e9e876e8914b53d89fcc3dc1870` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g20-leftover-join.v3.json | `1a04325f648b2cede73e932fb5083867dea4de57c1484b89ece8a983225f2617` |
| g20-leftover-join.v3.review-independent.claude2.json | `18ade8fa5f6d757612c166e9be6360551a1c335eb5d6ae7fd5d1ac6aab4df614` |
| g20-leftover-join.v3.review-independent.codex.json | `6160f479d17a5e6d5f06ea7b174c1913aa8f5e9e876e8914b53d89fcc3dc1870` |
| COORDINATOR-DECISIONS.md | `9e55e39f51c4d9224c0f6f5979f3a17f6bf9b00c483d33e7b9a87a0700877b34` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `e7070c9e2ed844a1304a75bb47735988c43a3b98` |
| Frozen v2 (historical, not this subject) | `2b54e9adfaebd9aa68c2071f9ea7d33f01bb3ba6a196248fb45492a09dd4acaa` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G20 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, cites
sdk leftover-join.v5 (D-184) as the current DR-125
remainder, and replaces D-167 placeholder sentences with
carry-safe phrasing. leftover-design of
OBL-G20-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v3. It is not
SATISFIED-GRADE. v2 stays frozen; do not record it as
current.

## Decision

1. Record `g20-leftover-join.v3.json` as G20 leftover
   remasurement after D-194. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G20 stays `OPEN`. leftover-design of
   OBL-G20-FX-AUTHORING remains. G20 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-125. Does not steal
   OBL-SDK-API-RESERVED. Gate 1 Class A is not opened. Not
   SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or reserved SDK APIs.
   Does not rewrite G20, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D195. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, or
D-194.
