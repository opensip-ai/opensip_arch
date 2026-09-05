# D-078 — Owner-record the DR-007 preview Route B disposition

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a new
> cycle. Frozen turn-1 subject is not edited.
> **Decision type:** RULE-GOVERNED. Owner recording under D-054 /
> D-057.
> **Does** owner-record DR-007, preview scope only.
> **Does not** mark SATISFIED.
> **Does not** edit file 08.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** owner-record DR-006, DR-009, or any other row.

Turn-1 subject `coordinator-decisions.D-078.draft.md`
`f4184bab55bc6870afca039e12e1cfa0d67f6aa81956bae070c310b75729504f`
held frozen. Claude 2 OBJECT, 0 MUST-FIX, 1 SHOULD-FIX
C2-D078-SF1. Codex OBJECTIONS, 1 MUST-FIX ADV-D078-01.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D078-01 | MUST-FIX | ACCEPTED. D-054 path added. Reversibility names supersession of this record if D-054, D-057, or D-071 is revoked, plus MF-6 reconciliation. |
| C2-D078-SF1 | SHOULD-FIX | ACCEPTED. Same pin completeness as D-077 turn 2: D-054 path, revocation sentence, MF-6 limb, Conditions 2–5 unchanged. |

D-077 is ADOPTED at `d401ecd8494cd3e1b5f7b3553d9d9e6fed4dd9e5`
(DR-006 owner recording). It is not this file. This entry does
not adopt or overturn D-077.

## Authority and dependency pins (D-057 clause 3)

- **Dependencies:** D-054, D-057, D-071, and D-075. Revocation
  or overturn of D-054, D-057, or D-071 requires this owner's
  supersession and reconciliation of dependent MF-6 notes.
- D-054 path
  `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
  sha256
  `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f`
  commit `29670ed29104f5f9e855c10206501e2f5e31ef6e`
- D-057 commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5`
- Route B selection D-071 commit
  `5f6b4e07bb9293041e494ab08d74942878a5af97`
- Coordinator recording D-075 commit
  `13ca9a71a49d252c9acf7e37b9366c5a325003ad`
- Disposition path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json`
  sha256
  `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7`
- Verdict path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.claude2.json`
  sha256
  `aa70e15095561c970853ef2a413759d4dedc8862a627986f7bed6b6e047f235b`
  ACCEPT 0/0
- Verdict path
  `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.review-independent.codex.json`
  sha256
  `807d0b630e1b2a23e16c7aacd8fa23e208ad0a102151f8a634590cc65464dc55`
  ACCEPT 0/0
- Owner role (file 08): D9 authority + evidence/retention owner
- Scope: architecture preview (D-002 / D-018) only
- Operative riders: none.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `ac159ae36e98e84eea7c9292baab89dd0a11d120e8caba4a4726608effe5f01b` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| D-077 commit | `d401ecd8494cd3e1b5f7b3553d9d9e6fed4dd9e5` |
| turn-1 subject | `f4184bab55bc6870afca039e12e1cfa0d67f6aa81956bae070c310b75729504f` |
| Claude 2 turn 1 | `76de9ca64548c32097e4c3486746e9ce3c02dac9dc71ba6c6596266a2ac25f02` |
| Codex turn 1 | `edb2c08554ff19f8fae35af7129900c54f8175f864d9fc5113187c735796a6d7` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

## Route A remainder (from the pinned disposition)

- D9 successor to v1.14 closing observation→faultCause, optional
  presence, success/policy/interrupted branch
- Reviewed retention degradation/refusal integration without
  invented codes
- Independent review of that successor

## Decision

1. As the named file-08 owner under D-054, record
   `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json`
   as the owner-recorded preview Route B disposition for
   DR-007.
2. This may discharge condition 1 for DR-007 within
   architecture-preview scope only.
3. Does not mark DR-007 SATISFIED. Invents no D9 code. The
   Route A remainder above stays owed. Doctor D9 mapping
   (DR-114) and DR-G21 goldens ship reduced, re-scoped, or
   wait. Conditions 2–5 remain. Condition 5 remains the only
   implementation authorization.
4. Does not edit file 08 (MF-6). A later cell note is a
   separate act.
5. Does not owner-record DR-006, DR-009, or any other row.

## Readiness effect

Condition 1 for DR-007 may discharge within preview scope.
Zero SATISFIED. Conditions 2–5 unchanged.

## Reversibility

Compound. Overturn: C-D078, plus reconciliation of any later
MF-6 note under its own reviewed act. Revoking or overturning
D-054, D-057, or D-071 requires superseding this owner record.
Does not overturn D-077, D-071, D-075, D-054, or D-057.
