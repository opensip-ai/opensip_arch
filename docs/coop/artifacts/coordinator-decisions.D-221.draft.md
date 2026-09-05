# D-221 — Record harness.DR-G12.doctor-purge.preview.v6 as G12 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G12.doctor-purge.preview.v6.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-220. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-221**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-114.
> **Does not** SATISFY DR-117.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** invent a D9 code.
> **Does not** steal leftover-join.v11 leftoverDesign.
> **Does not** close leftover-design of OBL-DOCTOR-FX-AUTHORING.
> **Does not** deny the 618cb5be v2 dispatch or the 618cb5be
> Claude ACCEPT.
> **Does not** record frozen v1, v2, v3, v4, or v5 as a
> current occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G20, G21, G22, G31, or G32.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-220 is ADOPTED at
`8281ffd14524d75699d9b763f59295b199f33b23`.
HEAD is `8281ffd14524d75699d9b763f59295b199f33b23`.
Last live heading is D-220. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G12.doctor-purge.preview.v6.review-independent.claude2.json` | `8f616719f40798913bf71b5cac2a15f4a9cfa3d10adf63297c63b3dc63196b67` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G12.doctor-purge.preview.v6.review-independent.codex.json` | `57176369eeebec50c792fed50d57ef15b3f8442c1eb2209e396678b7577d4274` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G12.doctor-purge.preview.v6.json | `e6b72a9e0cc7053c991c51c510531c6ecd263bb895c70a3e9ab84bd6b6256735` |
| harness.DR-G12.doctor-purge.preview.v6.review-independent.claude2.json | `8f616719f40798913bf71b5cac2a15f4a9cfa3d10adf63297c63b3dc63196b67` |
| harness.DR-G12.doctor-purge.preview.v6.review-independent.codex.json | `57176369eeebec50c792fed50d57ef15b3f8442c1eb2209e396678b7577d4274` |
| COORDINATOR-DECISIONS.md | `f6a40ffa90f6b1eda3db6eabda94ecc45a411f55f2a6edc09f062aacaf186a07` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `8281ffd14524d75699d9b763f59295b199f33b23` |
| Frozen v1 (Claude REJECT CLAUDE-G12H-V1-B1/SF1, not this subject) | `af23f0bf01805b62e1bd63a9a241a8f7c4ba9ab9c905275b36def82e9bb76b6e` |
| Frozen v2 (618cb5be Claude ACCEPT, not this subject) | `618cb5be1895f207d65f5e5739b562228490c32cccb70375432dc82a15b340f5` |
| Frozen v3 (Claude REJECT CLAUDE-G12H-V3-SF1, not this subject) | `4ee7352e8a81e17f38f883c84bf781e997eae58a56cad7a362112e5e1830d8f0` |
| Frozen v4 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `6ad74892e5e9f48beba8d411d9c354613d08abb666a717a9b49fdd3aeab840c8` |
| Frozen v5 (dual REJECT CLAUDE-G12H-V5-B1 / CODEX-G12H-V5-SF1, not this subject) | `09912b83aafbd93ebee1341c52a8063391e7430348e710ac01bf485ac287d79c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v6, both
Stage A verdicts, frozen v1 through v5, and this draft
unmoved, re-measure before adoption. Append-only COORD
after this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G12 lead
token remains `OPEN`; DR-114 remains `OPEN`. v6's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G12 (D-086). Frozen v4 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v5 remains a
dual-REJECT occupancy.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v4 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, leftoverDesignClosedIfAcceptedAndRecorded
OBL-G12-HARNESS-SPEC, leftoverDesignRemainingOnDR114 still
listing OBL-G21-HARNESS-SPEC and OBL-JOIN-FX-EXECUTION, and
doctor-actor leftover-join.v2 as the DR-114 leftover-join.
After file 08 cardinality 28, g12 leftover-join.v3 (D-190)
is the current G12 leftover-join and doctor-actor leftover-join.v11
(D-170) is the current DR-114 leftover-join.
leftover-join.v3 leftoverDesign remains
`[OBL-DOCTOR-FX-AUTHORING]`. Frozen v5 dual REJECT
CLAUDE-G12H-V5-B1 / CODEX-G12H-V5-SF1 (one shared class;
both identifiers preserved) landed in v6. Dual independent
ACCEPT 0/0 now exists. This entry records v6. It is not
SATISFIED-GRADE. v1 through v5 stay frozen; do not record
them as current.

## Decision

1. Record
   `harness.DR-G12.doctor-purge.preview.v6.json`
   as G12 occupancy remasurement after D-220. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 through v5 are not
   recorded as a current occupancy remasurement.
2. DR-G12 stays `OPEN`. leftover-design of OBL-G12-HARNESS-SPEC
   remains measured closed at leftover-join.v3 (D-190).
   leftover-design of OBL-DOCTOR-FX-AUTHORING remains.
   Remainder is G12 execution once the twelve doctor FC
   implementations exist. Does not pin QUALIFIED. Does not
   invent fixture bytes. Does not invent a D9 code. Does
   not steal leftover-join.v11 leftoverDesign. Does not
   deny the 618cb5be v2 dispatch or the 618cb5be Claude
   ACCEPT.
3. Does not SATISFY DR-114. Does not SATISFY DR-117. Gate 1
   Class A is not opened. Class B SATISFIED is not recorded.
   Not SATISFIED. Required-now stays 28. Condition-4 effect
   is zero. Condition 4 stays MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned zero advisories and four unlabeled
   observationsNotFindings. Codex Stage A returned zero
   advisories. The Claude observations carry no identifier.
   Codex Stage A returned no observations. CLAUDE-G12H-V5-B1
   and CODEX-G12H-V5-SF1 (one shared class; both identifiers
   preserved) were landed in the occupancy bytes.
   CLAUDE-G12H-V1-B1, CLAUDE-G12H-V1-SF1, and
   CLAUDE-G12H-V3-SF1 remain retained. Does not execute
   fixtures. Does not rewrite G07, G08, G09, G10, G12, G14,
   G15, G16, G18, G20, G21, G22, G31, or G32. Does not
   edit file 08. Does not invent a D9 code. Does not
   authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D221. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, or D-220.
