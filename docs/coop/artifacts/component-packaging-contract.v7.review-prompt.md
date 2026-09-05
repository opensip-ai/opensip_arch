# Independent review — component-packaging-contract.v7 (DR-120)

Independent, refute not confirm. Did not author v1–v7.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-packaging-contract.v7.json`
Expected digest (Python hashlib, start AND end):
`017c4e81f7f3e542be60eebc7ffed6058b945cdfd8f42d11b80c326071592ddf`

Predecessor v6 `c1fe8cb788b7da1d65356d055a826b852e3fa4752445b5e1778f1d910d7c0cf2`
Claude 2 v6 REJECT `a714c77142027bcd0ae42fa6e5eeb52b1af05a1ce8602168fd4d4bb305aad43f`

You MAY read v6 and the frozen Claude v6 REJECT. Do not read the
other current v7 reviewer. Codex v6 may still be in flight on v6;
do not invent a frozen Codex v6 verdict.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-packaging-contract.v7.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-packaging-contract.v7.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-120 or DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not choose a packager, toolchain, or CLI.

## Claimed repairs

- CLAUDE-V6-S1: `fixtureMemberMap` now includes every AT-* half and every
  AT-ARCHIVE-* golden/negative; `fixtureClassCoverage` requires those keys

## Attack

- AT-* / AT-ARCHIVE-* obligations with no map key and no report slot
- Trusted-install halves with no blocked-on-ride memberKey
- Checksum NUL-in-mask / hidden 100-byte cap / class-level `or` (must stay repaired)
- Silent v6-to-v7 path
- SATISFIED / QUALIFIED / implementation authorization / packager choice

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
