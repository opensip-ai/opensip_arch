# Independent review — component-packaging-contract.v13 (DR-120)

Independent, refute not confirm. Did not author v1–v13.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-packaging-contract.v13.json`
Expected digest (Python hashlib, start AND end):
`234831d97ea0cff1942906faddfd48be9251fd10e11811f6ca58b5af446ab204`

Predecessor v12 `487a33a6f9c0485ad73e61a5e9f66962e5f3620f32550ecc42b27a830edfb579`
Predecessor v10 `78628b56c7d252c9ed3566f499caf150a68c08175379b1cb774b762e5a0b09d9`
Claude 2 v10 ACCEPT-WITH-ADVISORIES
`b07dc19dbfb7686fdad4f7dfce99ffa489133db43bcea902ab58052f14c05f05`
Codex v10 REJECT
`52be660955c009c16bfb88db043591c6507fbb8fdd2f36fc96462703feed736d`
Codex v12 may still be in flight; do not invent a frozen digest.

You MAY read v10, v12, and the frozen Claude/Codex v10 verdicts. Do
not read the other current v13 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-packaging-contract.v13.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-packaging-contract.v13.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-120 or DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not choose a packager, toolchain, or CLI.

## Claimed repairs

- CODEX-V10-B1/S1: folded at v11
- CODEX-V10-S2: folded at v12 (SIZE-MAX split; archiveGoldenKeyCount 17)
- CODEX-V12-S1: mapKeyCount 80 equals len(members)

## Attack

- mapKeyCount that disagrees with len(fixtureMemberMap.members)
- archiveGoldenKeyCount that disagrees with kind=archive-golden members
- AT-8 aggregate map key
- SIZE-MAX scored only on the overflow half
- COORD governingSources digest that does not reproduce unless inherited
- Silent v12-to-v13 path
- SATISFIED / QUALIFIED / implementation authorization / packager choice

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
