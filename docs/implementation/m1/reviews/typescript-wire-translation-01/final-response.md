I've written the TS2 wire translation inventory to `/tmp/opensip-implementation/m1-typescript-wire-translation-01/`. The build script runs clean: every one of the 182 inherited wire-schema members has exactly one row, with 0 failures. It's a table for root review, not an approval, and it proposes no wire changes. Nothing was written to the architecture repo, and no commits were made.

**Files**
- `fields.json`: one row per member. Each row has the exact name, required/optional, CBOR wire type, bounds or closed vocabulary, and the original text with source path, SHA and selector. It also has the disposition, the schema-native replacement ref where one exists, the derivation, and handwritten checks (listed apart from shape) with gaps. It also holds 18 new member rows, 12 before/after member-list comparisons, the G7 traces, the inherited links and the gap register.
- `translation.md`: the same content as reviewable tables, plus sections on stage identity and FactBatch V1 vs V3.
- `coverage.json`: the counts.
- `tools/build.py` and `tools/rows_*.py`: the read-only script that regenerates all three and asserts coverage.

**Coverage**
- **Members:** 4 envelope, 16 frame-table rows, 78 definition members and 84 payload members. All 28 closed records had their required list checked against their field map.
- **Dispositions:** 106 retained, 61 replaced, 15 value-substituted, 18 new.
- **Refs:** 92 rows have a schema-native ref. All refs resolve, and 83 of them were checked against the row's wire type with 0 mismatches.
- **Pins:** the script checks the SHA of all 13 source files it reads; all match.

**What the table shows**
- **Envelope:** `protocolMajor` becomes exactly 2, and `frameType` gains `NativeContextVerified`. `TypeScriptFrameV2` is only a proposed implementation name, not a wire field.
- **Name-only replacements:** the Hello/HelloAck, OpenUniverse, UniverseAccepted, Coverage, Unavailable and BudgetExhausted successors keep every inherited member name. The only added members are Hello's `expectedCapabilities` and `identityVersions`, and HelloAck's `identityVersions`.
- **Stage identity:** logical C-2 `stageId` text, the Analyze `stageOrdinal` and the Plan ordinal (which exists only in the host's dispatch binding) are kept apart. Analyze may carry a subset of the Plan's stages.
- **FactBatch:** the historical `FactBatchV1` (`facts` plus `batchCommitment`) and the negotiated `FactBatchV3` (`candidates` plus `occupancyCompanions`, no batch commitment) are tabulated separately.
- **G7 trace:**
  - TS `FactCandidateV1` has the same 14 members as fact-plane's candidate schema, but its universe-id values are superseded by a different §0 row than Rust's.
  - TS `CoverageKeyV1` (8 members) stays the request key.
  - The native `CoverageKeyV2` (5 members, bare-hex universes) is a different record: the key inside each coverage entry.

**Open gaps (recorded, not guessed)**
- **TS2-G4 is the most significant.** The inherited subject-scope commitment is one value per stage, shared by every key. native-evidence §4.1a instead defines a per-key value that includes the universes and relation. §0 doesn't mark the inherited rule superseded, so for cross-universe keys the two rules can't both hold. This needs an owner decision.
- **G1:** the chunk `bytes` and `canonicalRelationPayload` are recorded only as byte-strings. Any JSON, TypeScript or Rust mapping needs your selection.
- **G2:** plain JSON Schema can't check NFC, UTF-8 byte bounds or canonical CBOR.
- **G3:** no bound is stated for the request/result `stageId`.
- **G5:** `AnchorRefV1` has no field types, so five of its members are marked `UNSTATED`.
- **G6:** the FactBatch and Unavailable payloads are chosen by negotiation or phase, not by anything on the wire.
- **G8:** the successor arrays are bounded more weakly than the inherited text implies.
- **G9:** it's unstated whether a major-2 projection needs its own wire-schema commitment.
- **G10:** `manifestSha256` is described as bare hex, but its commitment domain would produce `sha256:`-prefixed text.
- **G11:** several text and array members have no bound.
- **G12:** which commitment domain each coverage commitment field uses is inferred from names, not stated.

The reference-model functions linked as handwritten check owners are executable law within their stated scope, not implementation code. I didn't run a generator or validate any instances.
