# CODEX2 review — D4-4 r2

## Verdict

**ACCEPT-UNIT**

The frozen subject manifest SHA-256 is `c5773c306cffa8b68d4e7904bfe29636e176d8c60890aea002944047ac494056`. All 955 declared members rehash exactly. All 32 candidate paths match the frozen product map and the live candidate bytes; the 21 existing paths are based on product commit `c31809cb4993c5c2bbba3d004d9337f12f18d17b`, the 11 new paths are absent from that parent, and the architecture authority resolves at `a70566340747162650b863693e1ab3d887845b18`.

R1 remains a rejected historical subject with verdict **REQUIRED-FINDINGS** and manifest `5d129b0f2ad4b6563b7f6f15a7403b24c54a699135a3ff135be4cd8ed2f886e4`. This R2 verdict does not alter or accept R1. The frozen R1-to-R2 source delta is exactly the five declared paths.

## R1 correction

`TS2_IDENTITY_VERSIONS` is an independent literal projection of the selected `IdentityVersionsV1` schema. Its source control verifies the exact four required keys and constants, rejects extra schema properties through the closed definition, and ties both `TypeScriptHelloV2` and `TypeScriptHelloAckV2` required `identityVersions` fields to that definition.

The factory checks the actual sender Hello against this authority with an exact count and charged key/value checks. It separately checks the actual receiver context with an exact count and charged ordered key/value comparisons. These checks occur during specification validation before any native recheck; neither assembled output supplies the expected values for the other. The seven controls cover sender-only drift, receiver-only drift, agreed-wrong value, missing key, substituted key, extra key, and an empty map. The agreed-wrong cases explicitly establish output agreement and still refuse before any recheck.

All three correction mutants were compiled and killed by named runtime assertions: replacing the independent authority with output agreement, omitting the receiver-to-authority judgment, and drifting the independent constant map. Their original targets are restored and byte-exact with the frozen candidate.

## Complete-unit assessment

The unchanged D4-4 implementation remains consistent with the complete R1 review: independent control/selection and codec authorities, pristine realized sender transfer, exact TS2 and Rust3 limits and identity projections, charged comparisons and owned launch material, closed role-specific launch shapes, operation-borrowed retained-tree native checks, the exact CMS `Entrypoint` operation requirement, physical post-assembly rechecks, and typed Budget/Io/eight-way Corrupt refusal partitions are preserved. Refusal does not yield a `VerifiedLaunch`, disclose Source bytes, or spawn work.

The first-party peer audit correction is confined to the test fixture. It writes a complete pending sibling and atomically renames it over the observation while holding the existing audit mutex. The original host-r6 EOF/partial-JSON failure remains frozen as failed evidence. Fresh current-pin native owning evidence passes 13 controls and fresh full-host evidence passes 436 tests with the four existing ignored tests; the peer observations are complete JSON, retain actual HelloAck wire bytes, show zero Source bytes and zero Analyze calls, and distinguish the matching-Ack baselines from each deliberate substitution.

The current component suite passes 419 tests, documentation controls pass 16 checks, warning-denied all-target Clippy passes for the four affected crates, and repository/public-binding gates pass. The historical unchanged-owner platform 301-test and lifecycle 98-test results remain scoped reuse rather than current-run claims. Twelve compiled runtime mutants are killed by named assertions and restored. The five core, four native, and three identity mutant targets are byte-exact with R2; only the unrelated host peer audit file changed after those runs, and the applicability record correctly pairs that cutoff with fresh native and full-host validation without claiming rebuilt mutant executables.

The constructor census now records separate Unicode character and UTF-8 byte offsets. All 15 `from_recheck` occurrences reproduce at the recorded raw byte positions and classifications: one declaration, one production factory call, and 13 guarded test calls. This remains the stated D4 source pin and does not claim the general D5 structural gate.

## Inventory candidate assessment

**ACCEPT**

The proposed `repository-file-inventory.v239.json` is 809,382 bytes with SHA-256 `26ca2b0ab73dc8454f609e349ae07bcba058a790a54bb10b65fcf5f026fced5a`. Against v238, all 1,422 parent rows and all non-file fields are preserved by value; exactly 10 sorted, unique rows are added, producing 1,432 rows. `crates/components/src/session_factory.rs` remains its already planned row and is not added again.

The projection contains 161 distinct physical paths: 150 inherited meanings and 11 current direct meanings. Every reindexed pointer resolves to the stated path and byte-exact raw `before` description. All six current supersessions are folded, including the current provider-protocol dispatch chain, while the raw v239 descriptions remain unchanged. The direct contract pin resolves exactly. The R2 successor is 2,980 bytes with SHA-256 `c9ea8f5870ef6f5b519c25cb94fcac9f2c348d4fe8909318c0bba4a310f6fb6f`; its archive-qualified `codeProductMap` and `integrationCensus` references resolve to the exact frozen R2 bytes, and its publication map names the R2 archive prefix.

This assessment accepts the code unit and the proposed additive inventory mechanics. It does not bind or integrate v239, provide description contract 187, or establish product qualification.

## Acceptance boundary

No production C4/native selection or signed-descriptor producer, J2 caller, spawn/effect/settlement wiring, source39 registration, D5 general structural gate, Linux/platform completion, integration, inventory binding, status publication, or full-project qualification is accepted by this review.
