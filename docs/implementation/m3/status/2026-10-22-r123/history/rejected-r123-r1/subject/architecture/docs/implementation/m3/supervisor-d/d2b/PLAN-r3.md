# D2b implementation plan r3: the provider codecs, `crates/components/src/provider_protocol.rs` (M3-D items 10 and 11)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.** Round 3 answers Codex `codex-d2b-plan-r2` (REQUIRED-FINDINGS: two RFs, two NBOs). Round 2 answered `codex-d2b-plan-r1`.

## r3 changes

| Finding | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (an omitted echo faults; it cannot negotiate a token off) | **New LD-D2B-18, exact echo for every token.** NE §9.1's exact token-array equality holds for every optional token, in both protocols: `symbol-census-v1`, `subject-scope-reference-v1` and `target-attribution-v2` included. A HelloAck that omits an offered token, or adds one not offered, is `PROVIDER.PROTOCOL_VIOLATION` before OpenUniverse and before any source byte, and the session does not continue. The historical token-absent branch exists only when both exact arrays omit the token. LD-D2B-16, LD-D2B-17 and §4's FA-2 and RUST3-LIM controls are corrected: "negotiated off" is withdrawn, and the controls test omission and unoffered addition for each optional token, each refusing before disclosure. | §2 LD-D2B-16, -17, -18; §4 |
| **R2-RF-2** (one refusal point per control) | §4's RF-2 controls are partitioned by owner and refusal point. **Schema admission (step 8):** shape and count bounds, such as a FactBatch of 0 or 4,097 facts or candidates. **The builder or sender, before writing:** the host's request projection, the Plan-stage bytes and the request's `stageOrdinal`. **Contextual admission (step 9):** well-shaped worker frames that miscorrelate: another stage, another Analyze ordinal, a duplicate, skipped or decreasing `batchIndex` or first `candidateOrdinal`, and a T020 BudgetExhausted naming another stage or a wrong `observed`. Every refusal still precedes publication. No earlier check is bypassed, and no host check moves into worker admission. | §4 |
| **R2-NBO-1** (F-1 is a frame-size gap) | LD-D2B-17: RUST3-LIM's F-1 is an oversized inline Analyze, which can occur at or below 256 subjects (repeated rows, stages and path lengths). It is closed on the inline path by LD-D2B-9's full-envelope sizing and the schedule's pre-spawn refusal, not by the subject cap. §4 adds an at-or-below-256 oversized-inline control, distinct from the 257-subject cap case. | §2 LD-D2B-17; §4 |
| **R2-NBO-2** (the pattern consumers) | §3's OWNER-PATTERN-EVALUATION row names D2b's every consumer: the startup carriers, the occupancy-companion schema, and the transitive external wire schemas its schema checks reach, as well as H's relation-payload schema and the Plan side's evidence schema. | §3 |

## r2 changes (round 2, answering `codex-d2b-plan-r1`)

**Bases:**
- product main `56d0eb5` (inventory v214; 173 contract successors);
- architecture as the subject manifest names.

## r2 changes

| Finding | Change | Where |
| --- | --- | --- |
| **RF-1** (spool entry versus commitment preimages) | LD-D2B-3 is rewritten. **Commitments** use the received encodings of their preimage values (candidates, coverage entries, batch facts), bound field by field to the carriers' `commitmentMap`, including the terminal coverage arrays. **The spool entry** is a separate record: the closed map `{analysisOrdinal, stageId, candidate}`, built from the validated value and charged at its full deterministic-CBOR length before it is allocated or appended. The only byte-equality assertion compares a candidate's re-encoding with its own received slice. New controls separate the wrapper bytes, fact and coverage preimages, and terminal commitments. | §2 LD-D2B-3; §4 |
| **RF-2** (stateful admission before matching) | New **LD-D2B-15**: the per-frame contextual admission. It is supplied an immutable dispatch and request context, keeps live per-direction and per-stage counters, and runs the retained prechecks and payload guards (rust2 `framePrecheck`, T016, T020) before the table is matched. New **§3**: every one of the carriers' 55 admission rows is assigned to a sub-unit or to its owner outside D2b. New integration controls cover the exempt duties (stage and Analyze correlation, batch and candidate ordinals, Plan-stage bytes). Trial 07's replay is not claimed as proof of them. | §2 LD-D2B-12, LD-D2B-15; §3; §4 |
| **RF-3** (successor wire duties) | New **LD-D2B-16** (FA-2, X-FA2-D) and **LD-D2B-17** (RUST3-LIM, X-RL-D) allocate the successor behaviour to D2b-3 and D2b-4 and to the C4 and H interfaces. They cover the token combinations, both mismatch directions, the old no-token payloads, the complete and over-bound census, the D∅ and returned-census commitments with H's settlement boundary, and the reference-scope reconstruction. The successors' own vectors are pinned and replayed beside trial 07's. | §2; §4 |
| **NBO-1** (depth over the whole closure) | LD-D2B-2: the bound is computed over the complete successor-aware wire closure, after D2b-0. D2b-1's reader takes the bound as a parameter, so it changes nothing there. The embedded relation-payload reader has its own bound. Container depth is distinct from byte-string contents. There is a deepest-valid case and a one-over refusal. | §2 LD-D2B-2 |
| **NBO-2** (TS2 Cancel capability versus sender permission) | LD-D2B-7: the tables' and payloads' capabilities are kept distinct from the sender's. Under HOST-SEND-SCHEDULE (`appliesTo: both`), the host sends Cancel only after the Hello slot, as the exact echo, with reason `user-interrupt`, for both protocols. D2b reads TS2's `host-shutdown` and START Cancel rows, but never sends them. | §2 LD-D2B-7 |
| **NBO-3** (observable provenance) | LD-D2B-3: preimages are borrowed received slices, which only the reader makes (`ReceivedBytes`). The control checks that each preimage slice lies inside the received payload's allocation, which a re-encoding cannot. The black-box mutants for a wrong wrapper, order, domain or value class are kept. | §2 LD-D2B-3; §4 |
| Q2 (Unicode version) | The reference's Unicode database version (16.0.0, recorded in the differential corpus) and the NFC tables' (`opensip_identity::NFC_UNICODE_VERSION`, from `unicode-normalization`'s `UNICODE_VERSION`) are both pinned by the test, in addition to the vector agreement. | §2 LD-D2B-11 |

Unchanged from r1, and judged sound by the review: the split and its order (LD-D2B-1, Q1), the vendored tables (LD-D2B-4), LD-D2B-5, LD-D2B-6, LD-D2B-8, LD-D2B-10, LD-D2B-13 and LD-D2B-14's historical scope.

**What precedes it.** D2b's row in M3-D r5's units table is "`components/provider_protocol.rs`: items 10-11, the CBOR reader, P3T and T2O as data, the handshake checks", depending on P0 (met), size L. Its order is D1a → D2a ∥ D2b → D3a.
- D2a's plan is accepted, and its codec is built for review.
- D2b does not depend on D2a. They are separate codecs, with no shared frame type (item 11, rule 1).

**Authority:**
- **The law:** M3-D r5 items 10 and 11, with D2b-T1 to T5 and D5-C1's no-translation classes.
- **NE §9** (`docs/v2/contracts/product-v1/native-evidence.md`:2781-3316), as amended by FA-2's §9.8 and RUST3-LIM's §9.3a.
- **DLV** (`docs/coop/artifacts/delivery.v2.json`) and **RPP** (`docs/coop/artifacts/rust-provider-protocol.v2.json`).
- **P3T** (`docs/coop/design-corrections/native/protocol3-transitions.v1.json`), with its guard overlay `docs/implementation/m1/source-selection-v2/owners/native/p3-guard-successor.v1.json`, and **T2O** (`…/native/typescript-protocol2-order.v1.json`).
- **The product schemas:** `schemas/sources/handshake-v1.schema.json` (RCA-1's Rust3 identity), `startup-v1.schema.json` and `fact-batch-v3.schema.json`.
- **The wire carriers:** `schemas/wire/native-carriers-v1.json`, its `admission` rows and `commitmentMap`, with their generated types in `crates/contracts/src/generated/protocol.rs`.
- **The bound successors FA-2 and RUST3-LIM** (`docs/implementation/m3/native-successors-fa/`): their sections (`fa-2/section-9-8.md`, `rust3-lim/section-9-3a.md`), schemas, materialization maps and vectors, and their cross-law items X-FA2-D and X-RL-D.

## 0. What D2b delivers, and what it does not

**Delivers** `crates/components/src/provider_protocol.rs` and its data, library only, with no caller until D3a and D4:
- **the shared wire mechanics:** the 40-byte prefix (`uint64` BE length, 32 raw SHA-256 bytes), the length checked against 67,108,864 before any allocation, exact reads, digest verification, checked arithmetic, and per-direction sequences from 0;
- **a first-party strict deterministic-CBOR reader and encoder** for the two closed profiles, `ts2-cbor` (negative `int64` allowed) and `rust3-cbor` (no negative integers). Canonicality is proved by re-encoding and byte comparison. Text, map keys included, must be NFC. The reader records each node's received byte range;
- **two codecs, one per protocol,** with no common semantic type:
  - TS2 (`typescript-semantic`, major 2) and Rust3 (`rust-semantic`, major 3), selected at session construction from the admitted selection;
  - each payload decoded by hand-written, schema-checked code into the generated carriers (serde never reads wire bytes);
  - each payload checked against its closed product schema, under the negotiated tokens;
  - each worker frame admitted against the session's context before the table is matched (LD-D2B-15);
- **the transition tables as data:** P3T's 34 rows with the guard overlay, and T2O's 23 rows, vendored hash-pinned copies interpreted by one table engine with the pre-match law, first match on phase, frame and guard, the stage-dependent next, and the total fallback;
- **the handshake checks:**
  - exact identity echoes, the identity tokens and `identityNegotiated`;
  - the limits handshakes, TS2's ten-member map and Rust3's 32-member map, with deterministic-CBOR byte equality;
  - reject before disclosure;
- **the host's send side:** the canonical host send schedule's constructor (REQUEST-WIRE-ACCOUNTING), which C4 calls at Plan time, and the sender that consumes it (HOST-SEND-SCHEDULE), with the host payload builders;
- **the commitments,** `C(d, v) = "sha256:" + hex(SHA-256(UTF8(d) ‖ 0x00 ‖ dCBOR(v)))` and the manifest digests, recomputed from the received bytes;
- **the typed events** D2b emits to the host's consumers. It admits no fact and mints no Coverage (item 10).

**Not delivered:**
- the supervisor and its process events (D3a; D2b defines the event input it consumes);
- the session factory and manifest admission (D4);
- fact admission and the census's settlement (H);
- the Plan side: the Plan, the set admissions, the per-key scope2 descriptors and the refusal before spawn (C4 and the set owners). D2b gives C4 the schedule constructor;
- any Linux-specific code (none is needed).

## 1. The split (LD-D2B-1): five sub-units, each its own review and lane

Unchanged from r1:

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D2b-1** | The CBOR reader and encoder (both profiles), the framing, the digest, sequences, the commitment and manifest-digest functions, and `ReceivedBytes` | D2b-T2, D2b-T3; the reference decoder's probes and differential | — |
| **D2b-2** | The table engine over the vendored P3T, its overlay and T2O, with its pre-match hook | D2b-T1 | — |
| **D2b-0** | The successor schema materialization, FA-2's and RUST3-LIM's schemas, rebased on RCA-1's product handshake; then **a reviewed blind refresh** | the materialization's own checks; the refreshed receipt | — |
| **D2b-3** | The TS2 codec: contextual admission, payload builders, schedule and sender, FA-2 | D2b-T4, D2b-T5 (TS2); §4's TS2 controls | D2b-1, D2b-2, D2b-0 |
| **D2b-4** | The Rust3 codec: contextual admission, payload builders, schedule and sender, FA-2 and RUST3-LIM | D2b-T4, D2b-T5 (Rust3); §4's Rust3 controls | D2b-1, D2b-2, D2b-0 |

**Order:** D2b-1, then D2b-2, then D2b-0 with its blind refresh, then D2b-3 and D2b-4.
- **D2b-0 comes after the two mechanics units.** Its regenerated carriers change `tools/contracts/generator-closure.json`, a file the discovery census binds as reference-loading code. That makes the B2-b4c blind held-out receipt stale, and the census `--check` then fails on main.
- **So D2b-0 is followed at once by the reviewed blind refresh,** before any other lane needs the census: a pre-run Codex review of the blind mode, the lead's mechanical blind run (the owner's standing answer), and a post-run review. This is B2-b4c3's sequence.

## 2. Lead decisions

- **LD-D2B-2. The CBOR depth bound.** No source sets one, and the Python reference has none.
  - **The bound:** the deepest container path any closed payload admits, plus the envelope's levels. It is computed over the **complete successor-aware wire closure**: every carrier record and preimage-only record reachable from a frame, the transitive external schema references, every negotiated variant (the four FA-2 payload versions, `StageRequestV3`, the target-attribution variant), and the two successor schemas.
  - **When.** The constant is computed and checked by a test in D2b-3 and D2b-4, after D2b-0's materialization, and rechecked by that test on every later schema change. D2b-1's reader takes the bound as a parameter, so D2b-1 fixes no value.
  - **What counts.** Only CBOR containers (arrays and maps) count. A byte string is one leaf whatever its contents.
  - **The embedded payload.** `canonicalRelationPayload` is a byte string decoded by its own call of the same reader, under its own bound: the deepest path of the relation-payload schemas (`foundation/relation-payload-schemas.v2.json`), computed the same way.
  - **Controls:** for each bound, a deepest-valid payload decodes, and one level more refuses.
  - **Over the bound:** refused before any further allocation, as `PROVIDER.PROTOCOL_VIOLATION`.
  - **No recursion:** the reader and the encoder are iterative.
- **LD-D2B-3. Commitment preimages, the spool entry and provenance (r2, RF-1 and NBO-3).** These are three different representations.
  1. **Commitment preimages are received bytes.** The reader records every node's received byte range. A preimage element (a wire candidate, a `CoverageResultV3` entry, a facts array element) is identified by its range in the frame that carried it, and handed on as a `ReceivedBytes` view. Only the reader constructs one. A commitment over values from several frames is computed when its field arrives, over the retained received encodings of those values, in the order the value class states. Its array head is computed from the count: canonicality makes it the head the reference encodes.
  2. **Field by field, under `commitmentMap`.** Each commitment field uses exactly its `commitmentMap` row (COMMIT-MAP) for its domain and value class. The class decides the preimage:
     - `stage-entries`: one stage's ordered `CoverageResultV3` entries;
     - `stage-major-entries`: every requested stage's entries, stage-major, key order;
     - `stage-candidates` and `stage-major-candidates`: the wire `FactCandidateV1` values, of one stage or of all stages;
     - `batch-facts`: one `FactBatchV1` facts array (TS2 only).

     The Rust3 rows are `Startup1CoverageV3.coverageCommitment` and `Rust3StageResultV2.coverageCommitment` (stage coverage), `Rust3CompleteV2.coverageStreamCommitment`, **`Startup1UnavailableV3.coverageCommitment` and `Startup1BudgetExhaustedV3.coverageCommitment`** (the coverage stream, stage-major: the terminals' coverage is the stream), `Rust3StageResultV2.factCommitment` and `Rust3CompleteV2.factStreamCommitment`. The TS2 rows are the matching seven, plus `Ts2FactBatchV1.batchCommitment` (COMMIT-TS2-FACT-BATCH). Request-side commitments (`domainCommitment`, the subject scope, the per-key scope2 values) are built by the host from the Plan (§3).
  3. **The spool entry is constructed, never sliced** (RPP `limitPolicy.candidateSpoolAccounting`; RUST3-SPOOL). For each admitted Rust3 candidate, D2b-4 builds the closed map `{analysisOrdinal, stageId, candidate}` from the validated semantic value. It computes the entry's full deterministic-CBOR length (every header, key, `stageId`, ordinal and candidate byte), checked-adds it to the running spool bytes, and refuses the whole Analyze on overflow or above `maxCandidateSpoolBytes`. It then checked-adds one to `maxFactCandidatesTotal`. All of this precedes allocating or appending the entry. The empty spool is zero bytes. Received frame bytes are never sliced into an entry.
  4. **The one byte-equality assertion** compares the candidate's re-encoding with that candidate's own received slice: canonicality makes them equal, and a difference is a reader defect. It never compares the whole spool entry with received bytes.
  5. **Observable provenance (NBO-3).** For canonical input, a re-encoding equals the received bytes, so digest results alone cannot tell them apart. So the commitment functions accept only `ReceivedBytes`, which borrows from the frame's payload buffer, and the control asserts that every preimage slice lies within the received payload's allocation (pointer range). A re-encoding mutant fails that, and the black-box mutants (a wrong wrapper, element order, domain or value class) stay.
- **LD-D2B-4. The tables are data.** P3T, its guard overlay and T2O are vendored as byte copies under `crates/components/data/`, pinned to their architecture SHA-256, and embedded with `include_bytes!`. There is no code copy of any row (item 10). Every row, both catch-alls and the total fallback are replayed (D2b-T1), with the overlay's five vectors and the `protocol3_run` and T2O cases of `native-cases.v2.json`. The engine has one pre-match hook, through which D2b-3 and D2b-4 run LD-D2B-15's admission.
- **LD-D2B-5. TS2's Unavailable payload is selected by phase,** as the carriers do (`native-carriers-v1.json`:5813). A payload that does not match its phase refuses at the precheck, recorded as the precheck's trace rather than T2-23's. The outcome is the same, and the trace id is documented.
- **LD-D2B-6. Process events are D3's.** D2b defines the input `ProcessEvent {ZeroExit, Eof, Fault(kind)}`, with `kind` one of deadline, nonzero-exit, signal-death or stdout-byte. The table engine consumes it through the pre-match law. D3a feeds it under item 13's EOF and exit join.
- **LD-D2B-7. Cancel: what the tables read, and what the host sends (r2, NBO-2).**
  - **Read side.** Each table is replayed as published. TS2's T2O permits Cancel from START (T2-18), and its payload admits `host-shutdown`. Rust3's P3T has one Cancel row (P3-29, `*PRE_COMPLETE`, so never START), and RUST3-CANCEL-TYPES fixes the reason to `user-interrupt`.
  - **Send side.** The sender follows HOST-SEND-SCHEDULE, which applies to both protocols: at most one Cancel, taking the next sequence number, never before the Hello slot has been sent, with reason `user-interrupt`, as the exact correlation echo of the frames actually sent (CANCEL-NULLABILITY), compared by deterministic-CBOR bytes.
  - So the host never sends a START Cancel or `host-shutdown`, under either protocol, although TS2's table and payload could carry them. D3 chooses only when to revoke. Widening the sender needs the owner's decision, and none is proposed.
- **LD-D2B-8. No invented bound.** TS2 has no aggregate response bound in its law (gap 6), so D2b sets none and records the gap as a cross-law item for the protocol owner. Rust3's four aggregates are enforced as RPP:143-146 states them, each with its own checked accounting: the frame bound, the response payload total, the response frame count, and the candidate count with the full spool-entry bytes.
- **LD-D2B-9. The send schedule.** D2b provides the constructor of the canonical host send schedule (REQUEST-WIRE-ACCOUNTING): from the admitted Plan's values, it builds every planned slot (Hello, OpenUniverse, the manifests, their greedy max-size chunks and seals, Analyze, and the one reserved maximal Cancel), each with its exact deterministic-CBOR envelope payload, sequence number, chunk coordinates and planned payload SHA-256. It also applies the entry bounds, the frame bound and, for major 3, the request totals. C4 calls it at Plan time, after PlanId and every set admission and before spawn, and owns the refusal (route `native.provider-request-exceeds-wire-limit`). D2b's sender consumes the immutable schedule and emits exactly its slots. Every divergence, a different lawful chunking included, refuses before the frame is written. The running totals are rechecked after every frame.
- **LD-D2B-10. The Rust3 anchor order** is `cve1-bytes-strict` (carriers ANCHOR-WIRE-SPAN), using `opensip_identity::encode_cve1`. That is a byte ordering, not a CBOR reader, so it is consistent with the law's rejection of `capability_codec` as a reader. TS2 keeps `cbor-bytes-strict`.
- **LD-D2B-11. NFC.** `opensip-identity` gains one exported predicate, `is_nfc(&str)`, over its existing pinned `unicode-normalization` (=0.1.24), and the constant `NFC_UNICODE_VERSION`. The components crate takes only `opensip-identity` and `opensip-contracts`, among its permitted owners. **Both versions are pinned:** the reference's `unicodedata.unidata_version` (16.0.0), recorded in the differential corpus, and the tables' version (16, 0, 0). The vectors must also agree. A disagreement is reported, never papered over, and no wire text is normalized or repaired.
- **LD-D2B-12. The check order for one received frame:**
  1. the 8 length bytes;
  2. the length against the bound, and against any remaining aggregate;
  3. the 32 digest bytes;
  4. exactly `length` payload bytes, where EOF is truncation;
  5. the digest;
  6. the strict decode and the re-encode comparison;
  7. the envelope (`protocolMajor`, `frameType` known and of the direction read, `sequence` equal to that direction's counter, below 2^64 − 1);
  8. the closed payload schema, under the negotiated variant and tokens;
  9. **the contextual admission (LD-D2B-15):** the retained prechecks and payload guards and the carrier joins this frame can decide;
  10. the transition table.

  Each failure is `PROVIDER.PROTOCOL_VIOLATION` with its detail, recorded before anything is published to a consumer. A zero-length payload is a decode refusal (TRUNCATED). Under Rust3, steps 7 to 9 are rust2's retained `framePrecheck` (RUST3-FRAME-PRECHECK), with the same outcome as P3-34.
- **LD-D2B-13. RCA-1's product handshake is the base.** The FA-2 and RUST3-LIM materialization maps recorded after-hashes for `handshake-v1.schema.json` that predate RCA-1's product commit `5b53e5e`, so D2b-0 re-derives each materialization on the current product bytes. It reports every difference from the maps' recorded hashes, and its review judges each, with the registry, source-map and admission updates and every regenerated carrier.
- **LD-D2B-14. Replay.** The historical reference corpus D2b replays byte for byte is native wire owner trial 07 (`docs/implementation/m1/trials/native-wire-owner-07/subject/`, Grok "ACCEPT WITHIN STATED REFERENCE SCOPE"):
  - its 353 admission vectors (31 rules) and the decoder probes of `tools/check_reference.py` (`wire_examples`);
  - a differential corpus built by `tools/wirecodec.py` over generated inputs, replayed against D2b-1's reader (D2b-1's lane).

  They are vendored, hash-pinned, under `crates/components/tests/data/`. The native cases' 101 wire and startup cases are replayed where their executors' inputs are wire values. **Trial 07's scope is historical:** its admission file exempts DISPATCH-STAGE-CORRELATION, TS2-STAGE-PROJECTION and RUST3-PLAN-STAGE-BYTES, and its carriers carry neither successor token. D2b claims no conformance from it beyond that scope. §4's controls cover the rest.
- **LD-D2B-15. The per-frame contextual admission (r2, RF-2).** P3T and its overlay are not the complete payload validator: the overlay retains rust2's `framePrecheck` and the T016 and T020 payload guards as pre-match admission. So D2b-3 and D2b-4 each have an admission step between the schema and the table.
  - **The context it is supplied.** An immutable `DispatchContext`, built by D4's session factory from the admitted Plan before spawn and never changed: the selected protocol and tokens, the OpenUniverse values (executionId, snapshot2, plan2, universe ids, `dependencySourceSetId`), each requested stage's `DispatchBindingV1` (`expectedStageId`, its Analyze-relative ordinal, its plan-stage bytes, its budget, its requested keys and their scope2 commitments), the verified `providerBuildId`, the host-admitted target domain, the sent manifests' entries and digests, and the planned send schedule.
  - **The live state it keeps.** Per direction, the sequence counter. Per Analyze, the current stage, and per stage the next `batchIndex` and the next `candidateOrdinal`. The response totals and the spool. The frames sent, for the echoes and ProviderFault's possible-phase set.
  - **What it checks, before matching:**
    - DISPATCH-STAGE-CORRELATION: `stageId` is the current stage's `expectedStageId`; `stageOrdinal` is the Analyze-relative ordinal, never the retained one; a FactBatch's `analysisOrdinal`, `batchIndex` and first `candidateOrdinal` are exactly the next expected; the batch count is within 1 to the cap (T016);
    - RUST3-BUDGET-EXHAUSTED (T020): `triggerStageId` is the current stage, `unit` and `limit` are that stage's plan budget, `observed` is `limit + 1` (checked);
    - the worker-side echoes and joins of §3 (ECHO-SNAPSHOT2, ACCEPTED-EQUALS-SEAL, PER-KEY-SCOPE2's echo, UNIVERSE-NATIVE-IDENTITY's key suffixes, FP-CANDIDATE, RELATION-PAYLOAD-CBOR, ANCHOR-WIRE-SPAN, ANCHOR-FACT-REF-REFUSED, OCCUPANCY-JOIN, CANCELLED-ECHO, the observed phase, RUST3-PROVIDER-FAULT's possible-phase set);
    - the successor shapes and tokens (LD-D2B-16, LD-D2B-17).
  - **What it never does:** H's fact admission (no `fact2` minted, no registered-record validation), Coverage minting, or any decision outside the frame and its context. A refusal is typed and recorded before the frame's event is published, so a consumer never sees an unadmitted frame.
- **LD-D2B-16. FA-2's symbol census (r2, RF-3; X-FA2-D; NE §9.8).**
  - **Negotiation.** With `symbol-census-v1` in both exact token arrays (Hello and HelloAck; LD-D2B-18), Analyze is `TypeScriptAnalyzeV2` or `AnalyzeV3`, and Complete is `TypeScriptCompleteV2` or `CompleteV3`. Only when both arrays omit it do the inherited payloads stay. A census-bearing payload without the token, or an inherited one with it, refuses as `PROVIDER.PROTOCOL_VIOLATION`, in both directions and for both protocols.
  - **The request (D2b builds it from C4's Plan).** Analyze's `symbolCensus` is `{enumeratorClosure}` exactly when the Plan owes this worker a census, and `null` otherwise. Each `symbol`-kind key carries the §4.1a commitment of the census-free D∅. D2b takes the D∅ commitments and the owed flag from the Plan's values; C4 decides when a census is owed and refuses a non-conforming Plan before spawn.
  - **The return (D2b-3 and D2b-4 admit its shape).** Complete's `symbolCensus` is null exactly when the request's was. `complete` has canonical `examinedPaths`, and `rows` strictly ascending and unique by `nativeSubjectId` bytes, each `path` in `examinedPaths`. `over-bound` has `rowCount` and `examinedPathCount` and no rows, and is lawful only above 100,000 rows, 100,000 paths or 4,194,304 bytes. There is no partial census. A malformed, misordered, out-of-bound, wrongly null or token-mismatched census refuses as `PROVIDER.PROTOCOL_VIOLATION`.
  - **Coverage under the census.** A `symbol`-kind entry's `subjectScopeCommitment` departs from the requested key's only as §9.8 states: under a `complete` census, D∅ with the rows' subjects (canonical-set order) and `subjectCount` equal to the row count; under `over-bound`, and in a clean BudgetExhausted or post-Analyze Unavailable, the requested D∅ with `subjectCount` 0. D2b admits these entry shapes and echoes. **The symbol-key commitment check itself moves to H at clean settlement** (X-FA2-D): D2b hands H the census and the entries as received, and checks nothing the census decides.
  - **Over-bound is not a provider fault.** An `over-bound` census is admitted as a typed event, and its scope-limit route belongs to H and the subject-scope bound's owner. D2b manufactures no fault from it. The same holds for a projected record above 4 MiB, which H finds.
- **LD-D2B-17. RUST3-LIM's subject scope by reference (r2, RF-3; X-RL-D; NE §9.3a).**
  - **Negotiation.** With `subject-scope-reference-v1` in both exact token arrays (LD-D2B-18), every Rust Analyze stage is `StageRequestV3` (`{stageOrdinal, planStage, analysisDomain: StageAnalysisDomainV3}`), in AnalyzeV2 and AnalyzeV3 alike, for every subject count. Without it, `StageRequestV2` stays, with its inline subjects and the 256-subject cap. The token is independent of `target-attribution-v2` and `symbol-census-v1`, and all eight combinations are lawful.
  - **The host side (D2b-4's builder).** `RustSubjectScopeV1` is `{scopeKind: "nonempty-rs-files", subjectCount, subjectScopeCommitment}`, built with the host's analysis-domain constructor from the sealed snapshot: `subjectsAlgorithm` steps 1, 2, 4 and 5, with step 3's sort, duplicate and empty rules but not its cap. `domainCommitment` keeps its recipe over `{subjects, requestedCoverageDomain}`, so it equals the V2 value for the same inputs.
  - **The token-absent path** keeps the inline array and the cap: more than 256 subjects refuses before spawn (C4's refusal, through the constructor's result). **(r3, R2-NBO-1)** F-1 itself is an oversized inline Analyze, possible at or below 256 subjects (repeated rows, stages and path lengths). On the inline path it is closed by LD-D2B-9's full-envelope sizing: the schedule measures the exact Analyze payload, and C4 refuses before spawn. Whether the token is needed is C4's Plan-time decision.
  - **Mismatches.** A `StageRequestV3` without the token, or a `StageRequestV2` with it, is a host invariant that the sender refuses before writing. The worker's own reconstruction and its `input-rejected` ProviderFault are the worker's. D2b admits that ProviderFault under RUST3-PROVIDER-FAULT.
  - **Unchanged:** the limits map (all 32 members), the per-subject work charge, and the response bounds.

- **LD-D2B-18. Exact echo for every token (r3, R2-RF-1; NE §9.1).** HelloAck's token array must equal the Hello's exactly, in both protocols, for every token: the identity tokens and every optional token (`symbol-census-v1`, `subject-scope-reference-v1`, `target-attribution-v2` and the rest the closed enums list).
  - **An omitted offered token, or an added unoffered one,** is `PROVIDER.PROTOCOL_VIOLATION` at HelloAck, before OpenUniverse and before any source byte (reject before disclosure). The session does not continue, and no token is "negotiated off".
  - **A token's historical branch** (the inherited payloads, `StageRequestV2`) is taken only when the token is in neither exact array, which is the signed selection's own choice.
  - **The sender** builds the Hello's array from the admitted selection, and a payload variant inconsistent with the negotiated array is a host invariant refused before writing.

## 3. The duty allocation (r2, RF-2)

Every row of the carriers' `admission` list has one owner here. "Builder" means D2b's host payload builder and schedule constructor, which C4 calls before spawn, so the host's frame content is checked when the schedule is built. "Admission" means LD-D2B-15's received-frame admission.

| Carrier row | Applies to | Owner and point |
| --- | --- | --- |
| FRAME-LIMIT | both | D2b-1 (read: the length before allocation; the reader never allocates from a claimed length); builder (no planned frame over the bound) |
| TS2-ENV-MAJOR, TS2-ENV-DIRECTION-BY-FRAME, TS2-ENV-SEQUENCE | TS2 | D2b-3, envelope step (D2b-1's `Sequence`) |
| RUST3-FRAME-PRECHECK | Rust3 | D2b-4, steps 7 to 9, before the table (D2b-2's pre-match hook) |
| ECHO-SNAPSHOT2, ECHO-PLAN2, ECHO-OPEN-UNIVERSE | both / Rust3 | builder (the host's frames); admission (every worker echo) |
| TS2-MANIFEST-DIGEST, RAW-MANIFEST-DIGEST | TS2 / Rust3 | builder (D2b-1's `manifest_digest`); admission (SnapshotAccepted's echo) |
| TS2-SNAPSHOT-ORDER, RUST3-SNAPSHOT-ENTRY-TYPES, CHUNK-CUSTODY, SEAL-AGGREGATES | both | builder, from C1's sealed snapshot inventory |
| ACCEPTED-EQUALS-SEAL | both | admission: Accepted equals the Seal sent |
| TS2-LOGICAL-PATH-ADMISSION, CANONICAL-PATH-ADMISSION, PATH-SITE-SEGMENT-LAW | both | builder for the host-sent sites (snapshot entries and chunks, dependency chunks); admission for the worker-sent sites (anchor `source-span.path`, `Rust3SubjectV2.path`) |
| DEPSRC-CUSTODY, PACKAGE-KEY-JOIN | Rust3 | builder, from the Plan's admitted dependency-source set |
| DEPSRC-SET-KEY-CONSTRAINTS, DEPSRC-WIRE-REPRESENTABILITY | Rust3 | the dependency-source set admission, before PlanId (Plan side, C4); not D2b |
| PREPARED-V3-ENTRY | Rust3 | builder |
| PREPARED-V3-SET-JOIN | Rust3 | host part: the Plan side before spawn (C4); worker part: the worker's own |
| PREPARED-V3-READ-AUTHORITY, PREPARED-V3-WIRE-LIMIT, PREPARED-V3-PATH-REPRESENTABILITY | Rust3 | the prepared-output set admission and selection (Plan side, C4); not D2b |
| REQUEST-WIRE-ACCOUNTING | both | builder (the schedule constructor); C4 calls it and owns the refusal (LD-D2B-9) |
| HOST-SEND-SCHEDULE | both | D2b-3 and D2b-4's sender (LD-D2B-7, LD-D2B-9) |
| RELATION-PAYLOAD-PATH-LAW | both | H: `validate_registered_record`, at fact admission |
| OWNER-PATTERN-EVALUATION | both | each consumer of the owner schemas it scopes (r3, R2-NBO-2): D2b's schema checks of the startup carriers, of the occupancy-companion schema, and of every transitive external wire schema those checks reach; H for the relation-payload schema; the Plan side for the evidence schema |
| TS2-BUDGET-PROJECTION, TS2-STAGE-PROJECTION | TS2 | builder, from the Plan's selected stages |
| DISPATCH-STAGE-CORRELATION | both | builder (`stageId`, `stageOrdinal`); admission (stage, ordinals, batch counters, T016) |
| TS2-SUBJECT-SCOPE-RETAINED, TS2-DOMAIN-COMMITMENT, RUST3-DOMAIN-COMMITMENT, RUST3-SUBJECTS | both | builder (a fresh reconstruction, with the per-key scope2 values) |
| PER-KEY-SCOPE2 | both | the scope2 descriptors are minted before spawn by the Plan side (C4), and the same descriptor drives H's `admit_coverage_result_v3`; builder places them; admission checks the worker's echo (`entries[i].key` and `examinedUniverse` equal `keys[i]`, except §9.8's census departure) |
| RUST3-PLAN-STAGE-BYTES | Rust3 | builder: `dCBOR(planStage)` equals the selected Plan stage's bytes |
| UNIVERSE-NATIVE-IDENTITY | both | builder (OpenUniverse's ids); admission (Coverage keys' suffixes) |
| FP-CANDIDATE | both | admission: the candidate's wire law (registry relation, rung, layer and schemaId; producer and language constants; `producerVersion` equal to the verified `providerBuildId`; target universe in the host-admitted target domain). H then admits the fact |
| RELATION-PAYLOAD-CBOR | both | admission: the byte string decodes once under D2b-1's reader, re-encodes byte-equal, at most 1,048,576 bytes, within its own depth bound (LD-D2B-2). Its registered-record validation is H's |
| ANCHOR-WIRE-SPAN, ANCHOR-FACT-REF-REFUSED, OCCUPANCY-JOIN | both | admission |
| RUST3-SPOOL | Rust3 | admission (LD-D2B-3 item 3) |
| COMMIT-MAP, COMMIT-TS2-FACT-BATCH | both / TS2 | admission, recomputed over received bytes (LD-D2B-3) |
| CANCEL-NULLABILITY | both | sender |
| CANCELLED-ECHO, TS2-OBSERVED-PHASE, RUST3-CANCEL-TYPES, RUST3-PROVIDER-FAULT, RUST3-BUDGET-EXHAUSTED | both / TS2 / Rust3 | admission |

D2b-3's and D2b-4's lanes check this table against the carriers' list: every id is present once, and no id is missing.

## 4. Checks (each sub-unit's lane)

- **Suites:** the components suite at base and candidate, and the identity suite for LD-D2B-11, with equal failure sets.
- **Formatting and lints:** rustfmt, and warning-denied Clippy.
- **Repository checks:** the package edges under the O1-a package policy, the operability source census, the census-closure check, and verify_design. For D2b-0, also its generation checks and the census `--check` after the blind refresh.
- **D2b-1 controls:**
  - the reference probes with their codes;
  - every non-shortest head;
  - the closed forms;
  - claimed lengths never allocated;
  - depth bounded and iterative;
  - deterministic encoding;
  - the differential corpus (the reference's outcome for every input, under both profiles), with both Unicode versions pinned;
  - the frame prefix (bound before any further read, truncation at every cut, the digest, zero length, the aggregate allowance);
  - sequences;
  - the commitment and manifest-digest known answers;
  - `ReceivedBytes` provenance.
- **D2b-3 and D2b-4 controls, beyond D2b-T1 to T5 and trial 07's replay:**
  - **RF-1:**
    - a spool entry's charged length equals its full encoded wrapper, and differs from its candidate slice's length;
    - the spool and count bounds are each refused one over, before append;
    - each `commitmentMap` row recomputed, with a swapped domain, a swapped value class (fact ↔ coverage) and a reordered preimage each refused;
    - the terminal Unavailable and BudgetExhausted coverage commitments under the coverage-stream domain over stage-major entries;
    - the provenance assertion.
  - **RF-2, by owner and refusal point (r3, R2-RF-2).** Every refusal precedes publication, and no earlier check is bypassed.
    - **Schema admission (step 8):** a FactBatch of 0 or 4,097 facts or candidates (each carrier's 1 to 4,096), and the other shape and count bounds.
    - **The builder or sender, before writing:** a request `stageOrdinal` taken as the retained ordinal; a `planStage` whose bytes differ from the Plan's (including an optional member present as null); a request projection that is not the Plan's selected stages.
    - **Contextual admission (step 9), each frame well-shaped and passing its closed schema:** a FactBatch for another stage, or at another Analyze ordinal; a duplicate, skipped or decreasing `batchIndex` or first `candidateOrdinal`; a T020 BudgetExhausted naming another stage or with a wrong `observed`. Each refuses before the table is matched.
  - **RF-3, FA-2:**
    - per protocol, the census token in both exact arrays and in neither, independent of the other tokens (Rust3's eight combinations below);
    - **(r3)** the census token offered and omitted from the HelloAck, and unoffered and added to it: each refuses at HelloAck, before OpenUniverse and any source byte, and the session does not continue;
    - both payload mismatch directions on Analyze and on Complete;
    - the old no-token payloads still admitted, and the old no-token refusal controls kept;
    - `complete` and `over-bound` censuses, each bound one over and at the bound;
    - misordered, duplicate and off-extent rows, and a wrongly null census;
    - the D∅ request commitments against the Plan;
    - `symbol`-kind Coverage under `complete`, `over-bound` and the clean BudgetExhausted and Unavailable terminals;
    - an over-bound census admitted as a typed event, with no fault manufactured;
    - the handoff to H carrying exactly the received census and entries.
  - **RF-3, RUST3-LIM:**
    - all eight combinations of the three Rust tokens, each in both exact arrays or in neither;
    - **(r3)** the reference token, and `target-attribution-v2`, each omitted from or added to the HelloAck: each refuses before disclosure;
    - `StageRequestV3` without the token and `StageRequestV2` with it, both refused by the sender;
    - the reference scope's `subjectCount`, `subjectScopeCommitment` and `domainCommitment`, equal to the V2 values for the same inputs, at 1, 256, 257 and many subjects;
    - the token-absent path refusing 257 subjects through the constructor;
    - **(r3, R2-NBO-1)** a token-absent inline Analyze at or below 256 subjects whose payload exceeds the frame bound, refused by the schedule's sizing before spawn;
    - the worker's `input-rejected` ProviderFault admitted.
  - **The successors' vectors:** `fa-2/evidence/vectors.json` and `rust3-lim/evidence/vectors.json`, vendored and hash-pinned beside trial 07's, and replayed where their inputs are wire values.
  - **The duty table:** §3 checked against the carriers' admission list.
- **Mutations,** each failing its sub-unit's tests:
  - **D2b-1:**
    - a non-shortest integer accepted;
    - an unsorted map accepted;
    - a tag accepted;
    - a non-NFC text accepted;
    - the length checked after allocation;
    - the digest unchecked;
  - **D2b-2:** a table row skipped; the fallback not total;
  - **D2b-3 and D2b-4:**
    - an echo member ignored;
    - a limits member changed;
    - a commitment computed from a re-encoding (killed by the provenance assertion);
    - the spool charged at the candidate's length;
    - the stage correlation unchecked;
    - the batch counter unchecked;
    - a census token mismatch accepted;
    - the reference scope's count not reconstructed.

## 5. Not claimed

- No caller, no supervision, and no fact admission.
- No census settlement and no symbol-key commitment check (H).
- No Plan-side decision: when a census or the reference token is owed, the set admissions, the scope2 descriptors and the refusals before spawn are C4's.
- No qualification.
- D2's completion is not claimed until D2b-4 lands.

## 6. Questions for the reviewer

- **Q1.** Does LD-D2B-3 now separate the three representations as RPP and `commitmentMap` require, and is the `ReceivedBytes` pointer-range assertion an adequate observable for provenance?
- **Q2.** Is §3's allocation right, in particular the line between D2b's builder and admission and the Plan side (C4) and H? Are FP-CANDIDATE and RELATION-PAYLOAD-CBOR correctly D2b's wire admission, with registered-record validation left to H?
- **Q3.** Do LD-D2B-16 and LD-D2B-17 state X-FA2-D and X-RL-D completely, including the over-bound handoff and the token-absent inline path?
