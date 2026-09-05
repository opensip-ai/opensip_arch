# D-210 — Record harness.DR-G07.exact-bytes.v4 as G07 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G07.exact-bytes.v4.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-209. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-210**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-103.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** populate a filesystem allowlist.
> **Does not** populate treeRootDigest.
> **Does not** invent a section 7.1 recipe.
> **Does not** close leftover-design of OBL-G07-FX-AUTHORING.
> **Does not** close leftover-design of OBL-FILESYSTEM-COVERAGE.
> **Does not** record frozen v1, v2, or v3 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G31, or G32.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-209 is ADOPTED at
`269cf08e0244152c815e9e98771dc8b3e56f78fb`.
HEAD is `269cf08e0244152c815e9e98771dc8b3e56f78fb`.
Last live heading is D-209. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G07.exact-bytes.v4.review-independent.claude2.json` | `107a23d01e7b0bb580445e6f8eca0045043e681c18ef80318aa47b257e6d00d9` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G07.exact-bytes.v4.review-independent.codex.json` | `306396a1aa0e070a1ef0ffcd1d3d31115c2a3214945cbb04c670c153530c800f` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G07.exact-bytes.v4.json | `99be421cd11a7524c87ee56b31b1c3b8335d8156bdb0d27a3a94ddddae7a56ed` |
| harness.DR-G07.exact-bytes.v4.review-independent.claude2.json | `107a23d01e7b0bb580445e6f8eca0045043e681c18ef80318aa47b257e6d00d9` |
| harness.DR-G07.exact-bytes.v4.review-independent.codex.json | `306396a1aa0e070a1ef0ffcd1d3d31115c2a3214945cbb04c670c153530c800f` |
| COORDINATOR-DECISIONS.md | `3a199cd8003a6b631861f91f609b85d41df88a43f348f98930dca83f4a299e72` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `269cf08e0244152c815e9e98771dc8b3e56f78fb` |
| Frozen v1 (historical, not this subject) | `a93b38d0d392a7079fe81b934289038d91ba71d60f02772f1c327b26e43caecd` |
| Frozen v2 (historical, not this subject) | `e5f2f8697db382d586407bde9342cabd27af95b20bcf65b61a9163edaa1a90e1` |
| Frozen v3 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `a53125c63d93556d84f480502c42b98ee19df566ca06322326b171303b1fe196` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v4, both
Stage A verdicts, frozen v1/v2/v3, and this draft unmoved,
re-measure before adoption. Append-only COORD after this
remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G07 lead
token remains `OPEN`; DR-103 remains `OPEN`. v4's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G07 (D-086). Frozen v3 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v1 and v2
remain Claude-REJECT occupancies.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v3 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and leftoverJoinV2 as component-manifest
leftover-join.v2 (D-161). After file 08 cardinality 28,
leftover-join.v5 (D-172) is the current G07 leftover-join
and leftover-join.v6 (D-174) is the current DR-103 leftover-join.
v4 remasures occupancy at live pins, cites those current
leftover-joins, and consumes g07-coverage-domain.v1 as the
later dedicated coverage-domain act booked at v3
filesystems.laterAct. Dual independent ACCEPT 0/0 now exists.
This entry records v4. It is not SATISFIED-GRADE. v1, v2,
and v3 stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G07.exact-bytes.v4.json`
   as G07 occupancy remasurement after D-209. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1, v2, and v3 are not
   recorded as a current occupancy remasurement.
2. DR-G07 stays `OPEN`. leftover-design of OBL-G07-HARNESS-SPEC
   remains measured closed at leftover-join.v5 (D-172).
   leftover-design of OBL-G07-FX-AUTHORING and
   OBL-FILESYSTEM-COVERAGE remains. Remainder is G07
   execution once fixture implementations exist. Does
   not pin QUALIFIED. Does not invent fixture bytes.
   Does not populate a filesystem allowlist.
3. Does not SATISFY DR-103. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Advisory CLAUDE-G07-V4-ADV-1 travels as honesty work.
   Codex Stage A returned zero advisories. Does not execute
   fixtures. Does not rewrite G07, G31, or G32. Does
   not edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D210. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, or D-209.
