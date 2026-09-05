# D-058 — Owner-record the DR-002 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3. This file is one
> owner-recording entry and one cycle.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-002, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record DR-004 or any other row.

Turn-1 combined subject `coordinator-decisions.D-058-059.draft.md`
`81b67b5b41edcd0cf5f9db94d11519ad456104e20f5ae43e6444138b9522db1e`
OBJECTED. Claude 2 SHOULD-FIX C2-D058059-01. Codex MUST-FIX
ADV-D058-059-T1-01 (own cycle) and ADV-D058-059-T1-02 (verdict
paths and full Route-A remainder). This file is D-058 only.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D058-059-T1-01 | MUST-FIX | ACCEPTED. This file is D-058 only. |
| ADV-D058-059-T1-02 | MUST-FIX | ACCEPTED. Full paths and full Route-A remainder. |
| C2-D058059-01 | SHOULD-FIX | ACCEPTED. Same. |

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `de897fd68e1efdcbf649d1c91cd4e410fb2b2c4db7a2980e39bb9112518d637b` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json` | `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06` |
| `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.claude2.json` | `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1` ACCEPT 0/0 |
| `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.codex.json` | `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485` ACCEPT 0/0 |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, and D-047. Revocation or
  overturn requires this owner's supersession and
  reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-047 commit
  `aa75926d54d43d586c455809deb7832fba953aff`
- Coordinator recording D-049 commit
  `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`
- Disposition path
  `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json`
  sha256
  `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06`
- Verdict path
  `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1`
- Verdict path
  `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.review-independent.codex.json`
  sha256
  `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485`
- Owner role (file 08): Evidence authority + V1 coordinator
- Scope: architecture preview (D-002 / D-018) only
- Operative riders: none. D-049 recorded ACCEPT 0/0 with no
  rider. No ACCEPT-WITH-ADVISORIES advisories to classify.

## Route A remainder (from the pinned disposition)

- Focused independent AC-1 adjudication
- Repaired validator successor plus claim-register motion (AC-3)
- Eight-bullet Phase-1A packet (AC-4 / DR-004)
- Full V10 / G19 / publication-block (not this row's close;
  D-030 / D-028)

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for
   DR-002.
2. This may discharge condition 1 for DR-002 within
   architecture-preview scope only.
3. Does not mark DR-002 SATISFIED. The Route A remainder above
   stays owed. Conditions 2–5 remain. Condition 5 remains the
   only implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-003, DR-004, DR-005, or DR-008.

## Readiness effect

Condition 1 for DR-002 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D058, plus reconciliation of any later
MF-6 note. Does not overturn D-047, D-049, D-054, or D-057.
