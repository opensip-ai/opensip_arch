# D-225 — Record harness.DR-G25.preview-analyze-missing-rung.preview.v3 as G25 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-22
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G25.preview-analyze-missing-rung.preview.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-224. Not a three-limb act. Not a
> required-now successor.
> This is coordinator decision **D-225**, not a register
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
> **Does not** execute NT-3 by existing.
> **Does not** reopen leftover-design of DR-131 NT-3 as an
> unnamed remainder.
> **Does not** collapse the two NT-3 cells.
> **Does not** take over G23 DR-133 NT-3.
> **Does not** treat naming v6 as naming G25.
> **Does not** close leftover-design of OBL-G25-FX-AUTHORING.
> **Does not** record frozen v1 or v2 as a current occupancy
> remasurement.
> **Does not** add a DR-G* row or change required-now 28.
> **Does not** rewrite G07, G08, G09, G10, G12, G14, G15,
> G16, G18, G19, G20, G21, G22, G23, G24, G31, or G32.
> **Does not** rewrite frozen G25 v1 or frozen G25 v2.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-224 is ADOPTED at
`cb25125b9675b9149e74db37f5dfd0bc4f78e404`.
HEAD is `cb25125b9675b9149e74db37f5dfd0bc4f78e404`.
Last live heading is D-224. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G25.preview-analyze-missing-rung.preview.v3.review-independent.claude2.json` | `1d7ccc76ddbd06298a5734362508153ca6f7f5781d0d1ec1834cd6f881e5d863` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G25.preview-analyze-missing-rung.preview.v3.review-independent.codex.json` | `09f78d505b7bbb76987f020c5bf1fd87e66837f4796a2ed3dbd9dfd9d28059cb` | ACCEPT 0/0 |

Measured inputs:

| Path | sha256 |
|---|---|
| harness.DR-G25.preview-analyze-missing-rung.preview.v3.json | `4f124cd763974b603fb307e13830cc7f79bc559c3b05ab7d39c59194d2f5dfde` |
| harness.DR-G25.preview-analyze-missing-rung.preview.v3.review-independent.claude2.json | `1d7ccc76ddbd06298a5734362508153ca6f7f5781d0d1ec1834cd6f881e5d863` |
| harness.DR-G25.preview-analyze-missing-rung.preview.v3.review-independent.codex.json | `09f78d505b7bbb76987f020c5bf1fd87e66837f4796a2ed3dbd9dfd9d28059cb` |
| COORDINATOR-DECISIONS.md | `fa6f59a5b9c08c54b5648b0032a3f91c9bce02172aa0cd0c21180a859b8f52fb` |
| file 08 | `f909ddff7f3a8e9be864259808c4a2320170181001bdb746814b07393dd9d5e1` |
| HEAD | `cb25125b9675b9149e74db37f5dfd0bc4f78e404` |
| Frozen v2 (historical occupancy at HEAD `5d5d778` / required-now 26, not this subject) | `6d066ef5e78059dfd19e3828d45bcc211df0ad8e328c909d3ad69b3123090113` |
| Frozen v1 (not this subject) | `7ac3ddfdec91003db821020891fcd96ed7c4f0877cb5813d48b1e2eddc125248` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
Stage A verdicts, frozen v2, frozen v1, and this draft
unmoved, re-measure before adoption. Append-only COORD after
this remeasurement, with those files unmoved, is
**PASS-NO-SCOPE-EFFECT** and is not a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

Live remeasurement at draft time: required-now 28 of 28
named; owners 32 of 32; last gate row DR-G32; DR-G25 lead
token remains `OPEN`; DR-131 remains `OPEN`. v3's top-level
head, recordedInputs.HEAD, file08Pin, and
requiredNowUnchanged equal those live values. File 08
carries G25 (D-151). Frozen v2 remains a historical occupancy
as of HEAD `5d5d778` / required-now 26. Naming parent is
D-151 dual CONSENT, not naming v6.

This is a gate-row COORD draft. It does not claim that D-056
gates 2 and 3 do not hold.

## Why this entry exists

Frozen v2 asserted required-now 26, HEAD `5d5d778`, file 08
`3a9442d1`, and `Does not change required-now 26.` After
file 08 cardinality 28, g25 leftover-join.v3 (D-200) is the
current G25 leftover-join. leftover-join.v3 leftoverDesign
remains `[OBL-G25-FX-AUTHORING]`. Current INPUT basis as
measured by leftover-join.v3 is g25-input-corpus.v1. Dual
independent ACCEPT 0/0 now exists. This entry records v3.
It is not SATISFIED-GRADE. v2 and v1 stay frozen; do not
record them as current.

## Decision

1. Record
   `harness.DR-G25.preview-analyze-missing-rung.preview.v3.json`
   as G25 occupancy remasurement after D-224. The candidate
   binds NOTHING. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX. Frozen v1 and frozen v2 are
   not recorded as a current occupancy remasurement.
2. DR-G25 stays `OPEN`. leftover-design of OBL-G25-HARNESS-SPEC,
   OBL-G25-NAMED-CORPUS, and OBL-G25-INPUT-CORPUS remains
   measured closed at leftover-join.v3 (D-200). leftover-design
   of OBL-G25-FX-AUTHORING remains. Remainder is G25
   execution once fixture implementations exist. Does not
   pin QUALIFIED. Does not invent fixture bytes. Does not
   execute NT-3 by existing. Does not reopen leftover-design
   of DR-131 NT-3 as an unnamed remainder. Does not collapse
   the two NT-3 cells. Does not take over G23 DR-133 NT-3.
   Does not treat naming v6 as naming G25.
3. Does not SATISFY DR-131. Does not SATISFY DR-117. Does
   not SATISFY DR-133. Gate 1 Class A is not opened. Class B
   SATISFIED is not recorded. Not SATISFIED. Required-now
   stays 28. Condition-4 effect is zero. Condition 4 stays
   MET at 28 of 28 / 32 of 32.
4. Claude Stage A returned three unlabeled
   observationsNotFindings. They carry no identifier. Codex
   Stage A returned zero advisories and no observations.
   Does not invent identifiers for those unlabeled
   observations. Does not execute fixtures. Does not rewrite
   G07, G08, G09, G10, G12, G14, G15, G16, G18, G19, G20,
   G21, G22, G23, G24, G31, or G32. Does not rewrite frozen
   G25 v1 or frozen G25 v2. Does not edit file 08. Does not
   invent a D9 code. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (28 of 28). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
SATISFIED cycle, or file-08 cell rewrite. Overturn:
C-D225. Does not unwrite D-167, D-168, D-169, D-170,
D-171, D-172, D-173, D-174, D-175, D-176, D-177, D-178,
D-179, D-180, D-181, D-182, D-183, D-184, D-185, D-186,
D-187, D-188, D-189, D-190, D-191, D-192, D-193, D-194,
D-195, D-196, D-197, D-198, D-199, D-200, D-201, D-202,
D-203, D-204, D-205, D-206, D-207, D-208, D-209, D-210,
D-211, D-212, D-213, D-214, D-215, D-216, D-217, D-218,
D-219, D-220, D-221, D-222, D-223, or D-224.
