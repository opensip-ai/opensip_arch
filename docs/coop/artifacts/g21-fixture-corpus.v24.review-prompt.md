# Adversarial review — g21-fixture-corpus.v24

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g21-fixture-corpus.v24.json`
Expected sha256:
`e6bdde9804f1023913f57211cc38dd0ec0f53409107e205c493954013aa6b008`
Mode 0444. If the subject moves, OBJECT.

Copy bytes (four files; each sha256 must load-equal the D-348 payload):
- `docs/coop/artifacts/fixtures/g21.v21/macos-arm64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/macos-x86_64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/linux-x86_64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/linux-arm64/G21.cc5.prefix-far-over-posthandshake.bin`
Each sha256 `ad95131bc0b799c0b1af477fb14fcf26a6a9f76079e48bf090acb7e8367bfd0e`. Mode 0444. 4 bytes. If any copy moves, OBJECT.

Frozen live predecessor Claude review (authoritative bytes; 0444):
- `docs/coop/artifacts/g21-fixture-corpus.v22.review-independent.claude2.json`
  sha256 `0fc9a9fa1a765d40bf05bba1cfe862c8b47ede9cb9e95bc9fafa71953f830f15`
  Live verdict REJECT 0 MUST-FIX, 1 SHOULD-FIX CLAUDE-G21FXV22-S-1; advisory CLAUDE-G21FXV22-A-1; 5 unlabeled observations.
  If this file moves, OBJECT.

Frozen unrecorded predecessors:
- `docs/coop/artifacts/g21-fixture-corpus.v23.json` `d5cbc7fb39125aa2bdfd7546b80a201bff1f54fe37c561a1b87efad92d9e2af6`
  Stage A Claude REJECT 2 MUST-FIX CLAUDE-G21FXV23-M-1 CLAUDE-G21FXV23-M-2; advisories CLAUDE-G21FXV23-A-1 CLAUDE-G21FXV23-A-2; 6 unlabeled observations (`28e78935eaa19d6d6dfa5bff5288af0fb6da6748df8fd229a2f7a930ddb5b3ad`); Codex REJECT 1 unlabeled MUST-FIX (`dfd8feae5c8b675af08841269627ad290c5e494cd85851d45511af576068e90d`).
  Findings land at g21-fixture-corpus.v24. If g21-fixture-corpus.v23 moved, OBJECT.
- `docs/coop/artifacts/g21-fixture-corpus.v22.json` `9ce0febbddc2c8f16febee87ce8e270789a10041eb66c0ef1172c58658ea36c5`
  Stage A Claude REJECT 0 MUST-FIX, 1 SHOULD-FIX CLAUDE-G21FXV22-S-1 (`0fc9a9fa1a765d40bf05bba1cfe862c8b47ede9cb9e95bc9fafa71953f830f15`); Codex REJECT 0 MUST-FIX, 1 unlabeled SHOULD-FIX (`843f7d559e79b4ff73897b48f6561f0e4d07375032374e1dd801cf8dc282a206`).
  Findings land at g21-fixture-corpus.v23. If g21-fixture-corpus.v22 moved, OBJECT.

Frozen recorded:
- leftover-join.v25 of G21 `8ad2558da11acbc84f5f43adbb20fc22322bc09b6eb1728ddc18c64957e27271` current G21 leftover remasurement (D-349). Do not remasure.
- leftover-join.v14 of sarif `8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97` current DR-122 leftover remasurement (D-347). Do not remasure.
- g21-fixture-corpus.v21 `9409f374863cb9aa1b0e8c0f0c76663d0e15e577462b8466f731ea8d9b1ce385` D-348 first-authoring. Do not remasure.

g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. Do not collapse g21-fixture-corpus.v24 with leftover-join.v24 of G21. leftover-join.vN of G21 is one wrap token including `.vN`.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g21-fixture-corpus.v24.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g21-fixture-corpus.v24.review-independent.codex.json`

Write the review JSON with the Write tool. Freeze the written review 0444 after write. Do not hang on a shell write.

Do not edit the subject, copy bytes, fixtures/g21.v20/, g21-fixture-corpus.v23, g21-fixture-corpus.v22, g21-fixture-corpus.v22.review-independent.claude2.json, leftover-join.v25 of G21, leftover-join.v14 of sarif, occupancy v4, D-319 drafts, file 08, or COORD.
Do not commit. Do not SATISFY DR-114, DR-133, DR-117, DR-122, or DR-G21.
Do not remasure leftover-join.v25 of G21. Do not remasure leftover-join.v14 of sarif. Do not remasure g21-fixture-corpus.v21.
Do not invent an identifier for unlabeled Codex findings.
Do not invent observation identifiers.
Do not record g21-fixture-corpus.v22 or g21-fixture-corpus.v23 as current.
Do not rewrite basedOn.predecessorV22.role Findings land at g21-fixture-corpus.v23.
Do not rewrite basedOn.predecessorV23.role Findings land at g21-fixture-corpus.v24.
Do not rewrite basedOn.predecessorV20.role Findings land at g21-fixture-corpus.v21.
Do not read the other reviewer's current-turn review.

HEAD is `2fc2ae611a2bca187ec4f200a0da8a99fda3be22`. Last heading is D-349. Required-now is 28.
Live COORD sha256 is `8914b716ab415b7b61d470b910163221e1559fa87ddf8c31777a10f052aab66c`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-09-01.

Speaker is g21-fixture-corpus.v24. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d349.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v24.

Landed (do not re-open as unlanded):
- CLAUDE-G21FXV23-M-1: predecessorV22 Claude review digest pins live `0fc9a9fa1a765d40bf05bba1cfe862c8b47ede9cb9e95bc9fafa71953f830f15`.
- CLAUDE-G21FXV23-M-2: predecessorV22 Claude verdict restated from live bytes as REJECT 0 MUST-FIX, 1 SHOULD-FIX CLAUDE-G21FXV22-S-1.
- Codex unlabeled MUST-FIX: same class as CLAUDE-G21FXV23-M-1. identifierInvented false.
- CLAUDE-G21FXV22-S-1 and unlabeled Codex g21-fixture-corpus.v22 SHOULD-FIX: leftover-join wrap tokens qualified separately. Landed at g21-fixture-corpus.v23.
- CLAUDE-G21FXV22-A-1 / CLAUDE-G21FXV23-A-1 travel as honesty work.
- CLAUDE-G21FXV23-A-2 travels as honesty work (review outputs frozen 0444).

Attack:
- CLAUDE-G21FXV23-M-1 not landed
- CLAUDE-G21FXV23-M-2 not landed
- unlabeled Codex MUST-FIX not landed
- cited digest of g21-fixture-corpus.v22.review-independent.claude2.json does not load-equal live bytes
- predecessorV22 Claude verdict contradicts live bytes
- CLAUDE-G21FXV22-S-1 omitted or an identifier invented for unlabeled Codex findings
- basedOn.predecessorV22.role Findings land rewritten off g21-fixture-corpus.v23
- leftover-design of these copies measured stale as an authoring claim by this corpus
- leftover-design of OBL-G21-FX-AUTHORING claimed closed
- leftoverDesignClosedIfAcceptedAndRecorded not []
- leftover-join.v25 of G21 remasured
- leftover-join.v14 of sarif remasured
- g21-fixture-corpus.v21 remasured
- CC-5 claimed fully authored
- prefix exactly at the operative bound dropped
- N=65536 pinned as prefix-only RF-2
- Windows copied
- basedOn.d349.role is not the sole last-heading claimant
- proposedLaterWork[0] does not name g21-fixture-corpus.v24
- a deictic "This join" / "This leftover-join" / "This v24"
- SATISFIES DR-114, DR-133, DR-117, or DR-122
- cited digests do not match live bytes
- recordedInputs.HEAD differs from head
- g21-fixture-corpus.v22 or g21-fixture-corpus.v23 recorded as current

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
