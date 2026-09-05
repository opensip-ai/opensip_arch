# Adversarial review — g21-fixture-corpus.v25

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g21-fixture-corpus.v25.json`
Expected sha256:
`a529674de076ea925c0bb4431f58f5c0b512dc9b89593ee593415c5796a68753`
Mode 0444. If the subject moves, OBJECT.

Copy bytes (four files; each sha256 must load-equal the D-348 payload):
- `docs/coop/artifacts/fixtures/g21.v21/macos-arm64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/macos-x86_64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/linux-x86_64/G21.cc5.prefix-far-over-posthandshake.bin`
- `docs/coop/artifacts/fixtures/g21.v21/linux-arm64/G21.cc5.prefix-far-over-posthandshake.bin`
Each sha256 `ad95131bc0b799c0b1af477fb14fcf26a6a9f76079e48bf090acb7e8367bfd0e`. Mode 0444. If any copy moves, OBJECT.

Frozen unrecorded predecessor:
- `docs/coop/artifacts/g21-fixture-corpus.v24.json` `e6bdde9804f1023913f57211cc38dd0ec0f53409107e205c493954013aa6b008`
  Stage A Claude REJECT 0 MUST-FIX, 1 SHOULD-FIX CLAUDE-G21FXV24-S-1; advisory CLAUDE-G21FXV24-A-1; 6 unlabeled observations (`de2e2a4c705002f42971e28d4a132d722b2cb7b727884336c285bd4a32641ab2`); Codex REJECT 0 MUST-FIX, 1 unlabeled SHOULD-FIX (`654ff63cf222199c725a9b6c02e3fbdf059d13759d62b7cf3231d25bc951403d`).
  Findings land at g21-fixture-corpus.v25. If g21-fixture-corpus.v24 moved, OBJECT.

Live predecessor Claude review still frozen:
- `docs/coop/artifacts/g21-fixture-corpus.v22.review-independent.claude2.json` `0fc9a9fa1a765d40bf05bba1cfe862c8b47ede9cb9e95bc9fafa71953f830f15` mode 0444. If this file moves, OBJECT.

Frozen leftover-join.v25 of G21 `8ad2558da11acbc84f5f43adbb20fc22322bc09b6eb1728ddc18c64957e27271` is current recorded G21 leftover remasurement (D-349). Do not remasure. leftover-join.v25 of G21 and g21-fixture-corpus.v25 are different lineages; their version numbers are unrelated. leftover-join.vN of G21 is one wrap token including `.vN`. Do not use a bare leftover-join.v25.

leftover-join.v14 of sarif remains current DR-122 remasurement. Do not remasure. Do not remasure g21-fixture-corpus.v21.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g21-fixture-corpus.v25.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g21-fixture-corpus.v25.review-independent.codex.json`

Write the review JSON with the Write tool. Freeze the written review 0444 after write. Do not hang on a shell write.

Do not edit the subject, copy bytes, predecessors, leftover-join.v25 of G21, leftover-join.v14 of sarif, occupancy v4, file 08, or COORD.
Do not commit. Do not SATISFY DR-114, DR-133, DR-117, DR-122, or DR-G21.
Do not invent an identifier for unlabeled Codex findings.
Do not invent observation identifiers.
Do not record g21-fixture-corpus.v22, g21-fixture-corpus.v23, or g21-fixture-corpus.v24 as current.
Do not rewrite basedOn.predecessorV22.role Findings land at g21-fixture-corpus.v23.
Do not rewrite basedOn.predecessorV23.role Findings land at g21-fixture-corpus.v24.
Do not rewrite basedOn.predecessorV24.role Findings land at g21-fixture-corpus.v25.
Do not read the other reviewer's current-turn review.

HEAD is `2fc2ae611a2bca187ec4f200a0da8a99fda3be22`. Last heading is D-349. Required-now is 28.
Live COORD sha256 is `8914b716ab415b7b61d470b910163221e1559fa87ddf8c31777a10f052aab66c`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-09-01.

Speaker is g21-fixture-corpus.v25. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d349.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v25.

Landed (do not re-open as unlanded):
- CLAUDE-G21FXV24-S-1: doesNot no longer asserts a stale observation count.
- Codex unlabeled SHOULD-FIX from g21-fixture-corpus.v24: same class. identifierInvented false.
- CLAUDE-G21FXV23-M-1 / M-2 and Codex unlabeled MUST-FIX from g21-fixture-corpus.v23.
- CLAUDE-G21FXV22-S-1 and unlabeled Codex g21-fixture-corpus.v22 SHOULD-FIX (wrap tokens).

Attack:
- CLAUDE-G21FXV24-S-1 not landed
- unlabeled Codex SHOULD-FIX not landed
- doesNot asserts an observation count that live cited Claude reviews do not support
- leftover-join.v25 of G21 collapsed with g21-fixture-corpus.v25
- a bare leftover-join.v25
- leftover-design of these copies measured stale as an authoring claim by this corpus
- leftover-design of OBL-G21-FX-AUTHORING claimed closed
- leftoverDesignClosedIfAcceptedAndRecorded not []
- leftover-join.v25 of G21 remasured
- leftover-join.v14 of sarif remasured
- g21-fixture-corpus.v21 remasured
- basedOn.predecessorV24.role Findings land rewritten off g21-fixture-corpus.v25
- basedOn.predecessorV23.role Findings land rewritten off g21-fixture-corpus.v24
- basedOn.d349.role is not the sole last-heading claimant
- proposedLaterWork[0] does not name g21-fixture-corpus.v25
- a deictic "This join" / "This leftover-join" / "This v25"
- SATISFIES DR-114, DR-133, DR-117, or DR-122
- cited digests do not match live bytes
- recordedInputs.HEAD differs from head
- g21-fixture-corpus.v24 recorded as current

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
