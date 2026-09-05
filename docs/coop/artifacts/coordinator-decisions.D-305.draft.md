# D-305 — Record harness.DR-G01.core-download.v11 as G01 occupancy remasurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-29
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of
> `harness.DR-G01.core-download.v11.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-170 through D-235 and D-237 through D-271 and D-273 through D-304. D-272 is CONTESTED and is not on that
> no-cell-edit adoption branch. Not a three-limb act. Not a
> required-now successor. Not SATISFIED-GRADE. This is
> coordinator decision **D-305**, not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** SATISFY DR-101.
> **Does not** SATISFY DR-117.
> **Does not** SATISFY DR-131.
> **Does not** SATISFY DR-133.
> **Does not** pin QUALIFIED.
> **Does not** open D-056 Class A.
> **Does not** record Class B SATISFIED.
> **Does not** execute fixtures.
> **Does not** author fixture bytes.
> **Does not** write a derived D-006 byte constant.
> **Does not** invent G02 tree-accounting.
> **Does not** mint Rust-as-core.
> **Does not** close leftover-design of OBL-2, OBL-D1, or OBL-D2.
> **Does not** take over G02, G03, G04, G05, G07, G14, or G22.
> **Does not** treat naming v6 as not naming G01.
> **Does not** treat leftover-join.v9 as parentReview.
> **Does not** occupy the DR-103 leftover-join.
> **Does not** record frozen G01 occupancy v1 through v10 as a current occupancy remasurement.
> **Does not** add a DR-G* row or change live required-now 28.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit COORD except the append-only adoption of this entry after CONSENT.

D-304 is ADOPTED at
`36252c1fb23ef1ed36ce109785df24519d1b87b6`.
HEAD is `36252c1fb23ef1ed36ce109785df24519d1b87b6`.
Last live heading is D-304. Required-now is 28.

Stage A dual independent ACCEPT 0/0 of the frozen
occupancy (not this draft):

| Reviewer | Path | sha256 | Verdict |
|---|---|---|---|
| Claude 2 | `docs/coop/artifacts/harness.DR-G01.core-download.v11.review-independent.claude2.json` | `abed5382612a3c8124686efe7f704803a64314398ca2dc93fbb687ec605d59a2` | ACCEPT 0/0 |
| Codex | `docs/coop/artifacts/harness.DR-G01.core-download.v11.review-independent.codex.json` | `5901b4c4225e759efcb9496614d238f95b6425c459f0bf1e22a71deaf866da0f` | ACCEPT 0/0 |

Stage A observation disposition (no change requested; no identifiers invented):

| Source | Identifiers | Standing |
|---|---|---|
| Claude | CLAUDE-G01H-V11-OBS1, CLAUDE-G01H-V11-OBS2, CLAUDE-G01H-V11-OBS3 | Claude Stage A G01 occupancy v11 returned 3 named observations objects (CLAUDE-G01H-V11-OBS1, CLAUDE-G01H-V11-OBS2, CLAUDE-G01H-V11-OBS3 have members id, ifATasteIsWanted, observation, severity, where, whyItDoesNotStand). Empty advisories list. Empty findings list. No mustFix field. No shouldFix field. No observationsNotFindings field |
| Codex | none | Codex Stage A G01 occupancy v11 returned an empty mustFix list; an empty shouldFix list; an empty advisories list; an empty observations list; an empty blockers list. No observationsNotFindings field |

This entry names the Claude identifiers CLAUDE-G01H-V11-OBS1, CLAUDE-G01H-V11-OBS2, CLAUDE-G01H-V11-OBS3; no identifier is invented. It does not claim that both reviewers' identifiers are preserved. Codex Stage A G01 occupancy v11 returned no observation identifiers.

Frozen G01 occupancy v10 was Claude ACCEPT 0/0 with observations CLAUDE-G01H-V10-OBS1, CLAUDE-G01H-V10-OBS2, CLAUDE-G01H-V10-OBS3, and Codex REJECT 1 unlabeled MUST-FIX (basedOn.d304.role last-heading custody only). G01 occupancy v11 lands that unlabeled Codex MUST-FIX. This entry does not invent an identifier for that unlabeled Codex MUST-FIX.

## Subject

`docs/coop/artifacts/harness.DR-G01.core-download.v11.json` `f95f0178430c04b655121dcc9b68031f160e6ccf493057a8e288eec79306aa94` — G01 occupancy remasurement of the already-named identifier harness.DR-G01.core-download after D-293 Decision 7 C9 (MB means 1e6 bytes for the D-006 G01/G02/G04 quantities) and after D-304. Status CANDIDATE-NOT-APPLIED. binds NOTHING. not QUALIFIED. Naming parent is naming v6 (D-145) dual ACCEPT 0/0. Current DR-101 leftover-join at dispatch is distribution-core leftover-join.v9 (D-287). leftoverDesign remains `[OBL-2, OBL-D1, OBL-D2]`. G01 size comparison to 25 MB is specified scorable under MB = 1e6 bytes per D-293. G01 occupancy v11 does not write a derived byte constant. G02 tree-accounting remains UNDECIDED. Q14 is named and is not answered by writing a constant. Frozen G01 occupancy v9 `f28b0d97723550c8690eec2a6ac7803efba93fd797f266600b038b14e269277b` remains the current recorded G01 occupancy remasurement at draft time (D-231). Frozen G01 occupancy v10 `77726037771cbc8eae2824f59c9e8d04336e0429fe8aa7ec32d54d1c9bf91eab` is unrecorded. Frozen G01 occupancy v1 remains the CGHS promised-path occupancy.

## Decision

Record harness.DR-G01.core-download.v11 as G01 occupancy remasurement after D-304. The candidate binds NOTHING. DR-G01 stays `OPEN`. leftover-design of the G01 specification-authoring limb of OBL-2 remains measured stale. leftover-design of OBL-2, OBL-D1, and OBL-D2 remains. Remainder of OBL-2 on distribution-core leftover-join.v9 is (a) D-006 unit and G02 tree-accounting UNDECIDED, so size comparison cannot be scored on that join, and (b) G01-G05 execution, which remains qualification (D-056). D-293 decided the unit; G01 occupancy v11 cites that unit so G01 size comparison is specified scorable under MB = 1e6 bytes; G02 tree-accounting remains UNDECIDED. Does not write a derived byte constant. Does not pin QUALIFIED. Does not invent fixture bytes. Does not mint Rust-as-core. Does not take over G02, G03, G04, G05, G07, G14, or G22. Does not SATISFY DR-101. Does not SATISFY DR-117. Does not SATISFY DR-131. Does not SATISFY DR-133. Gate 1 Class A is not opened. Class B SATISFIED is not recorded. Not SATISFIED. Required-now stays 28. Condition-4 effect is zero. Naming parent is naming v6 (D-145) dual ACCEPT 0/0. leftover-join.v9 is not parentReview. Frozen G01 occupancy v1 remains the CGHS promised-path occupancy. Frozen G01 occupancy v9 remains a historical occupancy remasurement recorded at D-231; after this successor is recorded, G01 occupancy v9 is not current. Frozen G01 occupancy v10 stays frozen and unrecorded; do not record it as current. The unlabeled Codex Stage A G01 occupancy v10 MUST-FIX is landed. Claude Stage A observations CLAUDE-G01H-V11-OBS1, CLAUDE-G01H-V11-OBS2, CLAUDE-G01H-V11-OBS3 travel as honesty work. Advisory CLAUDE-G01H-V9-ADV1 travels as honesty work. Codex Stage A G01 occupancy v11 returned no observation identifiers. Does not invent an identifier for the unlabeled Codex G01 occupancy v10 MUST-FIX. Does not execute fixtures. Does not rewrite G02, G03, G04, G05, G07, G08, G09, G10, G12, G14, G15, G16, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31, or G32. Does not rewrite frozen G01 occupancy v1 through v10. Does not edit file 08. Does not invent a D9 code. Does not authorize `docs/v2/implementation/`.

## Readiness effect

Zero SATISFIED. Condition 2 stays 5 of 32. Condition 4 stays MET on the naming half (28 of 28). Condition 5 last.

## Reversibility

Total only before a later dependent leftover rewrite, SATISFIED cycle, or file-08 cell rewrite. Overturn: C-D305. Does not unwrite D-086, D-145, D-173, D-231, D-287, D-293, D-294, or D-304.
