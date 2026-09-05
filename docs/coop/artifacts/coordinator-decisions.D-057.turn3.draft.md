# D-057 turn 3 — Mechanics for D-054 preview-scope owner recording

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 3 of 3.
> **Decision type:** RULE-GOVERNED. Mechanics only. Authority is
> user-made adopted D-054, not this file.
> **Does not** grant owner authority.
> **Does not** mark SATISFIED. **Does not** record any row.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit file 08.
> **Does not** adopt a product-boundary successor.

New frozen path. Turn 2
`coordinator-decisions.D-057.turn2.draft.md`
`30b7b29978f926821fae66aecb7c3a45d2b7bf664adab0b0cbe69de4cd20daf3`
held frozen. Claude 2 CONSENT 0/0
(`…claude2.turn2.json`
`e84520cd2cd34ea520171311b23ea5c72802d553a66f2b556d48b45584d07d68`).
Codex OBJECTIONS 1 MUST-FIX ADV-D057-T2-01
(`…codex.turn2.json`
`80b0b29b7ae99bd0fad2ac6ec5d501b8a41d874c628225b38d7c1daa54ab881e`).

| ID | Sev | Disposition |
|---|---|---|
| ADV-D057-T2-01 | MUST-FIX | ACCEPTED. Clause 2 adds live-adoption preconditions. Clause 3 adds D-054 / D-057 / Route B selection pins and dependency declaration. |

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `fb1189620f7ac653d0d92c0fe223e3854806336a5738da70e2580ffad96b89a5` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` |
| D-054 commit | `29670ed` |
| Claude 2 D-057 t2 | `e84520cd2cd34ea520171311b23ea5c72802d553a66f2b556d48b45584d07d68` |
| Codex D-057 t2 | `80b0b29b7ae99bd0fad2ac6ec5d501b8a41d874c628225b38d7c1daa54ab881e` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Decision

1. **This file does not grant.** Adopted D-054 is the user
   amendment that permits preview-scope owner recording. This
   entry only states how later D-000 owner-recording entries
   must be written. Overturning this entry does not overturn
   D-054.
2. **Preconditions for one later owner-recording entry.** All
   of:
   - D-054 is still ADOPTED and not overturned or superseded;
   - D-057 is still ADOPTED and not overturned or superseded;
   - the row-specific Route B selection is still ADOPTED and
     not overturned or superseded;
   - a disposition draft exists and has independent ACCEPT or
     ACCEPT-WITH-ADVISORIES at 0 blockers from both Claude 2
     and Codex;
   - a coordinator recording of that draft is already ADOPTED
     and separately committed (D-000 clause 4). Same-commit
     bundling of the coordinator recording and the owner
     recording is forbidden;
   - the owner-recording entry is its own D-000 cycle and its
     own commit.
3. **Required pins on the owner-recording entry.**
   - `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md`
     path and sha256; D-054 ID plus full commit;
   - D-057 ID plus full commit;
   - the row-specific Route B selection ID plus full commit;
   - file-08 owner role; disposition path and sha256; both
     verdict paths and sha256s; preview scope; Route A
     remainder; coordinator-recording decision ID and commit;
     every operative rider or binding advisory that recording
     adopted.
   The owner entry must declare D-054, D-057, and the
   row-specific Route B selection as dependencies, and must
   state that revocation or overturn requires that owner's
   supersession and reconciliation of dependent MF-6 notes.
   DR-005 is v2 plus RB-DR005-V2-A1. An
   ACCEPT-WITH-ADVISORIES case must classify each advisory as
   non-operative or carry it into the owner record.
4. **What the later owner-recording may do.** Discharge
   condition 1 for that row within architecture-preview scope
   only. It may not mark the row `SATISFIED`. It may not
   discharge Route A obligations the disposition left owed.
   It may not authorize `docs/v2/implementation/`. It may not
   apply a V1 successor, move the freeze, or move the claim
   register.
5. **Eligible rows today.** DR-002 (D-047; D-049), DR-003
   (D-030; D-041), DR-004 (D-048; D-050), DR-005 (D-028;
   D-039 plus RB-DR005-V2-A1), DR-008 (D-029; D-040).
   DR-006, DR-007, and DR-009 enter only after their Route B
   selections are adopted. DR-010 remains Route C and is not
   this file. DR-001 is SATISFIED. DR-011 residuals follow
   their owning surfaces.
6. **This entry records no row.** Readiness effect zero. File
   08 is not edited here. A later MF-6 cell note is a
   separate act. This entry does not adopt
   product-boundary-preview.v1 or any other product successor.

## Alternatives

- Repeat the grant in this file. Rejected: D-054 already
  granted; this is mechanics.
- Same-commit coordinator + owner recording. Rejected:
  D-000 clause 4.
- Owner-record DR-005 v2 without RB-DR005-V2-A1. Rejected:
  D-039.
- Use this ID for the DR-010 Route C successor. Rejected:
  ADV-D057-T1-01.
- Pin only the candidate, verdicts, and coordinator
  recording. Rejected: ADV-D057-T2-01.

## Readiness effect

Zero.

## Reversibility

C-D057 revokes these mechanics. D-054 remains until C-D054.
Undoing effects also requires superseding every owner
recording that cites D-054/D-057 and reconciling each
dependent MF-6 note under its own reviewed act.
