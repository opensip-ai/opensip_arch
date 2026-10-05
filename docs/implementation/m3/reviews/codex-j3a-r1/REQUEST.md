Codex review: unit **J3a** r1 of law M3-J1 r6, the durable entry, with **inventory v139**. It implements item 14's J3a row: `RequestIdentity` and `ExecutionIdReservations` (item 2), the durable entry with its probe, two-slot attempt and `EntryRefusal` (item 3), the code of J1's successors S2 to S7, and `CommitSession::open`'s reservation (S10, X3d r9 S10.1). You accepted J1 r6 (`m3/reviews/codex-host-pipeline-j-r6/`) and the S2 to S6 batch (`m2/reviews/codex-j1-successors-s2-s6-r1/`). Grok leads as of 2026-10-04 (Claude Opus 5.5 stopped on its weekly limit). You are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the product change and inventory v139, with an **`inventoryCandidateAssessment`**. J3a has no contract successor.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-j3a-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Run every command at `nice -n 19` (a lead-set rerun unniced, see "Shared machine"), with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and cargo `--locked --offline`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

**Shared machine.** Several implementation agents and reviewers share this machine through one lane lock, `LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`.
- Before any cargo build, test or clippy run, take it with `mkdir "$LOCK"`, waiting while it exists. Remove it with `rmdir "$LOCK"` straight after, **only if your own `mkdir` succeeded** (track it with a flag).
- **A lead-set rerun** holds the lock for the whole set, unniced, with nothing else running: the crash matrix's 5000 ms timing guard fails under load. If your script checks for load before a set, match running executables by name (`ps -Ao pid=,comm=`), never by command line. A waiting script whose arguments mention `cargo` deadlocked two units on 2026-10-04.
- Don't stop a lane script mid-run: its cargo child is orphaned and keeps running outside the lock (J3a did this twice, see "Lead results").

## Law

All under arch `docs/implementation/`, accepted, each pinned by its accepted snapshot (`hashes.txt`).
- **M3-J1 r6**, `m3/host-pipeline-j/PROPOSAL-r6.md` (173682 bytes, `086e804a…`; your r6 review). The parts J3a implements:
  - **Item 14's J3a row (:912):** "`RequestIdentity` and `ExecutionIdReservations` (item 2); the durable entry, its probe, the two-slot attempt and `EntryRefusal` (item 3); the S2 to S7 code; `open`'s reservation (S10, item 2). Tests J-C2, J-C4, J-C4b and J-C5 to J-C9, with J-C6b."
  - **Item 2 (:216-271):** one RequestId per invocation, the sealed `RequestIdentity` lent to item 3's entry, the ExecutionId reservation registry, who reserves which id, and controls J-C2, J-C4 and J-C4b.
  - **Item 3 (:273-359):** `enter_durable_analysis`, its four steps, the probe and its race, the value-only `created` record, the amendments S2 to S8, and controls J-C5 to J-C9 with J-C6b.
  - **Item 1's J-C1 (:214)**; **item 4's rows R0, R2 and R3 (:367-370)**; **item 10's rows 1 and 3 to 11 (:757-767)**, the entry's refusal rows.
  - **Item 12 (:855):** both lead sets on a J unit's integration commit that touches `crates/security`, serialized.
  - **Item 13's rows S2 to S7 and S10 (:878-883, :887)** and the forbidden substitutes (:936-956).
- **J3a's successors**, each accepted:
  - **S2, 468 r6** (`m2/existing-root-admission-468/PROPOSAL-r6.md`, `93f4d014…`; Codex, `m2/reviews/codex-j1-successors-s2-s6-r1`): item 1's route and `created` record (:42-50), LD6-1 (:30-36), item 2's note (:51-58).
  - **S3, X1 r2** (`m2/ordinary-platform-x1/PROPOSAL-r2.md`, `1d03e1f7…`; same batch): item 1's third producing entry (:48-58), item 2's last sentence (:60-70), item 7's creator-class sequence (:87-98), LD2-1 to LD2-3 (:28-36), item 8's J3a (:99-106).
  - **S4, 464 r3** (`m2/creation-ingress-464/PROPOSAL-r3.md`, `e0803ad9…`; same batch): items 1 and 5 (:40-48, :61-70), LD3-1 (:28-32), item 7's note (:72-81).
  - **S5, X3a r6** (`m2/store-admission-x3a/PROPOSAL-r6.md`, `cb213261…`; same batch): item 2's creator paragraph (:58-67). It needs no X3a code (its r6 header).
  - **S6, X4B r6** (`m2/trust-bootstrap-x4b/PROPOSAL-r6.md`, `c8c54154…`; same batch): item 1's bullet (:90) and the forbidden substitute (:212). No X4B code.
  - **S7, X2 r10** (`m2/project-root-x2/PROPOSAL-r10.md`, `a0d43d99…`; CODEX2, `m2/reviews/codex2-jrw-successors-r1`): item 6's creator branch withdrawn (:244). Its header says S7 needs no code at `d2c00a9` "and J3a keeps it so". RW-S1's item 6c is J4b's.
  - **S10, X3d r9** (`m2/commit-session-x3d/PROPOSAL-r9.md`, `c727001a…`; Grok, `m2/reviews/grok2-x3d-r9`): S10.1 (:486-493), S10.7's `ReservedExecutionId` and `CommitSession` fixtures (:556-560), S10.8's J3a (:562-565).
- **X8 r3** (`m2/refusal-suite-x8/PROPOSAL-r3.md`, `1dc6b71f…`): item 3's export rule, groups D to G, and item 3a's census (:122-148), for the new compile-fail cases.
- **X9 r16** (`m2/crash-matrix-x9/PROPOSAL-r16.md`, `f08efe95…`), X9-6's accepted evidence at C = `3d2d5b5`, and X4-F3's lead sets (`m2/reviews/codex2-x4f3-r1/`), for the comparison.
- **M3-PLAN r10** (`m3/M3-PLAN-r10.md`, `ec8c38f8…`): J3a's row, "J3a, then its lead set" (:545).
- **Not J3a's:** J3b (the cancellation latch, source 9, J-C15 and J-C15b, S12's rows), J3d (the pipeline end to end, the wiring of R4 to R12, the envelope, J-BS and S12-O), J2b, J2c and J4b's item 6c.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-j3a`, detached at product main **`b7b87b7`** (J2a's inventory137 at `174aa30`, E2a's inventory138 at `b7b87b7`; 101 contract successors, 98 inventory successors, v138 selected). Nothing is committed; the sixteen new files are intent-to-add, so `git diff b7b87b7` includes them.
- **Diff:** `git diff b7b87b7` is 440293 bytes, sha256 `76c7f540cc5c0a06d8f249b51c4c6e38c24ab4ecab704a365ab1c866b6d5c171`. It covers 18 modified files and 16 intent-to-add cases. A copy is `evidence/j3a.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`, Node `~/.nvm/versions/node/v24.16.0/bin/node`. A fresh worktree lacks the generator's ignored inputs: copy `tools/contracts/node_modules` and `python-packages` from `/Users/sb/code/opensip-ai/opensip`.
- **Inventory unit (untracked in arch):** `m2/repository-file-inventory.v139.json`, `m2/durable-entry-j3a-inventory-v139/` (README, `successor.json`, `verify_projection.py`, `verification.*`, `verifier-anchor.json`, `evidence/{build_v139.py, stage_lock_j3a.py, verify_scratch.py, drift_scratch_j3a.py}`), `m2/durable-entry-j3a-inventory-v139-subject.json` and `-unit.json`.
- **Evidence:** `evidence/` here, every file pinned in `hashes.txt`: the scripts as run (`locked.sh`, `lanes.sh`, `newtests.sh`, `leadset.sh`, `release.sh`, `pins.sh`, `x9.sh`, `compare.py`, `records.py`), `lanes-summary.txt`, `lock-log.txt` and `j3a.diff`. There is no release-absence file and no `x9/` matrix log: the lead sets have not been run.

## What J3a changes

"pl" is `crates/platform/src/lib.rs`, "cb" `crates/platform/src/crash_barrier.rs`, "rq" `crates/host/src/request.rs`, "ii" `crates/security/src/initial_installation.rs`, "rt" `crates/security/src/custody/installation_routing.rs`, "rp" `read_premise.rs`, "ow" `ordinary_writer.rs`, "cs" `commit_session.rs` and "st" `installation_stage.rs` (all under `custody/` but `ii`). Line numbers are the worktree's.

### Item 2: the identities (platform and host)

- **`RequestIdentity`** (pl:83-111). One field, the 16 drawn bytes. Its only constructor is `RequestIdentity::draw()`, one `request_entropy` CSPRNG draw; a failed draw returns no identity. No literal (private field), no `Default`, `Clone`, `Serialize` or `Deserialize`, no `From` or `FromStr`. Its read-only projection is `bytes()`; `Debug` shows its `req1_` rendering.
- **The host's registry reserves it** (rq:15-80). `RequestAuthority::begin` now draws a `RequestIdentity` and reserves its bytes through the unchanged `allocate` (uniqueness-checked against every RequestId of the process, at most eight draws, nothing published on refusal), and keeps the reserved identity. `identity(&context)` is the lending accessor J3d's pipeline calls to lend `&RequestIdentity` to the durable entry (item 3); a foreign or unreserved context lends nothing. `project` is unchanged, so the envelope's `requestId` renders the same reservation. No forbidden symbol enters `request.rs` (J-C1).
- **`ExecutionIdReservations`** (pl:152-208), the process-custody registry, beside `request_entropy` as item 2 places it. One `BTreeSet` of reserved bytes per process in a static `Mutex`. `allocate` draws up to eight times, reserving the first draw no reserved id has; a failed draw is `Entropy`, exhaustion `CollisionExhausted`, and neither reserves anything. Nothing ever removes a reservation. The type is crate-private: `reserve_execution_id()` (pl:217) is the only way to reserve, and `execution_id_reserved(id)` (pl:223) the only read (it reserves and grants nothing).
- **`ReservedExecutionId`** (pl:113-141): the bytes and their `exec1_` rendering. Only the registry constructs it (and, under the test-only feature, cb's inject-id reservation, below). No literal, `Default`, `Clone`, `Serialize`, `Deserialize`, `From` or `FromStr`. `as_str()` is the read-only projection; `PartialEq` and `Debug` (its rendering).
- **The inject-id reservation** (cb:764-791). X9's draw point `x3d.session.execution-draw` admits `inject-id:<id>`. `reserve_injected_execution_id` reserves the injected id in the same registry, as a draw is (a grammar refusal, or `Reserved` if this process already holds it, which is never redrawn). It lives in the feature-only `crash_barrier` module, a child of the crate root, so it constructs the root's private types without any constructor existing in a release build and without a new `cfg` site (X9-1's site list is unchanged).

### Item 2 through S4 and S10: who reserves which id

- **The prelude's** (ii:640-702, S4). `mint_intent` takes `request: &RequestIdentity` and records its bytes; it draws no RequestId. In the same charged step it calls `reserve_execution_id()`, before the disclosure and before P0 is staged; a failure is `IntentRefusal::Entropy`, the host-I/O row. `CreationIntent` holds the `ReservedExecutionId`; `consume` moves it into `IntentInvocation.execution_id: ReservedExecutionId`; P0's `OwnedInputs` takes only its projection (st:692). `binding()` (465 item 9) is now the reserved ExecutionId's bytes: the RequestId is the whole invocation's and no longer tells intents apart. `IDS_COST` is unchanged (judgment call 6).
- **The durable attempt's** (cs:335-401, S10.1). `open`'s draw point wraps `reserve_execution_id()` in the same step, so the reservation exists before the session; the barrier's payload is the reservation's rendering, as the draw's was. `CommitSession.execution_id` and `StoppedSession`'s ids hold the `ReservedExecutionId`; `execution_id()` returns its projection (storage's binding reads it as before); `SealOutcome::CommitUndetermined` carries the projection (cs:982, :1017). Exhaustion or a failed draw is the host I/O row, as before; an injected id that is not identity §2's grammar is the invariant row, as before.
- **The ephemeral and render attempts'** are the host's draw at each attempt's start (J2c and J3d): `reserve_execution_id()`.

### Item 3: the durable entry (security)

- **`enter_durable_analysis(command, backup_custody_flag, &RequestIdentity, disclosure) -> Result<DurableEntry, EntryRefusal>`** (rt:169-178): no producer, home, profile or release selector. It is `enter(&Native, …)` (rt:233-277) over `EntryOwners` (rt:182-230), whose `Native` owners are production's and whose test owners put the same composition on scratch homes.
  1. **Step 1:** `owners.first()`, attempt A's producers through `produce_unsealed` (rp:420): the process's first attempt slot, the actor, InitialCore, InitialPlatform, each bound to the attempt. A development build ends at F0 here.
  2. **Step 2:** `probe` (rt:133-151): one `walk_chain` on attempt A's ledger with InitialPlatform's premise and H-filesystem check, gate step 0's predicates. `Present`, `PositivelyAbsent(Suffix)`, or the refusal's 468 item 6 row through `gate_refusal`. The walk's retained chain is dropped before it returns.
  3. **3a, `Present`:** `producers.seal()` (rp:401), the Write purpose fixed after the probe and before any receipt exists; then X1 item 2's steps 2 to 4 (`admit_receipt`, ow:515). No intent, no notice.
  4. **3b, `PositivelyAbsent`:** `run_initial_creator` (rt:291-348), the creator act, then `owners.admit_after(ended)`: `admit_ordinary_writer_after` (ow:504), X1 item 2's steps 1 to 4 on attempt B with the process's one gate.
- **The creator act** (468 r6 item 1): `run_initial_creator` consumes attempt A's `Producers` by value, mints the intent with the lent RequestId, runs the creator effects, and drops attempt A with its actor, core and platform inside its block. It enters no gate. `Published`, `LostRace` and `NotPristine` return `CreatorAct { ended, created }`; every refusal returns `EntryRefusal` on its 468 item 6 row.
- **The `created` record** (rt:56-71). `Created { classification, target }`, values only, with `target()` and `backup_status()` (J1 item 9's spelling). Its values are the intent's disclosed target and classification; whether it is `Some` comes only from the act's own typed result (LD6-1): `Published`, or `CreationRefusal::AfterRename` (any failure after the rename, a ledger refusal included). `LostRace`, `NotPristine` and every refusal before the rename, an indeterminate rename included, give `None`. `enter` carries it to `DurableEntry.created` and to every refusal of attempt B.
- **The two-slot attempt** (ii:28-33, :133-193; X1 r2 item 7). Slot A is `begin()`, unchanged. Slot B is `begin_after(CreatorActEnded)`, which consumes the token and is refused unless A is allocated and B is not; a third allocation, or a second B, is `AlreadyAllocated`, the invariant row. `CreatorActEnded` (rt:106) has a private field: only `run_initial_creator` makes one, only after `Published`, `LostRace` or `NotPristine`. The gate stays one per process (`DurableWriteGate::begin`, unchanged).
- **What did not change:** `admit_ordinary_writer()` (still the non-creator entry, still called once by the settlement sweep), the 458c read entries, every item 6 map, and `run_initial_creator` stays `pub(crate)` and defined once in `installation_routing.rs` (J-C1). 468c's `route`, `Entered` and `AdmittedInstallation` are gone: the creator act has no route of its own to the gate (X1 r2 LD2-3).


## Tests: every control J3a owns

"rt-tests" is `custody/installation_routing_tests.rs` (in `installation_routing`'s `tests` module), "pl-tests" platform `lib.rs`'s `reservation_tests`, "ii-tests" `initial_installation.rs`'s `tests`, "cs-tests" `custody/commit_session_tests.rs`, "rq-tests" `request.rs`'s `tests`, and "X8" `crates/host/tests/admission_tests.rs`'s driver over `tests/refusal/cases/`. Every security test runs on scratch homes with 462's signed test trees (the premise PM, or P469 without it), the real account's credentials and the production walk; the one live composition is J-C9's.

| Control (J1 r6) | Test | What it asserts |
|---|---|---|
| **J-C1** (:214) | apps/cli `no_creator_gate_writer_pack_or_commit_symbol_reaches_the_binary_or_the_ingress` (X11a, unchanged, passing) | No forbidden symbol in `apps/cli/src` or host's `outcomes.rs`, `doctor_ingress.rs`, `request.rs`, `lib.rs`; `run_initial_creator` and `admit_ordinary_writer` each defined once, `pub(crate)`, in their owners, and not named by security's `lib.rs`. X11a's binary pins are untouched. |
| **J-C2** (:264), security half | rt-tests `first_use_discloses_before_any_effect_and_admits_a_fresh_attempt_b`; ii-tests `intent_is_bound_charged_and_consumed_once_with_step_zero` and `mint_intent_records_the_lent_request_id_and_draws_only_the_execution_id` | P0's `invocation.requestId` is the lent identity's `req1_` rendering, and it is the only `requestId` anywhere in I. `mint_intent`'s body uses the lent identity once and calls no CSPRNG for a RequestId (source pin). Two intents of one invocation share the RequestId and differ by their reserved ExecutionIds. |
| **J-C2**, host half | rq-tests `the_lent_identity_is_the_projected_request_id` | The identity `RequestAuthority` lends renders exactly as `project` (the envelope's `requestId`); a foreign or unreserved context lends nothing; a forced-draw context has no lent identity. |
| **J-C4** (:266) | X8 `platform_request_identity_{literal, default, deserialize, from_bytes, from_text, clone, serialize}.rs` | No constructor but the draw: no literal from bytes (E0451), no `Default`, `Deserialize`, `From<[u8; 16]>`, `FromStr` (E0277), no `Clone` (E0277), no `Serialize` (E0277). |
| **J-C4b** (:267-271), bullet 1 | pl-tests `a_repeated_draw_is_redrawn_and_the_redraw_is_reserved` | A repeated draw is redrawn; only the redraw is reserved. |
| bullet 2 | pl-tests `eight_collisions_or_a_failed_draw_refuse_and_reserve_nothing` | Eight collisions are `CollisionExhausted`, a failed draw `Entropy`, and neither reserves anything; both map to the drawing owner's host-I/O row (`IntentRefusal::Entropy` → `T::HostIo`; `Draw::Entropy` → `T::HostIo`). |
| bullet 3 | X8 `platform_reserved_execution_id_{literal, default, deserialize, from_bytes, from_text, clone, serialize}.rs`, `platform_reserved_execution_id_injected_absent.rs`, `security_commit_session_open_reserved.rs`; cs-tests `open_reserves_its_execution_id_in_the_process_registry` (source pin on the field) | `ReservedExecutionId` has no other constructor on the plain surface (the feature-only inject-id reservation is unresolvable, E0432); `CommitSession::open` takes no ExecutionId, not even a reserved one (E0061), and the session's field is the reservation. P0's writer is crate-private and takes only `IntentInvocation.execution_id: ReservedExecutionId`'s projection (judgment call 5 on the frame builders). |
| bullet 4 | rt-tests `a_first_use_invocation_reserves_three_distinct_execution_ids`; pl-tests `the_process_registry_reserves_distinct_ids_and_never_releases_one`; cs-tests `open_reserves_its_execution_id_in_the_process_registry` | On first use, the prelude's (P0's), the session's (R12, on attempt B's real chain) and a render draw are reserved and distinct. A reservation outlives its value and the session. |
| **J-C5** (:342-345) | rt-tests `the_steady_state_takes_one_attempt_and_one_gate_and_writes_nothing` | On an existing I: one attempt (slot B never allocated), one InitialCore production, one gate; no intent, no notice write or flush, and every file of I byte-identical before and after; the admission holds the fence until released. |
| **J-C6** (:346-349) | rt-tests `first_use_discloses_before_any_effect_and_admits_a_fresh_attempt_b`, `the_two_slot_sequence_refuses_every_other_allocation`, `the_creator_act_hands_attempt_b_values_only` | The notice is written and flushed once, and at its flush `Library` does not exist yet (before the first creation effect). Attempt B has its own slot and lineage, and its core and platform are produced again on it; one gate. A third allocation (slot A again, or a second B), and B before A, are `Invariant`. The type-level pin: exhaustive struct patterns over `CreatorAct`, `CreatorActEnded`, `Created`, `EntryRefusal` and `DurableEntry` (a new field fails to compile), and the act consumes `Producers` by value (source pin). |
| **J-C6b** (:351-357) | rt-tests `attempt_bs_refused_producers_after_publication_carry_the_creation_record`, `attempt_bs_busy_gate_…`, `attempt_bs_failed_barrier_…`, `attempt_bs_failed_recheck_…`, `a_gate_that_cannot_charge_after_publication_keeps_the_record`, `a_refusal_after_the_rename_carries_the_record_and_one_before_it_does_not` | After `Published`, attempt B's producers (budget), a busy gate, a failed barrier, a failed step 4 recheck and a gate budget each refuse on their row with `created: Some { target: I, backup_status: "unknown" }`, and keep no fence. A failure after the rename (the I-parent barrier) carries the record; a rename not performed and an indeterminate rename (LD6-1) carry none. `LostRace` and `NotPristine` carry none (J-C8's tests). The envelope's `retentionDisclosure` and the `interrupted` branch are J3d's (item 9's first emitter). |
| **J-C7** (:350) | rt-tests `the_probe_has_three_outcomes_and_selects_the_route_only`, `present_then_absent_at_the_gate_ends_on_not_initialized`, `without_the_premise_the_probe_refuses_at_the_root_before_any_intent` | `PositivelyAbsent(Library)` on an empty H, `PositivelyAbsent(Installation)` under a present `OpenSIP`, `Present`, and refusals on their rows (the omitted ACL at `/` without the premise; a file at `Library`, which is not absence). The probe is charged to attempt A and holds no fence afterwards. `Present`, then I deleted before the gate, ends on `NotInitialized` with no intent or notice. Without the premise the entry refuses at `/` before any intent, and H stays empty. |
| **J-C8** (:358) | rt-tests `not_pristine_ends_the_act_and_attempt_b_admits_the_existing_installation`, `a_lost_race_ends_the_act_and_attempt_b_admits_the_winner`, `a_lost_race_to_a_foreign_entry_ends_at_attempt_bs_gate_in_the_custody_row` | Each continues to attempt B, whose writer then runs R4 to R12 on the real chain (project root, tracking, first registration, handoff, `CommitSession::open` with a reserved ExecutionId); `created` is `None`. A lost race to a foreign entry ends at attempt B's gate on the custody row. The commit itself is J3d's (judgment call 5). |
| **J-C9** (:359) | rt-tests `a_development_build_ends_at_f0_with_no_notice_and_no_installation_path` | The production entry, on the process's own attempt, ends `NoEmbeddedRelease` with no notice and no `created`; the real home's OpenSIP is absent. |
| S2 to S7, structure | rt-tests `the_entry_probes_first_and_has_exactly_two_routes`, `the_creator_act_has_no_store_trust_or_registration_entry`, `representative_refusals_choose_their_rows` (unchanged) | The producers, probe and two routes in order; no intent on the steady state; no `DurableWriteGate` in the module; one `mint_intent`. No endpoint, trust acceptance or registration in the creator act's module (S5, S6); first registration's one entry is the ordinary writer's (S7); no production source keeps `AdmittedInstallation`. |


## Item 10's rows and the successors' obligations

**The rows the entry reaches** (item 10 :757-767). `EntryRefusal.termination` is a 468 item 6 `InstallationTermination`, which J2a's projection maps unchanged (`outcomes.rs`, `Observation::Installation`). J3a adds no row or code. Row 1 (RequestId allocation) is the host registry's unchanged refusal. Rows 3 (F0) to 11 (budget) are reached and tested: 3 by J-C9; 4 by attempt B's recheck refusal (`PlatformUnqualified`); 5 by the probe without the premise, and the foreign entry; 7 by the probe race; 9 by attempt B's busy gate; 10 by a rename not performed, an indeterminate rename, a failure after the rename and a failed barrier; 11 by attempt B's producers and gate budgets. Row 6 (incomplete) and row 8 (backup choice) take their unchanged 468c maps; the constant `UNKNOWN` classifier cannot reach row 8.

| Successor | Obligation | J3a's change |
|---|---|---|
| **S2, 468 r6 item 1** | The creator act ends at `Published`, `LostRace` or `NotPristine`, attempt A is dropped with its core and platform, and the act enters no gate. The invocation continues through X1's ordinary admission on attempt B. | `run_initial_creator` consumes and drops attempt A's `Producers`; `enter` then calls `admit_after(ended)`. 468c's `route`, `Entered` and `AdmittedInstallation` are removed. |
| S2, item 1's `created` | Value-only, `Some` exactly when the act performed the rename (its typed result), on every later path; LD6-1's two edge cases. | `Created`, from the act's `Published` or `AfterRename`; `None` for `LostRace`, `NotPristine`, a rename not performed or indeterminate; carried to `DurableEntry` and every attempt B refusal. |
| S2, item 2's note | Attempt B's `InitialPlatform` lends the unchanged capability. | `admit_receipt` lends attempt B's receipt's qualification to the process's one gate; the gate is unchanged. |
| **S3, X1 r2 item 1** | A third producing entry that fixes the Write purpose after the probe and before any receipt exists; on `PositivelyAbsent` the producers serve the act unsealed. A process produces at most one receipt (LD2-1). | `produce_unsealed` and `Producers::seal`; `enter` seals only on `Present`. On first use only attempt B seals a receipt. `produce_for` is now `produce_unsealed` plus `seal`, unchanged in behaviour. |
| S3, item 2's last sentence (LD2-3) | The creator path has no route of its own to the gate. | As S2. |
| S3, item 7 | The two-slot attempt, `CreatorActEnded` (non-Clone, returned only by the act, consumed only by B's allocation), any other second or third allocation `Invariant`, one gate; the durable entry is the `Creator` class's entry (LD2-2). | `begin_after`, slot B's flag, `CreatorActEnded`'s private field, `admit_ordinary_writer_after`; `DurableWriteGate::begin` unchanged. The read receipt with or without a session needs no code (458c's `produce_read_platform` is unchanged). |
| **S4, 464 r3 items 1 and 5** | The intent holds the lent RequestId and a fresh, reserved ExecutionId (reserved before P0 is staged); a failure is the host-I/O row; P0's writer takes only the reservation or its projection. | `mint_intent(…, request: &RequestIdentity, …)`, `reserve_execution_id()` in its id step, `IntentInvocation.execution_id: ReservedExecutionId`, P0's `OwnedInputs` from `as_str()`. |
| **S5, X3a r6** | The creator act produces no endpoint; attempt B's endpoint is admitted from its own `OrdinaryWriteAdmission`. | No X3a code. Pinned: the act's module names no endpoint (`the_creator_act_has_no_store_trust_or_registration_entry`, beside X3a-1's own `the_creator_path_produces_no_endpoint`). |
| **S6, X4B r6** | No acceptance in the creator act; on first use acceptance runs at attempt B's fenced first read. | No X4B code. Pinned as S5. J-C8's and J-C4b's tests reach attempt B's fenced first read (with X4T-0's accepted store). |
| **S7, X2 r10 item 6** | First registration only under an `OrdinaryWriteAdmission`; J3a keeps it so. | No X2 code. Pinned: `register_on_gate` defined once and called only by `OrdinaryWriteAdmission`; no production source keeps `AdmittedInstallation`. J-C8's tests register on attempt B. |
| **S10, X3d r9 S10.1** | `open` reserves its drawn id in `ExecutionIdReservations` in the same step, before the session; failures are the host I/O row; never released; the session holds the reservation and accepts no other id; the draw point keeps its name, place and payload; F34's injected id still reaches the attempt row. | As "Item 2 through S4 and S10" above. |
| S10.7, S10.8 | X8 fixtures for `ReservedExecutionId` from bytes or text and `CommitSession` given another ExecutionId; J3a carries S10.1 with J-C4b. | The sixteen cases (inventory v139). |

**Forbidden substitutes (J1 :936-956), as J3a's code bears on them:** one RequestId per invocation, drawn only by the CSPRNG and reserved by the host (the intent draws none); no ExecutionId before its reservation (P0's and the session's are reserved in their drawing step); no intent or notice on `Present`; the probe grants nothing and its handles are dropped; nothing of attempt A reaches attempt B but `Created`'s values (the type-level pin); no second gate or third attempt; attempt B only with `CreatorActEnded`; no store, trust acceptance or registration in the act; the creation record only from the act's own result. No public code, class, exit, fault cause or detail is added, and every refusal map stays exhaustive with no wildcard arm.

## The X8 cases (sixteen new files)

| Case | Misuse | Expected |
|---|---|---|
| `platform_request_identity_literal.rs` | `RequestIdentity { bytes: [0; 16] }` | E0451 "field `bytes` of struct `RequestIdentity` is private" |
| `platform_request_identity_{default, deserialize, from_bytes, from_text, clone}.rs` | `T: Default`, `serde_json::from_str::<T>`, `T: From<[u8; 16]>`, `T: FromStr`, `T: Clone` | E0277 "the trait bound `RequestIdentity: …` is not satisfied" |
| `platform_request_identity_serialize.rs` | `serde_json::to_string(&identity)` | E0277 "`RequestIdentity: serde::Serialize`" |
| `platform_reserved_execution_id_literal.rs` | a literal of both fields | E0451 "fields `bytes` and `rendered` of struct `ReservedExecutionId` are private" |
| `platform_reserved_execution_id_{default, deserialize, from_bytes, from_text, clone, serialize}.rs` | as for `RequestIdentity` | E0277, each naming `ReservedExecutionId` |
| `platform_reserved_execution_id_injected_absent.rs` (F, item 3a) | `use opensip_platform::crash_barrier::reserve_injected_execution_id` | E0432 "unresolved import `opensip_platform::crash_barrier`" |
| `security_commit_session_open_reserved.rs` (F) | `CommitSession::open(operation, reserved)` | E0061 "this function takes 1 argument but 2 arguments were supplied" |

Each has a compiling control (the draw, `reserve_execution_id()`, or a lawful probe type), and a row in `admission_tests.rs`'s case table (unit `J3a`). `RequestIdentity` and `ReservedExecutionId` are exported, so X8's export rule gives each the full capability set; `ExecutionIdReservations` is crate-private (only its two functions are public), so it has no row. `RequestIdentity` and `ReservedExecutionId` have no non-public inherent constructor; item 3a's census finds the one feature-only constructor, which gets the F row.

## Judgment calls

Each is the implementation agent's reading where the law leaves the code open; the lead rules on each before sending (none changes a public code, row, class, exit, subject or remedy).

1. **`enter_durable_analysis` is `pub(crate)`.** J1 item 3 names it and makes it the durable request's one security call, but J3a wires no caller: the pipeline that lends `&RequestIdentity` and calls it is J3d's. Exporting it now would export `DurableEntry`, `EntryRefusal` and `Created` with no consumer, and each would owe X8's capability rows. J3d exports what its host call needs, with those rows. Likewise `RequestAuthority::identity` is `pub(crate)` and marked `allow(dead_code)` until J3d calls it.
2. **The inject-id reservation lives in `crash_barrier`.** X3d r9 S10.1 requires F34's injected id to "still reach the attempt row's trigger" while the session holds a `ReservedExecutionId` on every path, so the injected id must be reserved, which needs a constructor from text. It exists only under the test-only feature, in the feature's own module, so a release build has none and X9-1's site list (`crash_matrix_sites.rs`) is unchanged. An injected id already reserved in the process is the host I/O row (as eight collisions are), and one outside the grammar is the invariant row (as before). **Rejected:** a `pub(crate)` constructor from bytes in every build (dead outside the matrix), and a new `cfg(feature = "crash-matrix")` site in `lib.rs` (a change to X9-1's pinned list).
3. **The probe runs on attempt A's ledger, with the actor's H.** J1 places it after attempt A's producers and before the route, as "one charged … walk". It is charged to attempt A, so on the steady state the sealed write receipt's ledger carries the walk; the gate's own walk still observes the account itself. A probe refusal is attempt A's latch and the walk's row.
4. **Attempt B's admission is `admit_ordinary_writer_after(CreatorActEnded)`.** X1 r2 item 7 says "exactly one `admit_ordinary_writer` runs on attempt B", and that the token is "consumed only by attempt B's allocation". `admit_ordinary_writer()` keeps its signature, because it stays the non-creator entry and the settlement sweep's source pin requires its no-argument call. The new function is X1 item 2's same composition (`admit_receipt`, shared), whose step 1 allocates slot B with the token.
5. **J-C2, J-C4b and J-C8 at J3a's boundary.** J3a emits no envelope, opens no render attempt and wires no commit. So:
   - J-C2 is proved in two halves: P0's `invocation.requestId` (and every `requestId` in I) is the lent identity's rendering (security), and the host registry's projection, which the envelope uses, renders the identity it lends (host). The envelope itself is J3d's.
   - J-C4b's "three distinct ExecutionIds" reserves the render attempt's id through the platform registry, as J3d's render step will.
   - J-C8 takes `LostRace` and `NotPristine` through attempt B and R4 to R12 on the real chain, to an open `CommitSession` with a reserved ExecutionId. The commit (storage's `prepare_commit` and `publish`) is J3d's end-to-end leg.
6. **`mint_intent`'s charge is unchanged.** `IDS_COST` was "two CSPRNG draws"; it now covers the lent RequestId's copy and the ExecutionId's draw and reservation, at the same cost, so no ledger figure moves.
7. **`CreationIntent::binding()` is the reserved ExecutionId.** Law 465 item 9 binds a parent preparation to "exactly this intent". The RequestId is now lent and shared by every intent of the invocation, so it no longer identifies an intent; the reserved ExecutionId is unique in the process. One existing test (`installation_parent_tests.rs`) compared the permit's RequestId with the binding; it now compares the permit's ExecutionId.
8. **Existing tests rewritten for S2.** 468c's routing tests asserted the withdrawn route (the creator's `InitialPlatform` lending the gate). They are replaced by the entry tests below (same scratch scenarios: published, not pristine, lost race, foreign entry, gate budget, no premise, rename not performed, development build), with `representative_refusals_choose_their_rows` unchanged. Every other test edit only adds the lent identity to `mint_intent` calls or reads `IntentInvocation.execution_id` through `as_str()`.


## Not settled by the law (for the lead, before sending)

1. **R10's trust-admission record names an ExecutionId that J1 does not assign.** X4T r9 item 7's `host-trust-admission` floor publication (and X4B's first acceptance) records an invocation `{requestId, executionId, stepId}`, which `begin_operation` takes as `TrustInvocation` (`crates/security/src/trust/live_observation.rs:57-99`, built from two `&str` ids). That record is written at R10, under the fence, before R12's `CommitSession::open` draws the analysis attempt's ExecutionId. J1 item 2 says who reserves which id (the prelude, the session, the ephemeral and render attempts) and forbids "an ExecutionId used by P0, a provider frame, a session or a record before its process reservation", but names no ExecutionId for this record. J3a wires no R10 and leaves `TrustInvocation` unchanged; today only tests build one.
   - **Recommendation:** a J1 record note (or J3d's request) fixing it as a host-drawn, reserved ExecutionId for the trust-admission operation, drawn at R10 through `reserve_execution_id()` and never bound to the analysis attempt (as the render id is), with the RequestId the lent identity's projection; and `TrustInvocation::new` taking `&RequestIdentity` and `&ReservedExecutionId` in the unit that wires R10 (J3d).
   - **Rejected:** the analysis attempt's id (R12 follows R10, and J1 item 7 fixes that order) and the prelude's (never reused, 464 r3 item 5).
2. **Descriptions.** No inventory description becomes false, but several now understate their files: `initial_installation.rs` ("the one pre-installation attempt per process"; nor does it mention the intent or the two-slot sequence), `custody/installation_routing.rs` (still describes 468 r5's route, not the durable entry), `read_premise.rs` (no `Producers` or attempt B), `commit_session.rs` (open's reservation), `crates/platform/src/crash_barrier.rs` (the inject-id reservation) and `installation_routing_tests.rs`. **Recommendation:** fold them into the next description-only contract successor batch, as X1b was planned. J3a writes none.



**Lead rulings (2026-10-04), both accepted.**

1. The trust-admission ExecutionId stays undecided here. J3a does not wire R10 and does not change `TrustInvocation`. The record note belongs to J1's next revision or to J3d, as the recommendation says: a host-drawn reserved ExecutionId for that operation, not the analysis attempt's id and not the prelude's.
2. The understated descriptions stay inherited. The next description-only successor carries them. J3a writes no description successor.

## Not claimed

- No command wired and no host call of the entry (J1 item 1; J3d). No envelope, `retentionDisclosure` or `backupStatus` emitter (J-BS, J3d). No render or ephemeral attempt draw site (J3d, J2c). No R4 to R12 wiring beyond the tests' own composition (J3d).
- J3b's latch, window bits, `Operator`, `refused()` uses and S12 rows; X4-F3's sources are untouched.
- J-C3 (provider frames, M3-L's), J-C10 onwards (J3d's).
- A durable RequestId or ExecutionId registry (J1 item 2's stated limit): across processes, uniqueness rests on the 128-bit draw until an attempt row reserves an id durably.
- Linux: the durable entry is macOS-only, as the creator and gate it composes. The platform registry builds everywhere.

## Inventory v139

- **Candidate:** `m2/repository-file-inventory.v139.json`, 583181 bytes, `f3bf66a6584e4fd41cef228aee9062c97ff670228c5f919c27ccd4762ad3061c`. **Parent:** v138 (`m2/repository-file-inventory.v138.json`, 571539 bytes, `90d5b09c…`), which the lock at `b7b87b7` selects. **Record:** `m2/durable-entry-j3a-inventory-v139/successor.json`, 309837 bytes, `d7f57cc0caef2b2e8b5c1c69569773b6ab587771d036e7c0488dfe4bc843083e`. **Subject:** `m2/durable-entry-j3a-inventory-v139-subject.json`, 2556 bytes, `eb4b6f2f459d29f6ea8796baa381795923b00968dc62b64b59b282b3b5c4dac5`.
- Sixteen rows added, all `opensip-host` fixtures (the cases above); 995 inherited rows equal by value; packages, edges, pending decisions and carried obligations unchanged; seventeen planned rows change bytes and keep true descriptions (`plannedRowsChanged`; see "Not settled" item 2). Projection: the 103 inheritance rows re-parented, 84 selectors moved, no direct override or supersession on v138.
- **Staged lock.** The worktree's `design-lock.json` is HEAD's plus the v139 entry (`stage_lock_j3a.py`) with the 103 rows re-parented, in canonical formatting: 521422 bytes, `e9d8fc07acf4e447589d358919c376994f9302991e329e5d9b69620e15b70372`. Its review and assent pins are the `SCRATCH-J3A/` placeholders whose bytes `verify_scratch.py` serves. At integration the lead replaces exactly those two pins, then runs plain `verify_design`.
- **Order.** E2s may also stage an inventory successor. If it stages v139 first, this candidate is rebuilt as v140 on it (with its record, subject, staged lock and this review's pins); the lead re-sends it for a rebase-only recheck.
- `design-lock.json` stays outside the unit's `sourceBoundary`, as in every inventory unit; the diff sha covers it.

## Lead results

Recorded from `evidence/lanes-summary.txt` and the lane logs copied beside it. The worktree was `b7b87b7` before and after. `~/Library/Application Support/OpenSIP` was absent before and after. No source byte changed after these lanes. The sixteen case files were untracked during the lanes (cargo compiled them from the tree) and are intent-to-add now, so the subject diff includes them.

- **fmt** exit 0. The log is empty, which is `cargo fmt --check` with nothing to print.
- **builds** exit 0: workspace, crash-matrix feature, scenario-fixtures, and the security feature build.
- **clippy `-D warnings`** exit 0 on those three lanes.
- **new tests** exit 0: 35 passed, 0 failed, 4 binaries.
- **workspace tests, twice:** each run 1805 passed, 0 failed, 3 ignored, 20 binaries.
- **doc tests:** 20 passed, 0 failed, 12 binaries.
- **crash-matrix feature lane:** 1703 passed, 0 failed, 3 ignored, 10 binaries.
- **drift** exit 0, `changed: []`, 40 sources, 8 outputs.
- **verify_scratch** staged exit 0 (inventory successors 98 to 99, v139 selected). **Plain verify_design** on the staged lock exit 1 with `missing or escaping regular file: SCRATCH-J3A/review.json` (expected). Plain verify_design on HEAD's lock exit 0.
- **verify_projection** exit 0: 103 rows, positive PASS, 518 corruptions refused.
- **package edges, dependency checkers and their tests** exit 0.
- **X9 lead sets were not run.** J1 r6 item 12 runs both sets on the integration commit that touches `crates/security`, and M3-PLAN r10's row is "J3a, then its lead set." They are not part of this review. The lead runs them, unniced, under the lane lock, before integrating. `evidence/x9/` is empty on purpose.


## Decide

- **Law:** does J3a implement J1 r6 items 2 and 3 exactly, with S2 to S7 and S10.1: one RequestId per invocation, lent and recorded; every ExecutionId J3a's code draws reserved in the drawing step, never released; the entry's four steps in order; the probe selecting a route and nothing else; the creator act ending attempt A and entering no gate; attempt B only through the token; the value-only `created` record from the act's own result (LD6-1)?
- **Types:** can a `RequestIdentity` or `ReservedExecutionId` be made other than by the draw and the registry on the plain surface? Can anything of attempt A reach attempt B? Can a third attempt or a second gate be reached?
- **Tests:** do the tests cover J-C2, J-C4, J-C4b and J-C5 to J-C9 with J-C6b as J1 states them, within judgment call 5's reading?
- **Existing behaviour:** do the rewritten routing tests, the changed `mint_intent` and the `binding()` change (calls 7 and 8) keep every accepted outcome of 464 to 468, X1 and X3d?
- **X9:** the lead sets are not in this round (see Lead results). Do not treat their absence as a finding. From the diff alone, does any crash-matrix expected value, site list or required-run row move?
- **Judgment calls:** are calls 1 to 8 acceptable? Answer calls 2 and 5 directly.
- **Inventory v139:** pin it, and assess it as an inventory candidate.

Write REVIEW.md and review.json under the output directory.

review.json needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `76c7f540cc5c0a06d8f249b51c4c6e38c24ab4ecab704a365ab1c866b6d5c171`, the diff's sha256, as a single string;
- "subjectManifestSha256": `eb4b6f2f459d29f6ea8796baa381795923b00968dc62b64b59b282b3b5c4dac5`, as a single string;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent (v138's pin), and successorRecord (the pin of `durable-entry-j3a-inventory-v139/successor.json`).

Do not commit.
