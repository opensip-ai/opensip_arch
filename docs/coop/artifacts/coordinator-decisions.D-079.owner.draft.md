# D-079 — Owner-record the DR-009 preview Route B disposition

> **Status:** DRAFT — not dispatchable until D-076 is ADOPTED
> and C-D076 is pinned below. Do not freeze or dispatch this
> file with an OWED commit pin.
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
> **Does not** owner-record any other row.

Own cycle. D-077 and D-078 are other rows. D-057 clause 2
requires this entry's own D-000 cycle and commit. Same-commit
bundling with D-076 is forbidden.

Measured inputs (re-measure at dispatch; C-D076 is owed):

| Path | sha256 / standing |
|---|---|
| COORD (authoring; re-measure after D-076) | `ad6e24b251123f4b730d67e2c876fbfd173b61ccf084c9448335abad4d8f9855` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.json` | `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782` |
| `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.claude2.json` | `b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459` ACCEPT-WITH-ADVISORIES 0 blockers, 1 advisory RBDR009V2-C2-A1 |
| `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.codex.json` | `2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f` ACCEPT 0/0 |
| r1 v1.9 | `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-072. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-072 commit
  `5f6b4e07bb9293041e494ab08d74942878a5af97`
- Coordinator recording D-076 commit: **OWED**. Fill the full
  hash after C-D076. Do not dispatch this file until that pin
  is a real commit that records
  `route-b.DR-009.preview-disposition.v2.json`
  `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782`
  plus rider RB-DR009-V2-A1.
- Disposition path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.json`
  sha256
  `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782`
- Verdict path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `b4c593688fca2de24ddf7f0bdacd7c2610bd517176f35aacf4123e1d0b1c6459`
- Verdict path
  `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.review-independent.codex.json`
  sha256
  `2401819f4078dea4e470c8b7c15cd4d519580c1db3a24e3b874fb63538e9aa9f`
- Owner role (file 08): R-1/evidence authorities.
- Scope: architecture preview (D-002 / D-018) only.
- **Advisory classification (D-057 clause 3):** Claude 2
  RBDR009V2-C2-A1 is **operative**. It is carried as rider
  RB-DR009-V2-A1 (same form as D-039 / RB-DR005-V2-A1). Codex
  had no advisory. The rider does not close LN-13,
  derivationDigest, R1-PARK-*, or CIR-B1.

## Operative rider RB-DR009-V2-A1

The disposition this owner records is v2 plus: the applied
lineage head named by v2 is
`docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.9.json`
`37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab`.
Application of that head is still not park closure and is
still not SATISFIED.

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
5. Does not owner-record DR-006, DR-007, or DR-011.

## Readiness effect

Condition 1 for DR-009 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D079, plus reconciliation of any later
MF-6 note. Does not overturn D-072, D-076, D-054, or D-057.
