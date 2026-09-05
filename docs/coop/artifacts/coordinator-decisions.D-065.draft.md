# D-065 — Owner-record the DR-003 scoped preview TM

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. One owner-recording
> entry. Own commit.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-003, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record DR-002, DR-004, DR-005, or DR-008.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `540587a4411be79385ac386d475802ab7ed60f5a77b1b13999d3b8f36f4e7d29` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.json` | `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52` |
| `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.claude2.json` | `69b201e0916ac825f6326b9aad250bf3140eb2b1e9b7d078f38f5fa83a3a0ebf` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.codex.json` | `151be2a2367553fe7ad1d21a58859368008d9ae3f604000eb22b56e9086730ef` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-030. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-030 commit
  `d5721222623faa854d85282df408de1c5005d19f`
- Coordinator recording D-041 commit
  `56973db89be3539ff59c0d669aa794d2ddbabc6e`
- Disposition path
  `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.json`
  sha256
  `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52`
- Verdict path
  `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.claude2.json`
  sha256
  `69b201e0916ac825f6326b9aad250bf3140eb2b1e9b7d078f38f5fa83a3a0ebf`
- Verdict path
  `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.review-independent.codex.json`
  sha256
  `151be2a2367553fe7ad1d21a58859368008d9ae3f604000eb22b56e9086730ef`
- Owner role (file 08): Threat-model authority + V1 coordinator
- Scope: architecture preview (D-002 / D-018) only
- Operative riders: none.

## Route A remainder (from the pinned disposition)

- Reviewed closure of V10/custody and G19
- Publication block satisfied by required demonstration
- Final TM disposition for the authoritative product

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.json`
   as the owner-recorded scoped preview TM for DR-003.
2. This may discharge condition 1 for DR-003 within
   architecture-preview scope only. Not a security-complete
   claim. TM stays UNSET for the freeze.
3. Does not mark DR-003 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-002, DR-004, DR-005, or DR-008.

## Readiness effect

Condition 1 for DR-003 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D065, plus reconciliation of any later
MF-6 note. Does not overturn D-030, D-041, D-054, or D-057.
