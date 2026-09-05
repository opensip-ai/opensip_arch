# Independent review — distribution-core-inventory-contract.v3 (DR-101)

Independent, refute not confirm. Did not author v1–v3.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/distribution-core-inventory-contract.v3.json`
Expected digest (Python hashlib, start AND end):
`35a81f9bae4e0c5a75a1efec0de5130b628cd87fd0bbe3b1c8c2eedc2f971a1c`

Predecessor v2 `59dd0987bab9dbe38d04cd7ca3dd24bdb8ec36dfc2a4e082aff05f48f55068bc`
Claude 2 v2 ACCEPT `7c43e9fdc83eb92cfa1e1fd6e5ce85b1b3a2a08fc9dc8ade6577846f864d2b1b`
Codex v2 REJECT `0b54d0dc464ec81aab6c77d6266a85c897166c341594febc8fb7fff70b29f0a7`

Do not read the other current v3 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/distribution-core-inventory-contract.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/distribution-core-inventory-contract.v3.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-101 SATISFIED. Do not authorize implementation.

## Claimed repairs

- CODEX-V2-S1: `graphRules` make shared-executable layer assignment
  deterministic (one node, layer set `{L-DIST, L-HOST}`)

## Attack

- Shared executable still assignable L-DIST-only / L-HOST-only / duplicated
- Missing node granularity, roots, edge direction, or layer-set cardinality
- Collapsing three cores / minting core language / DR-106 in default install
- Silent v2→v3 path
- SATISFIED / QUALIFIED / implementation
- Row-verbatim mismatch against live file 08 `| DR-101 |`

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally. Final chat: verdict word.
