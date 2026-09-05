# Independent review — component-manifest-fixture-corpus.v2 (DR-103)

**DO NOT DISPATCH until schemas.v9 (or a later successor) is
independently ACCEPTED at 0 blockers / 0 SHOULD-FIX.** SATISFIED-GRADE
corpus review against an unaccepted schema is not lawful.

Independent, refute not confirm. Did not author the corpus or the schema.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-fixture-corpus.v2.json`
Re-measure the digest at dispatch; the draft digest at prompt authoring is
`70248781118452308399e91fcbecb7cac37dd5d58fd03c49ac9efcec445341d5`
and may move before dispatch.

Schema contract at draft time: `component-manifest-schemas.v9.json`
`52b3ab93d531d7e229f098deef8d944040bc93461c3e5c70be775002a6f7b791`.
If the accepted schema is a later successor, this prompt must be
rewritten before dispatch.

**WRITE ONLY (when dispatched):**
- Claude 2: `docs/coop/artifacts/component-manifest-fixture-corpus.v2.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-fixture-corpus.v2.review-independent.codex.json`

Do not edit the subject or any fixture bytes. Do not commit.
Do not mark DR-103 SATISFIED. Do not authorize implementation.

## Attack

- Any scored lock fixture while DR-111 is OPEN
- Calling a custody copy a lock
- V2-A1 / collisionUniverse violations (same-stableId RJ-1 unfirable;
  live-name uniqueness not over DIFFERENT (stableId, provenance))
- Maximal incomplete; missing NAME members; stale-alias clocks
- Packet cases missing live index / reserved / live-grammar bytes
- Fake signatureRef; lock-digest mismatch without retained bytes
- PATH fixtures masked by ENTRYPOINT_ABSENT
- SATISFIED / QUALIFIED / implementation authorization

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
