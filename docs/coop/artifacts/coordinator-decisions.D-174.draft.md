# D-174 — Record component-manifest-leftover-join.v6 as DR-103 leftover remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-20
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `component-manifest-leftover-join.v6.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 / D-171 / D-172 / D-173. Not a three-limb act. Not
> a required-now successor.
> This is coordinator decision **D-174**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-103.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design of Windows-path
> fixture bytes, ENVELOPE_MISMATCH, unicode-norm, OD-1, or
> OD-2.
> **Does not** invent fixture bytes or a reserved-device-name
> list.
> **Does not** record frozen v4 or v5 as a current
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G15, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-173 is ADOPTED at
`c77ff47d9a0800d3b26921f3ed554492e834755e`.
HEAD is `c77ff47d9a0800d3b26921f3ed554492e834755e`.
Last live heading is D-173. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
leftover-join (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/component-manifest-leftover-join.v6.review-independent.claude2.json` | `ef77d31bdf1cab61b8ac05a4bc6d256de46a450572d786a5e895117e313611a1` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/component-manifest-leftover-join.v6.review-independent.codex.json` | `6d8014a3a14b4af7801028bfd9b5f85e14d57e9dacfe387a5353db47cfa29863` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| component-manifest-leftover-join.v6.json | `9953f9692379f3f30254df12735d284559da6b6e979fd684296ace02d0e6e212` |
| component-manifest-leftover-join.v6.review-independent.claude2.json | `ef77d31bdf1cab61b8ac05a4bc6d256de46a450572d786a5e895117e313611a1` |
| component-manifest-leftover-join.v6.review-independent.codex.json | `6d8014a3a14b4af7801028bfd9b5f85e14d57e9dacfe387a5353db47cfa29863` |
| COORDINATOR-DECISIONS.md | `9a5ef237f76937bde8fddf56098853ee343e4ae78bb0f8fa041da3a86727a3d6` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `c77ff47d9a0800d3b26921f3ed554492e834755e` |
| Frozen v5 (not this subject) | `28f45a90f8062387a3b3b1e3e9d92d755cfb1716310a92be8a2c1b7cd4e7943e` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v6, both
Stage A verdicts, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-103 lead
token remains `OPEN`. v6's top-level head, recordedInputs.HEAD,
file08Pin, and both requiredNowUnchanged fields equal those
live values. Frozen v4 remains a historical measurement as
of HEAD `5d5d778` / required-now 26. Frozen v5 stays
unmoved and is not recorded.

## Why this entry exists

Wave 2. Frozen v4 asserted required-now 26 at HEAD
`5d5d778` and is not recordable as a current remasurement
after file 08 moved. v5 remasured live pins and received
dual REJECT 0/1 (CMLJ-V5-SF1 and CLAUDE-CMLJ-V5-SF1).
v6 lands both findings. leftover-design of Windows-path
fixture bytes, ENVELOPE_MISMATCH, unicode-norm, OD-1, and
OD-2 remains. Dual independent ACCEPT 0/0 now exists.
This entry records v6. It is not SATISFIED-GRADE. v4/v5
stay frozen; do not record them as current.

## Decision

1. Record `component-manifest-leftover-join.v6.json` as
   DR-103 leftover remasurement after D-173. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v4 and v5 are not
   recorded as a current remasurement.
2. DR-103 stays `OPEN`. leftover-design of Windows-path
   fixture bytes, ENVELOPE_MISMATCH, unicode-norm, OD-1,
   and OD-2 remains. G15 harness specification is measured
   authored and not QUALIFIED. Naming is not execution.
   Not QUALIFIED.
3. D-056 Eligibility gates 2 and 3 do **not** hold for
   DR-103. Gate 1 Class A is not opened. Not eligible in
   kind. Not SATISFIED.
4. Required-now stays 28. Condition-4 effect is zero.
   Condition 4 stays MET at 28 of 28 / 32 of 32.
5. Does not invent fixture bytes or a reserved-device-name
   list. Does not rewrite G15, G31, or G32. Does not edit
   file 08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D174. Does not unwrite D-013, D-104, D-106, D-161,
D-169, D-172, or D-173.
