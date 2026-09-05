# Independent review — signed-index-trust-contract.v7 (DR-112)

Independent, refute not confirm. Did not author v1–v7.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/signed-index-trust-contract.v7.json`
Expected digest (Python hashlib, start AND end):
`ce26f1621b4ff2a30d5501b710085de78a7dbc68259cc184d0e7c843125d2d40`

Predecessor v6 `c33d3436a264cbe01b34694bcc7d3bfb3fd8a332a6bd439d3e2b8baf3ad27056`
Claude 2 v6 ACCEPT `947a147a5f19f5b49cc71f7c5ea828f8ed2b19a16e0e1d6a5dddc2cefa184765`
Codex v6 REJECT `137a0d7dea2ea8dbebad6d9773c7476ee439923cf25d9b34281c286b8848d8f4`
Codex v5 (now frozen, A2 fold) `d1b710e33081c77d8ec880cd618432a32d519805b18ddc924a52c6fe299e8452`

You MAY read v6 and both frozen v6 verdicts plus the frozen Codex v5
REJECT. Do not read the other current v7 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/signed-index-trust-contract.v7.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/signed-index-trust-contract.v7.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-112 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

This is NOT a DR-111 / compatibility-matrices review.

## Claimed repairs

- CODEX-V6-S1: `outcomeBranchDiscipline` before fallback; `whenFailed` retired
  for `whenActiveFailure`; PRESENT/INSTALL/COMMIT `normativeExclusion`
- CLAUDE-V6-ADV-1 / CODEX-V6-A1: roster names whole paths, no omitted sibling
- CODEX-V6-A2: Codex v5 pinned as frozen COMPLETE REJECT `d1b710e3…`

## Attack

- INACTIVE named members falling through to event-fallback reasons
- `defaultTransition` still sending a false guard to fallback first
- RECOVER-COMMIT `whenFailed` still present or unqualified vs INACTIVE
- Fallback notes as the only exclusion (`normativeExclusion` missing)
- Roster parenthetical omitting `whenActiveSuccess` / `whenActiveFailure`
- Codex v5 still described as unpinned provisional
- Silent v6-to-v7 path
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Write incrementally with Python hashlib. Final chat: verdict word.
