Codex review: unit J4a r1, the shared primitives of the resume/repair writer and their X3c and X3b uses. It implements accepted law J-RW r4 (your `m3/reviews/codex-resume-repair-jrw-r4/`, ACCEPT) item 11's J4a row, through its accepted successors X3c r9 (RW-S3) and X3b r11 (RW-S4) (CODEX2's `m2/reviews/codex2-jrw-successors-r1/`, both ACCEPT). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the diff. This is a product code unit. It adds no file, so it has no inventory successor and no design selection, as for X4-F2.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-j4a-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Five implementation agents share this machine. Take the lane lock before any cargo run and release it straight after: `LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"; mkdir "$LOCK"` (wait while it exists), then `rmdir "$LOCK"`.
- Don't run a crash-matrix run set. None is needed (see "X9").
- Run every command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and cargo `--locked --offline`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Law

All pins are in `hashes.txt`. Each law is pinned by its accepted snapshot.
- **J-RW r4**, `m3/resume-repair-jrw/PROPOSAL-r4.md` (118261 bytes, `9c53bce7…`, your r4 `subjectSha256`). The parts J4a implements:
  - **Item 11's J4a row (:662):** "The shared primitives: C-ACL over P-ACL in `security::private_access`, used through `store_custody`, and C-SUFFIX over P-PREFIX. Their X3c and X3b uses: the store directories (RW-P1), the length-0 ledger file (RW-P2), and `trust/carrier-floors/` (RW-P3). Also the typed completion result these uses return, and `host.repair.completed` once O1 has landed (item 7). Tests RW-C1, C2, C3, C6, C7, C10 and C12 for these states."
  - **Item 2 (:163-176):** where and under which lock: RW-P1 and RW-P2 inside `prepare_commit` at `admit_layout`, under the namespace writer lease; RW-P3 at R10, X3b's floor step, under the fence. Never on a read path, never in the crashed process.
  - **Item 3's principle (:211-217), 3.1 C-ACL over P-ACL (:219-240), 3.2 C-SUFFIX over P-PREFIX (:242-250).**
  - **Item 4's rows RW-P1 to RW-P3 (:430-432)** and **item 5's N-P1 and N-P2 (:455-456).**
  - **Item 6 (CR-1 to CR-6), item 7 (:486-501), item 8 (:503-514), item 9's RW-C1, C2, C3, C6, C7, C10, C12 (:519-542), item 10's scope names (:639-646)** and the **forbidden substitutes (:744-761).**
- **X3c r9**, `m2/ledger-blob-x3c/PROPOSAL-r9.md` (81248 bytes, `46156e8e…`): item 1's C-ACL for the store directories (:107-116), item 2's length-0 file (:127-128), item 10's rows (:291), item 12a's J4a tests (:300-301), item 13's J4a (:331-334).
- **X3b r11**, `m2/journal-x3b/PROPOSAL-r11.md` (73641 bytes, `27ed0aaf…`): LD11-1 (:34-35), item 2's C-ACL for `trust/carrier-floors/` (:61-68), item 12's J4a (:364).
- **Not J4a's** (only the seams the law names are left): L-UNC and C-LEDGER (J4c), registration (J4b), C-TRUST and C-TDIR (J4d), the X9 rows, J4's census and release absence for the `.repair` names (J4e), and `host.repair.completed` (O1, not landed).

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-j4a`, detached at product main `d2c00a9d…` (SD-7). Nothing is committed or staged, and no file is added, removed or renamed.
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-j4a diff d2c00a9` is 125557 bytes, sha256 `4fbe89f1684846c70f1da639549669a31ee98775e526760f65bfcdede69f8bda`, 11 files, +2567 −42. A copy is at `evidence/j4a.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, generator `~/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator`, Node `~/.nvm/versions/node/v24.16.0/bin/node`.
- **Evidence:** `evidence/` here, every file pinned in `hashes.txt`: `lanes.sh` (as run, but for its drift step's interpreter; it names the lead's scratch paths) and `drift-rerun.sh`, `lanes-summary.txt`, `results.py` and its `results.json`, `j4a.diff`, `parallel-files.txt` (the parallel worktrees' changed files) and `x9-rows.txt` (the required runs J4a's behaviour moves).

## What J4a changes

| File | Change |
|---|---|
| `crates/security/src/private_access.rs` | The shared primitives: P-ACL's judgments and C-ACL; P-PREFIX's judgment and C-SUFFIX; `RepairCompletion`, item 7's record. Their tests (RW-C6, C7, C10, C12 on the primitives). |
| `crates/security/src/store_custody.rs` | RW-P1 in `create_or_admit_store_directory`; RW-P2 in the new write-path `admit_or_complete_store_file`. `StoreDirectoryDisposition::Completed`, `StoreFileAdmission`. A new `cfg(test)` module (RW-C1, C2, C3, C6, C12 at the step). |
| `crates/security/src/journal_store/carrier_floor.rs` | RW-P3 at the floor step (`admit_floor_directory`), and `floor_step_completing`, which returns the completion. `floor_step` and `floor_step_observed` keep their signatures. |
| `crates/security/src/journal_store/carrier_operation.rs` | `OperationFloor` carries the floor step's completion (`completion()`). |
| `crates/security/src/journal_store/carrier_floor_tests.rs` | RW-P3's tests (RW-C1, C2, C3, C6, C12). |
| `crates/security/src/lib.rs` | Re-exports `RepairCompletion`, `StoreFileAdmission` and `admit_or_complete_store_file`. |
| `crates/storage/src/ledger_store/project_ledger.rs` | The X3c uses: `create_or_open_ledger` calls `admit_or_complete_store_file` with RW-P2's own clause (no `-wal`); `ObjectDirectory::dispositions()` and `AdmittedLedger::completion()` return the typed results. |
| `crates/storage/src/ledger_store/project_ledger_tests.rs` | RW-P1's and RW-P2's tests through the X3c steps (RW-C1, C2, C3). |
| `crates/platform/src/filesystem/file_effects.rs` (+ `filesystem.rs`, `lib.rs` re-exports) | `write_regular_suffix_accounted` / `_reserved` / `_cost`: C-SUFFIX's positioned write of the missing suffix, with `write_new_regular`'s verification (shared through a private `verify_written`, which `write_new_regular_charged` now calls; its behaviour is unchanged). A platform test. |

Nothing else changes. No crate gains a dependency or a feature. No `cfg(feature …)` site, clock sample, public code, row, detail, subject or envelope member is added.

### The primitives (`private_access.rs`)

- **P-ACL, judged before any effect** (`judge_private_directory_creation`, `judge_private_file_creation`). Each takes exactly the ordinary private judgment's one sample first (`observe_private_directory`'s, or `open_store_file`'s), so an object judged private, or refused for any reason but an omitted ACL, ends exactly as it does today (`CreationJudgment::Private`, or that refusal). For an omitted ACL (`CapturedAclState::NotReturned` only; a NOACL sentinel or a present ACL is not omission), P-ACL's other clauses follow, through the owner's retained parent, no-follow and charged:
  1. the parent's device is the object's (one charged status read), and the descriptor's native name is the fixed name (`descriptor_name_matches_accounted`);
  2. owned by the invoking user, mode exactly `0700` or `0600`, and one link for a file (`private_shape`, on the same sample);
  4. a directory holds no entry but `.` and `..` (one charged `visit_entry_names(3, …)` scan); a file has length 0.

  Any clause that fails keeps today's refusal (`Access(AclNotReturned)`), with nothing written. A native failure while observing a clause leaves it unproven, so it keeps that refusal too; a budget refusal stays the budget row. Only when every clause holds is the result `CreationJudgment::Prefix(CreationPrefix)`, a token bound to the judged handle, not Clone.
- **C-ACL** (`complete_private_creation`) consumes the token and is exactly the fresh path's own step, `prepare_fresh_private_sample`: sample, append one zero-rights owner allow, sample, judge private; its sample, append and sample are reserved before the append, as that step reserves them. No mode bit, other ACE, name or byte changes.
- **P-PREFIX** (`judge_private_prefix`), for J4b's marker and J4d's leaves: the private judgment's sample, then one bounded, charged read of at most `expected.len() + 1` bytes from offset zero (`read_bounded_observed` over a positioned reader), whose length must equal the sampled size. A private file holding exactly `expected` is `Equal`, the ordinary admission, with no clause added. A private strict prefix (the empty one included) at the fixed name on the parent's filesystem is `Prefix`; any other private file is `Neither`, for the owner's own row. An omitted ACL is `Prefix` only with clause 2, clause 1 and a strict prefix; otherwise it keeps today's refusal.
- **C-SUFFIX** (`complete_private_suffix`) consumes `SuffixPrefix` and reserves its whole cost (`suffix_cost`) before the first effect. C-ACL first when the ACL was omitted. Then only `expected[existing..]` is written at offset `existing` (platform `write_regular_suffix_reserved`, a `write` primitive point), every byte read back through the judged handle and equal, nothing after it, `F_FULLFSYNC`; the parent's directory barrier; and a no-follow reopen of the name whose device and inode are the written file's and whose length is exactly `expected`'s. No existing byte is rewritten; nothing is truncated or removed.
- **`RepairCompletion`** is item 7's record: `kind()` gives the closed code (`store-directory`, `ledger-file`, `carrier-floors`) and `state()` the item 4 state (`RW-P1` to `RW-P3`). J4b to J4d add their own values.

### The uses

- **RW-P1** (`store_custody::create_or_admit_store_directory`). Only on a raw `EEXIST`, after the no-follow open, the judgment replaces `observe_private_directory`. On `Prefix`: C-ACL, then the step's unchanged remaining steps (`finish_store_directory`: exact name, parent's filesystem, own barrier, parent's barrier), all inside `crash_scope!("repair", …)`, and the disposition is `Completed`. `Created` and `Admitted` run exactly as before. The caller's scopes make the completion's names `x3c.ledger-create.projects.repair`, `x3c.ledger-create.namespace.repair`, `x3c.object.objects.repair` and `x3c.object.sha256.repair` (judgment call 2).
- **RW-P2** (`store_custody::admit_or_complete_store_file`, the write path's `open_store_file`). The same no-follow open and judgment as `open_store_file`. On `Prefix`, the owner's own clause (`resumable`) is observed, and only if it holds does C-ACL run, in `crash_scope!("repair", …)` (`x3c.ledger-create.repair`). `project_ledger::create_or_open_ledger` passes RW-P2's clause, "no `ledger.sqlite-wal`" (judgment call 3). The resumable-empty path then runs unchanged, with disposition `Resumed`, as X3c r9 item 2 says; `AdmittedLedger::completion()` is `Some(LedgerFile)`. The read paths (X6's `recover`, the sweep) keep `open_store_file`, which completes nothing.
- **RW-P3** (`carrier_floor::admit_floor_directory`, in `floor_step_completing`). Where `observe_private_directory` judged the existing `trust/carrier-floors/`: after the busy probe and the carrier classification, before the floor is read (LD11-1). On `Prefix`: C-ACL, then exact name, `trust`'s filesystem, its own barrier and `trust`'s, all in `x3b.floor.directory.repair`. A busy probe returns before it, so a skip writes nothing. Every other state keeps the host I/O row. `OperationFloor::completion()` carries it to the handoff.
- **The typed result** (judgment call 5): `StoreDirectoryDisposition::Completed` with `completion()`; `NamespaceDirectory::dispositions()` (unchanged) and the new `ObjectDirectory::dispositions()`; `StoreFileAdmission::Completed` and `AdmittedLedger::completion()`; `FloorStep::completion` and `OperationFloor::completion()`. **No event is emitted:** O1 has not landed (item 7, "A J4 unit that integrates before O1 returns the completion in its typed result only").

## Controls (J-RW r4 item 9), by test

All run in the ordinary workspace lanes on scratch directories under the per-process scratch parent, with no production seam. Each crash state is made by the owner's own primitive stopped before its owner allow: the platform's `create_exclusive_directory_accounted` (`mkdirat 0700`, `fchmod`) or `create_exclusive_regular_accounted` (exclusive `0600` create), exactly what the step calls before `prepare_fresh_private_sample`.

| Control | RW-P1 (store directories) | RW-P2 (length-0 ledger) | RW-P3 (`carrier-floors`) | Primitives |
|---|---|---|---|---|
| **RW-C1**, each state completes to its terminal state with only the owner's own step effects | storage `each_crashed_store_directory_completes_to_the_fresh_layout` (each of the four names; the layout then equals a fresh layout's names, modes and ACLs, and the directory keeps its inode and mode); security `a_crashed_store_directory_is_completed_then_admitted` | storage `a_crashed_ledger_file_completes_to_the_selected_schema` (`Resumed`, the selected schema, same inode); security `a_crashed_length_zero_store_file_is_completed_only_when_resumable` | security `a_crashed_carrier_floors_directory_is_completed_by_the_floor_step` (INIT floor written, the floor directory's names and the floor bytes equal a fresh step's; `OperationFloor` carries it) | |
| **RW-C2**, each neighbour keeps today's row and subject, writes nothing | storage `the_store_states_neighbours_keep_their_rows_and_are_unchanged` (non-empty `objects/`, RW-N6's state; `projects/` at `0750`); security `every_other_existing_store_directory_keeps_its_refusal` (non-empty, `0750`, a present ACL, another user, a link, a file) | storage, same test (a `-wal` beside it, a byte, a second link: `Custody("private")`); security `every_other_existing_store_file_keeps_its_refusal` (the owner's clause never consulted; `open_store_file` completes nothing). The private length-0 file with a `-wal` stays `LEDGER.CORRUPT` (`every_other_creation_footprint_is_ledger_corrupt`, unchanged) | security `the_floor_steps_neighbours_keep_their_rows_and_are_unchanged` (an entry inside, `0750`: the host I/O row; a busy probe: skipped, nothing completed; a format-2 carrier: refused by classification first) | |
| **RW-C3**, idempotence | the four-name test reruns the layout: all `Admitted`, ledger `Existing`, no completion, same tree | the second `create_or_open_ledger` is `Existing`, completion `None` | the next floor step is `Unchanged`, completion `None` | `c_acl_completes_exactly_a_crashed_private_directory_once` |
| **RW-C6**, each P-ACL clause negated refuses on today's row; exactly one zero-rights owner allow, no mode bit changed | security step tests above (one zero-rights allow for the user; mode and inode unchanged) | as for RW-P1 | as for RW-P1 | `p_acl_shape_needs_an_omitted_acl_and_the_fresh_paths_exact_shape` (clauses 2 and 3, the NOACL sentinel included); `every_negated_p_acl_clause_keeps_the_refusal_and_writes_nothing` (clause 4, mode, owner, the name and another filesystem (`/dev`'s devfs) for clause 1, a present foreign ACL); `c_acl_completes_exactly_a_crashed_length_zero_file` (name, filesystem, owner, length, mode, link count) |
| **RW-C7**, P-PREFIX and C-SUFFIX | — | — | — | `c_suffix_writes_only_the_missing_bytes_of_a_strict_prefix` (private torn and empty prefixes, an ACL-omitted zero-length file with C-ACL first; inode and prefix unchanged; equal is the ordinary admission; other, longer, wrong-name and ACL-omitted non-prefix files refuse unchanged); platform `charged_suffix_write_adds_only_the_missing_bytes_and_verifies_all` |
| **RW-C10**, census and `.repair` scopes | see "Crash points" | | | `every_completion_runs_inside_a_repair_scope` |
| **RW-C12**, an unreservable completion refuses before its first effect | security `an_unreservable_store_directory_completion_writes_nothing` | security `an_unreservable_store_file_completion_writes_nothing` | security `an_unreservable_carrier_floors_completion_writes_nothing` | `an_unreservable_c_acl_refuses_before_its_append` (one edge short refuses, the ACL stays omitted; exactly the reservation suffices); `an_unreservable_c_suffix_writes_nothing` |

**How RW-C12's limits are set at the step.** A first scratch runs the step unlimited and records `used()`. A second, identical scratch runs it with a ledger whose edges are `used − tail − 1`, where `tail` is the work the step charges after C-ACL's reservation: for a store directory the name sample and two barriers, for the store file nothing, for `carrier-floors` the name sample and two barriers. Everything before the reservation fits, and the reservation does not.

**Existing tests that must not move,** all unchanged and passing in the lanes below: X3c-1's `project_ledger_tests` (directories created then admitted; a `0755` directory, a link and a file at a directory name refused unchanged; ledger creation; the empty private file resumed; `every_other_creation_footprint_is_ledger_corrupt`, including N-P2; a `0644` ledger refused on the custody row), X3b-1a's `carrier_floor_tests` (a `0777` floor directory under `classification_wins_over_a_malformed_or_unreadable_floor`), the private-access tests (`fresh_private_file_gains_a_zero_allow_and_a_loose_file_is_not_rewritten`, whose loose, foreign-ACL and budget cases stay unchanged), platform's `write_new_regular` tests over the refactored verification, and the two census pins in the crash-matrix feature lane.

**RW-C1's terminal state.** J4a's tests run the owner's steps to the state each step owns: the admitted layout and created ledger (X3c), the written INIT floor and created carrier (X3b). "Committed" through `prepare_commit` and `publish` is RW-F00's R2 cell, which J4e's rows check end to end (J-RW item 10).

## Crash points, the census and X9

- **New points.** J4a adds one primitive point site, the `write` around platform's `write_regular_suffix_*` (C-SUFFIX only, which J4a does not yet use). Every other point a completion reaches is an existing primitive's (`directory-barrier`), reached only inside a `.repair` scope. J4a adds no `crash_barrier!` protocol point, no registered scope and no scope-registry line: `repair` is a relative component (`crash_barrier::resolve_scope`).
- **RW-C10's two clauses.**
  - *The lawful first commit's census is unchanged.* On every path that is not a completion, the code reaches the same primitives in the same order as at `d2c00a9`: `Created` and `Admitted` run the old code, the judgment's extra observations run only for an omitted ACL, and they are reads, not points. Security's `the_integrated_path_reaches_only_scoped_points_and_its_census_is_pinned` and storage's `the_ledger_path_reaches_only_scoped_points_and_its_census_is_pinned` pass unchanged in the crash-matrix feature lane.
  - *Every new durability point lies under a `.repair` scope.* `every_completion_runs_inside_a_repair_scope` reads every product source under `crates/*/src` (test modules and `*_tests.rs` excluded, comments stripped) and asserts that every call of `complete_private_creation` and `complete_private_suffix` lies inside a `crash_scope!("repair", { … })` block, that the suffix write is called only by C-SUFFIX, and that the call sites are exactly J4a's three (J4b and J4d extend the list by name). The completed paths' barriers are inside those blocks.
  - *Release absence of the new names, and J4's census of its own driver runs,* are J4e's (J-RW item 10, item 11's J4e row). `repair` never reaches a release binary: `crash_scope!` expands to its block without the feature.
- **The X9 rows that J4a's behaviour moves.** `evidence/x9-rows.txt` lists them. Six storage F00 rows kill at exactly RW-P1's, RW-P2's and RW-P3's points, and their transcribed R2 (and, for the five `x3c.*` rows, R1 and R4) are today's refusals: `kill-x3c-ledger-create-projects-create-after-1`, `-namespace-`, `kill-x3c-object-objects-create-after-1`, `-sha256-`, `kill-x3c-ledger-create-create-after-1` (`not-prepared:Refused(Custody { subject: "private" })`) and `kill-x3b-floor-directory-create-after-1` (`operation:HostIo`). After J4a, R2 completes the state instead. J-RW item 10's RW-F00 re-transcribes exactly these cells, and RW-K4, K5 and K7 add the crash-during-repair ladders: both are J4e's. J4a changes no `required-runs.v1.json`, X9 harness source or checker, and runs no set (judgment call 9). Host's required runs have no such row.

## Judgment calls

The lead accepts each as a lead decision (2026-10-04). Calls 1 to 4 are where a reviewer could most reasonably differ.

1. **Files.** J4a edits `crates/storage/src/ledger_store/project_ledger.rs` (its imports, `ObjectDirectory`, `admit_object_directory`, `AdmittedLedger` and `create_or_open_ledger_scoped`'s `Exists` arm) and appends to `project_ledger_tests.rs`, inside `ledger_store/`, where the parallel unit X3c-3 works. X3c r9 item 13 names X3c-3's files (`project_commit.rs`, `ledger_store.rs`, `recovery_material.rs`, doc comments in `commit.rs`, and their tests); `project_ledger.rs` is not among them, and X3c-3's worktree has not touched either file (`evidence/parallel-files.txt`). RW-P2 needs `project_ledger.rs`: its owner clause (no `-wal`) and its typed result live there, and the read paths' `open_store_file` must not complete. The hunks are disjoint from X3c-3's. The lead integrates in acceptance order.
2. **Scope names (item 10).** The law gives examples that follow two patterns: `x2.fence.register.repair.namespace` inserts `repair` after the protocol, while `x3b.floor.directory.repair` and `x4t.floor-publication.dependency.repair` append it to the completing step's scope. J4a uses one rule: `repair` is the innermost component of the completing step's scope (`crash_scope!("repair", …)` inside the owner's own scope). That gives `x3b.floor.directory.repair` and `x3c.ledger-create.repair` exactly as listed, and `x3c.ledger-create.projects.repair`, `x3c.ledger-create.namespace.repair`, `x3c.object.objects.repair` and `x3c.object.sha256.repair` for the four store directories, where the law lists `x3c.ledger-create.repair/…` and `x3c.object.repair/…`. The shared step does not know its caller's scope, so the insert-after-protocol form would need a scope argument at four call sites in `project_ledger.rs`. X9 r17's §RW scope table (J4e) records the exact names. **Question:** do you accept these four names, or do you require `x3c.ledger-create.repair.projects` and so on?
3. **RW-P2 with a `-wal` beside it.** J-RW defines RW-P2 as "length 0, ACL omitted, no `-wal`" and keeps every other state on today's row (item 5); X3c r9 item 2 says "With a `-wal` beside it, the file stays `LEDGER.CORRUPT` (JRW N-P2)". An ACL-omitted length-0 file with a `-wal` is refused today on the custody row, before the `-wal` is looked at. J4a checks the owner's clause before C-ACL, so that state appends nothing and keeps `Custody("private")`; N-P2 itself (a private length-0 file with a `-wal`) stays `LEDGER.CORRUPT`, unchanged. **Rejected:** C-ACL first, then `LEDGER.CORRUPT`: it would append an ACE to a state that is not a crash prefix and change its row. **Question:** do you agree X3c r9's sentence describes N-P2, not this state?
4. **Budget (item 8; X3c r9 item 1; X3b r11).** C-ACL reserves exactly what the fresh path's step reserves before its append (the sample, the append and the sample), "as the owner's own step does"; the step's remaining steps (name, filesystem, barriers) are charged as they run, as on the fresh path. The P-ACL observations are charged before they run. C-SUFFIX, which has no fresh-path twin, reserves its whole cost before its first effect. A budget refusal is always the budget row; an unreservable C-ACL appends nothing (RW-C12).
5. **The typed result.** Each use returns its completion in the owner's own result (above), and `RepairCompletion` carries item 7's `kind` and `state` codes, so J4e can name completions from typed results and O1 can emit the event without new fields. J4a does not thread them further (through `commit.rs`'s `Layout`, `prepare_commit` or `ProjectOperation`): J4e "joins every unit's typed completion result".
6. **P-ACL observation failures.** A native failure while observing clause 1 or 4 leaves the clause unproven, so the object keeps today's refusal (`Access(AclNotReturned)`), not a new I/O mapping: rows stay byte for byte for every state J4a does not complete.
7. **`carrier-floors`' remaining steps.** X3b r11 lists "exact name, filesystem, the directory's own barrier and its parent's". The creation path has no name or filesystem check of its own, so after C-ACL these two are re-checked in the completion and a mismatch is the host I/O row (`CarrierRefusal::Io`), like every other floor-directory failure.
8. **C-SUFFIX has no J4a use.** It is built and tested here (RW-C7, C12) because item 11 assigns it to J4a; J4b (the marker) and J4d (leaves) call it. Its read-back is through the judged handle, and the reopen compares device, inode and length: the bytes were verified through the same inode before the barriers.
9. **X9.** No run set: J4a has no row of its own (RW-F00, RW-K and RW-N are J4e's), and the six moved F00 cells are re-transcribed by J4e. Until then, a storage lead set run on a main that includes J4a disagrees at those six cells, by law; the lead sequences J4a's integration against X3c-3's lead set accordingly.
10. **What `.repair` wraps.** The completion and the remaining steps of the step that creates or admits the name: for a store directory and `carrier-floors`, the name, filesystem and both barriers; for `ledger.sqlite`, nothing, because its create-or-admit step (`create_store_file`, then the admission) has no barrier. X3c item 2's resumable-empty path that follows (the WAL selection, the DDL `COMMIT`, the namespace barrier, the verifying open) keeps its existing names, as it does for an empty private file today. So RW-P2's `.repair` scope holds no durability point (C-ACL's append is not one, J-RW item 10), and RW-K5's kill set under item 10's rule is empty. **Rejected:** running the resumable-empty path under `x3c.ledger-create.repair` after a completion. One path would then have two names, and a kill there leaves RW-L1, which ties RW-K5 to J4c's stop rule (N-L0), which item 10 states only for RW-K6. **Question:** do you agree, and that RW-K5's emptiness is J4e's to record in X9 r17 §RW?

## Not claimed

- J4b's registration (C-REG), J4c's L-UNC and C-LEDGER, J4d's C-TRUST and C-TDIR, and J4e's rows, census and lead set.
- `host.repair.completed`: O1 has not landed; the completion is returned in typed results only.
- RW-C4, C5, C8, C9, C11, C13 to C19: other units' controls.
- Any power-loss variant (X9 L1). Linux: the completion paths are macOS-only, as the store custody they live in.
- Descriptions: three v136 rows now understate or overstate J4a's files (below); J4a writes no description successor.

## No inventory

J4a adds, removes and renames no file, so it has no inventory successor (the lead reserved v139 only if a new file was unavoidable). Three v136 descriptions are now stale; they are listed for the next description batch:
- `crates/security/src/store_custody.rs`: "an existing mode or ACL is never changed". An existing directory or length-0 file that holds P-ACL now gains the one zero-rights owner allow.
- `crates/storage/src/ledger_store/project_ledger.rs`: "An empty file with no -wal is the only resumable creation state". Its ACL-omitted form is now completed first.
- `crates/security/src/journal_store/carrier_floor.rs`: "writes only the floor". The floor step may now also complete `trust/carrier-floors/`'s ACL.

## Lead results

All lanes ran serially with this diff (`evidence/lanes.sh`), each step under the shared lane lock, at `nice -n 10`, with a private 0700 TMPDIR and `--locked --offline`. The diff's sha256 was the same before and after the lanes. The real home was absent before and after. Summary: `evidence/lanes-summary.txt`; counts: `evidence/results.json`. Other units' lanes, X4-F3's crash-matrix lead set and two reviewers' lanes ran between J4a's locked steps. The build and clippy steps took seconds because a pre-check of the same bytes, under the lock, had just built and linted them, and cargo reused those results.

| Check | Result |
|---|---|
| `cargo fmt --all --check` | Clean |
| `cargo build --workspace --all-targets` | Pass |
| Clippy `-D warnings`, workspace `--all-targets` | Clean |
| Clippy `-D warnings`, platform, security, storage and host with `crash-matrix` | Clean |
| Clippy `-D warnings`, security, storage and host with `scenario-fixtures` | Clean |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1760 passed, 0 failed, 3 ignored (20 test binaries): `d2c00a9`'s 1738 plus J4a's 22 new tests (platform 1, security 18, storage 3). No existing test is removed or changed. |
| The same, run 2 | 1760 passed, 0 failed, 3 ignored |
| `cargo test --workspace --doc` | 20 passed (unchanged) |
| `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets --no-fail-fast` | 1658 passed, 0 failed, 3 ignored. Includes security's and storage's census pins, `every_test_feature_site_is_on_the_pinned_list` and `no_manifest_enables_the_crash_matrix_feature`. |
| `tools/generate_contracts.py` drift check | Passes (`selection-result.json`: `passed: true`, 40 source schemas, generator closure selected, 8 outputs, `changed: []`), on its rerun (below) |
| `verify_design.py --architecture ../opensip_arch --implementation .` | Passes: v136 selected, 96 inventory and 97 contract successors, 100 inheritance rows, 21 inventory and 1 contract passage supersessions |
| `check_package_edges.py --lane host` against v136 | Passes: 12 workspace packages, 22 declared and 20 resolved internal edges, none new |
| `check_package_edges.py --lane rust-provider` | Passes |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | Passes: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | Passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |

The commands are those of `evidence/lanes.sh`, from the worktree. **One rerun:** the first drift step stopped before the generator ran, because the fresh worktree lacked the git-ignored generator inputs (`missing regular input: tools/contracts/node_modules/typescript/LICENSE.txt`, exit 1). `tools/contracts/node_modules` and `python-packages` were then copied from the main checkout at `d2c00a9` (the generator admits each input by its pinned sha256), and `evidence/drift-rerun.sh` ran the step alone under the lock with the generator's child interpreter (`Python.app`'s `Python`, as the other units' lanes name it); `lanes.sh` now names that interpreter too. Nothing else was rerun, and the diff did not change.

## Lead rulings (Claude Opus 5.5, before sending)

| Item | Ruling | Rejected |
|---|---|---|
| S1: `project_ledger.rs` and its tests | **Accepted.** RW-P2's no-`-wal` clause and its typed result live there, and the edits are disjoint from X3c-3's. **Integration order:** X3c-3 integrates first. | Moving RW-P2 into a new file to avoid the overlap. That adds an inventory successor for no gain. |
| S2: six storage F00 rows go stale | **Hold J4a's product integration until X9 r17's §RW is accepted.** J4a then integrates in one commit with RW-F00's re-transcription of exactly those six rows, under §RW, and a full storage lead set. Every storage lead set run before then (X3c-3, J3a, J3b) runs on a main without J4a, so none disagrees. **This review judges J4a's code.** It doesn't judge the six rows; the §RW round transcribes them. | Integrating now, which makes every later storage lead set fail six cells until J4e. Holding J4a until all of J4e, which leaves a long rebase window. |
| S5: RW-K5's empty kill set | **Recorded for §RW** (RW-S6), which must state RW-K5's set. Codex's answer to judgment call 10 informs it. | None yet. |
| S6: three stale inventory descriptions | **Owed to the next description batch,** recorded in the work log. | A description successor inside J4a, which the law doesn't assign. |
| S8: lock hygiene | **Fixed.** X3c-3's lane script is being corrected to release only a lock it holds. | None. |

Judgment calls 2, 3 and 10 stay open for you, as written.

**Product main has moved** from `d2c00a9` to `0765f8c`: five binding commits, each changing only `design-lock.json`. Integration rebases.

**Shared machine.** Before any cargo build, test or clippy run, take the lane lock with `mkdir "$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"`, and remove it with `rmdir` straight after, only if your `mkdir` succeeded. Wait while the lock is held.

## Decide

- **Law:** does J4a implement J-RW r4 item 3.1's C-ACL over P-ACL and item 3.2's C-SUFFIX over P-PREFIX exactly, and X3c r9 items 1 and 2 and X3b r11 item 2 (with LD11-1) for RW-P1 to RW-P3? In particular: every clause judged before any effect, through the owner's retained parent, no-follow and charged; only an omitted ACL completed, and only by the fresh path's own step; the owner's remaining steps unchanged; nothing deleted, renamed, truncated or rewritten; no mode bit or other ACE; never on a read path (`open_store_file`, `admit_existing_store_directory`, recovery's floor capture, the carrier start and end steps are unchanged).
- **Exactness:** does every state that is not exactly RW-P1, RW-P2 or RW-P3 keep today's row and subject byte for byte, with nothing written (item 5's N-P1 and N-P2; judgment calls 3 and 6)?
- **The typed result and item 7:** is the result each use returns, with `RepairCompletion`'s codes, the seam item 7 names while O1 has not landed (call 5)?
- **Scopes and the census (RW-C10):** is the source pin, with the unchanged census pins, adequate for J4a, given that J4's own traced census and release absence are J4e's? Answer call 2's question.
- **Budget (RW-C12, call 4):** is "as the owner's own step does" met by C-ACL's reservation, and C-SUFFIX's by its whole reservation?
- **Tests:** do they cover RW-C1, C2, C3, C6, C7, C10 and C12 for RW-P1 to RW-P3 (the table above), with no existing test's expected value changed?
- **Judgment calls:** are calls 1 to 10 acceptable? Calls 2, 3 and 10 ask you direct questions.
- **Rerun:** run the lanes of `evidence/lanes.sh` yourself, with your own target directory, TMPDIR and output paths and the lane lock, or at least the platform, security and storage lib tests and the crash-matrix feature lane.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `4fbe89f1684846c70f1da639549669a31ee98775e526760f65bfcdede69f8bda`, the diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed: the unit adds no file, so it has no inventory successor or design selection. Do not commit.
