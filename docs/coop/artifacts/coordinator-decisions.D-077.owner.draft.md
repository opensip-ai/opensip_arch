# D-077 — Owner-record the DR-006 preview Route B disposition

> **Status:** DRAFT — not dispatchable until D-074 is ADOPTED
> and C-D074 is pinned below. Do not freeze or dispatch this
> file with an OWED commit pin.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-006, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record any other row.

Own cycle. D-078 and D-079 are other rows. D-057 clause 2
requires this entry's own D-000 cycle and commit. Same-commit
bundling with D-074 is forbidden.

Measured inputs (re-measure at dispatch; C-D074 is owed):

| Path | sha256 / standing |
|---|---|
| COORD (authoring; re-measure after D-074) | `ad6e24b251123f4b730d67e2c876fbfd173b61ccf084c9448335abad4d8f9855` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.json` | `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161` |
| `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.review-independent.claude2.json` | `d1f309203ecee7a1c8aee9f0d1090e2885cc9e3feb4a0ad7d90dfe9046c9d1ab` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.review-independent.codex.json` | `821ce53f9b42ec98fb707dc5388864261782ac11e321ff81b40c431376349fc1` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-069. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-069 commit
  `5f6b4e07bb9293041e494ab08d74942878a5af97`
- Coordinator recording D-074 commit: **OWED**. Fill the full
  hash after C-D074. Do not dispatch this file until that pin
  is a real commit that records
  `route-b.DR-006.preview-disposition.v2.json`
  `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161`.
- Disposition path
  `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.json`
  sha256
  `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161`
- Verdict path
  `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `d1f309203ecee7a1c8aee9f0d1090e2885cc9e3feb4a0ad7d90dfe9046c9d1ab`
- Verdict path
  `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.review-independent.codex.json`
  sha256
  `821ce53f9b42ec98fb707dc5388864261782ac11e321ff81b40c431376349fc1`
- Owner role (file 08): Each identity-owning V1 surface +
  FACT-PLANE/evidence authorities + coordinator.
- Scope: architecture preview (D-002 / D-018) only.
- Operative riders: none. Both v2 verdicts ACCEPT 0/0.

## Route A remainder (from the pinned disposition)

- Binding per-surface identity recipes; freeze §7.1 PROPERTY
  is the boundary
- Phase-1A subject-set agreement
- Declared sufficiency view type and closed
  `rungUnavailableBecause` vocabulary
- Retained negative controls and exact derivation/custody joins
- Independent review of those recipes

## Named D-002 rides this recording accepts

If this entry is adopted, SARIF for `analyze` drops; rebuildable
cache/index keys stay conceptual; Coverage on the TypeScript
provider dispatch path stays conceptual; PlanId for the
TypeScript role stays conceptual. None of these survives on
prose (D-002 T2-04).

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for DR-006.
2. This may discharge condition 1 for DR-006 within
   architecture-preview scope only.
3. Does not mark DR-006 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-007, DR-009, or DR-011.

## Readiness effect

Condition 1 for DR-006 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D077, plus reconciliation of any later
MF-6 note. Does not overturn D-069, D-074, D-054, or D-057.
