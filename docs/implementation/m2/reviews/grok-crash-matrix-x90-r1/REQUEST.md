Grok review: unit X9-0 r1, the crash-matrix mechanism (law X9 r1 item 12), with inventory v114 on v108. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x90-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.

## Inputs

- **Law.** `docs/implementation/m2/crash-matrix-x9/PROPOSAL-r1.md`, 50022 bytes, sha256 `325ccd7524c90d0611f6b4aabcd4549d5029dc7e901245cb552afcac5cd38d82`, which you accepted (`reviews/grok-crash-matrix-x9-r1/review.json`, `bc1e7af0…`). X9-0 is item 12's first unit: the platform feature, the barrier module and macros, the compile guard and manifest pin, the platform points, the child protocol, the census mechanism, `tools/check_crash_matrix.py`, and the self-tests. X9-1 and later are out of scope.
- **Product.** Worktree `/Users/sb/code/opensip-ai/opensip-x9-0`, detached at main `97f630a` (X3b-4 integrated), uncommitted. New files are intent-to-add. `git diff 97f630a` is 153961 bytes, sha256 `351f1b3b1842228287f494346a0476ee635813f7beeba0026b346bc101d7005a`; 15 files, +3465 −156. Every file is pinned in `hashes.txt`.
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, Python `python3.14`.
- **X8 coordination.** Your X8 r1 review requires the shared fixture gates (Image::Injected, HomeSource::Fixture, X4T-0, the fenced state.v1 publisher) to use `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`. Those gates belong to X9-1. X9-0 touches none of them, and adds no cross-crate fixture surface.

## What X9-0 builds

- **The feature (item 1; item 2, guards 1 and 2).**
  - `crates/platform/Cargo.toml` gains `[features] crash-matrix = []`. Platform has no internal dependencies to forward to, and no other crate declares the feature yet.
  - `src/lib.rs` carries the compile guard `#[cfg(all(feature = "crash-matrix", not(debug_assertions)))] compile_error!(…)`.
  - The barrier module `opensip_platform::crash_barrier` is `#[doc(hidden)] pub` only under the feature (and macOS or Linux, for `libc`).
- **The macros (`crash_macros.rs`, always compiled).** `crash_scope!(name, { body })` and `crash_barrier!(scope, step, kind, …)`. Without the feature, a point is `{}`, a wrapped point is its effect expression, a gate is its wait, a draw is its draw, and a scope is its block: no call, no string, no branch. Forms:
  - primitive points: `crash_barrier!(primitive, "rename", fallible, effect)`, `step`, and `write, bytes, |b| effect`;
  - protocol points under `_` (the current scope) or a named scope: `step`, `fallible` (with a fault-to-error closure), `gate` and `draw`.
- **The barrier (`crash_barrier.rs`).**
  - **Registry.** Item 5's 25 scope names, between `// BEGIN/END X9 SCOPE REGISTRY` markers that the checker reads. `x4.observer` and `x6.recover` are flagged read-only. Two `x9.selftest*` scopes exist only in platform's own test build.
  - **Grammar.** Kinds, the arming parser, and per-name occurrences.
  - **Disabled state.** No `OPENSIP_X9_ARMS` means one `OnceLock` read and a return.
  - **Child state.** With `OPENSIP_X9_ARMS` set (even empty) and `OPENSIP_X9_CHILD` set:
    - every reached point writes `X9|pid|thread|n|name#k|event|payload`, one `write(2)` of at most 512 bytes, numbered under one lock;
    - `hold` registers the point, writes `held`, and blocks on a stdin read. One held thread reads for all held threads and hands each `resume` to its target by condvar;
    - `fail-before` and `fail-after` return `EIO` (primitive) or the caller's error (protocol site), without or after the effect;
    - `torn` writes the first half of the bytes with the same effect, then holds;
    - gate and draw as item 4 describes;
    - any harness error is a `harness-error` record and exit status 86.
- **The parent driver (`crash_barrier/driver.rs`).**
  - **Spawn.** `MatrixChild::spawn` runs `current_exe() --exact <entry> --nocapture --test-threads=1` with `env_clear` plus the four variables, after validating the arming.
  - **Driving.** It reads records on a thread, drains stdout, and offers `await_held` / `await_event`, `resume`, `kill` (`SIGKILL`) and `finish`. Dropping an unfinished child kills it.
  - **Watchdog.** 300 s on a `recv_timeout` thread. When it expires it kills the child and records only `Watchdog`.
  - **Exit checks.** `Exit::verify_finished` and `Exit::verify_death_at` implement item 3's death rule.
  - **Census.** `Census::from_exit` and `kill_set` implement item 5's kill set: each durability point at #1, and a repeated one also at (n+1)/2 and n.
- **Platform points (item 1).** Each is `<scope>/<step>.before|after`:
  - `create`: the staging file in `replace_with`, plus `create_exclusive_regular` / `create_exclusive_directory` and their charged forms;
  - `write`: `NativePublication::write` and `write_new_regular_charged`'s loop, now `write_at_zero` with the same code;
  - `file-barrier`, `rename`, `directory-barrier`: the native `PublicationOps`, which also back the accounted barriers and `confirm_existing_regular`, plus `rename_replace_charged`;
  - `link`: `NativeNewPublication`'s `RENAME_EXCL` publication;
  - `reopen-confirm`: `confirm_existing_regular`'s reopen;
  - `lock` and `unlock`: `FileLock`.

  Test-injected `PublicationOps` carry no points. Without the feature each wrapped effect is the original expression.
- **Pins that run in every test build (`crash_matrix_tests.rs`).**
  - **Manifest pin (guard 2).** Every `Cargo.toml` and `.cargo/config*` in the repository may name `crash-matrix` only as a one-line `[features]` definition forwarding to `<dep>/crash-matrix`, or as a `[[test]]` `required-features = ["crash-matrix"]`. Every declaring crate must carry the guard. The pin's own refusals are tested.
  - **No-sleep source pin (item 3).** Over the macros, barrier, driver and self-tests, with comments skipped. Exactly one `recv_timeout` is admitted, the driver's watchdog.
  - **Featureless expansion test.**
  - **Shared self-test workload** with its pinned outcome and tree.
- **Self-tests (`crash_barrier/self_tests.rs`, `cfg(all(test, feature))`).** Item 12's list, plus addressed resumes and the kinds:
  - **Kills, verified.**
    - At `replace/rename.after`: the new bytes are visible.
    - At `write.before`: the empty staging file survives, because no destructor ran.
    - At `lock.after`: the flock is busy until the death.
  - **Hold then resume** to the pinned outcome, including the law's bare `resume`.
  - **Injected failures.** `fail-before` and `fail-after` at rename, file-barrier and directory-barrier, with the stage, visibility, `EIO` and state each leaves.
  - **Torn writes**, killed or resumed.
  - **Unarmed runs.**
    - An untraced child writes zero records and leaves the featureless outcome and tree.
    - A traced unarmed child does the same, records the pinned 42-point census and the 44-entry kill set, and its trace reproduces.
  - **Harness errors in the child:**
    - an armed point that is never reached;
    - six actions a point's kind does not admit;
    - a primitive outside any scope.
  - **Two held threads:**
    - addressed resumes;
    - read-only points after a kill point admitted, and a durability point refused;
    - a bare `resume` refused.
  - **Watchdog.** A 1 s watchdog, available only in tests, ends a never-resumed child as a harness error.
  - **Protocol kinds.** Gate, protocol fallible, and draw with `inject-id`.
  - **Grammar.** The arming grammar, durability, and the kill-set derivation.
- **The checker (`tools/check_crash_matrix.py`, stdlib, read-only) and its test.**
  - `check --repository --run-set --repeat --required --commit` implements item 7's refusals over both repetitions.
  - `release-absence --repository --binary` scans for `OPENSIP_X9_` and every registry scope.
  - `tools/README.md` gains a section.

## Judgment calls (narrowest choice consistent with the law)

1. **The feature in platform only.** Item 12 puts the feature in platform for X9-0. Forwarding in security, storage and host is X9-1's. It stays separate from X8's `scenario-fixtures`, and touches no shared fixture gate.
2. **Point names.** Item 1's grammar `<scope>[/<primitive-step>].<before|after>` is read together with the law's own examples (`x3d.publish.commit-returned`, `x3c.attempt.commit.after`, `x3c.evidence.stage-<table>`).
   - A protocol point is `<scope>.<step>`, where the placing unit chooses the step segments, which may end in `.before` or `.after`.
   - A primitive point is `<scope>/<step>.<before|after>`.
   - A `crash_scope!` name that is or extends a registered scope is absolute; any other name is a segment under the current scope. That yields `x3b.append.seal.witness-pending/rename.after`.
   - Segments are `[a-z0-9_-]+`.
3. **When tracing is on.** Tracing is on exactly when `OPENSIP_X9_ARMS` is present. Empty means a census. `OPENSIP_X9_ARMS` without `OPENSIP_X9_CHILD` exits as a harness error, so a stray variable cannot silently trace a normal run.
4. **Where each action is armed.** Each action is armed at the point where it acts:
   - `fail-before` at `.before`;
   - `fail-after` at `.after`;
   - `torn` at a write's `.before`;
   - `inject-id` only at `x3d.session.execution-draw`, refused at parse because the law fixes it by name.

   The parser is otherwise syntactic. Admission by kind happens in the child, as item 4 requires ("a HARNESS-ERROR in the child").
5. **The injected native failure is `EIO`** at file-barrier, rename and directory-barrier. Existing rules then classify it: a Rename `EIO` is `Indeterminate`, and SyncTemporary is `Unchanged`.
6. **`.after` is reached only when the effect succeeded.** A native failure propagates with no `.after` record. A busy `LOCK_NB` attempt therefore reports only `lock.before`.
7. **Torn.** The first `len/2` bytes are written through the same write. A torn write that is resumed instead of killed fails with `EIO`: the process survived a failed write.
8. **Addressed resume.** The control line `resume <name>#<k>` is added beside the law's bare `resume`. The bare form is accepted only when exactly one thread is held. Item 11's scripts hold the main thread and an observer tick at the same time and resume the tick first, which a bare line cannot address. Exactly one held thread blocks in the stdin read; the others wait on a condvar (blocking, not polling). A held point registers before writing `held`, so a resume can never arrive before its target exists.
9. **Platform point placement.** Points sit in the native `PublicationOps` implementations and the native syscall sites, so every caller is covered once and test-injected ops carry none. The following are not instrumented:
   - `directory_publication.rs` (the creator's directory publication);
   - the macOS ACL append;
   - the staging cleanup `unlink`.

   Item 12 does not list them, and no M2 matrix row kills inside them. X9-1's census of the integrated path will show whether any is reached inside a matrix scope.
10. **Read-only scopes.** Only `x4.observer` and `x6.recover` are flagged read-only: the law calls the observer "gated" and recovery "read-only". Every other protocol scope, and every primitive point, is a durability point. X9-1 can refine this from its census.
11. **Self-test scopes.** `x9.selftest` and `x9.selftest-observer` are not law scope names. They exist only under platform's `cfg(test)`, outside the registry block the checker and the release scan read.
12. **Where the self-tests run.** They are feature-gated unit tests inside platform (`cargo test -p opensip-platform --features crash-matrix`), not a new `[[test]]` target. Guard 2 names exactly two matrix targets, and the watchdog shortening is a crate-private test seam.
13. **The watchdog.** 300 s, with one `#[cfg(test)]` constructor that shortens it for the watchdog self-test.
14. **"Unarmed identical to featureless".** This is shown by:
    - a pinned workload outcome and tree, asserted in the featureless build;
    - the same outcome and tree reproduced by an untraced child (with zero records) and by a traced unarmed child;
    - the featureless expansion test;
    - the release scan.

    No binary comparison between the two builds is attempted.
15. **The census at X9-0.** Item 5 says X9-0 "runs a lawful commit, recovery and sweep", but at X9-0 no point exists above platform: recovery and sweep are X6, and the protocol scopes are X9-1's. Item 12 gives "the census of the then-integrated path" to X9-1. X9-0 therefore delivers the census mechanism, proved on the self-test workload (42 points and 44 kills). I read this as no contradiction, because item 12 governs the unit split.
16. **Extra record events.** Beyond `pass` and `held`, the events are `resumed`, `fail-before`, `fail-after`, `inject-id`, `outcome` and `harness-error`. The last two use the point field `-`. A draw that is held still writes its `pass` with the payload after it is resumed. The self-test child also prints `OUTCOME …` on stdout so that an untraced child can be compared.
17. **Guard 4's feature build.** The law names `opensip-storage`, which has no feature until X9-1. X9-0 shows the refusal on `opensip-platform`.
18. **Checker shapes.** The law fixes the run record only. X9-0 defines:
    - `required-runs.v1.json` as `{schema, runs: [{case, variant, units, labels, script, expected}]}`;
    - `matrix.json` as `{schema, product, runs: [pins], census: {points, trace}, killSet, releaseAbsence, limits}`.

    Its rules:
    - `--repeat` is mandatory;
    - process-death holds exactly when the script kills;
    - coverage means every kill-set point is killed by a process-death run, and runs may also kill outside the census (F32's rollover);
    - a census point that a product change removes shows up as that run's harness-error verdict.
19. **The trace digest.** Platform has no SHA-256. The driver exposes the trace lines without the process id, and X9-1's run writer digests them.
20. **The gate form.** It takes a unit wait expression (`if !gate { wait }`). X4a can widen it if its wait returns a value.

## Checks on 97f630a with this diff

- **Full workspace without the feature, twice:** 1464 passed, 0 failed, 3 ignored each, 26 binaries. The baseline is 1459; the 5 additions are the always-on pins.
- **Feature lane, `cargo test -p opensip-platform --features crash-matrix`:** 291 passed, 0 failed, 1 ignored. That includes the 17 X9 self-tests and the 4 pins; the featureless expansion test is cfg'd out. The 17 self-tests passed in all 11 runs made during the unit, with no failure.
- **Clippy, `--workspace --all-targets -D warnings`:** clean without the feature, and clean with `--features opensip-platform/crash-matrix`.
- **Formatting:** `cargo fmt --check` is clean.
- **`check_package_edges --lane host`** against v114 passes, with 19 declared and 19 resolved internal edges, unchanged.
- **Checker tests:** `python3.14 -I -B tools/tests/test_check_crash_matrix.py`, 11 OK.
- **Release guard 4:**
  - `cargo build --release -p opensip-cli` (no features) builds `target/release/opensip`, 6273264 bytes, sha256 `cf1a28dc207c1c8c7723d9b98eefcc0bbdcd196528e7c899f19675255ca8866f`. `check_crash_matrix.py release-absence` passes it, finding none of the 26 strings.
  - Positive control: the same scan of the feature-enabled platform test executable finds all 26.
  - `cargo build --release -p opensip-platform --features crash-matrix` exits 101 at `src/lib.rs:6`: "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions".
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Inventory

`evidence/build_v114.py` adds seven rows to the parent the lock selects: inventory108, 376570 bytes, `9c6953f28572f6882bbdc71ae945104e4a4e65e5d7b87cae9cf91318d9eb1f44`.
- **The rows.**
  - `crash_macros.rs` is public-api.
  - `crash_barrier.rs` and `crash_barrier/driver.rs` are service.
  - `crash_barrier/self_tests.rs` and `crash_matrix_tests.rs` are test.
  - `tools/check_crash_matrix.py` is a tooling validator, and its test is a tooling test.
- **Totals.** 793 inherited rows equal by value, for 800 files. Packages and dependencies, pending decisions and carried obligations are unchanged. 16 projection rows.
- **Existing rows whose descriptions stay true:** platform `Cargo.toml`, `lib.rs`, `filesystem.rs`, `file_effects.rs`, `file_replace.rs`, `directory_effects.rs`, `locks.rs` and `tools/README.md`. The README explains why a feature needs no package row or edge-checker change.
- **Rebuilds.** The builder's parent map also covers v106 and v111 (X2e), so a parent-only rebuild follows whichever integrates first. It refuses tracked paths. Reruns are byte-identical.
- **Bytes.**
  - v114: 385872 bytes, `98f92e519e54b8a3ae7951a30faf6ddc3bd643c4f34939789fd592dcbf361ccb`;
  - successor.json: 20395 bytes, `9fba2d42e3300cd932a2fb0bccb1def534050dfd8a46be6784f2eb983656ba04`;
  - subject manifest `crash-matrix-x90-inventory-v114-subject.json`: 2109 bytes, `4a236fd21f0b52076dfcacdae1d267311f5e175a8397a9924fe599e65ea34af7`.
- **Verification.**
  - verify_projection against the real lock at 97f630a: PASS, 16 rows, 83 corruptions refused.
  - evidence/verify_scratch.py (v114 appended in memory over the real lock, with a synthetic review and assent): passed, 76 inventory successors, 72 contract successors, 16 inheritance rows, v114 selected.

## Decide

- Does X9-0 implement items 1 to 5, 7 and 12's X9-0 scope faithfully, with nothing of X9-1 or later?
- Are the four release guards (as far as X9-0 owns them) and the unarmed-behaviour claim met?
- Is the child protocol sound: no sleep or timed decision, a death verified by `SIGKILL` and the trace, no hold lost or misrouted, harness errors never passing?
- Are the platform points complete for item 12's list and correctly placed? Is every featureless expansion exactly the prior code?
- Is each judgment call acceptable?
- Is v114 right on v108?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `4a236fd21f0b52076dfcacdae1d267311f5e175a8397a9924fe599e65ea34af7`, the sha256 of `docs/implementation/m2/crash-matrix-x90-inventory-v114-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path `docs/implementation/m2/repository-file-inventory.v114.json`, bytes 385872, sha256 `98f92e51…`, parent (the v108 pin above), successorRecord (path `docs/implementation/m2/crash-matrix-x90-inventory-v114/successor.json`, bytes 20395, sha256 `9fba2d42…`)}.

Write REVIEW.md and review.json. Do not commit.
