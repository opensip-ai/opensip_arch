# D2b-3b r2: the TS2 codec's send side and participant (D2b plan r3 as amendments A1 and A2 amend it)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.** Round 1 (`d2b-3b-r1/`, subject `c7aed617…31e7`) returned one required finding (`codex-d2b-3b-r1`). Round 2 fixes it, and rebases the candidate onto D3a-3's supervisor seam (main `2ead5cf`). Round 1's files are not edited.

## Round 1's disposition

| Finding | Disposition |
| --- | --- |
| **D2B3B-R1-RF-1** (P2): latch snapshot read failures before returning them from the sender | **Fixed.**<br>• `realize_next` is now a guard over a private `realize`: any error it returns is latched by `refuse` first. That covers a failed or short read, the end of the schedule, and `send_next`, which goes through it.<br>• `cancel()` latches its `cancel-before-hello` refusal, as `admit_cancel` already did.<br>• The audit of every public sender exit (`realize_next`, `send_next`, `admit`, `cancel_payload`, `admit_cancel`, `cancel`) finds no other unlatched failure.<br>• Controls: `a_snapshot_read_failure_ends_the_transcript` injects a one-shot I/O failure at the first chunk and at a later chunk, through `send_next` and through `realize_next` directly. With the source restored and a read counter, it asserts that `next_slot` and `cancel_payload` are absent, that every later operation returns `AfterRefusal`, and that nothing is read again. The failed-source divergence case and the cancel-before-Hello case gain `ended()`.<br>• Mutations: `source-failure-unlatched` and `cancel-before-hello-unlatched`. |

A2-1's D2b-3b row: "The TS2 send side: the host payload builders, LD-D2B-9's schedule constructor (REQUEST-WIRE-ACCOUNTING), the HOST-SEND-SCHEDULE sender with LD-D2B-7's Cancel law and LD-D2B-18's sender half (the Hello's array from the selection), and the TS2 participant the supervisor drives (D3a's `Participant`)". Its controls are section 4's RF-2 builder and sender controls, for TS2, and A2-3's mutation (a limits member changed).

**Base:** product main `d113fa7`, holding D2b-3a at `feb7739` and D3a-3 at `2fbb779`. The worktree was cut at `2ead5cf`, and the lane moved it onto `d113fa7` (D4-1, inventory v229 and a lifecycle unit, none on a D2b-3b path). D3a-3 changed `supervisor.rs`, so R1's `HostFault` variant and arm are re-applied to its bytes; no other D2b-3b path moved.

**The rebase onto D3a-3's seam** (D3a-3 r2, accepted):
- **`Participant::discard()`** (item 20, DLV:1140-1143): `Ts2Participant` drops its spool and any minted output.
- **`TerminalOutput::mint(kind, spool)`:** each admitted FactBatch frame's received payload bytes are spooled `CANDIDATE_ONLY`, in admission order (D3a-3's fixture spools the same unit). They move into the one terminal output when it is minted. A FactBatch the receiver refuses is never spooled.
- **`ParticipantStep.boundaries`** (M3-L r1:400):
  - `TransferStarted` when the SnapshotManifest is accepted;
  - `TransferEnded` when SnapshotAccepted is admitted;
  - `ContextVerified` when NativeContextVerified or the pre-Analyze Unavailable is admitted.

  Each is carried in the next step. **Owed:** D3a-4 (in its round 2, not integrated) adds three `Boundary` variants. Ts2Participant does not push them yet; that is owed when D3a-4 integrates (rebase or a later unit). **D2b-3a r1 NBO-1:** D2b-3a's SCOPE overview named its base as `0985273` and v222. Its subject, product map, source record and lane bind `01769e9` and v223, as accepted; that round's files are not edited.

## What it changes

| File | Change |
| --- | --- |
| `crates/components/src/provider_protocol/ts2/send.rs` (new) | **The builders, the schedule constructor and the sender.**<br>• `Ts2Plan`: the admitted Plan's values for one worker (no producer yet: C4's). `Ts2Request::build(&Ts2Plan)` builds the seven host frame families' payloads, closed-checks each, then plans the schedule; `PlanRefusal::{HostInvariant, ExceedsWireLimit {route, faults}}`.<br>• `Ts2Schedule`: the slots (`Slot`, every member of HOST-SEND-SCHEDULE's `slotBinding`) and the Cancel reserve.<br>• `Ts2Sender`: `realize_next`, `admit`, `send_next`, `cancel_payload`, `admit_cancel`, `cancel`; `SendRefusal::{Divergence, Source, AfterRefusal}`.<br>• `SnapshotSource`: the sealed snapshot's bytes, read at send time (no producer here: C1's custody). |
| `crates/components/src/provider_protocol/ts2/participant.rs` (new) | **`Ts2Participant`**, D3a's `Participant` for TS2 (LD-D3A-3), including D3a-3's `discard`: the receiver, the sender, D2b-1's accumulator, one pending write, the spool and the boundaries; `new(table, context, request, source)` and `cancel()`. |
| `crates/components/src/provider_protocol/ts2_send_tests.rs` (new) | 19 tests (below), a child of D2b-3a's test module so its worker-frame fixtures are reused. |
| `crates/components/src/provider_protocol/ts2.rs` | The two modules and their re-exports. Two read-only accessors on `Ts2Receiver`: `admits(&HostFrame)` (the gate, LD-D2B3B-6) and `terminal_kind()`. `sent` now builds its event through the same `host_event` the gate uses (no behaviour change). |
| `crates/components/src/provider_protocol/ts2_tests.rs` | **D2b-3a r1 NBO-2:** the depth bound's positive witness is now a lawful TS2 frame, a Coverage frame of depth exactly 7, read under the bound and admitted by the receiver in a session (`T2-13`); one level more (an array inside its `unresolvedEdgeClasses`) refuses at the reader (`Depth`). One line declares the new test module. |
| `crates/components/src/supervisor.rs` | **R1**, re-applied to D3a-3's bytes: `ParticipantStatus::HostFault`, and its one `apply_step` arm. The transition into it triggers `Cause::HostFault` once, as `Fault` triggers `provider-protocol` (LD-D2B3B-1). |

## The builders (section 3's builder rows, for TS2)

Each payload is built from the Plan's values and checked against its closed schema before the schedule: the carriers' record (`Payload::Record`) or the product schema an extern frame names (`Payload::Extern`, through the embedded registry), as the carriers' `frames` list selects for each host frame. A failure is a host invariant, refused before spawn.

- **Hello** (handshake-v1 `TypeScriptHelloV2`, :443):
  - `limits`: `TypeScriptProtocolLimitsV1`'s ten constants, and `identityVersions`: `IdentityVersionsV1`'s, each read from the schema's `const` (handshake-v1:257);
  - `expectedCapabilities`: the selection's tokens exactly (LD-D2B3B-7). An unordered, duplicate, unknown or identity-incomplete array refuses, and nothing is sorted or repaired;
  - LD-D2B-18's sender half: a selection offering `symbol-census-v1` refuses, since the census-bearing Analyze is D2b-3c's.
- **OpenUniverse** (startup-v1 `TypeScriptOpenUniverseV2`): the universe carried exactly. `universeKey` is the host's recomputation, `"sha256:" + hex(H("native.semantic-universe.typescript.v2", universe.resolvedInputs))` (startup-v1 `universeIdentity` and `typescriptOpenUniverse.universeKey`, "recomputed by host and worker"; identity-schemas.v3 `native-semantic-universe`) (UNIVERSE-NATIVE-IDENTITY).
- **SnapshotManifest**, from C1's sealed inventory:
  - every `snapshotId` is OpenUniverse's (ECHO-SNAPSHOT2);
  - `manifestSha256` is D2b-1's `manifest_digest` (TS2-MANIFEST-DIGEST);
  - the closed check holds TS2-SNAPSHOT-ORDER, and TS2-LOGICAL-PATH-ADMISSION's lexical rule over each complete host-sent path (PATH-SITE-SEGMENT-LAW).
- **SnapshotFileChunk:** the greedy chunks, header members checked at plan time, each whole chunk at send time (CHUNK-CUSTODY).
- **SnapshotSeal:** `entryCount`, the checked sum of file lengths, and the checked sum of greedy chunk counts (SEAL-AGGREGATES).
- **Analyze** (DLV `multiStageAnalyze` and `stageRequestProjection`):
  - OpenUniverse's echoes (ECHO-OPEN-UNIVERSE);
  - all and only the selected stages in their order, with Analyze-relative ordinals 0..n-1 and `dependsOn` `[]` when absent (TS2-STAGE-PROJECTION; DISPATCH-STAGE-CORRELATION's builder side);
  - the budget projection (TS2-BUDGET-PROJECTION; LD-D2B3B-8);
  - the subject scope over every file entry in manifest order, under the carriers' `commitmentMap` domain for `Ts2SubjectScopeV1.subjectScopeCommitment` (TS2-SUBJECT-SCOPE-RETAINED);
  - the keys placed as the Plan minted them, `producerVersion` the verified `providerBuildId` (DLV CoverageKeyV1; PER-KEY-SCOPE2's placement);
  - `domainCommitment` over `{subjectScope, keys}` under the `commitmentMap` domain for `Ts2RequestedCoverageDomainV1.domainCommitment` (TS2-DOMAIN-COMMITMENT).
- **Cancel:** built by the sender from the sent state (below).

## The schedule (REQUEST-WIRE-ACCOUNTING; LD-D2B-9)

The constructor reads REQUEST-WIRE-ACCOUNTING's `params` and refuses at load unless they are the implemented ones: `lengthScope` envelope-payload, `prefixIncluded` false, `chunking` greedy-max-chunk, `schedule` canonical-greedy, `reserveCancel` true, the SnapshotManifest entry bound `maxSnapshotEntries`, and request totals not applying to TS2. HOST-SEND-SCHEDULE's `planConsumption`, Cancel `maxCount` and the ten-member `slotBinding` are checked the same way. The planner follows trial 07's `representability.py` (`plan_ts2_request`):
- **the slots:** Hello, OpenUniverse, SnapshotManifest, each file entry's greedy chunks, SnapshotSeal and Analyze. Each is measured as its exact envelope payload and bound to the SHA-256 of its payload's deterministic CBOR;
- **the chunks:** sized in closed form and never materialized. A chunk's digest covers the payload without `bytes`; the entry's `contentSha256` rides on its last chunk slot;
- **the reserved Cancel:** the maximal echo (`executionId`, `analysisOrdinal` 0, `user-interrupt`) at the last sequence a Cancel can take. It is measured and frame-bounded;
- **the refusals,** each through the carriers' `params.route` (`native.provider-request-exceeds-wire-limit`):
  - more entries than `maxSnapshotEntries`, refused before the manifest is built (LD-D2B3B-9);
  - any planned frame over `maxFramePayloadBytes` (FRAME-LIMIT's builder side).

  TS2 declares no request totals.

## The sender (HOST-SEND-SCHEDULE)

It follows trial 07's `sender_ref.py` (`consume` and `realize`):
- **Realization** is independent of the planner: its own greedy walk over the file entries, each chunk's bytes read from the sealed snapshot, and the seal over the chunks the walk emitted.
- **Each frame,** before it becomes sent state, is compared with its slot:
  - the sequence and frame type;
  - a chunk's coordinates (`path`, `chunkIndex`, `byteOffset`, byte length);
  - the seal's `totalChunkCount`;
  - the closed schema;
  - the payload length and digest.

  The frame bound is rechecked (defensive); TS2 has no request totals. The entry's bytes actually sent must hash to its `contentSha256` at its last chunk.
- **A divergence** (`SENDER_DIVERGENCE:<reason>`) or a snapshot read failure ends the transcript: nothing is written, and every later call refuses.
- **The Cancel** (LD-D2B-7; CANCEL-NULLABILITY):
  - at most once, never before the Hello slot, at the next sequence;
  - reason `user-interrupt` only;
  - the exact echo of what was sent (`executionId` null until OpenUniverse is sent, `analysisOrdinal` null until Analyze is), compared by deterministic-CBOR bytes;
  - within the reserve (defensive);
  - nothing follows it.

## The participant (A2-1; LD-D3A-3)

- **Writes.** Each call writes at most once from the one pending frame. A slot is accepted, and recorded in the receiver, only when T2O admits it (LD-D2B3B-6). So OpenUniverse waits for the HelloAck, the snapshot for UniverseAccepted, and Analyze for NativeContextVerified. The Cancel is queued after the frame in flight, and dropped if a terminal arrives first.
- **Reads.** Each call reads at most once, at most `READ_QUANTUM` bytes (LD-D2B3B-11), into D2b-1's accumulator. Each completed frame goes to D2b-3a's receiver.
- **Progress** comes from admitted transitions only (item 15):
  - SnapshotAccepted gives `SnapshotAcknowledged`;
  - FactBatch V1 or V3 gives `FactBatch`;
  - Coverage gives `Coverage`, and `StageChanged` when the table moved to the next stage.

  `admitted_payload_bytes` is the admitted frames' payload bytes (D3a-2's TS2 aggregate).
- **The status** is the table's (`Running`, `Terminal`, `Done`), or:
  - `Fault` for a refused worker frame, an accumulator refusal or truncation at EOF;
  - `HostFault` for a sender divergence, a snapshot read failure, a failed read or write of the host's own pipe end, or a write that takes no byte of a pending frame (std's `WriteZero`; r2) (LD-D2B3B-1).
- **The terminal output** is minted once, when the terminal frame is admitted (the receiver recomputed its commitments), and handed out once.

## Lead decisions

- **LD-D2B3B-1. `ParticipantStatus::HostFault`** (R1, accepted). The participant's own failures are the host's: `Cause::HostFault`, never `provider-protocol`. The edit is the variant and its one `apply_step` arm. D3a's fixture participant never reports it, and no supervisor-level test drives it in this unit. Its controls are the participant's tests and the `host-fault-reported-as-protocol` mutation.
- **LD-D2B3B-2. `Ts2Plan`** (decision (a)): the Plan's TS2 values as one input type. There is no producer yet; C4 owns the Plan and calls the constructor (LD-D2B-9).
- **LD-D2B3B-3. `SnapshotSource`** (decision (b)): the caller implements it (C1's custody through D4). Its bytes are read at send time and bound by the entry digest.
- **LD-D2B3B-4. The user Cancel is `Ts2Participant::cancel()`** (decision (c)). It sends `user-interrupt` only. D3b, which owns user cancellation, adds the trait hook and the caller.
- **LD-D2B3B-5. The context and the request must join.** `Ts2Participant::new` refuses (`Ts2Refusal::Context`) unless every value the receiver checks an echo against equals the value the sender sends:
  - the tokens, identity versions and descriptor digests;
  - OpenUniverse's ids;
  - the manifest digest and files, and the seal's totals;
  - each stage's id, ordinal, relations, budget and keys, with `producerVersion` the context's `providerBuildId`.
- **LD-D2B3B-6. The T2O gate** (decision (f)). `Ts2Receiver::admits` steps a copy of the run with the host frame; no row is copied into code (LD-D2B-4). The sender writes a slot only when it holds. T2O admits a Cancel from START (T2-18), but the sender never sends one before the Hello slot (LD-D2B-7).
- **LD-D2B3B-7. The Hello's array is the selection's exactly** (decision (d)): handshake-v1:443's "the selected signed capability row's tokens". Its order and closure are the schema's to check, and the builder never sorts.
- **LD-D2B3B-8. The absent budget** (decision (e)): DLV `budgetProjection.absent`'s source is the signed TypeScript provider budget profile, so `Ts2Plan.default_budget` carries its six values and must name exactly the six wire dimensions (read from the carriers' `Ts2ProviderWorkBudgetV1`). Work-units L gives L in every dimension. Every projected value is within 1..2^63-1 (DLV `work-units` `minimum` and `maximum`; the carriers' note "the host projection emits 1..2^63-1 only"). The tests use DLV's two projection vectors.
- **LD-D2B3B-9. The entry bound refuses first.** A manifest over `maxSnapshotEntries` would also fail its closed check (`maxItems`), so the bound is checked before the manifest is built, and its refusal is the route's, as REQUEST-WIRE-ACCOUNTING states. The reference collects entry and frame faults together; here an entry-bound refusal reports that fault alone.
- **LD-D2B3B-10. Literal constants.** `providerId` and `producer` `typescript-semantic`, `operator` `semantic-provider`, `scopeKind` `all-snapshot-files`, `schemaVersion` 1, `analysisOrdinal` 0, the Cancel reason and the universe domain are written as their sources state them. Each except the domain is held by the closed check. The domain is startup-v1's `universeIdentity` instantiated for TypeScript, and a test recomputes the key with it.
- **LD-D2B3B-11. `READ_QUANTUM`** is 65,536 bytes: D3a's service quantum for fd1 reads (`TOOL_READ_BUFFER`, LD-D3A1-8), not a bound of the law.
- **LD-D2B3B-12. Sent state at acceptance.** A frame becomes sent state when the sender accepts it, before its first byte is written (HOST-SEND-SCHEDULE: "checked before the frame becomes sent state"). The receiver records it then, so the Cancel echoes and the table see the accepted prefix.

## The tests

**`ts2_send_tests.rs` (19; r1's 15 and r2's 4):**
- **The builders (4):**
  - the Hello's limits and identity versions equal handshake-v1's constants, read independently; its tokens are the selection's; four malformed arrays refuse; an optional token is carried; `symbol-census-v1` refuses;
  - OpenUniverse's `universeKey` recomputed independently; the universe carried exactly; a schema-invalid universe refuses;
  - the manifest digest, the symlink entry, the seal's totals and the snapshot echoes; five path and order refusals;
  - Analyze's echoes, DLV's two projection vectors, the subject scope and domain commitments recomputed with DLV's domains (DLV:1080-1081), the keys, and DLV's `reject-unordered-requested-domain`, two out-of-range budgets, an incomplete profile and an empty stage list, each refused.
- **The schedule (2):**
  - the canonical slots, the chunk coordinates (a 2 MiB + 5 entry in three chunks, an empty entry in none), the entry digests on last chunks, the seal count, each slot's size and digest against the sender's realized frame, and the reserve against the maximal Cancel's envelope;
  - the route read from the carriers; 200,001 entries refused by the entry bound; a 16,500-entry manifest of 4,096-scalar paths refused by the frame bound.
- **The sender (3):**
  - exactly the schedule, sequenced, with the sealed bytes sent;
  - eleven divergences, each refused before writing and ending the transcript:
    - a sequence, and a frame out of order;
    - a changed Hello limits member;
    - a same-length executionId substitution;
    - Analyze with a retained `stageOrdinal`, a stage dropped, or the stages reordered;
    - a different lawful chunking;
    - bytes the manifest does not commit;
    - the seal's count;
    - a failed snapshot read;
  - the Cancel law: before the Hello; after the Hello (both null); four wrong echoes, `false` for null among them; a wrong sequence; after OpenUniverse; after Analyze, at sequence 9 within the reserve; and a second Cancel.
- **The gate (1):** T2O admits Cancel at START while the sender has none; the gate does not step the run.
- **The participant (5):**
  - a lawful session from Hello to DONE: the host frames in T2O order, OpenUniverse only after the HelloAck, the progress, the terminal output once, and no Cancel after the terminal;
  - a snapshot read failure is `HostFault`, with no chunk written;
  - a HelloAck adding an unoffered token is `Fault` before OpenUniverse; truncation at EOF is `Fault`;
  - the Cancel after the Hello in flight, its exact null echo, then WAIT_CANCELLED and no second Cancel;
  - six context/request disagreements, each refused at construction;
  - **(r2)** the spool: two candidates in one admitted FactBatch become the terminal output's one spooled payload, its received bytes exactly; a discard drops the output; the three boundaries in order;
  - **(r2)** a pre-Analyze Unavailable gives `ContextVerified` and is the terminal, with no Analyze sent;
  - **(r2)** the host pipe ends: WouldBlock and Interrupted on read and write are neither progress nor fault; a zero-length write, a write error and a read error are each `HostFault`, after which nothing is written and no Cancel is lawful.
- **(r2) The sender's latch (RF-1):** `a_snapshot_read_failure_ends_the_transcript` (four cases: two chunks, two entry points).

**`ts2_tests.rs`:** the depth test's witness (NBO-2), unchanged in count.

## Checks

Lane r2, attempt 1, `evidence/d2b3b-checks-r2/` (the lane of record), on product `d113fa7`. allPassed. No void attempt.

- **The suites,** at base (main's checkout) and candidate. D3a's fixture record is written beside each side's lib test binary first, so the supervisor's tests run on both sides:

  | Suite | Failed (base / candidate) | Passed (base → candidate) |
  | --- | --- | --- |
  | components | 0 / 0 | 145 → 164 (the 19 new tests) |
  | identity | 0 / 0 | 72 → 72 |
  | contracts | 0 / 0 | 0 → 0 |

  No test differs, and none was rerun in isolation.
- **Lints:** rustfmt on the six changed and new Rust files, all base-clean or new and all clean. Warning-denied all-targets Clippy on contracts and components.
- **The focused TS2 tests:** D2b-3a's 16 and D2b-3b's 19 pass.
- **The duty table:** 30 rows, the carriers' 55 ids each listed once, and all 19 TS2 builder and sender rows named.
- **Repository checks:** the environment exceptions, the operability source census (114 rows, no findings, the mint audit unchanged), the census-closure check (no closure file changed) and verify_design (52 admission sources).
- **Seventeen mutations,** each caught by failing focused tests:

  | Mutation | Caught by |
  | --- | --- |
  | limits-member-changed (A2-3) | every test that builds a request, and the Hello constants test |
  | payload-digest-unchecked | `every_divergence_refuses_before_writing` |
  | chunk-content-unchecked | `every_divergence_refuses_before_writing` |
  | cancel-echo-unchecked | `the_cancel_law` |
  | cancel-before-hello | `the_cancel_law`, `the_table_gates_the_host_frames` |
  | budget-range-unchecked | `analyze_is_the_plans_projection` |
  | stage-ordinal-not-analyze-relative | `analyze_is_the_plans_projection` and the participant tests |
  | universe-key-not-recomputed | `open_universe_recomputes_the_universe_key` |
  | send-gate-removed | the participant session tests |
  | host-fault-reported-as-protocol (R1) | `a_host_failure_is_a_host_fault` |
  | context-request-joins-unchecked | `the_context_and_request_must_join` |
  | source-failure-unlatched (RF-1) | `a_snapshot_read_failure_ends_the_transcript`, `every_divergence_refuses_before_writing` |
  | cancel-before-hello-unlatched (RF-1's audit) | `the_cancel_law` |
  | candidate-not-spooled | `the_participant_spools_its_candidates_and_discards_them` |
  | discard-keeps-the-output | `the_participant_spools_its_candidates_and_discards_them` |
  | context-boundary-dropped | `a_pre_analyze_unavailable_verifies_the_context_boundary`, the spool test |
  | zero-write-is-progress (checklist item 3) | `the_host_pipe_ends_fail_as_host_faults` |

## Self-review (the lead's pre-submission checklist)

1. **Charge before work.** Not applicable: D2b's codec runs under no work ledger. No plan, law row or seam charges the builder, the sender or the participant: the frame bound, the closed schemas and the schedule bound the work, and D3a meters the child. No charge is claimed.
2. **Exact charges vs bounds.** Not applicable, as in item 1. The schedule's sizes are exact (each slot's envelope payload, the chunks in closed form) and are compared with the realized frames byte for byte (`the_schedule_is_canonical`). The frame bound is a bound, never a size.
3. **System-call error conventions.** The participant calls no raw system call: fd0 and fd1 are `io::Write` and `io::Read`, and the snapshot is `SnapshotSource`'s `io::Result`, with no errno.
   - **Empty versus failure:** a read of 0 bytes is EOF, judged at a frame boundary, and truncation otherwise. A write of 0 bytes of a pending frame was counted as progress in r1, which could spin; **r2 makes it `HostFault`** (std's `WriteZero`).
   - WouldBlock and Interrupted are neither progress nor failure. Every other error is `HostFault`.
   - Controls: `the_host_pipe_ends_fail_as_host_faults`, and the `zero-write-is-progress` mutation.
4. **Pinned-source equality.** Each constant comes from its source and is checked member by member:
   - the limits and identity versions are each schema's `required` members with their `const`s, and a test reads them independently and compares the maps by deterministic-CBOR bytes, so a substitution or an added member is caught;
   - the host frame list must equal the seven implemented;
   - HOST-SEND-SCHEDULE's ten-member `slotBinding` must equal the implemented list, in order;
   - REQUEST-WIRE-ACCOUNTING's parameters are each compared;
   - the budget's dimensions are the carriers' `Ts2ProviderWorkBudgetV1` members;
   - the commitment domains are the carriers' `commitmentMap` rows, and the route its `params.route`.
5. **Immutable context pins.** The source record pins accepted or submitted bytes only: plan r3 and its amendments, the accepted reviews and unit records (D2b-3a r1, D3a-1 r3, D3a-2 r1, D3a-3 r2), trial 07's reference, DLV, and round 1's submitted subject. Codex's round 1 review is pinned in `priorRounds`. No file another fork is editing is pinned, and D3a-4 is not consumed.
6. **Time and measurement provenance.** The participant measures no time. It reports boundary events, and D3a's supervisor timestamps them (`supervisor.rs` `boundary`). No duration is fabricated here.
7. **Failure latching** (RF-1). The sender latches every failure exit (above). Participant: once `protocol_fault` or `host_fault` is set, `pump` sends nothing, `wants_write` is false, a read admits no further frame, a process event is not stepped, and `cancel()` is refused. The receiver latches its own refusals (`AfterRefusal`). Controls: RF-1's test, the participant fault tests, and the `source-failure-unlatched` and `cancel-before-hello-unlatched` mutations.
8. **Disclosure.** Untested here:
   - no supervisor-level test drives `ParticipantStatus::HostFault` through `apply_step`, since D3a's fixture participant never reports it; the `host-fault-reported-as-protocol` mutation and the participant tests cover the participant's side;
   - the supervisor's use of `boundaries`, the spool and `discard` is D3a-3's, tested there with its fixture participant;
   - no TS2 session runs under the real supervisor or a real child (D4's session factory is absent);
   - the `cancel-over-reserve`, `frame-limit` and request-limit branches are defensive and unreachable under the planning limits, as HOST-SEND-SCHEDULE states;
   - D3a-4's boundaries are owed.
9. **Mutations.** Seventeen, each required to fail a focused test, never only a compile: r1's eleven, and r2's six (`source-failure-unlatched`, `cancel-before-hello-unlatched`, `candidate-not-spooled`, `discard-keeps-the-output`, `context-boundary-dropped`, `zero-write-is-progress`). Items 1 and 2 have no applicable mutation (no ledger).

## Not delivered

- **D2b-3c:** FA-2 for TS2 (the census-bearing Analyze and Complete, the census payloads' admission, the depth bound recomputed), trial 07's TS2 replay and FA-2's vectors, and D2b-T4 and D2b-T5.
- **D2b-4a to D2b-4c:** the Rust3 codec.
- **D3a-4's three `Boundary` variants:** owed, as above.
- **D3b:** the Cancel trigger and the trait hook; **D4:** the context, the source and the session factory; **C4:** the Plan values, the call at Plan time and the refusal's route; **C1:** the sealed snapshot's custody behind `SnapshotSource`.
- **TS2's aggregate response bound** stays gap 6 (LD-D2B-8). D3a-2 counts the participant's `admitted_payload_bytes` against its own bound.

## Not claimed

- No caller, no supervision of a provider, no fact admission.
- No qualification; D2b's completion is not claimed.

## Inventory

Three new product paths (`ts2/send.rs`, `ts2/participant.rs`, `ts2_send_tests.rs`): an inventory successor follows acceptance. The changed paths' rows stay true: `ts2.rs` (the receive side, with the gate's two accessors), `ts2_tests.rs` (D2b-3a's tests, with a lawful depth witness), and `supervisor.rs`'s row.
