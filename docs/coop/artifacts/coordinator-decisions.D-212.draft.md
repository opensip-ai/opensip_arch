# D-212 — Record harness.DR-G10.provider-conformance.ts-major-1.v2 as G10 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G10.provider-conformance.ts-major-1.v2.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-211. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-212**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-102 a second time.
> **Does not** reopen DR-102 SATISFIED.
> **Does not** SATISFY DR-133.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent a V2 selector.
> **Does not** pull Rust merged-major-2 into the preview
> runner.
> **Does not** invent a D9 code.
> **Does not** close leftover-design of OBL-G10-FX-AUTHORING.
> **Does not** close leftover-design of OBL-SELECTOR-REFRESH.
> **Does not** record frozen v1 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G10, G31, or G32.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-211 is ADOPTED at
`a58ec0ae26de78cd9d04cac99d27500d3e46eed5`.
HEAD is `a58ec0ae26de78cd9d04cac99d27500d3e46eed5`.
Last live heading is D-211. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G10.provider-conformance.ts-major-1.v2.review-independent.claude2.json` | `04d90eb40a9e1461305cfd3570258180b19ecff8d2dd1ef6e7ce15371e3c0d6c` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G10.provider-conformance.ts-major-1.v2.review-independent.codex.json` | `de7bb2a593b45182d0c0397a2ec6fb7d1895b4dffdfe05666ba4e02b7ae7e6a2` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G10.provider-conformance.ts-major-1.v2.json | `b0cbce06487b96bbe7f6af1dae62ba3b3ca55aaa41305cb96f531099e86bf7c9` |
| harness.DR-G10.provider-conformance.ts-major-1.v2.review-independent.claude2.json | `04d90eb40a9e1461305cfd3570258180b19ecff8d2dd1ef6e7ce15371e3c0d6c` |
| harness.DR-G10.provider-conformance.ts-major-1.v2.review-independent.codex.json | `de7bb2a593b45182d0c0397a2ec6fb7d1895b4dffdfe05666ba4e02b7ae7e6a2` |
| COORDINATOR-DECISIONS.md | `11c412845db7815f61f5b8f6629837581f747e3a02c2595d0c30f13ddfad8340` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `a58ec0ae26de78cd9d04cac99d27500d3e46eed5` |
| Frozen v1 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `e827c1663dceed72e84e75511a81846985704bfd842cef304bf999c019b93ac8` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v2, both
Stage A verdicts, frozen v1, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G10 lead
token remains `HARD-BLOCKED pending selector refresh`;
DR-102 remains SATISFIED under D-056 Class A (D-085) and is
not reopened. v2's top-level head, recordedInputs.HEAD,
file08Pin, and requiredNowUnchanged equal those live
values. File 08 carries G10 (D-086). Frozen v1 remains a
historical occupancy as of HEAD `5d5d778` / required-now 26.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverNameNote that no leftover-join
existed. After file 08 cardinality 28, provider leftover-
join.v3 (D-187) is the current G10 leftover-join. v2
remasures occupancy at live pins and cites that current
leftover-join. Dual independent ACCEPT 0/0 now exists.
This entry records v2. It is not SATISFIED-GRADE. v1 stays
frozen; do not record it as current.

## Decision

1. Record
   `harness.DR-G10.provider-conformance.ts-major-1.v2.json`
   as G10 occupancy remasurement after D-211. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 is not recorded as
   a current occupancy remasurement.
2. DR-G10 stays `HARD-BLOCKED pending selector refresh`.
   leftover-design of OBL-G10-HARNESS-SPEC remains measured
   closed at leftover-join.v3 (D-187). leftover-design of
   OBL-G10-FX-AUTHORING and OBL-SELECTOR-REFRESH remains.
   Remainder is G10 execution once fixture implementations
   exist and after the owed selector refresh. Does not pin
   QUALIFIED. Does not invent fixture bytes. Does not
   invent a V2 selector. Does not pull Rust merged-major-2
   into the preview runner.
3. Does not SATISFY DR-102 a second time. Does not reopen
   DR-102 SATISFIED. Does not SATISFY DR-133. Does not
   SATISFY DR-117. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories. Codex Stage A
   returned zero advisories. Does not execute fixtures. Does
   not rewrite G07, G08, G10, G31, or G32. Does not edit
   file 08. Does not invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D212. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
or D-211.
