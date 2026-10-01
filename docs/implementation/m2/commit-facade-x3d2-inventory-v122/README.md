# Commit facade storage inventory122

Adds exactly twenty-one files to inventory119 (unit X3d-1, selected at product 7be09a7, where contract successor D1 is bound on it):
- crates/storage/src/commit_tests.rs
- crates/storage/src/schema_sources.rs
- nineteen `crates/host/tests/refusal/cases/storage_*.rs` compile-fail fixtures (law X8 r3 item 3's owner rows for this unit; the full list is the successor record's `addedFiles`)

`crates/storage/src/commit.rs` is not added. It is already a planned row of the parent ("Require evaluator ReplayedRun and security CommitSession; bind immutable target/inventory, publish verified objects, then coordinate SEAL/ledger barriers and private recovery association before producing PublishedCommit. …"), and that description stays true, so the row is kept by value.

It keeps all 897 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 918 planned files.

**The storage → evaluator edge.** The parent already declares `opensip-storage` → `opensip-evaluator` (the build plan's source graph, line 34; recorded since inventory89, as Grok's X3d r1 review notes). This unit adds the edge to `crates/storage/Cargo.toml` and `Cargo.lock`, so the declared graph is unchanged and `check_package_edges --lane host` passes against both inventory119 and inventory122, with 20 declared and 20 resolved edges.

The rows are unit X3d-2: law X3d r6 items 1, 3, 4, 6, 8 and 9, and item 13's X3d-2 list. That covers:
- `prepare_commit` (items 3 and 8);
- `PreparedCommit::publish`;
- the private adapter implementation;
- `PublishedCommit`;
- the `storage → evaluator` edge.

They also carry law X9 r1 item 5's `x3d.publish.published` point, and law X8 r3 item 3's rows for this unit: groups A to E, G and H for `prepare_commit`, `PreparedCommit` and `PublishedCommit`, and item 3b's adapter source pin.

- **commit_tests.rs (test).** It is included under `commit.rs`'s `cfg(test)` module. Storage cannot build a `CommitSession`, so it runs the very functions `prepare_commit` and `publish` compose, without a session. It uses a scratch private `I/stores/S` and the evaluator's real replay of the corpus Run that security's SEAL tests replay.
- **schema_sources.rs (adapter).** It is storage's embedded copy of the registry's pinned schema sources. The staging owners need the selected registry. The public `prepare_commit` takes no registry (group H's arity), and storage cannot reach host's copy.
- **The nineteen `refusal/cases` files (fixture).** These are law X8 r3 item 3's owner rows. Only X8a's driver compiles them, against the plain `cargo check -p opensip-host` surface. In each, the control compiles and the misuse fails with exactly one error, carrying the annotated code, fragment and line.
  - **Group A** (E0308): a raw `JsonValue`, and the generated contracts `Identity3Run`, in place of `ReplayedRun` at `prepare_commit`.
  - **Group B:** `prepare_commit(true, session)` (E0308), and `PublishedCommit { verified: true }` (E0560).
  - **Group C** (E0308): the inert `RetainedInputs` at `prepare_commit`.
  - **Groups D, E and G**, for each of `PreparedCommit` and `PublishedCommit`: a literal (no code, "private fields"), `Default`, `Deserialize`, `Clone` and `Serialize` (E0277 each).
  - **Group E reuse** (E0382): `prepare_commit` with a consumed session, and `publish` twice.
  - **Group H** (E0061): `prepared.publish(adapter)`, and `prepare_commit(run, session, outcome)`.
  - **Item 3a's census:** neither type has a non-public inherent function or a `cfg(test)` producer, so no group F case is owed.

**Changes to existing rows.** Every row stays by value. Where D1 overrides a row, the text judged here is D1's effective description, which this successor projects. Descriptions marked "out of date" are left for the next description-only successor, as earlier units left theirs.
- `crates/storage/Cargo.toml`: declares `opensip-evaluator`. The description stays true.
- `Cargo.lock`: storage's dependency list gains `opensip-evaluator`. The description stays true.
- `crates/storage/src/lib.rs`: declares `commit` and `schema_sources` (macOS), and exports `prepare_commit`, `PreparedCommit`, `PublishedCommit`, `CommitOutcome` and `NotPrepared`. The description ("the guarded commit facade") is now true.
- `crates/storage/src/ledger_store.rs`: re-exports X3c's location, ledger, attempt and object owners to `crate::commit`. It also gains `WriteTransaction::next_commit_sequence`, the one counter accessor. That accessor orders the stored canonical decimal text by length and then bytes, decodes the result exactly, and returns the next value, starting at 1. The description stays true.
- `crates/storage/src/recovery.rs`: `DecimalCounter::parse_text`, the exact decoder for that accessor. The description stays true.
- `crates/storage/src/ledger_store/project_ledger.rs`: the production `ProjectStoreLocation::selected` and the re-exports of its child module. D1's effective description ends "Only tests construct a location.", which is out of date: X3d-2 is the production constructor that X3c-1 named.
- `crates/storage/src/ledger_store/project_commit.rs`: `attempt_and_objects_cost`, `PreparedLedger::next_commit_sequence`, and `h_digest`.
  - The staging join now holds the published set to the inventory's blob digests and its typed objects' H digests (judgment call 5).
  - The description's "the Run material whose blob digests must equal the published objects exactly" is out of date.
- `crates/storage/src/ledger_store/recovery_material.rs`: `stage_run_material` returns the inventory's typed objects as well as its blobs. D1's effective description, "returning the inventory's blob digests", is out of date.
- `crates/security/src/custody/commit_session.rs`: two read-only hooks for X3d-2, `CommitSession::project_id` and `CommitSession::store_root`, with the exported `StoreRoot` (judgment calls 2 and 3). The description does not mention them.
- `crates/security/src/custody/operation_handoff.rs`: the free function `open_store_root`, which `store_root` calls (no new inherent function on `ProjectOperation`). D1's effective description does not mention it.
- `crates/security/src/custody/commit_session_tests.rs`: one test of the two hooks. The description's list does not name it.
- `crates/security/src/lib.rs`: re-exports `StoreRoot`. The description stays true.
- `crates/host/tests/admission_tests.rs` (X8a's driver): the nineteen owner rows in the census, and law X8 r3 item 3b's adapter source pin with its self-check. D1's effective description lists the census rows by unit up to X3d-1 and the scenario-fixtures pin; it is out of date by X3d-2's rows and the adapter pin.

**Order.** This successor's parent is the inventory the real product lock selects: inventory119 (unit X3d-1) at product 7be09a7. X4B-b (no inventory) landed at 8240856 after X3d-1, and 7be09a7 binds contract successor D1 on inventory119 (a lock entry only). The unit was written on 5f4395d, moved to 8240856 before any edit, and moved to 7be09a7 before review; its product diff applies unchanged, and only this successor's projection changed. No earlier candidate was reviewed. The lead assigned the number 122; it sits above inventory118 (X9-1, in flight). Succession is by the lock's parent pin, not by number.

`evidence/build_v122.py` reads the parent from the lock. Its PRIOR table maps inventory119 to the successor record that bound its sixteen rows. It writes only its own two paths, refuses to write over any path git already tracks, and refuses while a lock selects inventory122. Reruns reproduce the same bytes.

**Projection.** Fifty-five effective description overrides stay bound by stable file path, with parent inventory119, as 461b's joined at inventory81 (D1's README, "After selection"):
- the sixteen bound to inventory119, carried unchanged from inventory113 and inventory116 back to inventory81;
- D1's thirty-nine overrides on inventory119, each with D1's selector as its parent selector and D1's after text as its effective description.

The inherited rows themselves stay equal by value to inventory119's bytes, because an inventory successor carries rows by value. `build_v122.py` refuses unless D1 is bound in the lock, each override's parent is inventory119 and its before text equals the parent's row. `verify_projection.py` is inventory119's helper with its row count raised from 16 to 55 and its comment corrected; it gathers D1's overrides from the lock's contract successors. It runs against the real lock at 7be09a7: 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` appends inventory122 in memory over the worktree's lock (7be09a7, D1 bound) and replaces the lock's sixteen inheritance rows with the record's fifty-five, with a synthetic review and assent. It reads the architecture checkout at its fixed path and writes nothing.
