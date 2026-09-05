# Adversarial review — g21-fixture-corpus.v20

Independent, refute not confirm.

**SUBJECT:** `docs/coop/artifacts/g21-fixture-corpus.v20.json`
Expected sha256:
`9b8b88a7143bf65eefa6f9a47ec3cb61b0cefdf7b93a93bb030f2314436b41ae`
Mode 0444. If the subject moves, OBJECT.

Fixture bytes:
- `docs/coop/artifacts/fixtures/g21.v20/G21.cc5.prefix-far-over-posthandshake.bin`
  sha256 `ad95131bc0b799c0b1af477fb14fcf26a6a9f76079e48bf090acb7e8367bfd0e`
  Mode 0444. 4 bytes. If the fixture moves, OBJECT.

Frozen recorded predecessors (unmoved; not this speaker):
- `docs/coop/artifacts/g21-fixture-corpus.v19.json` `c447c03df470bd03cab4931f3753f95a3b1a2daa04e70da22696f4cf73f14342`
  Recorded D-337. Dual ACCEPT 0/0.
- `docs/coop/artifacts/g21-fixture-corpus.v16.json` `5b04ead4cb88950c9ccf43f6b416a71d3157b56825a27cad02f2b323ca36865b`
  Recorded D-335. Dual ACCEPT 0/0. Prefix 16777217 must not be reused.
- `docs/coop/artifacts/g21-fixture-corpus.v11.json` `13ede1101e3d689130557e070bd683b62cd931b30c670ed2188a825a49fefd91`
  Recorded D-301. Dual ACCEPT 0/0. Prefix 16777216 must not be reused.
- leftover-join.v20 of G21 `docs/coop/artifacts/g21-leftover-join.v20.json` `213d11c824c2c775461211f073b8a77249baae5a95aba2083b45adbf3646ba5c`
  Recorded D-338. Dual ACCEPT 0/0. Current recorded G21 leftover remasurement. leftoverDesign [OBL-G21-FX-AUTHORING]. Do not remasure.
- leftover-join.v14 of sarif `docs/coop/artifacts/sarif-leftover-join.v14.json` `8ecea58e0b6823968ebffbbe75640ba3473446985047fd709e308a4a7e40bf97`
  Recorded D-347. Dual ACCEPT 0/0 then dual CONSENT 0/0. Current recorded DR-122 leftover remasurement. Do not remasure.
If any of those moved, OBJECT.

Frozen g21-fixture-corpus.v17 and g21-fixture-corpus.v18 stay unrecorded. Do not record them as current. Do not rewrite basedOn.predecessorV18.role Findings land at g21-fixture-corpus.v19. Do not rewrite basedOn.predecessorV17.role Findings land at g21-fixture-corpus.v18. Do not rewrite basedOn.predecessorV15.role Findings land at g21-fixture-corpus.v16.

g21 leftover-join and g21-fixture-corpus are different lineages; their version numbers are unrelated. Do not collapse g21-fixture-corpus.v20 with leftover-join.v20 of G21.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/g21-fixture-corpus.v20.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/g21-fixture-corpus.v20.review-independent.codex.json`

Write the review JSON with the Write tool. Do not hang on a shell write.

Do not edit the subject. Do not edit the fixture bytes. Do not edit prior corpora, leftover-join.v20 of G21, leftover-join.v14 of sarif, occupancy v4, D-319 drafts, file 08, or COORD.
Do not commit. Do not SATISFY DR-114, DR-133, DR-117, DR-122, or DR-G21.
Do not remasure leftover-join.v20 of G21. Do not remasure leftover-join.v14 of sarif.
Do not close leftover-design of OBL-G21-FX-AUTHORING.
Do not pin N=65536 as prefix-only RF-2.
Do not invent 26214400.
Do not invent identifiers.
Do not read the other reviewer's current-turn review.

HEAD is `6eb703f972650d840d033e67b33244837e6a5589`. Last heading is D-347. Required-now is 28.
Live COORD sha256 is `b43bed3702aaad3b40f6201179f94282803cee6a87ead1c90a5fa9ec163b0325`; file 08 sha256 is `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`. Date 2026-08-31.

Speaker is g21-fixture-corpus.v20. Candidate binds NOTHING. leftoverDesignClosedIfAcceptedAndRecorded []. basedOn.d347.role is the sole last-heading claimant. proposedLaterWork[0] names g21-fixture-corpus.v20. This is first-authoring of G21.cc5.prefix-far-over-posthandshake. It is not a leftover-join remasurement.

Attack:
- leftover-design of OBL-G21-FX-AUTHORING claimed closed
- leftoverDesignClosedIfAcceptedAndRecorded not []
- CC-5 claimed fully authored
- prefix exactly at the operative bound dropped from remainderAfterThisCorpus or whatIsNotAuthored
- N=65536 pinned as prefix-only RF-2
- 26214400 invented as a bound
- 4294967295 invented rather than quoted from the 4-byte unsigned encoding width
- 16777216 prefix bytes from g21-fixture-corpus.v11 reused
- 16777217 prefix bytes from g21-fixture-corpus.v16 reused
- fixture bytes are not closed 4-byte big-endian unsigned 4294967295 with no body
- leftover-join.v20 of G21 remasured
- leftover-join.v14 of sarif remasured
- g21-fixture-corpus.v20 collapsed with leftover-join.v20 of G21
- basedOn.d347.role is not the sole last-heading claimant
- a deictic "This join" / "This leftover-join" / "This v20"
- SATISFIES DR-114, DR-133, DR-117, or DR-122
- per-D-002-platform copies claimed authored by this speaker
- NT-6 or FC-NC-CA1-PROCESS-TREE authored
- live required-now claimed other than 28
- file 08 edited
- cited digests do not match live bytes
- recordedInputs.HEAD differs from head
- authoredCatalog.doesNotMutate dropped frozen fixture directories that exist on disk
- authorizes docs/v2/implementation/

ACCEPT only if no MUST-FIX or SHOULD-FIX.
Final chat: ACCEPT or REJECT.
