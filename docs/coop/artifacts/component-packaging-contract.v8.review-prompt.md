# Independent review — component-packaging-contract.v8 (DR-120)

Independent, refute not confirm. Did not author v1–v8.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-packaging-contract.v8.json`
Expected digest (Python hashlib, start AND end):
`533389cba8af7f41b8b61e84e2fe23f6a16ea28f442482b94c6e272ba52c7c97`

Predecessor v7 `017c4e81f7f3e542be60eebc7ffed6058b945cdfd8f42d11b80c326071592ddf`
Claude 2 v6 REJECT (AT-* slot, folded at v7)
`a714c77142027bcd0ae42fa6e5eeb52b1af05a1ce8602168fd4d4bb305aad43f`
Codex v6 REJECT `53a569875cdf97ac425e5bcebd39bb65b40ffd30fa62cead76c489c1e917f1d6`

You MAY read v6–v7 and those frozen verdicts. Do not read the other
current v8 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-packaging-contract.v8.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-packaging-contract.v8.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-120 or DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not choose a packager, toolchain, or CLI.

## Claimed repairs

- CODEX-V6-B1: `payloadBytes` input; mode/size capacities; octet-equal admission;
  adapter-identity-independent golden
- CODEX-V6-S1: `fixtureMemberMap.members[memberKey]`; live RJ-2 subcodes; no
  invented RJ-3 subcodes; split conjunctive TC-NAME arms
- CODEX-V6-S2: `subject.role`; exact one health `{role,platform}` member
- CLAUDE-V6-S1: already folded at v7 (AT-* / AT-ARCHIVE-* keys)

## Attack

- byteAlgorithm.inputs that cannot produce a nonempty file body
- mode/size overflow with no owned typed refusal
- admission that accepts nonzero uid / noncanonical pad
- AT-ARCHIVE-IDENTITY requiring shared CI-1 adapterVersionDigest
- Reports addressing `fixtureMemberMap[memberKey]` not `.members[memberKey]`
- Invented subcodes (`ENTRYPOINT_ABSENT`, `typed-stale-alias`)
- Empty or off-subject health applicability
- Silent v7-to-v8 path
- SATISFIED / QUALIFIED / implementation authorization / packager choice

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
