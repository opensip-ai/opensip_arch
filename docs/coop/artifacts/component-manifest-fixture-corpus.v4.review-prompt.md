# SATISFIED-GRADE review — component-manifest-fixture-corpus.v4 (DR-103)

Independent, refute not confirm. Did not author the corpus or the schema.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-fixture-corpus.v4.json`
Expected digest (Python hashlib, start AND end; re-measure at dispatch):
`3f70ec3ba5b0eabfb67cecb8ca91d19713732b8599b6754ae539b6813a73d949`

Schema contract: `component-manifest-schemas.v11.json`
`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`
(D-104 accepted schema successor).

Predecessor v3 `7fe3d17161147089f00157598e268bba5ea2a37a6d77a94571489d916c9cdb84`
Claude 2 v3 REJECT `46452a7cba74fc016033baae6083c9a10e2e37cc18b602ec16719697545e52c2`
Corpus v2 remains frozen at
`70248781118452308399e91fcbecb7cac37dd5d58fd03c49ac9efcec445341d5`
and must not be retargeted. Do not retarget corpus v3. Do not mutate
`fixtures/dr-103.v2/`.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-fixture-corpus.v4.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-fixture-corpus.v4.review-independent.codex.json`

Do not edit the subject or any fixture bytes. Do not commit.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.

You MAY read corpus v3 and the frozen Claude v3 REJECT. Do not read
the other current v4 reviewer.

## Claimed repairs

- CLAUDE-V3-S1: `TC-PATH.unicode-norm-duplicate` now includes `bin/entry`
  (new path under `fixtures/dr-103.v4/`)
- CLAUDE-V3-ADV-1: mismatch arm of reserved-list/live-grammar parity

## Attack

- Any scored lock fixture while DR-111 is OPEN
- Silent retarget of corpus v2 or v3
- Mutation of `fixtures/dr-103.v2/`
- unicode-norm-duplicate still masked by ENTRYPOINT_ABSENT
- Schema pin not the D-104 v11 successor
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus the verdict word.
