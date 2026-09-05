# Independent review — distribution-core-inventory-contract.v4 (DR-101)

Independent, refute not confirm. Did not author v1–v4.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/distribution-core-inventory-contract.v4.json`
Expected digest (Python hashlib, start AND end):
`729d04067af84e7f4b467c9e755100d7b466eda6caa9d0004ca841c76bc4a7cc`

Predecessor v3 `35a81f9bae4e0c5a75a1efec0de5130b628cd87fd0bbe3b1c8c2eedc2f971a1c`
Claude 2 v3 REJECT
`921c773562b0717c29ec66d0b41bcef83c149be07bbae0e9a95a6ece0ad4eb99`
Codex v3 REJECT
`ab8fde9bc45054ef7e58b248fb7cb97bd1edff2e79ea1544301cfe2e4029b28c`

Do not read the other current v4 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/distribution-core-inventory-contract.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/distribution-core-inventory-contract.v4.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-101 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

HEAD is `8fdd59c` (D-106 ADOPTED). File 08 means only
`docs/v2/architecture/08-decision-and-readiness-register.md`.

## Claimed repairs

- CLAUDE-V3-S1: dependencyGraph no longer owns layer assignment;
  graphRules fix cardinality/overlap/shared-exec only; L-EVAL is a
  tag, not a separately-published-file requirement
- CODEX-V3-S1: alias-edge exception removed; duplicate path or
  duplicate sha256-under-different-path fails unconditionally

## Attack

- A dependencyGraph that still claims this artifact owns assignment
  against DR-126
- An alias-edge exception naming an undefined second edge relation
- Silent v3→v4 path
- SATISFIED / QUALIFIED / implementation authorization
- Row-verbatim mismatch against live file 08 `| DR-101 |`

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
