Grok review: unit X8a r1, the opaque API refusal suite's compile-fail fixture driver (law X8 r3), with inventory v117 on v114. Claude Opus 5.5 leads. You are the single reviewer.

**Ground rules.**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-refusal-suite-x8a-r1`.
- If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git only read-only, and only against the worktree below.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Inputs

- **Law.** `docs/implementation/m2/refusal-suite-x8/PROPOSAL-r3.md`, 44288 bytes, sha256 `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385`. You accepted it (`reviews/grok-refusal-suite-x8-r3/review.json`). `PROPOSAL.md` is the same text plus the acceptance note.
- **X8a's scope** (law "Units after the law"):
  - item 1's driver, annotation, toolchain check, census and self-test;
  - item 3's groups I, K and L, including the ports of the 17 existing `compile_fail` doctests;
  - item 4f's `scenario-fixtures` source pin, which passes vacuously until X8b adds the feature.

  Owner rows (X2e, X4a, X3d-1, X3d-2, X5a, X7a), X8b and X8c are out of scope.
- **Trial.** `/tmp/opensip-x8-trial`, if it is still there. Its driver shape is reused.
- **Product.** Worktree `/Users/sb/code/opensip-ai/opensip-x8a`, detached at main `daa7b01` (X9-0 integrated, lock selects inventory114), uncommitted. All 32 new files are intent-to-add. No existing file changes.
  - `git diff daa7b01` is 55118 bytes, sha256 `8d2b30704cf2cc11e0a0c21cb993896c961d36c653b4b88061a5455396984d0b`; 32 files, +1274.
  - Every file is pinned in `hashes.txt`.
  - The unit was first built on `abf2a48`. It was rebased onto `daa7b01` with no product change except one added unit check (judgment call 10).
- **Toolchain.** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin` (then `/usr/bin:/bin`), rustc and cargo 1.95.0, Python `python3.14`.

## What X8a builds

All of it is in `crates/host/tests/`. `admission_tests.rs` is the integration test to which build-plan line 593 assigns the public-boundary scenarios.

- **`opaque_api_misuse_fails_for_the_intended_reason`**, item 1's one test, runs these steps in order:
  1. **Census (item 1f), before anything compiles.** `CASES` is the case table, one `(file, krate, ty, unit, group, category)` row per fixture. The test fails if:
     - a row is duplicated;
     - a file is `main.rs` or does not name its crate and type;
     - the `cases/` listing differs from the table;
     - any of the seven categories of lines 597–598 and 1071 has no case.

     `SELFTESTS` pins the `selftest/` listing the same way.
  2. **Toolchain (item 1d).** It uses `RUSTC`, or else `rustc`, and requires a `rustc -vV` line exactly equal to `release: 1.95.0`. `CARGO` must be set. A missing or different toolchain fails; nothing skips.
  3. **Surface (item 1b).** `$CARGO check --locked --offline -p opensip-host --message-format=json --manifest-path <workspace>/Cargo.toml --target-dir $CARGO_TARGET_TMPDIR/x8-surface`, with `RUSTC` set to the checked compiler. Each `opensip_*` library and `serde_json` must have exactly one `.rmeta` in cargo's `compiler-artifact` messages; a duplicate name fails. `opensip_host` and `serde_json` must be present. The `-L dependency=` directory is the one directory those `.rmeta` files share.
  4. **Each case (item 1c), compiled twice** with `--edition 2024 --crate-type lib --crate-name x8_case --emit=metadata --error-format=json --cap-lints allow`, an `--extern` per surface library:
     - the control, which must exit 0 with no error diagnostic;
     - the misuse, with `--cfg x8_misuse`.

     The misuse passes only if:
     - it has exactly one error diagnostic, not counting "aborting due to";
     - its code equals the annotation's, or is absent for `none`;
     - its message contains the fragment;
     - one of its primary spans in the case file starts on the annotated line.

     A non-JSON line from rustc is a failure. The annotation is exactly one `//~ ERROR <E####|none> "<fragment>"` per file.
  5. **Self-test (item 1e).** Every file in `selftest/` must be rejected, and for the reason its `SELFTESTS` row names.
- **`annotations_are_parsed_exactly`** covers the annotation grammar and 11 malformed forms.
- **`scenario_fixtures_stays_out_of_release_manifests`**, item 4f's source pin.
  - It reads the root manifest and every workspace member's manifest, from `cargo metadata --locked --offline --no-deps`.
  - `scenario-fixtures` may appear only:
    - in `[features]` of `opensip-security` and `opensip-storage`, never in the value of `default`;
    - in `[dev-dependencies]`, including the dotted and `target.*.` forms.
  - Anything else fails, including a table name and `[workspace.dependencies]`.
  - It passes vacuously today.
- **`the_feature_pin_refuses_every_release_route`** covers the pin's refusals:
  - inline and dotted `[dependencies]`;
  - `target.*.dependencies`;
  - `[build-dependencies]`;
  - `[workspace.dependencies]`;
  - single-line and multi-line `default`;
  - `[features]` outside security and storage;
  - a package name.

  It also covers the accepted forms, comments ignored, and X9's `crash-matrix` table in platform's `[features]`.

**The 23 cases in `cases/`.**

| Group | File | Category | Misuse → expected |
|---|---|---|---|
| I | storage_ledger_store_private | storage internals | `use opensip_storage::ledger_store` → E0603 "module `ledger_store` is private" |
| K | evaluator_replayed_empty_literal | forged receipt | `ReplayedRun {}` → none "cannot construct `ReplayedRun` with struct literal syntax due to private fields" |
| K | evaluator_replayed_deserialize | serialized previous session | `serde_json::from_str::<ReplayedRun>` → E0277 "the trait bound `ReplayedRun: serde::Deserialize<'de>` is not satisfied" |
| K | evaluator_replayed_raw_json | raw DTO | `JsonValue` for `ReplayedRun` → E0308 "mismatched types" |
| K | evaluator_replayed_bool | boolean verified | `true` for `ReplayedRun` → E0308 |
| K | evaluator_replayed_retained_inputs | structural-only | `RetainedInputs` for `ReplayedRun` → E0308 (judgment call 2) |
| L | platform_settlement_clone | cloned or reused | `reserve.clone()` → E0599 "no method named `clone` found for struct `SettlementReserve`" |
| L | platform_settlement_settle_twice | cloned or reused | second `settle` → E0382 "use of moved value: `reserve`" |
| L | platform_settlement_default | private constructor | `SettlementReserve::default()` → E0599 "no function or associated item named `default` …" |
| L | platform_settlement_literal | forged receipt | named-field literal → E0451 "fields `issuer` and `allowance` of struct `SettlementReserve` are private" |
| L | platform_settlement_reserve_in_scope | private constructor | `helper.reserve_settlement` → E0599 on `&mut WorkScope<'_>` |
| L | platform_settlement_settle_in_scope | scope confinement | `helper.settle` → E0599 on `&mut WorkScope<'_>` |
| L | platform_settlement_reserve_in_postchecks | private constructor | `post.reserve_settlement` → E0599 on `&mut ReservedPostchecks<'_>` |
| L | platform_settlement_settle_in_postchecks | scope confinement | `post.settle` → E0599 on `&mut ReservedPostchecks<'_>` |
| L | platform_scope_replace | scope confinement | `*helper = WorkLedger::new()` → E0308 |
| L | platform_scope_swap | scope confinement | the second ledger's scope donated out of its nested borrow → E0521 "borrowed data escapes outside of closure" (judgment call 4) |
| L | evaluator_replayed_literal | forged receipt | `let _forged = ReplayedRun {}` → none, the private-fields message |
| L | evaluator_admitted_pack_literal | forged receipt | the four-field literal → E0451 naming all four fields |
| L | evaluator_capability_manifest_literal | forged receipt | the three-field literal → E0451 naming all three fields |
| L | security_fence_capture_after_drop | scope confinement | `drop(fence)` before the capture's use → E0505 "cannot move out of `fence` because it is borrowed" |
| L | security_fence_capture_escape | scope confinement | `ProvisionalHeldFile<'static>` from a local fence → E0515 "cannot return value referencing function parameter `fence`" |
| L | security_trust_session_after_drop | scope confinement | `drop(fence)` before `raw_current` → E0505 |
| L | security_trust_session_escape | scope confinement | `NativeTrustReadSession<'static>` → E0515 |

**The 8 self-tests in `selftest/`**, each with the rejection it must hit:
- `wrong_reason_typo` (E0422 path typo): WrongReason;
- `wrong_extra_error`: ErrorCount;
- `wrong_line`: WrongLine;
- `wrong_vacuous_reference_clone` (`.clone()` on `&ReplayedRun` compiles): ErrorCount;
- `wrong_broken_control`: BrokenControl;
- `wrong_fragment` (right E0308, wrong type in the fragment): WrongReason;
- `wrong_none_for_coded` (`none` where rustc emits E0308): WrongReason;
- `wrong_two_annotations`: Annotation.

The 17 doctests stay unchanged (law item 2).

## Judgment calls (narrowest choice consistent with the law)

1. **Census categories.** The census enum holds the seven law categories plus two labels for cases outside them:
   - `StorageInternals` for group I;
   - `ScopeConfinement` for group L rules where a borrowed scope, fence or session stays with its owner: spending from a helper, replacing the scope, donating it, use after the fence drops, and escape.

   Every case has exactly one category. The census requires only the seven to be non-empty. A census row also carries its item 3 group letter, which is the law table's own column.
2. **Structural-only input at X8a.** Item 1f makes the census fail if any of the seven categories has no case, and X8a must land green ("a working suite"). Groups I, K and L as listed cover six of them. Structural-only arrives only with X3d-2's row C. X8a therefore adds one group K case of the same kind as K's own list: the inert `opensip_identity::RetainedInputs` that `replay_run` reads, in place of `ReplayedRun`, E0308. The rejected alternative was a census that skips empty categories until later units land. That contradicts item 1f.
3. **Categories of the K and L cases.**
   - K's `Deserialize` probe is "serialized previous session": a stored replay cannot be read back.
   - Literals are "forged receipt".
   - `SettlementReserve::default()` and `reserve_settlement` on `WorkScope` or `ReservedPostchecks` are "private constructor". That is row F's absent-constructor shape, E0599: the only constructor is missing from that type.
   - `.clone()` and a second `settle` are "cloned or reused".
4. **The swap doctest cannot be ported verbatim.** On 1.95.0, `WorkLedger::scope`'s second doctest misuse, `core::mem::swap(original, other)`, yields two E0521 errors on the same line: `other` escapes, and `original` escapes. Item 1c and the forbidden substitutes allow exactly one error.
   - Measured alternatives that keep a `&mut` swap all give two or more errors: a swap after a donation, reborrows, a `move` closure, and a nested scope of the same ledger.
   - The port keeps the doctest's stated rule ("a second ledger cannot donate a scope which escapes its nested borrow") and its one-direction core. Inside the same nesting, the second ledger's scope is donated by shared reference to a slot in the outer closure. That yields exactly one E0521, "`other` escapes the closure body", which is the first of the verbatim swap's two errors.
   - The fixture header records the two-error fact.
   - I treat this as a gap in the law: it assumed each doctest misuse is a single error. I do not treat it as a contradiction, because item 2 ports the doctests' cases so that "their reasons are pinned", and this reason is pinned. If you read L's "every existing doctest's misuse" as requiring the verbatim swap, items 1c and 3L contradict each other for this one doctest, and that needs a law decision.
5. **Doctest ports otherwise keep the misuse line verbatim**, with these changes only:
   - each is wrapped in a `pub fn`, because a doctest body is `main`;
   - each gets a statement-level `cfg` and a lawful twin;
   - the doctest's `.clone()` method call is kept, and yields E0599. Row D's `Clone` probe (E0277) is the owner units' shape.
   - The E0451 annotations sit on the literal's first field line, because rustc 1.95.0 puts one primary span on each named field, not on the type.
6. **Fragments.**
   - Each is rustc's full message wherever the message names the type and trait (E0451, E0277, E0599, E0505, E0515, E0603).
   - E0308's message is only "mismatched types". The types are in span labels, and item 1c matches the message, so code, line and single-error pin the rest.
   - `wrong_fragment` shows that a fragment naming another type is rejected.
7. **Self-test strength.** Beyond item 1e's five shapes, the self-test adds:
   - `wrong_fragment`;
   - `wrong_none_for_coded` (the forbidden "`none` where rustc emits a code");
   - `wrong_two_annotations`.

   Each self-test must be rejected for the reason its row names. A must-reject case that broke for some other reason would otherwise still count as rejected.
8. **Surface hygiene, beyond item 1b.** The nested cargo:
   - gets `RUSTC` equal to the checked compiler, so the `.rmeta` files and the fixtures share one compiler;
   - drops `RUSTFLAGS`, `CARGO_ENCODED_RUSTFLAGS`, `CARGO_BUILD_RUSTFLAGS`, the rustc wrappers, `CARGO_TARGET_DIR` and `CARGO_BUILD_TARGET`, so an inherited setting cannot change the release surface.

   The dependency directory is taken from cargo's artifact paths, not from a hard-coded `debug/deps`.
9. **Pin scope and grammar.**
   - **Scope.** "Every `Cargo.toml` in the workspace" is read as the root manifest plus `cargo metadata --no-deps`'s workspace members. The excluded `providers/rust` and `tools/contracts` workspaces and `.cargo` configuration are left out. X9-0's own pin walks the repository for its own feature.
   - **Reader.** The scanner is a minimal line-based TOML reader, because no new dependency is allowed. It tracks strings, comments, multi-line arrays and inline tables, and dotted or quoted table names.
   - **Letter of the law.** In security's and storage's `[features]`, only `default` is refused. Another feature that enables `scenario-fixtures` is not, because the law forbids only a default feature.
10. **X9's `crash-matrix`.** The pin keys only on `scenario-fixtures`, so platform's `[features] crash-matrix = []` (X9-0, `daa7b01`) passes under X8 r3's rules. A unit check pins this. It is the only product change made in the rebase.
11. **Fixture formatting.** The fixtures are outside `cargo fmt`'s reach, because they are not modules, but each is clean under `rustfmt --edition 2024 --check`.
12. **Platform.** `installation_observation` and `NativeTrustReadSession` are exported on macOS only. The driver claims the pinned toolchain on this host, and the law claims no other target.
13. **Inventory.**
    - `admission_tests.rs` keeps its planned row by value. Its description of behavioural refusals is the file's planned purpose, which X8c completes. Adding the compile-fail driver to it is left to a description-only successor, so the inherited rows stay equal by value.
    - The 31 fixtures are role `fixture`, the role of the security crate's test fixtures.
    - `build_v117.py` follows the lock's own pinned `record` for the selected parent instead of a hard-coded map, so a parent-only rebuild after X4a (v116) needs no edit.

## Checks on daa7b01 with this diff

- **Full workspace, `cargo test --workspace --all-targets --offline --locked`, twice** (the documented lane; run 1 with a cold surface): 1476 passed, 0 failed, 3 ignored each, in 17 test binaries (400 s and 371 s). The `daa7b01` baseline is 1472; the 4 additions are `admission_tests`.
- **`admission_tests`:** 4 passed in both runs (23.9 s in run 1 with the cold nested surface check, 1.8 s in run 2). 23 cases and 8 self-tests.
- **Driver timing:**
  - surface check 15.2 s cold, 0.05 s warm;
  - compiling all 23 cases and 8 self-tests takes 1.5 s.
- **Clippy, `--workspace --all-targets -D warnings`:** clean.
- **Formatting:** `cargo fmt --all --check` is clean.
- **`check_package_edges --lane host`** passes against v114 and v117: 19 internal edges, unchanged.
- **`verify_design`** against the real lock passes, with v114 selected.
- **Mutations, each reverted:**
  - a case annotated one line off fails as WrongLine;
  - a stray `cases/extra.rs` fails the census;
  - `RUSTC=/usr/bin/true` fails the pin check;
  - `features = ["scenario-fixtures"]` on host's `[dependencies]` fails the pin;
  - a storage `default = ["scenario-fixtures"]` fails the pin;
  - a security `[features] scenario-fixtures = []` passes.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Inventory

`evidence/build_v117.py` adds 31 rows to the parent the lock selects: inventory114, 393913 bytes, `5a6f2b74f549e2e7b8bce26e6df9f3e9b00c01039728f47e68521fc5002fceb4`, with record `crash-matrix-x90-inventory-v114/successor.json` (20395 bytes, `808220d3…`).
- **Totals.** 804 inherited rows equal by value, for 835 files. Packages, dependencies, pending decisions and carried obligations are unchanged. 16 projection rows.
- **Rebuilds.** It refuses tracked paths, and refuses while a lock selects v117. Reruns are byte-identical.
- **Bytes.**
  - v117: 414580 bytes, `0601e3fa93ad00a09197dc199aafe74b8102f7d90c62916881ff90d0bd6f3138`;
  - successor.json: 22276 bytes, `96a896eb0f5db82e40ad47bf04c77f17826775560db5d5c48e999bc3e8de9681`;
  - subject manifest `refusal-suite-x8a-inventory-v117-subject.json`: 2118 bytes, `b310afb3b37b6857c23a0be6005c79320168108dcb4712d8deeb3f0bb31e838e`.
- **Verification.**
  - `verify_projection.py` against the real lock at `daa7b01`: PASS, 16 rows, 83 corruptions refused.
  - `evidence/verify_scratch.py` (v117 appended in memory, with a synthetic review and assent): passed, 78 inventory successors, 72 contract successors, 16 inheritance rows, v117 selected.

## Decide

- Does X8a implement item 1, groups I, K and L, and item 4f's pin faithfully, with nothing of X8b, X8c or the owner rows?
- Does each case fail for its intended reason under the four checks, with a compiling control?
- Does the self-test show that the driver separates intended from unintended failures?
- Is the swap port (judgment call 4) acceptable, or is it a contradiction that needs a law decision?
- Is each other judgment call acceptable?
- Is v117 right on v114?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": `b310afb3b37b6857c23a0be6005c79320168108dcb4712d8deeb3f0bb31e838e`, the sha256 of `docs/implementation/m2/refusal-suite-x8a-inventory-v117-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path `docs/implementation/m2/repository-file-inventory.v117.json`, bytes 414580, sha256 `0601e3fa…`, parent (the v114 pin above), successorRecord (path `docs/implementation/m2/refusal-suite-x8a-inventory-v117/successor.json`, bytes 22276, sha256 `96a896eb…`)}.

Write REVIEW.md and review.json. Do not commit.
