# D2B-1-r2 review

**Verdict: ACCEPT-UNIT.** Both round-1 required findings are resolved. No new required findings or nonblocking observations.

## Exact subject

Verified the 9,866-byte subject manifest SHA-256 `931d73e381636170d7e929060986798bd896735907b400d89d2a6e966f92234f` and rehashed all 43 members successfully. All eight product-map candidate files and archived copies match their recorded sizes and SHA-256; the three existing parent files match the named base. Authority, prior-round and candidate design-lock pins in source.json also match.

The candidate remains detached at `a68be52fdb6290ead2beff4adaccefd92c81624c`, with exactly the mapped changes. Compared every file with the archived round-1 candidate: only provider_protocol.rs and provider_protocol_tests.rs differ. The CBOR reader/encoder, reference corpus, CBOR tests, NFC exports and dependency/module edits are byte-identical to round 1. The base move incorporates C1a3 on disjoint paths.

## D2B1-R1-RF-1: completed frames before a refusal

Resolved. push accumulates completed ReceivedFrames in Pushed.frames, appending in wire order. On a later step error it sets the sticky refusal state, records Pushed.refusal and breaks without discarding the frames. Subsequent pushes return no frame and AfterRefusal, including when the next slice is empty. Each successful step consumes exactly one complete frame; incomplete state remains held for the next push. No completed frame is lost on a later digest, CBOR, frame-bound or aggregate-bound error.

The new a_frame_completed_before_a_refusal_is_kept_at_every_split control compares the ordered payloads and exact first refusal with repeated read_frame calls. It uses the original 41-byte valid empty-array frame, followed separately by an oversized length, wrong digest and correctly digested noncanonical payload, at every two-way split and byte by byte. The helper also checks that later pushes after the refusal return no frame and AfterRefusal. Together with the existing two-valid-frame controls and direct inspection of the shared decode path, this covers the reported split-dependent defect. The frames-dropped-on-refusal mutant compiles and fails this control.

SCOPE explicitly records the changed interface for D3a: its participant consumes Pushed rather than the round-1 Result signature, with D3a-1 recording the concrete integration. Consumers must process the returned frames in order before the trailing framing refusal, applying the codec's own earlier admission/transition refusals as appropriate. This unit supplies wire mechanics, not contextual admission or a D3 caller.

## D2B1-R1-RF-2: length before digest acquisition

Resolved. The first take_prefix call caps copying at eight bytes. Once those bytes are complete, both MAX_FRAME_PAYLOAD_BYTES and the remaining aggregate are checked before the second take_prefix can copy toward byte 40. Payload capacity is allocated only after the full permitted prefix. An oversized length returns before either later action. A split that ends before byte eight preserves only its partial length; resumption crosses the check exactly once.

The new no_digest_byte_is_copied_before_the_length_is_judged control observes internal acquisition state, rather than only the final error. It covers a complete oversized prefix in one push, seven length bytes followed by the remaining 33 prefix bytes, and a within-frame-bound length exceeding the aggregate. Each case asserts Oversize, no returned frame, have equal to eight, untouched digest slots and no payload allocation. The changed length-phase mutant copies toward 40 and is caught by this control as well as other framing tests. Existing tests retain the seven-plus-one refusal, successful aggregate decrement, digest/decode errors and sticky refusal checks.

## Lane and independent checks

The recorded r2 lane is consistent with its runner and logs:

- Components: **16 base / 35 candidate passing tests**, equal empty failure sets, 19 new passing tests. Identity: **72 / 72**, equal empty failure sets, none new.
- All **19 focused provider-protocol tests** pass.
- Warning-denied all-targets Clippy passes for components and identity. Rustfmt passes for the new/base-clean edited files. Identity lib.rs remains the disclosed base-dirty exclusion; its candidate change is the unchanged appended NFC predicate/version export.
- The 7,550-case differential regenerates byte for byte. Package-edge evidence shows components' internal edges exactly contracts and identity, both normal.
- Environment exceptions (10 tests), operability, census-closure-unchanged and verify_design pass in the logs.
- All **eleven mutations** compile and produce actual test failures. The two r2 controls catch copying digest bytes during the length phase and discarding completed frames; the other mutants retain canonicality, depth, framing/digest and received-byte provenance coverage. The runner restores exact bytes after each mutation, consistent with the rehashed product map.

After checking the generator's nonwriting --check path and confirming it is unchanged from round 1, independently ran only the permitted checks:

1. build_cbor_differential.py against the candidate corpus with python3 -I -B and --check: **cbor differential corpus current**.
2. python3 -I -B tools/check_operability.py source --repository . in the candidate: **passed, 114 rows, no findings**.

Rust suites, Clippy, formatting, package edges and verify_design were inspected as recorded lane evidence, not rerun.

## Regression and scope

No regression identified in round-1 conclusions: closed strict profile decoding and refusal ordering, no claimed-container-length allocation, iterative depth handling, preorder received ranges, blocking frame acquisition order, deterministic writer, sequence checking, NFC table/version pinning, received-only commitment provenance, domain-separated host commitments and bare manifest digest remain unchanged. The accumulator's remaining accounting, partial payload retention, boundary/truncation distinction and digest-before-decode order remain intact.

The eight mapped paths intersect none of the 19 census-closure files. The source adds no mint-census call, environment read or let-underscore discard. No extra package edge or external dependency is introduced by this round.

provider_protocol.rs realizes only shared mechanics of its existing planned row. The four additional inventory paths remain cbor.rs, cbor_tests.rs, provider_protocol_tests.rs and cbor-differential.v1.json. No table engine, codec, contextual admission, supervision, production caller, selected depth value, completed D2b or qualification is accepted by this unit verdict.

## Boundaries

Only REVIEW.md and review.json in the requested directory were written. Neither repository, candidate worktree nor control files were edited. No Cargo, rustc, build, lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing keys, held trees, T2 store or T2 cache was read.
