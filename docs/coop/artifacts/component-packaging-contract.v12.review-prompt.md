# Independent review — component-packaging-contract.v12 (DR-120)

Independent, refute not confirm. Did not author v1–v12.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-packaging-contract.v12.json`
Expected digest (Python hashlib, start AND end):
`487a33a6f9c0485ad73e61a5e9f66962e5f3620f32550ecc42b27a830edfb579`

Predecessor v11 `11395bea1ee95bf15d7fdad1905be0336b241a669540ac902f64766da514912b`
Predecessor v10 `78628b56c7d252c9ed3566f499caf150a68c08175379b1cb774b762e5a0b09d9`
Claude 2 v10 ACCEPT-WITH-ADVISORIES
`b07dc19dbfb7686fdad4f7dfce99ffa489133db43bcea902ab58052f14c05f05`
Codex v10 REJECT (now frozen)
`52be660955c009c16bfb88db043591c6507fbb8fdd2f36fc96462703feed736d`

You MAY read v10, v11, and the frozen Claude v10 ACCEPT. Do not read
the other current v12 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-packaging-contract.v12.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-packaging-contract.v12.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-120 or DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not choose a packager, toolchain, or CLI.

## Claimed repairs

- CODEX-V10-B1: already folded at v11 (live COORD pin `b9819d6e…`)
- CODEX-V10-S1: already folded at v11 (AT-8 aggregate map key removed)
- CODEX-V10-S2: AT-ARCHIVE-SIZE-MAX split into 8589934591 ACCEPT and
  8589934592 refuse:SIZE-EXCEEDS-USTAR-FIELD; archiveGoldenKeyCount 17

## Attack

- COORD governingSources digest that does not reproduce at the live path
  unless it is an inherited pin with live remasurement
- AT-8 map key with expected `see AT-ARCHIVE-* members`
- SIZE-MAX scored only on the overflow half
- archiveGoldenKeyCount that disagrees with kind=archive-golden members
- D-105 facts presented as file-08 cell measurements
- Silent v11-to-v12 path
- SATISFIED / QUALIFIED / implementation authorization / packager choice

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
