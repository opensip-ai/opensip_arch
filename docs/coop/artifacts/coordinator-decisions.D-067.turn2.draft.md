# D-067 turn 2 — File 08 MF-6 notes for preview owner recordings

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. File-08 content change (D-001
> MF-6). Does not mark SATISFIED.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** coin a new file-08 status token.

Turn-1 subject `coordinator-decisions.D-067.draft.md`
`f75fe1e66fbec2cd1dcc7ef597297e7bea30abc080f4be33973343066ab9bda2`
held frozen. Claude 2 OBJECT 0 MUST-FIX 2 SHOULD-FIX
(C2-D067-SF1, C2-D067-SF2). Codex OBJECTIONS 1 MUST-FIX
ADV-D067-T1-01 plus SHOULD-FIX ADV-D067-T1-02 / T1-03.

| ID | Sev | Disposition |
|---|---|---|
| ADV-D067-T1-01 | MUST-FIX | ACCEPTED. Snapshot preamble and condition-1 row get an explicit two-axis algorithm. Leading labels stay the sole status-token source. |
| ADV-D067-T1-02 | SHOULD-FIX | ACCEPTED. Status is under review. Measured-input table is filled. |
| ADV-D067-T1-03 | SHOULD-FIX | ACCEPTED. Six-row note table below is the exact replacement text. |
| C2-D067-SF1 | SHOULD-FIX | ACCEPTED. Status is under review. |
| C2-D067-SF2 | SHOULD-FIX | ACCEPTED. Digests are pinned. |

Measured inputs:

| Path | sha256 |
|---|---|
| COORD | `0e9d36d2fca2b5a6e0ef4c972b3c4b9133c21c23724fc3214b2901d5b874234b` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| freeze | `e809d4395f394a507c36c23c069d566c838b2283c931b6d2d13797be53406dbd` |
| claim-register.v1.json | `767dc210d4fa8b6d2588a6746df124192ff19af9da4e7be663164e9fde32d59c` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Decision

1. **Keep leading labels as the sole status-token source.** Do not
   invent a new file-08 status token. DR-002/003/004/005/010 stay
   **HARD-BLOCKED**. DR-008 stays **PARTIALLY SATISFIED**.
2. **Amend the snapshot preamble** so condition-1 accounting is a
   second axis, not a reread of lead labels. Exact replacement of
   the regeneration sentence:

   Current: "Regenerate it by reading the *leading label* of each
   status cell — the cells carry long-form prose, so substring
   matching on words like "satisfied" mis-reads them."

   New: "Regenerate *status-token* counts by reading the *leading
   label* of each status cell — the cells carry long-form prose, so
   substring matching on words like "satisfied" mis-reads them.
   Condition 1's disposed count is a separate union: (a) rows whose
   leading label is `SATISFIED`, plus (b) rows whose status cell
   carries an exact scoped owner-recording note of the form this
   entry writes. A `HARD-BLOCKED` or `PARTIALLY SATISFIED` lead
   label is unchanged by that note. Lead labels alone cannot
   distinguish a preview-disposed HARD-BLOCKED row from an
   undisposed one."
3. **Rewrite the condition-1 snapshot row** "Measured now" to:

   **1 of 11 `SATISFIED`; 6 of 11 explicitly disposed for
   architecture preview** — DR-001 `SATISFIED`; DR-002 (D-058),
   DR-003 (D-065), DR-004 (D-064), DR-005 (D-060 + RB-DR005-V2-A1),
   DR-008 integration half (D-061), DR-010 (D-068) have
   owner-recorded preview dispositions; DR-006, DR-007, DR-009,
   DR-011 remain without SATISFIED or scoped owner-recorded
   disposition. Arithmetic: 1 + 6 + 4 = 11. Zero SATISFIED added.
   Standing stays **NOT MET**.
4. **Append the exact notes below** to the six status cells. Use
   "remaining independently required work (Route A where
   applicable)" rather than a uniform Route A label.
5. Does not mark any row SATISFIED. Does not apply a V1 successor.
   Does not move the freeze or claim register. Does not authorize
   `docs/v2/implementation/`.
6. Condition 1 still does not discharge.

## Exact six-row notes

| Row | Owner-recording | Effective disposition | Remaining independently required work |
|---|---|---|---|
| DR-002 | D-058 commit `21f0945e270904b7b663f428a866485f167cadb7` | `docs/coop/artifacts/route-b.DR-002.preview-disposition.v2.json` `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06` | Focused independent AC-1 adjudication; repaired validator successor plus claim-register motion (AC-3); eight-bullet Phase-1A packet (AC-4 / DR-004); full V10 / G19 / publication-block (D-030 / D-028) |
| DR-003 | D-065 commit `fde6e276d2b35020148853fc800dec958ef441d0` | `docs/coop/artifacts/route-b.DR-003.preview-tm.v2.json` `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52` | Reviewed closure of V10/custody and G19; publication block satisfied by required demonstration; final TM disposition for the authoritative product. Not a security-complete claim. TM stays UNSET for the freeze. |
| DR-004 | D-064 commit `dfa21be1cd1373cc0a0ad0cb52055301fd673edf` | `docs/coop/artifacts/route-b.DR-004.preview-disposition.v2.json` `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76` | Exact eight-bullet packet with retained proof, custody, joins, and status update; successor honesty on section31 v4 advisories S31V4-01, S31V4-02, S31V4-CX-A1, S31V4-CX-A2; DR-002 AC-4 still names this packet |
| DR-005 | D-060 commit `fce0546ce65921fcb6a9245c1c2a4b9625d7fcc1` | `docs/coop/artifacts/route-b.DR-005.preview-disposition.v2.json` `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809` **plus operative rider RB-DR005-V2-A1** (if Operational metadata is denied, doctor fails closed; D-032 BLK-6; no grant or class admission) | Applied evidence/retention/D9 integration; executable custody; durable-authoritative negative controls for G19; full V10 / publication-block demonstration |
| DR-008 | D-061 commit `6842e8d084402acb2f04d4160b7d5eb351de97c2` | `docs/coop/artifacts/route-b.DR-008.preview-disposition.v2.json` `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c` — integration half only; posture half stays closed | Evidence-side successor consuming retention AND Phase-1A; Lane R §3.1 instrument; full V10 / G19 / publication-block |
| DR-010 | D-068 commit `0a05f7fa273bde9a7b8158dd54045f746c16a4fa` | `docs/coop/artifacts/product-boundary-preview.v2.json` `ff7a09130a2b5b409b02725a839f9d7b5fb88e945d7f9bbb63c0d0154c627b85` — Route C product disposition, not Route A | DR-117 and DR-011-R16 remain independently required (condition 2 / residual). Not a Route A remainder. |

Each cell note begins: "Preview-scope owner recording 2026-08-14
(architecture preview only; not SATISFIED):" then the row's
owner-recording, effective disposition, and remaining work from
this table.

## Alternatives

- Leave file 08 silent. Rejected: hides landed condition-1
  alternatives.
- Change lead labels to SATISFIED. Rejected: DR-204.
- Count disposed rows by rereading lead labels only. Rejected:
  ADV-D067-T1-01.

## Readiness effect

Condition 1 remains NOT MET. 1 SATISFIED + 6 preview-disposed +
4 unresolved = 11. Zero SATISFIED added.

## Reversibility

C-D067 plus restore of the prior file-08 cells and prior snapshot
preamble.
