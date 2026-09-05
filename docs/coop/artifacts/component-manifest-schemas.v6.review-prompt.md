# Independent review — component-manifest-schemas.v6 (DR-103 successor)

Independent, refute not confirm. Did not author v2–v6.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-schemas.v6.json`
Expected digest at dispatch (measure yourself at start AND end):
`51b0a0b7c884dc106b89768661d9550597b941064454b2155f138f6dd164f401`

Predecessor v5 `c58f062dd9974cd7df7edb18f47eab238eea6e4bceed28c0c66a7a4ce0fb3835`
Codex v5 REJECT `112b522d0f1f2695a81d34a115ed0c4ffff12ad7d42786ee78bec9977c5288ab`
Claude 2 v5 REJECT `c5b300e895ccf2e5d1726d2676f0c9409f03799a69fe14463264c8e3ff36b8e6`

You MAY read those two v5 verdicts and the predecessor. Do not read
the other current v6 reviewer.

**WRITE ONLY (when dispatched):**
- Claude 2: `docs/coop/artifacts/component-manifest-schemas.v6.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-schemas.v6.review-independent.codex.json`

Do not edit the subject. Do not commit. If the subject moves, OBJECT.
Do not mark DR-103 SATISFIED. Do not authorize implementation.

## Measure without hanging

Do **not** shell-out `shasum` on the ~118KB subject inside a long agent
loop. Use Python:

```python
import hashlib, pathlib
p = pathlib.Path("docs/coop/artifacts/component-manifest-schemas.v6.json")
print(hashlib.sha256(p.read_bytes()).hexdigest())
```

Write the verdict file incrementally (header, then findings, then
environment). Do not keep the whole subject in the chat as a paste.

## Claimed repairs (both v5 REJECT verdicts)

Finding-id collision: Claude V5-S1 ≠ Codex V5-S1; Claude V5-A1 ≠ Codex
V5-A1. The repairLog uses `CLAUDE-V5-S1` and `CLAUDE-V5-A1` for the
Claude-unique ids.

- V5-B1 (both): lock-bearing TC-SIG / TC-BYTE-EXACT members deferred
  to DR-111; admission+index halves remain
- V5-B2 (Claude) / V5-S1 (Codex): `measuredAtAuthoring` renamed
  `measuredAtV2Authoring`; live SRC-08/SRC-D/SRC-FRZ pins only at
  `reMeasurementAtV6`; historical V4-S2 entry left unmutated
- V5-A1 (Codex) / CLAUDE-V5-S1: `basedOn.method` roster is closed;
  no successor-hedge
- V5-S2 (Claude): `lockSchema.resolved` and the ordering rule carry
  `scope`; join is `(stableId, version, scope)`
- CLAUDE-V5-A1: `lockSchema.purpose` carries the no-lock-until-DR-111
  clause
- V5-A2: both request forms are future schema shapes
- V5-A3: dual-scope exclusion is provenance-qualified
- V5-A4: `shadowedBy` phrasing matches the triple
- V5-A5: RJ-2 qualifier covers live names/aliases AND mounted roots

## Attack

- Any still-producible lock (production sites AND requirement sites)
- Calling a custody copy a lock
- `lockSchema.resolved` still unable to address a
  `(stableId, version, scope)` index entry
- Open-ended `basedOn.method` roster / in-place future-fold hedge
- `measuredAtAuthoring` (or equivalent) still asserted on moved
  whole-document pins
- RJ-1 unfirable
- Dual-scope key regression
- Silent v5→v6 path outside the v6 repairLog
- SATISFIED / QUALIFIED / implementation authorization
- Inventing Claude or Codex findings the named verdict files do not
  contain

ACCEPT only at 0 blockers and 0 SHOULD-FIX.

Final chat: short coordinator summary plus verdict word.
