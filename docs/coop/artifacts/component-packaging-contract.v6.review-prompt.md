# Independent review — component-packaging-contract.v6 (DR-120)

Independent, refute not confirm. Did not author v1–v6.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-packaging-contract.v6.json`
Expected digest (Python hashlib, start AND end):
`c1fe8cb788b7da1d65356d055a826b852e3fa4752445b5e1778f1d910d7c0cf2`

Predecessor v5 `eda5855e01777d884ac972ef71804dd4bf1e30fd4c2ab5a190b9754a80c2876c`
Claude 2 v5 REJECT `893601ad90e14280fe9fff968d36d6a603e3d948808b3afe4c4b8ab1c7925c0e`
Codex v4 REJECT (folded residue) `6f7ab491bddace9afa76df720fea6686f428658d8e188463dac517cc40a55c7c`

You MAY read v5, the frozen Claude v5 REJECT, and the frozen Codex v4
REJECT. Do not read the other current v6 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-packaging-contract.v6.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-packaging-contract.v6.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-120 or DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not choose a packager, toolchain, or CLI.

## Claimed repairs

- CLAUDE-V5-S1: all-spaces checksum mask; devmajor/devminor octal7nul of 0
- CLAUDE-V5-ADV-1: Codex v4 now frozen and folded
- CODEX-V4-B1: complete tree-to-byte algorithm; OD-P2 owns 100-byte profile
  capacity as typed non-success; no schemas.v2 pointer; CI-5 remains the pin
- CODEX-V4-S1: fixtureMemberMap (45 requires + named arms); no class-level `or`
- CODEX-V4-S2: closed health applicability standing
- CODEX-V4-S3: already folded at v5

## Attack

- Checksum still computed with a NUL-in-mask
- POSIX ustar still a family (typeflag NUL, prefix split, unbound body, trailer pad)
- Hidden path/link cap not owned at OD-P2
- fixtureClassRides class-level alternatives standing in for members
- Health result omittable with no applicability standing
- OD-P2 still pointing at schemas.v2
- Silent v5-to-v6 path
- SATISFIED / QUALIFIED / implementation authorization / packager choice

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
