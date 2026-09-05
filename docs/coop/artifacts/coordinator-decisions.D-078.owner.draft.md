# D-078 — Owner-record the DR-007 preview Route B disposition

> **Status:** DRAFT — not dispatchable until D-075 is ADOPTED
> and C-D075 is pinned below. Do not freeze or dispatch this
> file with an OWED commit pin.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-007, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** invent a D9 code.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record any other row.

Own cycle. D-077 and D-079 are other rows. D-057 clause 2
requires this entry's own D-000 cycle and commit. Same-commit
bundling with D-075 is forbidden.

Measured inputs (re-measure at dispatch; C-D075 is owed):

| Path | sha256 / standing |
|---|---|
| COORD (authoring; re-measure after D-075) | `ad6e24b251123f4b730d67e2c876fbfd173b61ccf084c9448335abad4d8f9855` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json` | `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7` |
| `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.claude2.json` | `aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.codex.json` | `807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55` ACCEPT 0/0 |
| live D9 contract | `8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-071. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-071 commit
  `5f6b4e07bb9293041e494ab08d74942878a5af97`
- Coordinator recording D-075 commit: **OWED**. Fill the full
  hash after C-D075. Do not dispatch this file until that pin
  is a real commit that records
  `route-b.DR-007.preview-disposition.v2.json`
  `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7`.
- Disposition path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json`
  sha256
  `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7`
- Verdict path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b`
- Verdict path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.codex.json`
  sha256
  `807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55`
- Owner role (file 08): D9 authority + evidence/retention owner.
- Scope: architecture preview (D-002 / D-018) only.
- Operative riders: none. Both v2 verdicts ACCEPT 0/0.

## Route A remainder (from the pinned disposition)

- D9 successor to v1.14 closing observation→faultCause,
  optional presence, success/policy/interrupted branch
- Reviewed retention degradation/refusal integration without
  invented codes
- Independent review of that successor

## Named D-002 rides this recording accepts

If this entry is adopted, doctor's D9 mapping (DR-114) and
containment goldens (DR-G21) that need the
observation→faultCause successor ship reduced, re-scoped, or
wait. Preview may still emit a D9 exit (D-018) using v1.14
without those closures. No D9 code is invented.

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for DR-007.
2. This may discharge condition 1 for DR-007 within
   architecture-preview scope only.
3. Does not mark DR-007 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-006, DR-009, or DR-011.

## Readiness effect

Condition 1 for DR-007 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D078, plus reconciliation of any later
MF-6 note. Does not overturn D-071, D-075, D-054, or D-057.
