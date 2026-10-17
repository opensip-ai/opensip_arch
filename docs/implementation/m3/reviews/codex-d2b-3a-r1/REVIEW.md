# D2B-3a-r1 review

**Verdict: ACCEPT-UNIT. Amendment A2: ACCEPT. Product qualification: false.**

No required findings. Two non-blocking observations appear below. Acceptance covers the pinned TS2 receive-side unit and the proposed plan amendment; it does not establish completion of the sender, FA-2 admission, Rust3 codec, supervisor integration or product qualification.

## Subject and boundaries

Independently rehashed the 26,486-byte subject manifest (`a53b885883c9db386e877a5e0d8a767e85527e59126cfd43294a327127e32ab2`) and all 111 members, including a final rehash before writing this review. Checked the detached candidate at product base `01769e93db878836612d9e3d483a054f7ad1da94`, architecture base `8fde46bb981e1304a79aa997ed154cdc4435632a`, all ten product-map paths and their archived/candidate bytes, the three edited parents, seven new paths, source authority pins and product lock. The lock selects inventory v223 and 176 contract successors. Both vendored registry files equal their architecture sources byte for byte.

Read A2 first, then SCOPE, implementation, tests and evidence. Ran only the three expressly permitted read-only checks in the candidate: operability source census, duty-table check and DLV-record comparison. All passed. No Cargo, rustc, builds, generators, lanes, network, delegation or prohibited fixture/installation/store reads were performed. Neither repository nor the candidate was edited.

## Amendment A2

A2's replacements preserve the accepted plan and A1's dependencies while dividing each codec into receive, sender/Participant, and FA-2/admission/replay units. Rust3 receive-side spool and pre-match guards remain assigned to D2b-4a. Moving Participant to the sender unit is coherent because it needs pending writes. The amendment leaves the law and carriers unchanged.

The added context fields come from handshake-v1's `typescriptDescriptorBinding` rule and TypeScriptHelloAckV2 description: seven provider descriptor fields and four runtime descriptor fields. This closes the context requirement needed to compare verified descriptor contents as well as digests. A2 allocates the original eight mutations across explicit successor units without removing their obligations. Receive-side echo, commitment provenance, stage and batch controls are present here; spool, sender, census and reference-count controls retain their stated owners.

## Admission and state

The receive path checks envelope membership, major, worker direction and sequence; selected closed payload typing; contextual admission; then the unchanged T2O engine. Conversion and publication follow successful table admission. A refusal latches the session closed. An Unavailable frame with no payload selector for the current phase reaches a table refusal without payload publication; T2O's no-match law prevents an admission bypass.

The carrier interpreter checks closed records, variants, scalar and byte bounds, constants, enumerations, NFC, supported patterns, logical path grammar and declared array orders. Its load rejects unsupported type forms, keywords, patterns, lexical rules and orders. The DLV check verifies 20 records' declared structural correspondences and pins; it is not a substitute for semantic code review. Likewise, the duty-table check establishes all 55 admission IDs are listed once and 22 TS2 receive IDs are named in code, rather than proving those checks by name alone. Reviewed their implementations against their sources.

Piecewise admission is equivalent for the three pinned startup payloads: their closed wrappers have no cross-item composition constraints, the selected arrays are plain item references with the present count bounds, and the reduced wrapper checks all other properties. Every original item is independently admitted and original array length is checked. Current minimum bounds permit the first-item reduction. This conclusion is specific to the pinned schemas; future compositions or changed minima require renewed review.

HelloAck compares the complete capability array, identity versions, both descriptor digests and all eleven verified descriptor fields before deriving the table observation. UniverseAccepted, SnapshotAccepted and NativeContextVerified bind the proper OpenUniverse/Seal values. FactBatch checks current-stage identity, batch and candidate counters; analysisOrdinal is fixed to zero by its carrier schema. Candidate checks bind requested relation, registry ladder/schema/version, fact-plane layer, verified producer build, source universe and admitted target domain. Anchor checks bind snapshot, manifest path and digest and enforce a non-empty in-file byte span; fact-reference anchors refuse. V3 occupancy companions join batch candidate ordinals and targets.

Coverage checks current stage, exact requested key count/order, scope echoes and universe suffixes. Complete compares stage order, Analyze-relative ordinals, observed counts and commitments. Pre-Analyze Unavailable checks the OpenUniverse identity and unequal native-context recomputation. Post-Analyze Unavailable and BudgetExhausted require all requested keys in stage-major order, proper unknown/deficiency values and coverage commitments. Budget values join the named requested stage and require checked limit-plus-one. Cancelled binds the sent Cancel and T2O's observed-phase rule.

## Commitments and remaining lead decisions

Batch, stage, stream and terminal commitments select their domains from commitmentMap and consume received node slices, with the necessary array framing supplied by the integrated commitment helper. Retained frame/node references preserve provenance. The test-only address-range log checks every recorded preimage lies within received frames and checks the expected calls; the re-encoding mutation fails that control despite equal canonical semantic bytes. This provides meaningful evidence beyond output-hash equality.

The GeneratedJson re-export exposes an existing contracts dependency without adding a package edge or using serde to decode received wire bytes. Components embeds the same 52 source files in the same order as storage; registry admission checks their full-document pins. The fact-plane member scanner operates within a fully pinned document and parses only the exact top-level relationRegistry bytes, avoiding unrelated float values without rewriting the source. Relation payload decoding uses the registry's restricted canonical profile and rejects embedded byte strings.

The schema traversal follows embedded references and compositions and recomputes frame depth 7 and relation payload depth 1; the positive boundary witness limitation is recorded below. Context separates immutable admitted inputs from live counters and retained preimages; its future D4 producer and sender-only additions remain explicitly owned. The 64 MiB schema evaluation budget reuses the existing policy per admitted document. Participant remains owned by D2b-3b. The missing fact-plane layer for unresolved-edge is disclosed and fails closed; this unit supplies no invented layer. No present TS2 stage requests it. FA-2 contexts are refused until D2b-3c.

## Evidence and regression assessment

Reviewed the recorded lane runner and raw logs, rather than rerunning its prohibited operations. Components records 53 base versus 70 candidate passes with the same 40 failures; independently matched the named raw failure sets. Identity remains 72/0 and contracts 0/0. The 17 focused tests pass. These comparison results do not make the full component suite green.

All eight mutation logs show behavioral test failures, without compilation failure: echo member, re-encoded commitment, stage correlation, batch counter, token echo, runtime descriptor, piecewise item checks and empty anchor span. Recorded warning-denied all-target Clippy passes; all eight changed Rust files are rustfmt-clean. The ten environment-exception tests pass. Recorded verify_design passes with productQualification false and inventory v223. Independently confirmed the 19-file discovery census closure does not intersect the ten candidate paths. The permitted live source census passes 114 rows; the duty-table and DLV checks pass independently as described above. Recorded private TMPDIR mode, lane ownership and niceness are consistent with the runner; they were not recreated during this review.

No blocking regression or unowned D2b-3a receive obligation was found. Sender scheduling, Participant, successor admission/replays, Rust3 work and the disclosed aggregate-response-bound cross-law item retain their explicit later ownership.

## Non-blocking observations

**D2B3A-R1-NBO-1 — stale base in SCOPE (P3).** SCOPE.md:15 names product `0985273` and inventory v222. The request, manifest, source metadata, product map and lane consistently bind `01769e9` and v223. Correct the overview in a later documentation subject; the reviewed bytes are unambiguous.

**D2B3A-R1-NBO-2 — depth witness wording and coverage (P3).** ts2_tests.rs:1703 correctly derives the depth bounds and exercises the reader at seven/eight containers. Its accepted witness is nested arrays around null, rather than a valid TS2 frame as the comment and SCOPE describe. Add a schema-valid maximum-depth frame witness when strengthening this control. The computed bound and lawful-session tests remain useful independent evidence.
