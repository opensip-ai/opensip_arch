# D-059–D-063 — Preview-scope owner recordings

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 1 of 3.
> **Decision type:** RULE-GOVERNED. Five severable owner recordings
> under user-made D-054. Mechanics: adopted D-057.
> **Does not** mark SATISFIED.
> **Does not** authorize `docs/v2/implementation/`.
> **Does not** edit file 08 in this entry.

Adopting or overturning one does not adopt or overturn the others.
Each adopted entry is its own commit (D-000 clause 4).

Authority is D-054. This file does not grant.

Measured inputs:

| Pin | value |
|---|---|
| COORD | `de897fd68e1efdcbf649d1c91cd4e410fb2b2c4db7a2980e39bb9112518d637b` |
| file 08 | `6547e6ace2ae61e664af0f65059b66c2cb3d0539d64f6687aba04f8f54dc4cd7` |
| D-054 user amendment | `docs/coop/artifacts/coordinator-decisions.D-054.user-amendment.md` `c274d140f15e207ad3cd4a00f6dc29292832f3c1c664ba55e9715ffff235462f` commit `29670ed29104f5f9e855c10206501e2f5e31ef6e` |
| D-057 | commit `33597e8339b5b1f219bc7f3cdca8d8ce670f45c5` |

If a cited file moves, re-measure. Do not edit this subject after dispatch.

## Shared clauses (every entry)

- D-054, D-057, and the row's Route B selection are still ADOPTED
  and not overturned or superseded.
- Dependencies: D-054, D-057, and the row Route B selection.
  Revocation or overturn requires that owner's supersession and
  reconciliation of dependent MF-6 notes.
- Scope: architecture preview (D-002 / D-018) only.
- Does not mark the row SATISFIED.
- Does not discharge Route A remainders the disposition named.
- Does not apply a V1 successor, move the freeze, or move the
  claim register.
- Does not authorize `docs/v2/implementation/`.
- Conditions 2–5 remain. Condition 5 remains the only
  implementation authorization.
- File 08 is not edited here. A later MF-6 cell note is a
  separate act.

## D-059 — Owner-record DR-002

- **Owner role:** Evidence authority + V1 coordinator.
- **Route B selection:** D-047, commit `aa75926d54d43d586c455809deb7832fba953aff`.
- **Disposition:** `route-b.DR-002.preview-disposition.v2.json`
  `301ea338c4f4a5b7194cdf8a827c21bdc99a2b8cc091880b553a7c4a6f7dfc06`.
- **Verdicts:** Claude 2
  `4619a113518271d2539f057dd6338c36e25d7ddb4208c141521f9385d8266ec1`
  ACCEPT 0/0; Codex
  `b3be13e2f26609aaf4fc33fbe5da9031226f1ef49858349c4c6f9661119f7485`
  ACCEPT 0/0. No operative rider.
- **Coordinator recording:** D-049, commit `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`.
- **Route A remainder:** AC-1 focused adjudication; AC-3 validator
  + claim-register motion; AC-4 Phase-1A packet.
- **Decision:** Record that disposition as the named owner's
  preview-scope recording. Condition 1 for DR-002 may discharge
  within architecture-preview scope only.
- **Readiness effect:** Condition 1 for DR-002 only, preview
  scope. Not SATISFIED.
- **Overturn:** C-D059.

## D-060 — Owner-record DR-004

- **Owner role:** Evidence/retention authority.
- **Route B selection:** D-048, commit `aa75926d54d43d586c455809deb7832fba953aff`.
- **Disposition:** `route-b.DR-004.preview-disposition.v2.json`
  `2866dd87b9950650b08b5323ea299db050a4ba42f0488bb7b1130dcd86a6da76`.
- **Verdicts:** Claude 2
  `a2ab3306fabc9438e6ffc1fab77dbe651f2e62d426239892293ed158f869ab5e`
  ACCEPT 0/0; Codex
  `9813080054f0acd1960997af650c75fb8148985ccddc0eae568799d8e57cbde3`
  ACCEPT 0/0. No operative rider.
- **Coordinator recording:** D-050, commit `88764faccb1ff4935ac8ed3b61a00e3cfbddfd2e`.
- **Route A remainder:** eight-bullet Phase-1A packet; section31
  v4 is not the packet.
- **Decision:** Record that disposition as the named owner's
  preview-scope recording. Condition 1 for DR-004 may discharge
  within architecture-preview scope only.
- **Readiness effect:** Condition 1 for DR-004 only, preview
  scope. Not SATISFIED.
- **Overturn:** C-D060.

## D-061 — Owner-record DR-003

- **Owner role:** Threat-model authority + V1 coordinator.
- **Route B selection:** D-030, commit `d5721222623faa854d85282df408de1c5005d19f`.
- **Disposition:** `route-b.DR-003.preview-tm.v2.json`
  `d9084d4dc16bb450562520c2bed77cd80129bc65763f7ec2f55f3476c8989f52`.
- **Verdicts:** Claude 2
  `69b201e0916ac825f6326b9aad250bf3140eb2b1e9b7d078f38f5fa83a3a0ebf`;
  Codex
  `151be2a2367553fe7ad1d21a58859368008d9ae3f604000eb22b56e9086730ef`.
- **Coordinator recording:** D-041, commit `56973db89be3539ff59c0d669aa794d2ddbabc6e`.
- **Route A remainder:** full TM / V10 / G19 / publication-block.
- **Decision:** Record that scoped preview TM as the named
  owners' preview-scope recording. Condition 1 for DR-003 may
  discharge within architecture-preview scope only. Not a
  security-complete claim. TM stays UNSET for the freeze.
- **Readiness effect:** Condition 1 for DR-003 only, preview
  scope. Not SATISFIED.
- **Overturn:** C-D061.

## D-062 — Owner-record DR-005

- **Owner role:** Evidence, storage, and operability authorities.
- **Route B selection:** D-028, commit `d5721222623faa854d85282df408de1c5005d19f`.
- **Disposition:** `route-b.DR-005.preview-disposition.v2.json`
  `3b50bcf15e207b698283cb51e77335bceaf46f053f961f0de2b9b8d20982b809`
  **plus operative rider RB-DR005-V2-A1** (D-039): if the
  Operational metadata class is denied, doctor fails closed
  (D-032 BLK-6); this disposition supplies no grant or class
  admission.
- **Verdicts:** Claude 2
  `479b3a191703746355accc9da819e058d772b4efbcc8ee81bdfadd4e8887de5b`;
  Codex
  `4dc772dec715277aac1b6058a374d88d6ec9dd363eb8a7e04ea8ed2927f9b4aa`.
  Codex independent verdict was ACCEPT-WITH-ADVISORIES. The
  operative advisory is carried as RB-DR005-V2-A1.
- **Coordinator recording:** D-039, commit `7e7a63687c49092df4622949cd80825cb4a4e681`.
- **Route A remainder:** V10/custody and G19 demonstration.
- **Decision:** Record v2 plus RB-DR005-V2-A1 as the named
  owners' preview-scope recording. Condition 1 for DR-005 may
  discharge within architecture-preview scope only.
- **Readiness effect:** Condition 1 for DR-005 only, preview
  scope. Not SATISFIED.
- **Overturn:** C-D062.

## D-063 — Owner-record DR-008

- **Owner role:** evidence/retention authority (contract half).
- **Route B selection:** D-029, commit `d5721222623faa854d85282df408de1c5005d19f`.
- **Disposition:** `route-b.DR-008.preview-disposition.v2.json`
  `8b2d21392bde0906ea75a6c29b1083e3b441205fd3eafb66a13135734a9ca41c`.
- **Verdicts:** Claude 2
  `adc954fd99f03b61b5613e06fe63968fc2feecf70fdf83e12c3939feff772ac5`;
  Codex
  `a96987960d99cf0bde80d5f86a6d7ce244545eab1235788432246c2be4aebcb4`.
- **Coordinator recording:** D-040, commit `56973db89be3539ff59c0d669aa794d2ddbabc6e`.
- **Route A remainder:** evidence-side successor consuming
  retention, plus Phase-1A. Posture half stays closed.
- **Decision:** Record that disposition as the named owner's
  preview-scope recording of the integration half. Condition 1
  for DR-008's integration half may discharge within
  architecture-preview scope only. Row stays PARTIALLY SATISFIED
  as to posture; not SATISFIED.
- **Readiness effect:** Condition 1 for DR-008 integration half
  only, preview scope. Not SATISFIED.
- **Overturn:** C-D063.
