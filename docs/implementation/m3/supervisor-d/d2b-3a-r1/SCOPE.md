# D2b-3a r1: the TS2 codec's receive side (D2b plan r3 as amendments A1 and A2 amend it)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1. This unit proposes D2b plan r3 amendment A2 (`supervisor-d/d2b/PLAN-r3-A2.md`) for acceptance with it.** Accepting the unit accepts the amendment. Until then, plan r3 with A1 stands as written.

A2 splits each codec into three parts (A2-1). D2b-3a is the TS2 receive side. Each worker frame takes LD-D2B-12's steps 7 to 10 in order:
- **step 7, the envelope:** TS2-ENV-MAJOR, TS2-ENV-DIRECTION-BY-FRAME and TS2-ENV-SEQUENCE;
- **step 8, the closed schema:** the carrier-typed decode for the inherited frames (LD-D2B3-1), the product schema for the extern ones (LD-D2B3-2);
- **step 9, LD-D2B-15's contextual admission:** over every TS2 admission row section 3 gives received-frame admission;
- **step 10, the T2O table:** D2b-2's engine, fed the event this unit derives.

Only an admitted frame reaches the generated carriers (`Ts2FrameV2Payload`). Every refusal is `PROVIDER.PROTOCOL_VIOLATION`, is typed by its step, ends the session, and comes before any payload is published.

**The scope correction** (lead decision; A2-1 restates it): the spool and the retained `framePrecheck`, T016 and T020 are Rust3's, and stay with D2b-4a (LD-D2B-3 item 3; section 3's RUST3-SPOOL and RUST3-FRAME-PRECHECK rows).

**Base:** product main as the subject manifest names: `0985273`, the v222 lock on D3a-1's `72e0787`.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/provider_protocol/ts2.rs` (new) | **`Ts2Receiver`.**<br>• `new(table, DispatchContext)`; `sent(HostFrame)` records each host frame the sender wrote and steps the table; `process(ProcessEvent)` takes D3a-1's `ProcessEvent` unchanged; `receive(ReceivedFrame) -> Admitted {sequence, trace, payload}`.<br>• **`DispatchContext`:** exactly LD-D2B-15's fields, plus A2-2's descriptor fields. There is no producer yet (D4).<br>• The per-frame admission and the stage live state.<br>• **The received-byte commitments:** every commitment goes through one helper over `ReceivedBytes`, under the domain the carriers' `commitmentMap` row names for its field.<br>• The constants `TS2_FRAME_MAX_DEPTH` (7) and `RELATION_PAYLOAD_MAX_DEPTH` (1). |
| `crates/components/src/provider_protocol/ts2/carrier.rs` (new) | **The carrier interpreter** (LD-D2B3-1). It interprets the TS2 records' type grammar over the decoded tree, and fails closed on any form, keyword, array order, pattern or lexical rule it does not implement. Its extern admission goes through the embedded registry. |
| `crates/components/src/provider_protocol/ts2/build.rs` (new) | **The hand-written conversion** of the admitted tree into the generated carriers (item 10). |
| `crates/components/src/provider_protocol/ts2_tests.rs` (new) | 16 tests (below). |
| `crates/components/src/schema_sources.rs` (new) | The components crate's copy of the 52 pinned schema sources, as storage's (law X3d r6). `RegisteredSchemas::from_sources` refuses any absent, extra, reordered or replaced source. One test. |
| `crates/components/data/fact-plane.v1.json`, `relation-payload-schemas.v2.json` (new) | Hash-pinned vendored copies (lead decision 4). At load, each is checked against the carriers' own `sourcePins` (`factPlane`, `relationRegistry2`), as D2b-2's tables are. |
| `crates/components/src/provider_protocol.rs`, `crates/components/src/lib.rs` | `pub mod ts2;` and `mod schema_sources;`. |
| `crates/contracts/src/lib.rs` | `pub use serde_json::Value as GeneratedJson;` (LD-D2B3-3). |

## The admission, frame by frame (step 9)

- **HelloAck.** LD-D2B-18's exact echo:
  - the token array equals the Hello's `expectedCapabilities`: an omitted offered token or an added unoffered one refuses before OpenUniverse, and the session does not continue;
  - `identityVersions` and the two descriptor digests equal the Hello's;
  - A2-2's eleven `providerDescriptorFields` and `runtimeDescriptorFields` equal the verified descriptors' values.

  The table's `identityNegotiated` is derived from the admitted array, using the four identity tokens read from `TypeScriptCapabilitiesV2`'s `contains`.
- **UniverseAccepted:** executionId, snapshotId, planId and universeKey are OpenUniverse's (ECHO-OPEN-UNIVERSE, ECHO-SNAPSHOT2).
- **SnapshotAccepted:** exactly the Seal's values (ACCEPTED-EQUALS-SEAL, and TS2-MANIFEST-DIGEST's echo).
- **NativeContextVerified:** both ids are OpenUniverse's native context (startup `nativeContextVerified`).
- **FactBatch, V1 or V3** (by `negotiated-target-attribution-v2`):
  - **DISPATCH-STAGE-CORRELATION:** the current stage's `expectedStageId`; `batchIndex` the stage's next; the first `candidateOrdinal` the stage's next, and contiguous within the batch (the carrier's order);
  - **COMMIT-TS2-FACT-BATCH (V1):** recomputed over the received candidates;
  - **FP-CANDIDATE:** relation requested by the stage and registered; rung on the relation's ladder; the relation's layer; `producerVersion` the verified `providerBuildId`; the registry's `relationSchemaId` and `schemaVersion`; source universe OpenUniverse's `universeKey`; target in the admitted target domain;
  - **RELATION-PAYLOAD-CBOR:** decoded once under the registry's restricted profile and its own depth bound, re-encoding byte-equal, and holding no byte string;
  - **ANCHOR-WIRE-SPAN:** snapshot2, a manifest `kind: file` path, its digest, a non-empty span within its length; with ANCHOR-FACT-REF-REFUSED;
  - **OCCUPANCY-JOIN (V3).**
- **Coverage:**
  - the current stage;
  - one entry per requested key, in key order, each echoing its key (PER-KEY-SCOPE2: the key's and `examinedUniverse`'s `subjectScopeCommitment`; UNIVERSE-NATIVE-IDENTITY: the universes' 64-hex suffixes);
  - the stage-coverage commitment over the received entries.
- **Complete:**
  - one result per requested stage, in request order, its counts as observed;
  - its stage-facts and stage-coverage commitments, and the fact-stream and coverage-stream commitments, recomputed over the retained received bytes (COMMIT-MAP).
- **Unavailable**, selected by the host phase:
  - **pre-Analyze**, in WAIT_NATIVE_CONTEXT_VERIFIED: OpenUniverse's ids; a recomputed id that differs;
  - **post-Analyze:** all requested stage ids in order; stage-major coverage, each entry `unknown` with `provider-unavailable`, under the coverage-stream domain;
  - in any other phase there is no payload selection, and the table refuses the frame before any typing.
- **BudgetExhausted:**
  - `triggerStageId` is a requested stage (DLV: "one requested stageId");
  - `limit` is that stage's budget for `dimension`, and `observed` is `limit + 1` (checked);
  - stage-major coverage with `budget-exhausted`, under the coverage-stream domain.
- **Cancelled:** the Cancel's echo (CANCELLED-ECHO). The observed phase is `snapshot` when the Cancel was sent in WAIT_NATIVE_CONTEXT_VERIFIED or READY_ANALYZE (TS2-OBSERVED-PHASE, read from T2O's `cancellationObservedPhase`). For every other interval only the enum applies, because the law does not restate the inherited meanings.

## Lead decisions

- **LD-D2B3-1. The carrier-typed decode is the closed check for the inherited frames** (lead decision 3).
  - **Why:** SnapshotAccepted, FactBatch, Complete and Cancelled have no product-registered schema. Their closed schemas are DLV's `payloadSchemas` and `definitions`, and the carriers' `records` are those schemas as data, each naming its DLV selector.
  - **The interpreter** checks a record's exact member set, each member's type, constants, enums, NFC, scalar and byte bounds, the five hex patterns, the `logical-path-segments` lexical rule and the array orders. Loading refuses any form, keyword, order, pattern or lexical rule outside that list.
  - **The lane check** (`check_d2b3a_dlv_records.py`) compares each TS2 record with its DLV source, for all 20 records: DLV's required and optional members equal the record's members, and DLV's schema is closed; a variant record's member order is DLV's required list; every count bound DLV names by a limit is the record's `maxItems`, and every "uint64 exactly N" is the record's constant.
  - The envelope's `protocolMajor` is 2 by the handshake law (`frameAndMajor`), not DLV's 1; DLV states it with a semicolon form the check does not compare.
- **LD-D2B3-2. Three extern payloads are admitted piecewise** (a lead decision, flagged for review).
  - **Why:** the identity crate's JSON reader has a 4 MiB and depth-32 bound (`canonical.rs` `MAX_BYTES`, `MAX_DEPTH`). A lawful TS2 payload may exceed the byte bound: up to 4,096 CoverageResultV3 entries per Coverage frame, and every stage's keys in a terminal's coverage.
  - **The payloads:** Coverage, post-Analyze Unavailable and BudgetExhausted.
  - **The method:** the wrapper is admitted with its array reduced to its first item, so every other member, and the item type once, are checked by the schema itself. Every item is admitted by the item schema. The array's own count bounds are checked as declared.
  - **The precondition, asserted at load:** each such member schema is exactly a plain array of one item `$ref` with count bounds, so this is equivalent to admitting the whole document.
  - The other extern payloads (HelloAck, UniverseAccepted, NativeContextVerified, pre-Analyze Unavailable) are small, and are admitted whole.
- **LD-D2B3-3. `GeneratedJson`** (lead decision 3).
  - **Why:** three generated carriers (HelloAck, NativeContextVerified, pre-Analyze Unavailable) type schema constants as `serde_json::Value`.
  - **The change:** contracts re-exports that type as `GeneratedJson`, and the conversion builds those members by hand. Contracts' public API gains this one re-export.
  - **What it is not:** no package edge, and no serde decoding of wire bytes.
  - **The inventory:** contracts' `lib.rs` row ("Expose inert versioned contract modules …") stays true.
- **LD-D2B3-4. The relation registry's sources.**
  - Relations, ladders, `schemaId` and `schemaVersion` are read from `relation-payload-schemas.v2.json`'s `x-opensip-relation-registry`, "the SINGLE authority for every relation's resolution ladder". Layers are read from `fact-plane.v1.json`'s `relationRegistry`, the layer authority DLV's FactCandidateV1 names.
  - **An observation:** `unresolved-edge`, which the v2 registry adds, has no fact-plane layer, so a TS2 candidate with that relation refuses. No TS2 stage requests it today. A layer for it is a cross-law item for the fact-plane owner.
- **LD-D2B3-5. The vendored files are read exactly.**
  - Both are pinned to the carriers' `sourcePins` at load.
  - `fact-plane.v1.json` holds floating-point numbers, which the canonical reader refuses, so only its top-level `relationRegistry` member is parsed. It is read over its exact bytes within the pinned file, by a scan that tracks string and nesting state.
- **LD-D2B3-6. The depth bounds** (LD-D2B-2). Both are recomputed by a test from the documents themselves:
  - **`TS2_FRAME_MAX_DEPTH` = 7:** the deepest container nesting of any TS2 frame, envelope included, over the carriers' TS2 records and every product schema they reach (`$ref` followed across the embedded documents; deepest branch of `oneOf`, `anyOf`, `allOf`, `if`, `then`, `else` and `not`; containers count, scalars do not, as D2b-1's reader counts them);
  - **`RELATION_PAYLOAD_MAX_DEPTH` = 1:** over every `relation-payload-schemas.v2.json` definition.

  A deepest-valid frame reads, and one level more refuses. D2b-3c recomputes the frame bound with FA-2's payloads.
- **LD-D2B3-7. The context's shape** (lead decision 5).
  - `DispatchContext` holds exactly LD-D2B-15's values: the tokens, the OpenUniverse values, each stage's `DispatchBindingV1` (stage id, Analyze-relative ordinal, relations, budget, keys with their scope2 commitments), the target domain, and the sent manifest's file entries and Seal. It adds A2-2's descriptor fields.
  - The plan-stage bytes, `dependencySourceSetId` and the planned send schedule are send-side or Rust3 values. D2b-3b and D2b-4 add them with the code that reads them.
  - The live state is the sequence, the stages' counters, the retained frames of the commitment preimages, and the Cancel sent.
- **LD-D2B3-8. The schema evaluator's budget** is B1's configuration admission bound, `SCHEMA_BUDGET` (64 MiB of evaluator work, `crates/host/src/configuration.rs`), as C1a3's sealing reuses it. It applies per admitted document. No new bound is introduced.
- **LD-D2B3-9. The relation payload's profile** is the registry's own (`fact-plane.v1.json` `canonicalPayloadEncoding`: no negative integers, no byte strings). It is read with D2b-1's `rust3-cbor` reader, which refuses negatives, and a byte-string scan.
- **LD-D2B3-10. The supervisor's `Participant`** (D3a-1) needs the sender's pending writes, so its TS2 implementation lands with D2b-3b (A2-1). D2b-3a exposes the receiver it will drive.
- **The TS2 aggregate response bound** stays gap 6 (LD-D2B-8): no bound is set, and the cross-law item stands (lead decision 6).

## The tests

**`provider_protocol::ts2` (16):**
- **a lawful session**, Hello to DONE: every row's trace, and each payload reaching its carrier;
- **the envelope:** major 1, a host frame read from the worker, a skipped and a duplicate sequence, and no frame after a refusal;
- **the HelloAck echo:**
  - an omitted and an added optional token, and each of the two digests and the eight non-constant descriptor fields changed: each an admission refusal, before OpenUniverse;
  - a changed `protocolMajor`, a changed `identityVersions` constant and a missing member: schema refusals;
  - the `identityNegotiated` guard;
- **the startup echoes:** each UniverseAccepted, SnapshotAccepted and NativeContextVerified member changed;
- **the FactBatch stage correlation and counters:** another stage, an unrequested stage, a skipped, duplicate or decreasing `batchIndex`, a wrong or repeated first `candidateOrdinal`. Each refuses before the table, on a frame that passes its closed schema;
- **step 8's bounds:** 0 and 4,097 facts, a negative integer, an unknown member;
- **the candidate law:** each FP-CANDIDATE, RELATION-PAYLOAD-CBOR and anchor rule broken, and the anchors' order;
- **the commitments:** a swapped domain, a reordered preimage, a coverage commitment under the fact class's domain, Complete's two stream commitments under the stage domains, and a stage result's count;
- **provenance:** every commitment's every preimage part lies inside a retained received payload, and the number of commitments is the session's nine. A re-encoding, which only `built_commitment` could compute, would not be logged;
- **the coverage echoes:** each key member, the examined scope, another stage;
- **the terminals:**
  - pre-Analyze Unavailable admitted, with an equal recomputed id refused, and refused by the table outside its phase;
  - post-Analyze Unavailable admitted, with refusals for the stage domain, another deficiency, one stage only, the affected stages, and one invalid piecewise item;
  - BudgetExhausted admitted, with refusals for an unrequested stage, another limit and a wrong `observed`;
- **Cancelled:** `snapshot` in WAIT_NATIVE_CONTEXT_VERIFIED; another phase and another execution refused;
- **FactBatchV3:** OCCUPANCY-JOIN's three refusals;
- **construction:** the FA-2 token (D2b-3c's), descriptor fields other than A2's, and the Rust3 table;
- **the interpreter** fails closed on an unknown pattern, order, form and keyword;
- **the depth bounds**, recomputed.

**`schema_sources` (1):** the embedded sources are the registry's pinned set, in order.

## Checks

Lane r1, attempt 3, `evidence/d2b3a-checks-r1/` (the lane of record), on product `01769e9`. allPassed.

**Void history** (kept, not acceptance evidence):
- **Attempt 1** (`evidence/d2b3a-checks-r1-void-attempt1/`) failed warning-denied Clippy only:
  - `unnecessary_fallible_conversions` on `build.rs`'s `ExactInteger::try_from(u64)`, now allowed with its reason (the infallible `From` would add a `from` call to the mint census);
  - `type_complexity` on the test-only provenance log, now the `Provenance` alias;
  - `explicit_counter_loop` in a test, now a `zip`.

  Every other control passed in attempt 1.
- **Attempt 2** (`evidence/d2b3a-checks-r1-void-attempt2/`) passed every control on `813d559`, unchanged code. It was superseded before packaging, when main moved to `e770404` (C2a-1, security paths only) and then `01769e9` (the v223 lock).

The checks:
- **The suites,** at base and candidate, with equal failure sets and no differing test:

  | Suite | Failed | Passed (base → candidate) |
  | --- | --- | --- |
  | components | 40 | 53 → 70 (the 17 new tests) |
  | identity | 0 | 72 → 72 |
  | contracts | 0 | 0 → 0 |

  The 40 components failures are D3a-1's `supervisor::tests`, identical on both sides. They need `supervisor_fixture.path`, which only D3a-1's lane writes (LD-D3A-9: "this test runs only there"). They are not a D2b-3a change.
- **Lints:** rustfmt on the new and base-clean edited files (none base-dirty), and warning-denied all-targets Clippy on contracts and components.
- **The focused receiver tests:** pass.
- **The duty table** (`check_d2b3a_duty_table.py`): 30 rows, each of the carriers' 55 admission ids listed once, and all 22 rows that give D2b-3 received-frame admission named in the receiver.
- **The carriers against DLV** (`check_d2b3a_dlv_records.py`): 20 records, no problem, with DLV pinned.
- **Repository checks:** the environment exceptions, the operability source census (114 rows, no findings), the census-closure check (no closure file changed) and verify_design (52 admission sources).
- **Eight mutations,** each caught by its named test:

  | Mutation | Caught by |
  | --- | --- |
  | echo-member-ignored | `the_startup_echoes_are_exact` |
  | commitment-reencoded | `every_commitment_preimage_is_a_received_slice` |
  | stage-correlation-unchecked | `fact_batch_stage_correlation_and_counters` |
  | batch-counter-unchecked | `fact_batch_stage_correlation_and_counters` |
  | token-echo-unchecked | `the_hello_ack_echo_is_exact` |
  | runtime-descriptor-unchecked | `the_hello_ack_echo_is_exact` |
  | piecewise-items-unchecked | `the_terminals` |
  | empty-anchor-span-admitted | `the_candidate_law` |

## Not delivered

- **D2b-3b:** the payload builders, the schedule constructor, the sender, the Hello's token array and limits, and the TS2 `Participant`.
- **D2b-3c:** FA-2 for TS2 (the census request and payloads, the depth bound recomputed), trial 07's TS2 replay and FA-2's vectors, and D2b-T4 and D2b-T5.
- **D2b-4a to D2b-4c:** the Rust3 codec, with the spool and the retained `framePrecheck`, T016 and T020.
- **H's fact admission** and the census settlement; **C4's** Plan-side decisions; **D4's** context producer.

## Not claimed

- No caller, no supervision of a provider, no fact admission.
- No qualification; D2b's completion is not claimed.

## Inventory

Seven new product paths (the four receiver files, `schema_sources.rs` and the two vendored data files): an inventory successor follows acceptance. The changed paths' rows stay true: `provider_protocol.rs`'s planned role ("Dispatch the selected provider wire protocol and validate its transaction boundaries."), components' `lib.rs`, and contracts' `lib.rs`.
