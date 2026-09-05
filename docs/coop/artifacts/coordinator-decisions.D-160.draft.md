# D-160 — Record distribution-core-leftover-join.v3 as DR-101 leftover-design measurement

> **Status:** DRAFT — under review.
> **Date:** 2026-08-16
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT of `distribution-core-leftover-join.v3.json`
> (0 blockers, 0 SHOULD-FIX). Same no-cell-edit branch as
> D-155 / D-148. This is coordinator decision **D-160**,
> not a register row.
> **Does not** mark any row SATISFIED.
> **Does not** open D-056 Class A.
> **Does not** close leftover-design.
> **Does not** make D-056 gates 2 or 3 hold for DR-101.
> **Does not** add a DR-G* row or change requiredNow (26).
> **Does not** decide OD-101-1 or mint Rust-as-core.
> **Does not** decide OD-101-2 ceremony or notarization.
> **Does not** invent G01-G05 harness specifications.
> **Does not** retarget D-159.
> **Does not** edit file 08.
> **Does not** invent a D9 code.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** mint a D-096 (A) grant.
> **Does not** edit COORD except the append-only adoption
> of this entry after CONSENT.

D-159 is ADOPTED at `19b52312e27fcb71d67b514d18309625ad0b254c`.
HEAD is `19b52312e27fcb71d67b514d18309625ad0b254c`.

Measured inputs:

| Path | sha256 |
|---|---|
| distribution-core-leftover-join.v3.json | `808eeb93c53fbdd88de56e455db25c0821402a30643c6e4fce05cf339c7ee3c4` |
| Claude 2 v3 verdict | `52ba8a1f173fe47e672d8ff3936c5ecc559788b9f894d8a3c5932282bdcab07c` ACCEPT, 0/0 |
| Codex v3 verdict | `4cc622f7f8eb3b851460c557c3f9f38c533fc24a834bb9c772995d460bd33525` ACCEPT, 0/0 |
| distribution-core-inventory-contract.v16.json | `429b8c7a9cd5c8f2b495337c055ccbd262e796ba1cc42efb173779c72018fb5b` |
| COORDINATOR-DECISIONS.md | `f820a5857cede8b2079e8874c2fb65e40c648275c1ec4db6662bdeadeb10e850` |
| file 08 | `3a9442d1761864de59f103374489a9fbffdd12cc4ba39ddd7c7f491f64357e44` |
| D-159 commit | `19b52312e27fcb71d67b514d18309625ad0b254c` |
| HEAD | `19b52312e27fcb71d67b514d18309625ad0b254c` |

If a cited file moves in a way that is not append-only COORD
growth or COORD heading hygiene, with file 08, v3, both
verdicts, v16, and this draft unmoved, re-measure before
adoption. Append-only COORD after this remeasurement, with
those files unmoved, is **PASS-NO-SCOPE-EFFECT** and is not
a MUST-FIX.

"File 08" means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Why this entry exists

D-114 recorded distribution-core-inventory-contract.v16 and
left DR-101 leftover-design / OPEN. D-139 L authorizes
drafting that leftover-design closure. Join v3 received
independent dual ACCEPT at 0 blockers and 0 SHOULD-FIX after
Codex REJECT of v1 (DCLJ-V1-B1, DCLJ-V1-SF1). This entry
records that measurement. It does not add a row and does
not SATISFY DR-101.

## Decision

1. Record `distribution-core-leftover-join.v3.json` as
   DR-101 leftover-design measurement. The candidate binds
   NOTHING. Both independent reviewers returned 0 blockers
   and 0 SHOULD-FIX.
2. DR-101 stays `OPEN`. Leftover-design is not closed.
   OBL-2 (unauthored G01-G05 harness specifications),
   OBL-D1 / OD-101-1 (core implementation language), and
   OBL-D2 / OD-101-2 (signing/notarization ceremony)
   remain leftover-design. OBL-1, OBL-D-INV, OBL-D-LAY,
   and OBL-D3 are specified on v16 and capable-of-riding
   the already-named G01-G05 identifiers. This entry does
   not invent those harness specifications and does not
   decide language or ceremony.
3. D-056 Class A is not opened. Gates 2 and 3 do not
   hold for DR-101. No SATISFIED. Required-now stays 26.
   D-159's gates-2/3 holding for DR-117 is not retargeted.
4. Live G01-G05 owners remain as measured: G01/G03/G04
   Release engineering; G02 Architecture + release; G05
   Component publisher + release. This entry does not
   rewrite those cells.
5. Does not edit file 08. Does not authorize
   `docs/v2/implementation/`.

### Readiness effect

Zero SATISFIED. Condition 2 stays 4 of 32. Condition 4
stays MET on the naming half (26 of 26). Condition 5 last.

### Reversibility

Total only before a later dependent leftover rewrite,
naming successor, harness-spec authoring, or SATISFIED
cycle. Overturn: C-D160. Does not unwrite D-114, D-157,
D-158, or D-159.
