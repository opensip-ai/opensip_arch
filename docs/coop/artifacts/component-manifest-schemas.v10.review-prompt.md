# Independent review — component-manifest-schemas.v10 (DR-103 successor)

Independent, refute not confirm. Did not author v2–v10.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v10.json`
Expected digest (Python hashlib, start AND end):
`e71dda5d5c5fdea2cc0845c5e2816dd98166daf888516c92363d46571d38d1e6`

Predecessor v9 `52b3ab93d531d7e229f098deef8d944040bc93461c3e5c70be775002a6f7b791`
Claude 2 v9 REJECT `0f15bd315fa8dbbfe259255ffb97db0d56b22845f90b89630d4081391d8ecb5e`
Codex v9 REJECT `7eb3a857d6da18f9d1886b5963649633fd0c50555d26c63de640e8fe1acf4abd`

You MAY read those two v9 verdicts and the predecessor. Do not read
the other current v10 reviewer.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v10.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v10.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.
Do not edit file 08 or COORDINATOR-DECISIONS.md.
Do not edit `component-manifest-fixture-corpus.v2.json` (frozen 0444).

## Measure without hanging

Use Python hashlib over `pathlib.Path.read_bytes()`. Write incrementally.

## Claimed repairs

- V9-S1 (both): corpus v2 cited at live frozen digest
  `70248781118452308399e91fcbecb7cac37dd5d58fd03c49ac9efcec445341d5`;
  `reMeasurementAtV10` records it; no post-freeze retarget
- V9-A1: `citationDiscipline` version-neutral (`reMeasurementAtVN`)
- V9-A2: method roster order matches repairLog append order
- V9-A3: OD-2 file-08 echo named as application-time only

## Attack

- Stranded / unresolvable fixture-corpus digest
- Silent retarget of the frozen corpus v2 file
- Any still-producible lock
- Calling a custody copy a lock
- Silent v9→v10 path outside the v10 repairLog
- SATISFIED / QUALIFIED / implementation authorization
- Inventing findings the named v9 verdicts do not contain

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: short coordinator summary plus verdict word.
