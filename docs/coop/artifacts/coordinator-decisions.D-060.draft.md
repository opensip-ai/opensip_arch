# D-060 — Owner-record the DR-005 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-005, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record any other row.

Own cycle. D-058 adopted for DR-002. D-059 is CONTESTED and is
not this file.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `e53567c03e5d470547406c115645bcb32266600c9f0aba40b65436e936a2df23` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.json` | `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809` |
| `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.claude2.json` | `479b3a191703746355accc9da819e058d772b4efbcc8ee81bdfadd4e8887de5b` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.codex.json` | `4dc772dec715277aac1b6058a374d88d6ec9dd363eb8a7e04ea8ed2927f9b4aa` ACCEPT-WITH-ADVISORIES 0 blockers |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-028. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-028, C-D028, first COORD appearance
  commit `d5721222623faa854d85282df408de1c5005d19f`
- Coordinator recording D-039 commit
  `7e7a63687c49092df4622949cd80825cb4a4e681`
- Disposition path
  `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.json`
  sha256
  `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809`
- Verdict path
  `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `479b3a191703746355accc9da819e058d772b4efbcc8ee81bdfadd4e8887de5b`
- Verdict path
  `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.review-independent.codex.json`
  sha256
  `4dc772dec715277aac1b6058a374d88d6ec9dd363eb8a7e04ea8ed2927f9b4aa`
- Owner role (file 08): Evidence, storage, and operability
  authorities
- Scope: architecture preview (D-002 / D-018) only
- **Operative rider (D-039 / D-057):** RB-DR005-V2-A1 is
  operative disposition text. If the Operational metadata class
  is denied, doctor fails closed (D-032 BLK-6). This
  disposition supplies no grant or class admission. Owners
  record v2 plus this rider.
- **ACCEPT-WITH-ADVISORIES classification:** Codex advisory
  RB-DR005-V2-A1 is OPERATIVE (carried as the D-039 rider).
  Claude 2 returned ACCEPT 0/0; no further advisories.

## Route A remainder (from the pinned disposition)

- Applied evidence/retention/D9 integration
- Executable custody
- Durable-authoritative negative controls for G19
- Full V10 / publication-block demonstration (D-028 and D-030
  both say D-028 does not discharge that)

## Decision

1. As the named file-08 owners under D-054, record
   `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.json`
   **plus** rider RB-DR005-V2-A1 as the owner-recorded preview
   Route B disposition for DR-005.
2. This may discharge condition 1 for DR-005 within
   architecture-preview scope only.
3. Does not mark DR-005 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-002, DR-003, DR-004, or DR-008.

## Readiness effect

Condition 1 for DR-005 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D060, plus reconciliation of any later
MF-6 note. Does not overturn D-028, D-039, D-054, or D-057.
