# D-059 — Owner-record the DR-004 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-004, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record DR-002 or any other row.

Own cycle. D-058 already adopted at `21f0945` for DR-002.
This file is D-059 only.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `6f5557df175ed6873d40581a538ccf2449d6df04fbfb320c9884ad8ac466b365` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json` | `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76` |
| `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.claude2.json` | `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.codex.json` | `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-048. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-048 commit
  `aa75926d54d43d586c455809deb7832fba953aff`
- Coordinator recording D-050 commit
  `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`
- Disposition path
  `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json`
  sha256
  `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76`
- Verdict path
  `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e`
- Verdict path
  `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.codex.json`
  sha256
  `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3`
- Owner role (file 08): Evidence/retention authority
- Scope: architecture preview (D-002 / D-018) only
- Operative riders: none. D-050 recorded ACCEPT 0/0 with no
  rider. No ACCEPT-WITH-ADVISORIES advisories to classify.

## Route A remainder (from the pinned disposition)

- The exact eight-bullet packet inserted through the V1 process
  with retained proof, custody, joins, and status update
- Successor honesty on section31 v4 advisories S31V4-01,
  S31V4-02, S31V4-CX-A1, S31V4-CX-A2 (D-045)
- DR-002 AC-4 still names this packet

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for
   DR-004.
2. This may discharge condition 1 for DR-004 within
   architecture-preview scope only.
3. Does not mark DR-004 SATISFIED. The Route A remainder above
   stays owed. section31 v4 stays the binding instrument, not
   the packet. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-002, DR-003, DR-005, or DR-008.

## Readiness effect

Condition 1 for DR-004 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D059, plus reconciliation of any later
MF-6 note. Does not overturn D-048, D-050, D-054, or D-057.
