# D-081 — File 08 MF-6 notes for DR-006 / DR-007 / DR-009 owner recordings

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 turn 2 of 3. Same cycle as turn 1. Not a new
> cycle. Not a fourth turn of D-070. Frozen turn-1 subject is
> not edited.
> **Decision type:** RULE-GOVERNED. File-08 content change (D-001
> MF-6). Does not mark SATISFIED.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin a new file-08 status token.

Turn-1 subject `coordinator-decisions.D-081.draft.md`
`d9992a4f79b8e8716e0640ce2c21ad343762bbaa0743ea237628b53d14efe17f`
held frozen. Claude 2 CONSENT, 0 MUST-FIX, 0 SHOULD-FIX. Codex
OBJECTIONS, 0 MUST-FIX, 1 SHOULD-FIX ADV-D081-01.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D081-01 | SHOULD-FIX | ACCEPTED. The two-axis algorithm stays. Only the embedded count "six explicitly disposed" becomes "nine explicitly disposed." |

D-070 is ADOPTED at `e40b3f190e68264a24ac5098b1cef300434d6709`.
This entry does not overturn D-070.

## Decision

1. **Keep leading labels as the sole status-token source.**
   DR-006, DR-007, and DR-009 stay **HARD-BLOCKED**.
2. **Keep D-070's two-axis algorithm.** Replace only the
   embedded count in the snapshot preamble:

   Current: "The two components are counted separately in the
   snapshot: one SATISFIED and six explicitly disposed, with
   set-union deduplication if a future row has both."

   New: "The two components are counted separately in the
   snapshot: one SATISFIED and nine explicitly disposed, with
   set-union deduplication if a future row has both."

   Do not rewrite the rest of the regeneration sentence.
3. **Do not change the snapshot heading date.** It is already
   2026-08-14.
4. **Rewrite the condition-1 snapshot row** "Measured now" to:

   **1 of 11 `SATISFIED`; 9 of 11 explicitly disposed for
   architecture preview** — DR-001 `SATISFIED`; DR-002 (D-058),
   DR-003 (D-065), DR-004 (D-064), DR-005 (D-060 + RB-DR005-V2-A1),
   DR-006 (D-077), DR-007 (D-078), DR-008 integration half (D-061),
   DR-009 (D-079 + RB-DR009-V2-A1), DR-010 (D-068) have
   owner-recorded preview dispositions; DR-011 remains without
   SATISFIED or scoped owner-recorded disposition. Arithmetic:
   1 + 9 + 1 = 11. Zero SATISFIED added. Standing stays **NOT MET**.
5. **Append the exact notes below** to the three status cells.
   Use "remaining independently required work (Route A where
   applicable)" rather than a uniform Route A label.
6. Does not mark any row SATISFIED. Does not apply a V1 successor.
   Does not move the freeze or claim register. Does not authorize
   `docs/v2/implementation/`. Does not edit DR-002/003/004/005/008/010
   notes.
7. Condition 1 still does not discharge.

## Exact three-row notes

| Row | Owner-recording | Effective disposition | Remaining independently required work |
|---|---|---|---|
| DR-006 | D-077 commit `d401ecd8494cd3e1b5f7b3553d9d9e6fed4dd9e5` | `docs/coop/artifacts/route-b.DR-006.preview-disposition.v2.json` `28fb23ec9f01de17753624d9e90bec53d75df2344d62594321c17da8a799d161` | Binding per-surface identity recipes; the §7.1 PROPERTY is the boundary; Phase-1A subject-set agreement; declared sufficiency view type and closed rungUnavailableBecause vocabulary; retained negative controls and exact derivation/custody joins; independent review of those recipes |
| DR-007 | D-078 commit `17bbf202107e8f8fa78366ce5422fd53a1bf6363` | `docs/coop/artifacts/route-b.DR-007.preview-disposition.v2.json` `53b72a910507e31dd8d20e29c8d3dd9c673a68944f086c7e33d9ca39af5f42b7` | D9 successor to v1.14 closing observation→faultCause, optional presence, success/policy/interrupted branch; reviewed retention degradation/refusal integration without invented codes; independent review of that successor |
| DR-009 | D-079 commit `927ab94a5e796b596b93985c4e6d46ce753d09cf` | `docs/coop/artifacts/route-b.DR-009.preview-disposition.v2.json` `5e2f6572d1473176545d83ee2f8babf8daf8a3d7702ffa55bca7c7065841b782` **plus operative rider RB-DR009-V2-A1** (applied head `docs/coop/artifacts/r1-lifetime-neutrality.conformance.v1.9.json` `37897be0cca011e88c04b93b6f9912f444006b4b3c71e99a08b253d613c9c0ab`; application is not park closure and is not SATISFIED) | Close LN-13, policyOutcome.derivationDigest, and R1-PARK-*; reviewed retained validator or explicit accepted alternative; CIR-B1 closure |

Each cell note begins: "Preview-scope owner recording 2026-08-14
(architecture preview only; not SATISFIED):" then the row's
owner-recording, effective disposition, and remaining work from
this table.

Measured inputs at dispatch:

| Path | sha256 |
|---|---|
| COORD | `c0c6207030b9e08a701c4e681f887f5188f391fa57517c5392921f4822d7309f` |
| file 08 | `9495c70f96936c4d33fcaf8e8a395c59a44ad2b7203af38be7f0ac2b62dc2dfd` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| claim-register.v1.json | `767dc210d4fa8b6d2588a6746df124192ff19af9da4e7be663164e9fde32d59c` |
| D-070 commit | `e40b3f190e68264a24ac5098b1cef300434d6709` |
| turn-1 subject | `d9992a4f79b8e8716e0640ce2c21ad343762bbaa0743ea237628b53d14efe17f` |
| Claude 2 turn 1 | `3dff87148d2d6db3410971c64c9c6a2b8e678c7d1e761e4b5b72f458ada36ef4` |
| Codex turn 1 | `629c546b6e3a279aafae5742738ddca7d14fa9727c45bc29901f5c5b3fd7147e` |

If a cited file moves, re-measure. Do not edit this subject after
dispatch.

## Alternatives

- Leave file 08 silent on D-077/078/079. Rejected.
- Change lead labels to SATISFIED. Rejected: DR-204.
- Freeze the D-070 "six" count while adding three notes.
  Rejected: ADV-D081-01.

## Readiness effect

Condition 1 remains NOT MET. 1 SATISFIED + 9 preview-disposed +
1 unresolved (DR-011) = 11. Zero SATISFIED added.

## Reversibility

C-D081 plus restore of the prior three file-08 cells, the prior
condition-1 snapshot row, and the prior preamble count ("six
explicitly disposed"). Does not overturn D-070, D-077, D-078,
or D-079.
