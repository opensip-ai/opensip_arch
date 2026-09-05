# D-079 — Owner-record the DR-009 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-009, preview scope only, as v2 plus
> rider RB-DR009-V2-A1.
> **Does not** mark SATISFIED.
> **Does not** close LN-13, derivationDigest, R1-PARK-*, or CIR-B1.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record DR-006, DR-007, or any other row.

D-077 is ADOPTED at `d401ecd8494cd3e1b5f7b3553d9d9e6fed4dd9e5`
(DR-006 owner recording). It is not this file.

D-078 is ADOPTED at `17bbf202107e8f8fa78366ce5422fd53a1bf6363`
(DR-007 owner recording). This file does not adopt or overturn
D-077 or D-078.

D-080 is ADOPTED at `9b9b1e699db228370f52e90c3b9c7e38b217c838`
(one-locus pin correction of D-074's Codex verdict digest;
D-076 inherits that pin). This entry does not adopt or
overturn D-080.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, D-072, D-076, and D-080
  (pin correction inherited by D-076). Revocation or overturn
  requires this owner's supersession and reconciliation of
  dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-072 commit
  `5f6b4e07bb9293041e494ab08d74942878a5af97`
- Coordinator recording D-076 commit
  `13ca9a71a49d252c9acf7e37b9366c5a325003ad`
- Pin correction D-080 commit
  `9b9b1e699db228370f52e90c3b9c7e38b217c838`
- Disposition path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.json`
  sha256
  `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782`
  **plus operative rider RB-DR009-V2-A1** (D-076): applied head
  `docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.9.json`
  `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab`.
  Application of that head is still not park closure and is
  still not SATISFIED.
- Verdict path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459`
  ACCEPT-WITH-ADVISORIES 0 blockers, 1 advisory RBDR009V2-C2-A1
- Verdict path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.codex.json`
  sha256
  `2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f`
  ACCEPT 0/0
- Owner role (file 08): R-1/evidence authorities
- Scope: architecture preview (D-002 / D-018) only
- **Advisory classification (D-057 clause 3):** Claude 2
  RBDR009V2-C2-A1 is **operative**. It is carried as rider
  RB-DR009-V2-A1 (same form as D-039 / RB-DR005-V2-A1). Codex
  had no advisory. The rider does not close LN-13,
  derivationDigest, R1-PARK-*, or CIR-B1.

Measured inputs at authoring (re-measure at dispatch):

| Path | sha256 |
|---|---|
| COORD | `b329fdd056cb83fd0b475390aff1517bebf43345d481832264efd04019d5ad61` |
| D-078 commit | `17bbf202107e8f8fa78366ce5422fd53a1bf6363` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| D-077 commit | `d401ecd8494cd3e1b5f7b3553d9d9e6fed4dd9e5` |
| D-080 commit | `9b9b1e699db228370f52e90c3b9c7e38b217c838` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

## Route A remainder (from the pinned disposition)

- Close LN-13, `policyOutcome.derivationDigest`, and `R1-PARK-*`
- Reviewed retained validator or explicit accepted alternative
- CIR-B1 closure

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.json`
   plus rider RB-DR009-V2-A1 as the owner-recorded preview
   Route B disposition for DR-009.
2. This may discharge condition 1 for DR-009 within
   architecture-preview scope only.
3. Does not mark DR-009 SATISFIED. The Route A remainder above
   stays owed. Applied r1 v1.9 is not park closure. Conditions
   2–5 remain. Condition 5 remains the only implementation
   authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-006, DR-007, or any other row.

## Readiness effect

Condition 1 for DR-009 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D079, plus reconciliation of any later
MF-6 note under its own reviewed act. Revoking or overturning
D-054, D-057, or D-072 requires superseding this owner record.
Does not overturn D-072, D-076, D-080, D-077, D-078, D-054, or
D-057.
