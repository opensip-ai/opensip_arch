# Adversarial review — g21-fixture-corpus.v21

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g21-fixture-corpus.v21.json`
Expected sha256:
`9409f374863cb9aa1b0e8c0f0c76663d0e15e577462b8466f731ea8d9b1ce385`
Mode 0444. If the subject moves, OBJECT.

Fixture bytes remain:
- `docs/coop/artifacts/fixtures/g21.v20/G21.cc5.prefix-far-over-posthandshake.bin`
  sha256 `ad95131bc0b799c0b1af477fb14fcf26a6a9f76079e48bf090acb7e8367bfd0e`
  Mode 0444. 4 bytes. If the fixture moves, OBJECT.

Frozen predecessor:
- `docs/coop/artifacts/g21-fixture-corpus.v20.json` `9b8b88a7143bf65eefa6f9a47ec3cb61b0cefdf7b93a93bb030f2314436b41ae`
  Unrecorded. Stage A Claude REJECT 1 MUST-FIX CLAUDE-G21FXV20-M-1; advisories CLAUDE-G21FXV20-A-1 CLAUDE-G21FXV20-A-2; 9 unlabeled observations (`9a38058ed3e96e7e10247a7fc8511c2939ac7b9bf95d0b242a08c3dfa9addf31`); Codex REJECT 1 unlabeled SHOULD-FIX (`2203804f6b5cdc837c2d4a5da791a042d6f90f3480f389ab7aa9584ca9500e71`).
Findings land at g21-fixture-corpus.v21. If g21-fixture-corpus.v20 moved, OBJECT.

Frozen recorded predecessors (unmoved; not this speaker):
- `docs/coop/artifacts/g21-fixture-corpus.v19.json` `c447c03df470bd03cab4931f3753f95a3b1a2daa04e70da22696f4cf73f14342`
  Recorded D-337. Dual ACCEPT 0/0.
- leftover-join.v20 of G21 `docs/coop/artifacts/g21-leftover-join.v20.json` `213d11c824c2c775461211f073b8a77249baae5a95aba2083b45adbf3646ba5c`
  Recorded D-338. Current recorded G21 leftover remasurement. Do not remasure.
- leftover-join.v14 of sarif `docs/coop/artifacts/sarif-leftover-join.v14.json` `8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97`
  Recorded D-347. Current recorded DR-122 leftover remasurement. Do not remasure.
If any of those moved, OBJECT.

Frozen g21-fixture-corpus.v17 and g21-fixture-corpus.v18 stay unrecorded. Do not record them as current. Do not rewrite basedOn.predecessorV18.role Findings land at g21-fixture-corpus.v19. Do not rewrite basedOn.predecessorV17.role Findings land at g21-fixture-corpus.v18. Do not rewrite basedOn.predecessorV15.role Findings land at g21-fixture-corpus.v16.

g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. Do not collapse g21-fixture-corpus.v21 with leftover-join.v20 of G21.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g21-fixture-corpus.v21.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g21-fixture-corpus.v21.review-independent.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not edit the fixture bytes. Do not edit g21-fixture-corpus.v20, prior corpora, leftover-join.v20 of G21, leftover-join.v14 of sarif, occupancy v4, D-319 drafts, file 08, or COORD.
Do not commit. Do not SATISFY DR-114, DR-133, DR-117, DR-122, or DR-G21.
Do not remasure leftover-join.v20 of G21. Do not remasure leftover-join.v14 of sarif.
Do not close leftover-design of OBL-G21-FX-AUTHORING.
Do not pin N=65536 as prefix-only RF-2.
Do not invent 26214400.
Do not invent an identifier for the unlabeled Codex SHOULD-FIX.
Do not invent observation identifiers for the 9 unlabeled Claude observation strings.
Do not record g21-fixture-corpus.v20 as current.
Do not read the other reviewer's current-turn review.

HEAD is `6eb703f972650d840d033e67b33244837e6a5589`. Last heading is D-347. Required-now is 28.
Live COORD sha256 is `b43bed3702aaad3b40f6201179f94282803cee6a87ead1c90a5fa9ec163b0325`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

Speaker is g21-fixture-corpus.v21. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d347.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v21. Frozen g21-fixture-corpus.v20 stays unrecorded. Fixture bytes remain at fixtures/g21.v20/.

Landed g21-fixture-corpus.v20 Stage A findings (do not re-open as unlanded):
- Claude CLAUDE-G21FXV20-M-1: authoredCatalog.doesNotMutate restores the thirteen dropped frozen fixture directories that exist on disk. fixtures/g21.v16/ is retained. fixtures/g21.v20/ stays out because this speaker authors it.
- Codex unlabeled SHOULD-FIX: same class. identifierInvented false.
- Claude CLAUDE-G21FXV20-A-1, CLAUDE-G21FXV20-A-2 travel as honesty work. Not a fix.
- Claude 9 unlabeled observation strings travel as honesty work. No observation identifier invented.

Attack:
- CLAUDE-G21FXV20-M-1 not landed
- unlabeled Codex SHOULD-FIX not landed
- an identifier invented for unlabeled Codex SHOULD-FIX
- observation identifiers invented for the 9 unlabeled Claude observation strings
- authoredCatalog.doesNotMutate still drops frozen fixture directories that exist on disk
- leftover-design of OBL-G21-FX-AUTHORING claimed closed
- leftoverDesignClosedIfAcceptedAndRecorded not []
- CC-5 claimed fully authored
- prefix exactly at the operative bound dropped from remainderAfterThisCorpus or whatIsNotAuthored
- N=65536 pinned as prefix-only RF-2
- 26214400 invented as a bound
- 16777216 prefix bytes from g21-fixture-corpus.v11 reused
- 16777217 prefix bytes from g21-fixture-corpus.v16 reused
- fixture bytes moved off fixtures/g21.v20/ or are not closed 4-byte big-endian unsigned 4294967295
- leftover-join.v20 of G21 remasured
- leftover-join.v14 of sarif remasured
- g21-fixture-corpus.v20 recorded as current
- g21-fixture-corpus.v21 collapsed with leftover-join.v20 of G21
- basedOn.d347.role is not the sole last-heading claimant
- basedOn.predecessorV20.role Findings land rewritten off g21-fixture-corpus.v21
- a deictic "This join" / "This leftover-join" / "This v21"
- SATISFIES DR-114, DR-133, DR-117, or DR-122
- per-D-002-platform copies claimed authored by this speaker
- live required-now claimed other than 28
- file 08 edited
- cited digests do not match live bytes
- recordedInputs.HEAD differs from head
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
