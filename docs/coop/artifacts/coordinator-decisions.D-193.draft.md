# D-193 — Record g18-leftover-join.v4 as G18 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g18-leftover-join.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-192. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-193**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-107.
> **Does not** steal OBL-ENCODING-RESERVED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-G18-FX-AUTHORING.
> **Does not** invent fixture bytes or a journal.
> **Does not** record frozen v1 through v3 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G18, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-192 is ADOPTED at
`9a324dcfc0c2c988b0ba0813078ab16863be7538`.
HEAD is `9a324dcfc0c2c988b0ba0813078ab16863be7538`.
Last live heading is D-192. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g18-leftover-join.v4.review-independent.claude2.json` | `646897da1ff53d1725507d2d1bffa816f8be2012fde69e2485700939a71825c8` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g18-leftover-join.v4.review-independent.codex.json` | `d736e82e2fa7e518445ff5bb97484bfee2d385df7b49a28e711d21cf94f93619` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g18-leftover-join.v4.json | `f18f08bcb360a68b76e08330b716129a69193a3d91a8e2623f0a396ecba33228` |
| g18-leftover-join.v4.review-independent.claude2.json | `646897da1ff53d1725507d2d1bffa816f8be2012fde69e2485700939a71825c8` |
| g18-leftover-join.v4.review-independent.codex.json | `d736e82e2fa7e518445ff5bb97484bfee2d385df7b49a28e711d21cf94f93619` |
| COORDINATOR-DECISIONS.md | `8045f6b4f048a11d96ee11ae889aed62c7446c5d8cb5e6683d74c75aca371f7e` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `9a324dcfc0c2c988b0ba0813078ab16863be7538` |
| Frozen v3 (historical, not this subject) | `fa24a22d4967575fa8d2eb77f7525947a4c83da467b217564974fe8220e53010` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G18 lead
token remains `OPEN`. v4's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v3 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v3 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v4 remasures live pins, cites
lifecycle leftover-join.v3 (D-176) as the current DR-107
ROW leftover-join, and replaces D-167 placeholder
sentences with carry-safe phrasing. leftover-design of
OBL-G18-FX-AUTHORING remains. Dual independent ACCEPT
0/0 now exists. This entry records v4. It is not
SATISFIED-GRADE. v3 stays frozen; do not record it as
current.

## Decision

1. Record `g18-leftover-join.v4.json` as G18 leftover
   remasurement after D-192. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 through v3 are not recorded as a
   current remasurement.
2. DR-G18 stays `OPEN`. leftover-design of
   OBL-G18-FX-AUTHORING remains. G18 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-107. Does not steal
   OBL-ENCODING-RESERVED. Gate 1 Class A is not opened.
   Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a journal. Does not
   rewrite G18, G31, or G32. Does not edit file 08. Does
   not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D193. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, or D-192.
