# SATISFIED-GRADE review — component-manifest-fixture-corpus.v6 (DR-103)

Independent, refute not confirm. Did not author the corpus or the schema.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-fixture-corpus.v6.json`
Expected digest (Python hashlib, start AND end):
`8dfa9346ada4fefce0aabca96062208e4fea7371a6aab68eaee75cdc908a21a5`

Schema contract: `component-manifest-schemas.v11.json`
`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`

Predecessor v5 `a2bca0e18aa6012453ab68cf4bc2c77c09592a877a7ce0a34fb4e83eb463e3eb`
Claude 2 v5 REJECT `bb00a70ad990ebabf51414bf9a8e0371dfc28dfdc1e00f69cb805d02f03ce77e`
Codex v5 ACCEPT `9660ffda5dd990067792e6c9d3a2e079ffb3ce8ef02ac3e4862bbc42752d3358`
Frozen Codex v4 REJECT `fafeb4e3c29076287caa46917188395590249e8665a79c13953e1116d4c26d72`

Do not retarget v2, v3, v4, or v5. Do not mutate `fixtures/dr-103.v2/`
or `fixtures/dr-103.v4/`.

You MAY read v5 and the frozen v5 verdicts. Do not read the other
current v6 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-fixture-corpus.v6.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-fixture-corpus.v6.review-independent.codex.json`

Do not edit the subject or any fixture bytes. Do not commit.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

## Claimed repairs

- CLAUDE-V5-S1 / CODEX-V5-ADV-1: supportingBytes note no longer says
  "also authored"
- CLAUDE-V5-ADV-1: predecessorV2Path / predecessorV2Sha256 restored
- CODEX-V5-ADV-2: frozen Codex v4 REJECT is pinned

## Attack

- Scoring unicode-norm-duplicate as proof of the NFC-duplicate arm
- A supportingBytes note that still asserts the member is authored
- Any scored lock fixture while DR-111 is OPEN
- Silent retarget of corpus v2/v3/v4/v5
- Mutation of frozen fixture directories
- Silent v5-to-v6 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
