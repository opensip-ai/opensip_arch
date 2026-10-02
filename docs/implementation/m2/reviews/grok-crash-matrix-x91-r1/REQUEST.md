Grok review: unit X9-1 r1, the crash-matrix support surface and the barrier points at the integrated sites (law X9 r2 item 12), with inventory v118 on v128. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x91-r1. If you build or test, use a CARGO_TARGET_DIR under that directory, and a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)` (other experiments churn the shared temp folder). Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.

## Inputs

- **Laws** (all pinned in `hashes.txt`):
  - X9 r2, `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r2.md`, 55703 bytes, sha256 `b9b254c37599cb8adaf99fea666a062b24abad2a7edf236a516e74a07f05a9a9` (accepted). Item 12 defines X9-1: the feature in security, storage and host; the `crash_matrix_support` modules (item 6) and the pinned list of feature sites; scopes and points at the integrated sites; the post-state capture, normalizer and run writer; the census of the then-integrated path; and (r2) item 3's scripted wall clock in `observe_clock`, the `fixture` driver, the `scripted-clock` label and the census equality check. G1–G4 are the cross-law gaps.
  - X8 r3, `docs/implementation/m2/refusal-suite-x8/PROPOSAL-r3.md`, 44288 bytes, sha256 `1dc6b71f…bbf385` (accepted). Items 4b and 5a: one shared site list under the joint predicate `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`, owned and pinned by X9-1 and extended by X8b; the fenced `state.v1` publisher beside the trust owner's publication code, on the list, called by both surfaces; `AppendStep`, `ObjectStep` and the ledger commit hook stay `cfg(test)`.
  - X10 r4, `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md`, 17619 bytes, sha256 `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a` (accepted). Item 5's test-bridge pin, narrowed: no bridge reaches the binary, the doctor ingress or a default or release build; `apps/cli` and reporting declare no features; host, security and storage may declare only `crash-matrix` and `scenario-fixtures`. X9-1 found the conflict with X10 r3 and implements r4's pin.
- **Product.** Worktree `/Users/sb/code/opensip-ai/opensip-x9-1`, detached at main `099de03` (X6b, X4B-c, X6c, X11a, F6 and X7b integrated), uncommitted. The eight new files are intent-to-add. `git diff 099de03` is 255380 bytes, sha256 `c267442e21aae7fa8704e638e40d2c13dabe0f37336f09a7bc30af11a820a2df`; 52 files, +4369 −218. F6's `churned` import in the widened `initial_platform` test module stays `cfg(test)`, since F6's retry exists only in the crate's test build. Every file is pinned in `hashes.txt`.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.
- **X9-0** (the mechanism) is integrated at `daa7b01`; X4a, X3d-1, X3d-2, X5a, X6a, X6b, X6c and X7a placed their own `x4.*`, `x3d.*`, `x6.recover`, `x6.sweep` and `x7.delivery` points. X9-1 places none of those. X4B-c's changes to X4T-0 (built through X4B's producer) keep its declaration under the joint predicate; X4T-0's own pin and this unit's site pin pass.

## What X9-1 builds

- **The feature and its guards (items 1, 2).** `crash-matrix` in security (`["opensip-platform/crash-matrix"]`), storage (`["opensip-security/crash-matrix", "opensip-platform/crash-matrix"]`) and host (storage, security and platform), each one line, never default and named by no dependency table. Each crate's `lib.rs` carries the compile guard. Security also declares an empty `scenario-fixtures` (judgment call 1). X9-0's manifest pin and X8a's `scenario-fixtures` pin both pass.
- **Support modules (item 6).** `#[doc(hidden)] pub mod crash_matrix_support`, only under the feature, in security; storage's and host's re-export it unchanged. Security's offers:
  - `SyntheticInstallation`: `create` through the real creator path (injected loaded image, synthetic V2 profile set with the ACL-omission premise), or `open` by paths in a matrix child; `revocation_version`; `install_accepted_trust` (X4T-0's signed store for S in place); `publish_revocation` (a thin caller of the shared fenced publisher);
  - `plant_inherited_carrier` (format 1 or 2) and `plant_committed_tail` (X3b-2's reserved-slot technique);
  - `post_state` (capture, normalize, `normalizedSha256`) and `run_record` (the run writer, trace digest, census and kill set in `matrix.json`'s shape);
  - the `FIXTURE` and `PROFILE_STANDING` labels.

  Nothing returns an authority type.
- **The shared fenced `state.v1` publisher (X8 r3 items 4b, 5a).** `publish_store_fenced` beside X4T-b's `publish` in `trust/floor_publication.rs`, under the joint predicate. The shared fixture (`InstallationAt::publish_accepted_trust_fenced`) takes I's fence by the write gate's production walk over the scratch H, binds the retained owner to the gate's one read, publishes X4T-0's store at the requested revocation version through `publish` (records first, `state.v1` last), advances the gate's owner, and releases the fence. It returns the revocation version before and after, and refuses without writing while another holder has the fence. `x4t.floor-publication` is opened inside `publish` itself, so every caller's writes (X4T-b's write-ahead, X4B's bootstrap, this publisher) fall inside it.
- **The pinned site list (item 6; X8 item 4b).** `crash_matrix_sites.rs` scans every `cfg(…)` and `cfg!(…)` in `crates/*/src` and `crates/*/tests` and requires exactly its table (judgment call 2 lists it). A scanner self-test pins the forms it reads, and no source names a test feature in `cfg_attr`.
- **Barrier points (item 5).** Scopes, each a no-op without the feature:
  - `x2.fence.gate` (the gate's lock and barriers), `x2.fence.release` (every unlock of the gate's fence, by release or drop, through a private `FenceLock`), `x2.fence.end` (the end path's fence), `x2.fence.register.{reserved,namespace,marker-directory,marker,active}` (X2c's effects under the fence);
  - `x2.lease.{writer,readers}` (each lease lock and unlock);
  - `x3b.floor` (`probe`, `directory`, `write`), `x3b.init` (`create`, `ddl.commit.before/after`, `file-barrier.before/after`, `directory-barrier`, then `witness`), `x3b.start.witness.{revert,advance,init,open}`;
  - `x3b.append.<seal|rev|cln|terminal>` with `begin`, `level-four`, `built`, `witness-pending/*`, `insert.before/after`, `commit` (fallible), `witness-committed/*`, `release-level-four`, `release-level-three`. The append kind is known only to the caller, so the scope is opened at X3d-1's `begin_journal_txn` and `seal_under_append_lock` (seal), at X3d-1's `finish` (rev, cln), and inside the rollover (terminal);
  - `x3b.rollover` with each `RolloverStep` and its lease locks and unlocks, and `x3b.end.floor` (`probe`, `write`);
  - `x4t.floor-publication.{dependency,pointer}`;
  - `x3c.ledger-create` (with `.projects`, `.namespace`, `wal`, `ddl.commit.before/after`), `x3c.attempt.{begin,insert,commit}` (commit fallible), `x3c.object` (with `.objects`, `.sha256`), `x3c.evidence.{begin,stage-recovery_pair,stage-run_material,stage-availability,stage-pins,commit}` (commit fallible).

  Every point sits where the existing `cfg(test)` hook fires (`AppendStep`, `RolloverStep`, `ObjectStep`, the commit hook), which stay `cfg(test)`.
- **The scripted wall clock (r2 item 3).** `opensip_platform::crash_barrier::scripted_wall`, read by `observe_clock` under the feature only: with `OPENSIP_X9_CLOCK=<E>:<k>` in a matrix child, the n-th wall reading is `E + 3600·k + n` seconds and zero nanoseconds; the monotonic and boot readings stay native; a 3600th reading, a malformed script or a script outside a matrix child is a harness error. `ChildSpec` gains `clock: Option<ScriptedClock>`. `test_scratch`'s per-process parent in security and storage is named by an entropy draw instead of `SystemTime`, so a matrix child takes no OS wall reading.
- **Censuses (item 5, r2).** Every process of a run is a matrix child under the script, numbered in spawn order; the `fixture` child (ordinal 0) publishes the installation, X4T-0's store and a project root, and the parent takes no wall reading.
  - Security (`crash_matrix_census.rs`): X1's writer, X2c's registration, X2d, the floor step, creation and start, X2e's handoff with X4a's monitor, SEAL, REV and CLN, the end path, an exhausted generation's rollover, an `EXCLUSIVE` operation and the shared publisher. **277 points (276 durability; kill set 437)**, scopes `x2.fence`, `x2.lease`, `x3b.append.{cln,rev,seal,terminal}`, `x3b.end.floor`, `x3b.floor`, `x3b.init`, `x3b.rollover`, `x4t.floor-publication`, and on the way X3d-1's `x3d.finish` and X4a's read-only `x4.observer.tick`. Two census runs agree point for point.
  - Storage (`project_commit_census.rs`, a child of X3c-2's tests): ledger creation, attempt, two objects, the evidence transaction and COMMIT. **46 points (kill set 70).**
- **Verified deaths and injections.** Security: kill at `x3b.append.seal.witness-pending/rename.after#1` (PENDING durable; the next writer, its own process, reverts); at `commit.after#1` (SEAL landed; the next writer advances); `fail-after` and `fail-before` at the SEAL commit (undetermined; the next writer advances or reverts); kill at `x2.fence.gate/lock.after#1` (the fence busy until the death, free after); a hold at `x2.lease.writer/lock.after#2` resumed to the census outcome; kill at `x4t.floor-publication.pointer/rename.after#1` (the new `state.v1` visible, and the fenced publisher advances after). Storage: kill after the attempt commit; a torn object write; a kill before the evidence commit; `fail-after` and `fail-before` at the evidence commit. From storage, where security has no `cfg(test)`, the forwarded surface works end to end.
- **Post-state and records (item 7, r2).** Two runs' post-states differ raw and agree on `normalizedSha256`, trust store included. A killed run is written in the checker's run shape and passes its `check_run`, with `clock` and each child's `ordinal`.
- **Checker (r2).** `tools/check_crash_matrix.py` requires `scripted-clock` in every required and run label set, the required runs' `clockEpoch`, each run's `clock` equal to `{epoch, script: "x9-ordinal-3600"}`, and child ordinals increasing; its test has 12 cases.
- **X10 r4's pin.** `apps/cli/tests/doctor_tests.rs` keeps its source checks; its manifest check now refuses any `[features]` in `apps/cli` and reporting, and any feature but `crash-matrix` and `scenario-fixtures` in host, security and storage.

## Judgment calls (narrowest choice consistent with the laws)

1. **`scenario-fixtures` declared now, empty, in security only.** The joint predicate must be a known cfg or the compiler warns. X8b gives it its module, storage's forward and the dev-dependencies. `cargo clippy -p opensip-security --features scenario-fixtures` is clean.
2. **The site list.** X8 r3's four named gates, each with the closure it needs to compile and be reached, all under the joint predicate:
   - `Image::Injected` (variant and ten arms) with `initial_core`'s `tests` module (the injected image and signed tree); the synthetic V2 profile set: `initial_platform`'s `tests` module and its re-exports, the SYNTHETIC-standing `cfg!`, `core_authentication`'s `tests` module and its import, `InitialInstallationAttempt::for_tests`, and `lib.rs`'s `test_scratch`;
   - `HomeSource::Fixture` and its arms (the gate, the read session, and X6b's recovery admission), `create_at` and `prepare_installation_parent_at`, `DurableWriteGate::for_tests`, and `custody.rs`'s `installation_read_fixture` module (its read-session, F5 and X4a helpers stay `cfg(test)` inside it);
   - X4T-0's declaration and its one accessor `accepted_store_files`, re-exported by `trust.rs`;
   - `publish_store_fenced` and its re-exports.

   Crash-matrix-only, `any(test, feature = "crash-matrix")`: the reserved-slot and inherited-carrier fixtures in `carrier_operation.rs` and their re-export. Also pinned: the guards, the support modules, the census test modules, X9-0's platform sites and r2's `clock.rs` sites. Whole test modules are widened (with `cfg_attr(not(test), allow(dead_code, unused_imports))`) rather than moving fixture code; their `#[test]`s exist only under `cfg(test)`. X4T-0's own pin now accepts the joint predicate.
3. **Revocation version.** The fenced publisher publishes a regenerated X4T-0 store for the same S at version n+1 (X4a's Spec extension), as X4a's `swap_trust` does unfenced, not a new successor-publication generator.
4. **The replay-run candidate is deferred** to X9-5 (host): it is host-side and its rows are X9-5's.
5. **Point placement.** X2c's registration effects are named under `x2.fence.register.*` (under the held fence). The append's `begin`, `level-four` and `release-*` points take the caller's `x3b.append.<kind>` scope, opened in X3d-1's composition, the only place the kind is known. `std`'s `sync_all` in carrier creation gets protocol points `file-barrier.before/after`.
6. **`FenceLock`.** The census found the gate's fence unlocked by `Drop` on refusal paths outside any scope; a private newtype names every unlock `x2.fence.release`, with identical behaviour.
7. **Two census children.** Security and storage each run their own; storage's lease stand-in is its X3c-2 fixture's held `writer.lease`, named `x2.lease.writer`. The full commit composition (X3d-2's facade) is censused by X9-2's commit driver, which needs X8b's or this surface's operation path.
8. **Normalizer.** Drawn values are numbered by first appearance with members ordered by their unnumbered shape; native clock members (`mono`, `bootId`, `wall`, `wallClockData`) become their name alone, because under r2 the monotonic and boot readings stay native and whether two are equal is not a product property; `trustState` is one digest over the trust files each normalized alone.
9. **Clock script grammar.** `<E>:<k>` with no sign, space or leading zero; it is refused outside a matrix child, like X9-0's arming; the driver validates it before spawning. The clock epoch used by the censuses is 2026-10-03T00:00:00Z (1791072000).
10. **Release refusal per crate.** `cargo build --release --features crash-matrix` for each of platform, security, storage and host stops at platform's guard (`crates/platform/src/lib.rs:6`), which compiles first; each crate's own guard is pinned by X9-0's manifest pin.

## Disclosed gap for X9-2 and X9-6

- **Observer timing.** The census is unarmed, so X4a's observer waits on its native 5 s period. Each operation finishes well inside it, and two census runs agree; an operation slower than 5 s would add an observer reading and point, which r2 makes a `HARNESS-ERROR` (two censuses must agree), never a smaller kill set. Matrix rows that arm `x4.observer.tick` (item 11) are unaffected.
- **The X9 r1 clock-dependence finding** is settled by r2's script and implemented here.

## Checks on 099de03 with this diff

- **Full workspace without the feature** (private TMPDIR): 1707 passed, 0 failed, 3 ignored. (On f097c5b, before X6b to X7b, it was run twice: 1642 passed, 0 failed, 3 ignored each; on d64ef7b once: 1693 passed.)
- **Feature lane,** `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets`: 1592 passed, 0 failed, 3 ignored, both pinned censuses included. The censuses are unchanged by X6b's and X6c's recovery and sweep modules, which the census workload does not reach (X9-3's drivers will census them).
- **Clippy `-D warnings`:** clean on the workspace without the feature, on the four crates with `crash-matrix`, and on security with `scenario-fixtures` alone.
- **`cargo fmt --check`:** clean.
- **`check_package_edges --lane host`:** passes against v118 and v128, 20 declared and 20 resolved internal edges.
- **Checker tests:** `python3.14 -I -B tools/tests/test_check_crash_matrix.py`, 12 OK.
- **Release guard 4:** `cargo build --release -p opensip-cli` → `target/release/opensip`, 6314176 bytes, sha256 `e1b545662b2b913a680ba42721a0edfa75989b5461e143dc336dcb83f89628a8`; `check_crash_matrix.py release-absence` passes, none of the 26 strings found. The feature's release build is refused for platform, security, storage and host (exit 101, the guard).
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Inventory v118

`crash-matrix-x91-inventory-v118/evidence/build_v118.py` adds eight rows to the parent the lock selects, inventory128 (X11a), 530975 bytes, sha256 `c6bcf2f4818869756b99cec4a4d97c85c48353e2f66035ed92406165550c3ce2`. Its PRIOR table maps inventory125 through inventory128 (first built on v125 before any review, then moved):
- `crash_matrix_support.rs`, `crash_matrix_support/post_state.rs`, `crash_matrix_support/run_record.rs` (security), and storage's and host's `crash_matrix_support.rs`: service;
- `crash_matrix_census.rs`, `crash_matrix_sites.rs` (security) and `ledger_store/project_commit_census.rs` (storage): test.

949 inherited rows equal by value, 957 files; packages, pending decisions and carried obligations unchanged; the fifty-five inheritance rows (sixteen carried, D1's thirty-nine, D2's four supersessions folded) re-projected by stable path, `supersessionsFolded: 0`. The README lists the changed existing rows and which descriptions go out of date by omission. Reruns are byte-identical; the builder refuses tracked paths and a lock that selects v118.
- v118: 539833 bytes, sha256 `ae94d003acdd4ee203a672c7164513705acc876a723faf4eb45a25fb99eaa925`;
- successor.json: 145488 bytes, sha256 `a6e50642315c7c103892552adbd0be3bfe2b5ad9ea652ffedb70e8b71b4331b1`;
- subject manifest `crash-matrix-x91-inventory-v118-subject.json`: 2110 bytes, sha256 `8c1025ba7282f9459aa46dbb5616bacb012d54650ab4cbb065fed5a878de88af`.
- verify_projection against the real lock at 099de03: PASS, 55 rows, 278 corruptions refused. `evidence/verify_scratch.py` (v118 appended in memory over the worktree's lock, synthetic review and assent): passed, 89 inventory successors, 74 contract successors, 55 inheritance rows, v118 selected.

## Decide

- Does X9-1 implement X9 r2 item 12's X9-1 scope (with items 1, 2, 3's clock, 5, 6 and 7) faithfully, and X8 r3 items 4b and 5a's share of it, with nothing of X8b or later units?
- Is every test-feature site on the pinned list, under the right predicate, and is the list the narrowest that compiles and reaches the four named gates? Is anything production-reachable without a feature?
- Are the points complete for the integrated sites and correctly scoped (no durability primitive outside a scope on the censused paths), and is every featureless expansion the prior code?
- Is the shared fenced publisher sound (production fence walk, the trust owner's protocol, `state.v1` last, no write under contention, no authority returned)?
- Is the scripted clock as r2 states, and do the censuses and post-states depend on nothing but the script and the product?
- Is each judgment call acceptable? Is v118 right on v128?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `8c1025ba7282f9459aa46dbb5616bacb012d54650ab4cbb065fed5a878de88af`, the sha256 of `docs/implementation/m2/crash-matrix-x91-inventory-v118-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path `docs/implementation/m2/repository-file-inventory.v118.json`, bytes 539833, sha256 `ae94d003…`, parent (the v128 pin above), successorRecord (path `docs/implementation/m2/crash-matrix-x91-inventory-v118/successor.json`, bytes 145488, sha256 `a6e50642…`)}.

Write REVIEW.md and review.json. Do not commit.
