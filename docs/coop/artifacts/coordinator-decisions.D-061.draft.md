# D-061 — Owner-record the DR-008 integration-half preview disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-008's EVIDENCE/D9 integration half,
> preview scope only.
> **Does not** mark SATISFIED.
> **Does not** reopen the posture half.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record any other row.

Own cycle. D-058, D-060, D-064, and D-065 are other rows.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `3ef58dde184e8012a884e149e94e0a25b9edf1eb9488e9de24e1b25e8c9522d1` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.json` | `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c` |
| `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.claude2.json` | `adc954fd99f03b61b5613e06fe63968fc2feecf70fdf83e12c3939feff772ac5` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.codex.json` | `a96987960d99cf0bde80d5f86a6d7ce244545eab1235788432246c2be4aebcb4` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-029. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-029, C-D029, first COORD appearance
  commit `d5721222623faa854d85282df408de1c5005d19f`
- Coordinator recording D-040 commit
  `56973db89be3539ff59c0d669aa794d2ddbabc6e`
- Disposition path
  `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.json`
  sha256
  `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c`
- Verdict path
  `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `adc954fd99f03b61b5613e06fe63968fc2feecf70fdf83e12c3939feff772ac5`
- Verdict path
  `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.review-independent.codex.json`
  sha256
  `a96987960d99cf0bde80d5f86a6d7ce244545eab1235788432246c2be4aebcb4`
- Owner role (file 08): evidence/retention authority (contract
  half). Product owner remains the posture owner.
- Scope: architecture preview (D-002 / D-018) only;
  EVIDENCE/D9 integration half only.
- Operative riders: none. Both v2 verdicts ACCEPT 0/0.

## Route A remainder (from the pinned disposition)

- Evidence-side successor consuming retention AND Phase-1A
  (D-029)
- The §3.1 supplier-coverage instrument (Lane R; not this
  disposition)
- Full V10 / G19 / publication-block (D-030: D-028 does not
  discharge that; this entry does not either)

## Decision

1. As the named file-08 contract-half owner under D-054,
   record
   `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for
   DR-008's EVIDENCE/D9 integration half only. Posture half
   stays closed.
2. This may discharge condition 1 for that half within
   architecture-preview scope only. The posture half is
   already closed and is not re-opened or re-satisfied here.
3. Does not mark DR-008 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-002, DR-003, DR-004, or DR-005.

## Readiness effect

Condition 1 for DR-008's integration half may discharge within
preview scope. Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D061, plus reconciliation of any later
MF-6 note. Does not overturn D-029, D-040, D-054, or D-057.
