# D-224 — Record harness.DR-G24.preview-analyze-well-formed-admission.preview.v3 as G24 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-223. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-224**, not a register
> row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** execute NT-1 or NT-2 by existing.
> **Does not** reopen leftover-design of NT-1 and NT-2 as
> unnamed remainders.
> **Does not** treat naming v6 as naming G24.
> **Does not** close leftover-design of OBL-G24-FX-AUTHORING.
> **Does not** record frozen v1 or rejected v2 as a current
> occupancy remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G19, G20, G21, G22, G23, G31, or G32.
> **Does not** rewrite frozen G24 v1 or rejected G24 v2.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** invent a pack IR.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-223 is ADOPTED at
`ffe5bdd68fb57e2a2bd9ae12892ec16f817873b9`.
HEAD is `ffe5bdd68fb57e2a2bd9ae12892ec16f817873b9`.
Last live heading is D-223. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.review-independent.claude2.json` | `f7a606a781287a774b84eb4c1333596bb71de1fb1ebbcbfdbeb1456e4e995ea5` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.review-independent.codex.json` | `e816a9cb76acdcca7dbd0500e40ebcd3be0d4a4343de20b98dc9dfb39bab8324` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json | `ee41d14c7896ce97ebbf6611054991688ef1755499fbdc9d7f274498ebf9fdd4` |
| harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.review-independent.claude2.json | `f7a606a781287a774b84eb4c1333596bb71de1fb1ebbcbfdbeb1456e4e995ea5` |
| harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.review-independent.codex.json | `e816a9cb76acdcca7dbd0500e40ebcd3be0d4a4343de20b98dc9dfb39bab8324` |
| COORDINATOR-DECISIONS.md | `00e157e98adc0e7ca139b61437746864e59fbfeec24908f225f68ae0895caef8` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `ffe5bdd68fb57e2a2bd9ae12892ec16f817873b9` |
| Frozen v2 (rejected occupancy, not this subject) | `fb0a14c50c57aa1ebe67b069c328dfbe4693143f97e5be8a01c6bafbe5b9d399` |
| Frozen v1 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `9d8fb91395d683d40093c4e962f1e1e44cd0d0db84fce424e34eceeedb663ef3` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, frozen v2, frozen v1, and this draft
unmoved, re-measure before adoption. Append-only COORD after
this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G24 lead
token remains `OPEN`; DR-131 remains `OPEN`. v3's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G24 (D-150). Frozen v1 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Frozen v2 remains a
rejected occupancy. Naming parent is D-150 dual CONSENT, not
naming v6.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v1 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, leftoverDesignClosedIfAcceptedAndRecorded
OBL-G24-HARNESS-SPEC. After file 08 cardinality 28, g24
leftover-join.v3 (D-199) is the current G24 leftover-join.
leftover-join.v3 leftoverDesign remains
`[OBL-G24-FX-AUTHORING]`. Current INPUT basis as measured by
leftover-join.v3 is g24-input-corpus.v1. Occupancy v2 dual
REJECT on one shared class: Claude MF-1 / Codex
CODEX-G24-V2-SF1 (`$.doesNot[27]` still said required-now
26). v3 repairs that sentence to `Does not change live
required-now 28.` Dual independent ACCEPT 0/0 now exists.
This entry records v3. It is not SATISFIED-GRADE. v2 and v1
stay frozen; do not record them as current.

## Decision

1. Record
   `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json`
   as G24 occupancy remasurement after D-223. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 and rejected v2 are
   not recorded as a current occupancy remasurement.
2. DR-G24 stays `OPEN`. leftover-design of OBL-G24-HARNESS-SPEC,
   OBL-G24-NAMED-CORPUS, and OBL-G24-INPUT-CORPUS remains
   measured closed at leftover-join.v3 (D-199). leftover-design
   of OBL-G24-FX-AUTHORING remains. Remainder is G24
   execution once fixture implementations exist. Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   execute NT-1 or NT-2 by existing. Does not reopen
   leftover-design of NT-1 and NT-2 as unnamed remainders.
   Does not treat naming v6 as naming G24.
3. Does not SATISFY DR-131. Does not SATISFY DR-117. Does
   not SATISFY DR-133. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Occupancy v2 Claude returned advisories A-1 and A-2.
   Occupancy v2 Codex returned no advisories; its SHOULD-FIX
   CODEX-G24-V2-SF1 is the same class as Claude MF-1 and is
   repaired in v3. Occupancy v3 Claude Stage A returned
   zero advisories. Occupancy v3 Codex Stage A returned
   zero advisories and no observations. The Claude v2
   identifiers A-1 and A-2 are preserved. Codex v3 returned
   no observation identifiers. Does not execute fixtures.
   Does not rewrite G07, G08, G09, G10, G12, G14, G15, G16,
   G18, G19, G20, G21, G22, G23, G31, or G32. Does not
   rewrite frozen G24 v1 or rejected G24 v2. Does not edit
   file 08. Does not invent a D9 code. Does not invent a
   pack IR. Does not authorize `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D224. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, or D-223.
