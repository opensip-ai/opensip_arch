# D-191 — Record g15-leftover-join.v3 as G15 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-21
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `g15-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-190. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-191**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-120.
> **Does not** SATISFY DR-103.
> **Does not** steal DR-120 or DR-103 leftover.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of OBL-AT-FX-AUTHORING.
> **Does not** invent fixture bytes, an adapter implementation,
> a numeric threshold, or an envelope.
> **Does not** record frozen v1 or v2 as a current remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G15, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-190 is ADOPTED at
`03033d4622dd76d6ab3c3ab42aa97f2faad7419b`.
HEAD is `03033d4622dd76d6ab3c3ab42aa97f2faad7419b`.
Last live heading is D-190. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/g15-leftover-join.v3.review-independent.claude2.json` | `d5066b45f417f874417cb8d2084c01a616ec285154458a91b60ead1197b0ce81` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/g15-leftover-join.v3.review-independent.codex.json` | `b064bbbd7ee3d782b0f59bdba4cd6e53524fc3c1b1785e4bcc7b90179e18ac39` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| g15-leftover-join.v3.json | `31d37bb0dd08bd96f28a976bda803174c518e75ddec80ba64b6bab740e7e3041` |
| g15-leftover-join.v3.review-independent.claude2.json | `d5066b45f417f874417cb8d2084c01a616ec285154458a91b60ead1197b0ce81` |
| g15-leftover-join.v3.review-independent.codex.json | `b064bbbd7ee3d782b0f59bdba4cd6e53524fc3c1b1785e4bcc7b90179e18ac39` |
| COORDINATOR-DECISIONS.md | `79d94a5cb154eb1818228dd2b77286a9f7b8a009bc2506ef25a9714fd88ef664` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `03033d4622dd76d6ab3c3ab42aa97f2faad7419b` |
| Frozen v2 (historical, not this subject) | `0eef2e4d755d24afa298bb52db40b63d42e54dca9c27820ea41fc485e163eee2` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G15 lead
token remains `OPEN`. v3's top-level head,
recordedInputs.HEAD, file08Pin, and both
requiredNowUnchanged fields equal those live values.
Frozen v2 remains a historical measurement as of HEAD
`5d5d778` / required-now 26.

## Why this entry exists

Wave 2. Frozen v2 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v3 remasures live pins, cites
packaging leftover-join.v3 (D-180) as the current DR-120
ROW leftover-join and component-manifest leftover-join.v6
(D-174) as the current DR-103 ROW leftover-join, and
replaces D-167 placeholder sentences with carry-safe
phrasing. leftover-design of OBL-AT-FX-AUTHORING remains.
Dual independent ACCEPT 0/0 now exists. This entry records
v3. It is not SATISFIED-GRADE. v2 stays frozen; do not
record it as current.

## Decision

1. Record `g15-leftover-join.v3.json` as G15 leftover
   remasurement after D-190. The candidate binds NOTHING.
   Both independent reviewers returned 0 blockers and 0
   SHOULD-FIX. Frozen v1 and v2 are not recorded as a
   current remasurement.
2. DR-G15 stays `OPEN`. leftover-design of
   OBL-AT-FX-AUTHORING remains. G15 harness specification
   is measured authored and not QUALIFIED. Not QUALIFIED.
3. Does not SATISFY DR-120. Does not SATISFY DR-103. Does
   not steal DR-120 or DR-103 leftover. Gate 1 Class A is
   not opened. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes, an adapter
   implementation, a numeric threshold, or an envelope.
   Does not rewrite G15, G31, or G32. Does not edit file
   08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D191. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, or D-190.
