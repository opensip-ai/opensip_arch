# D-058 / D-059 turn 2 — Owner-record DR-002 and DR-004

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Two severable owner-recording
> entries under D-054 / D-057.
> **Does** owner-record, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.

New frozen path. Turn-1 subject `81b67b5b…` is history.
C2-D058059-01 accepted: verdict and disposition pins now use
paths, not labels or bare filenames.

Adopting or overturning one does not adopt or overturn the other.

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `de897fd68e1efdcbf649d1c91cd4e410fb2b2c4db7a2980e39bb9112518d637b` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json | `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06` |
| docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.claude2.json | `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1` ACCEPT 0/0 |
| docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.codex.json | `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485` ACCEPT 0/0 |
| docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json | `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76` |
| docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.claude2.json | `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e` ACCEPT 0/0 |
| docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.codex.json | `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## D-058 — Owner-record the DR-002 preview Route B disposition

- **Dependencies (D-057 clause 3):** D-054, D-057, and D-047.
  Revocation or overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- **Authority pins:**
  - D-054 `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
    `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
    commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
  - D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
  - Route B selection D-047 commit
    `aa75926d54d43d586c455809deb7832fba953aff`
  - Coordinator recording D-049 commit
    `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`
- **Disposition path:** `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json`
  `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06`
- **Verdict paths:**
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.claude2.json`
    `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1`
    ACCEPT 0/0
  - `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.codex.json`
    `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485`
    ACCEPT 0/0
- **Owner role (file 08):** Evidence authority + V1 coordinator
- **Operative riders:** none. D-049 recorded ACCEPT 0/0 with no
  rider. No ACCEPT-WITH-ADVISORIES advisories to classify.
- **Severable:** adopting or overturning this entry does not
  change D-059.

### Decision

1. As the named file-08 owner under D-054, record the v2
   disposition as the owner-recorded preview Route B
   disposition for DR-002.
2. This may discharge condition 1 for DR-002 within
   architecture-preview scope only.
3. Does not mark DR-002 SATISFIED. AC-1, AC-3, and AC-4 stay
   owed on Route A. Conditions 2–5 remain. Condition 5 remains
   the only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.

### Readiness effect

Condition 1 for DR-002 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

### Reversibility

Compound. Overturn: C-D058, plus reconciliation of any later
MF-6 note. Does not overturn D-047, D-049, D-054, or D-057.

## D-059 — Owner-record the DR-004 preview Route B disposition

- **Dependencies (D-057 clause 3):** D-054, D-057, and D-048.
  Revocation or overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- **Authority pins:**
  - D-054 `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
    `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
    commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
  - D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
  - Route B selection D-048 commit
    `aa75926d54d43d586c455809deb7832fba953aff`
  - Coordinator recording D-050 commit
    `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`
- **Disposition path:** `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json`
  `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76`
- **Verdict paths:**
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.claude2.json`
    `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e`
    ACCEPT 0/0
  - `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.review-independent.codex.json`
    `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3`
    ACCEPT 0/0
- **Owner role (file 08):** Evidence/retention authority
- **Operative riders:** none. D-050 recorded ACCEPT 0/0 with no
  rider. No ACCEPT-WITH-ADVISORIES advisories to classify.
- **Severable:** adopting or overturning this entry does not
  change D-058.

### Decision

1. As the named file-08 owner under D-054, record the v2
   disposition as the owner-recorded preview Route B
   disposition for DR-004.
2. This may discharge condition 1 for DR-004 within
   architecture-preview scope only.
3. Does not mark DR-004 SATISFIED. The eight-bullet Phase-1A
   packet stays owed on Route A. section31 v4 stays the
   binding instrument, not the packet. Conditions 2–5 remain.
   Condition 5 remains the only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.

### Readiness effect

Condition 1 for DR-004 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

### Reversibility

Compound. Overturn: C-D059, plus reconciliation of any later
MF-6 note. Does not overturn D-048, D-050, D-054, or D-057.
