# Independent review — component-manifest-fixture-corpus.v1 (DR-103 fixture half)

Independent, refute not confirm. Did not author the corpus.
Work in `/Users/sb/code/opensip-ai/opensip`.

**SUBJECT:** `docs/coop/artifacts/component-manifest-fixture-corpus.v1.json`
Expected digest at dispatch (measure yourself at start AND end):
`d81a4ef9ed26405a07e84ae0be9a3d2048fd9a6126b1f93d139a5a499204b542`

Every path named in `authored[]` and `supportingBytes[]` is part of
the subject. Recompute each sha256 from live bytes. If any digest
in the index does not match live bytes, that is a blocker.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/component-manifest-fixture-corpus.v1.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/component-manifest-fixture-corpus.v1.review-independent.codex.json`

Do not read the other reviewer's files. Do not edit any other file.
Do not commit. Do not edit the subject. If the subject moves, OBJECT.

This is SATISFIED-GRADE review of fixture authoring, not a recording.
You do not mark DR-103 SATISFIED. You do not edit file 08. You do
not authorize `docs/v2/implementation/`.

## Governing sources (re-measure)

- `docs/coop/artifacts/component-manifest-schemas.v2.json`
  `73114ddec12d3ec6dfbcb51b7002d983ff9dbfa1fa39189bb025008f1f501381`
  especially `/testCorpusRequirements/classes` (TC-ACCEPT through
  TC-BYTE-EXACT) and `/rejectionRules`.
- `docs/coop/artifacts/component-manifest-schemas.v2.review-independent.json`
  `42004c95474a66a8bd7685862c9e205fe7c4a7fadc97ab90e408a2fb04f238dd`
  advisory V2-A1 (same-stableId multi-version coexistence).
- File 08 DR-103 row (locate by ID). D-013 SATISFIED-refusal stands
  until fixture authoring exists and is independently reviewed.
- D-056: DR-103 remains ineligible for SATISFIED until fixture
  authoring exists and is independently reviewed. Fixture generation
  is routed to DR-120 / DR-G15 (ID-DEP-8).
- D-002: Windows deferred. First slice TypeScript / CLI-first /
  offline / contained.

## What to attack

- A required class member is missing or only named, not authored.
- Alias-cycle is still alias-equals-name (must be a real cycle).
- Digest-mismatch is not a single-byte flip of stored bytes against
  a recorded digest of the unflipped source.
- ACCEPT fixtures that cannot coexist share one (stableId, version).
- Index does not carry the ACCEPT set that can coexist.
- Lock does not resolve a multi-component closure.
- Windows-only path classes silently present, or silently claimed
  complete without naming the D-002 deferral.
- Ceremony fixtures (wrong key, expiry, revoked namespace, threshold)
  smuggled in from DR-112.
- ENVELOPE_MISMATCH authored while ID-DEP-1 and ID-DEP-5 are open.
- Informal expected outcomes that cannot be decided from the schema
  (`ACCEPT iff`, `RESOLVE`, `DISCLOSE`) unless the packet actually
  carries the custody data those outcomes require.
- Digests that do not recompute. Duplicate JSON keys in any fixture
  other than the dedicated TC-BYTE-EXACT.duplicate-json-key file.
- Silent SATISFIED / QUALIFIED / implementation authorization.
- Claiming this corpus is a DR-120 adapter or that ID-DEP-8 is closed.

CONSENT / ACCEPT only if 0 MUST-FIX / 0 blockers and 0 SHOULD-FIX.
Advisories are allowed under ACCEPT-WITH-ADVISORIES.

Output: verdict ACCEPT | REJECT | ACCEPT-WITH-ADVISORIES, blockers,
advisories, whatIVerified, whatIDidNotCheck, recordedInputs,
environment (git HEAD, subject digest start/end, did not read the
other reviewer).

Final chat: short coordinator summary plus verdict word.
