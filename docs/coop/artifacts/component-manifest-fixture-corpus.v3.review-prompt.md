# SATISFIED-GRADE review — component-manifest-fixture-corpus.v3 (DR-103)

Independent, refute not confirm. Did not author the corpus or the schema.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-fixture-corpus.v3.json`
Expected digest (Python hashlib, start AND end; re-measure at dispatch):
`7fe3d17161147089f00157598e268bba5ea2a37a6d77a94571489d916c9cdb84`

Schema contract: `component-manifest-schemas.v11.json`
`1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005`
(D-104 accepted schema successor). Fixture-facing subtrees are
value-identical to schemas.v9. Corpus v2 remains frozen at
`70248781118452308399e91fcbecb7cac37dd5d58fd03c49ac9efcec445341d5`
and must not be retargeted.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-fixture-corpus.v3.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-fixture-corpus.v3.review-independent.codex.json`

Do not edit the subject or any fixture bytes. Do not commit.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not retarget corpus v2.

You MAY read corpus v1 REJECT verdicts and corpus v2. Do not read
the other current v3 reviewer.

## Attack

- Any scored lock fixture while DR-111 is OPEN
- Calling a custody copy a lock
- Silent retarget of corpus v2
- Schema pin not the D-104 v11 successor
- V2-A1 / collisionUniverse violations
- Maximal incomplete; missing NAME members; stale-alias clocks
- Packet cases missing live index / reserved / live-grammar bytes
- Fake signatureRef; lock-digest mismatch without retained bytes
- PATH fixtures masked by ENTRYPOINT_ABSENT
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
