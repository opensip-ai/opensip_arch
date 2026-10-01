# X8a r1 — compile-fail fixture driver

**Verdict: ACCEPT-UNIT.** Inventory v117 is ACCEPT on v114.

X8a is law X8 r3's host-test unit: item 1's driver, annotation, toolchain check, census and self-test; groups I, K and L, including the 17 doctest ports; and item 4f's `scenario-fixtures` source pin, which passes vacuously. Owner rows, X8b and X8c are absent. Judgment calls 1–13 are accepted. Call 4 is accepted as the lead's decision: the one-directional donation keeps the swap doctest's rule under the one-error rule.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-x8a` is detached at `daa7b0130027937c1de371d4ca6efe7e996deaaf`. `git diff daa7b01` is 55118 bytes, sha256 `8d2b30704cf2cc11e0a0c21cb993896c961d36c653b4b88061a5455396984d0b`: 32 files, 1274 insertions. All 32 are intent-to-add. No existing file changes, so the 17 `compile_fail` doctests stay as they are (10 in `work_ledger.rs`, one each in `replay.rs`, `policy.rs` and `capabilities.rs`, two each in `installation_observation.rs` and `native_read_session.rs`). Every hashes.txt pin matches. Law `PROPOSAL-r3.md` is the accepted text (`1dc6b71f…`, 44288 bytes). `PROPOSAL.md` adds only the acceptance note. The lock and `/Users/sb/code/opensip-ai/opensip/design-lock.json` are the same bytes; the tip is inventory v114 (393913 bytes, `5a6f2b74…`) with record `crash-matrix-x90-inventory-v114/successor.json` (20395 bytes, `808220d3…`). `~/Library/Application Support/OpenSIP` is absent.

## Driver

`opaque_api_misuse_fails_for_the_intended_reason` runs the census before any compilation. The table has 23 rows, each `X8a`, groups I, K and L only. It rejects a duplicate row, a `main.rs`, a file that omits its crate or type, and a `cases/` or `selftest/` listing that differs from the table. The seven item 1f categories are each non-empty. `StorageInternals` and `ScopeConfinement` are extra labels and are not required by that check.

The toolchain reads `RUSTC` or `rustc`, requires a `rustc -vV` line equal to `release: 1.95.0`, and requires `CARGO`. The surface is `cargo check --locked --offline -p opensip-host --message-format=json` into `CARGO_TARGET_TMPDIR/x8-surface`, with `RUSTC` set to that compiler and with `RUSTFLAGS`, the encoded and build rustflags, the rustc wrappers, `CARGO_TARGET_DIR` and `CARGO_BUILD_TARGET` removed. Each `opensip_*` library and `serde_json` must contribute exactly one `.rmeta`, and `opensip_host` and `serde_json` must be present. The `-L dependency=` directory is the single directory those files share.

Each case is compiled twice with `--edition 2024 --crate-type lib --emit=metadata --error-format=json --cap-lints allow`. The control must exit 0 with no error diagnostic. The misuse (`--cfg x8_misuse`) passes only with exactly one error diagnostic, ignoring a message that starts with `aborting due to`, with the annotated code or an absent code for `none`, with the fragment contained in the message, and with a primary span in the case file on the annotated line. A non-JSON rustc line fails the case. Each file has one `//~ ERROR` annotation. The eight self-tests must be rejected for the `SELFTESTS` reason named for that file.

`annotations_are_parsed_exactly` accepts one well-formed annotation and a `none` code, and rejects the eleven malformed forms. `scenario_fixtures_stays_out_of_release_manifests` reads the root manifest and `cargo metadata --locked --offline --no-deps` workspace members. `scenario-fixtures` may appear in `[features]` of `opensip-security` and `opensip-storage`, never as `default`, and in `[dev-dependencies]` including dotted and `target.*.` forms. A package name, `[dependencies]`, `[build-dependencies]` and `[workspace.dependencies]` fail. The live manifests pass. `the_feature_pin_refuses_every_release_route` covers those refusals, the accepted forms, comments, and platform's `[features] crash-matrix = []`.

## Judgment call 4

Accepted. This is the lead's decision, and it is the reading this review adopts.

The doctest on `WorkLedger::scope` (`work_ledger.rs` lines 235–246) states the rule: a second ledger cannot donate a scope which escapes its nested borrow. Its misuse is `core::mem::swap(original, other)`. Item 1c, and the forbidden substitute that bars a misuse with more than one error, require exactly one error diagnostic.

Recompiled here against the same surface `.rmeta` and the same rustc 1.95.0 flags, that swap yields two `E0521` diagnostics, both `borrowed data escapes outside of closure`, both with a primary span on the swap line. The first label is `` `other` escapes the closure body ``. The second label is `` `original` escapes the closure body ``.

`platform_scope_swap.rs` keeps that rule in one direction. Inside the same nesting, the second ledger's scope is stored by shared reference in a slot of the outer closure (`donated = Some(&*other)`). The annotation is `E0521` `"borrowed data escapes outside of closure"`, the first of the swap's two errors. The fixture header records the two-error fact. The driver's four checks passed this case with its compiling control. Item 2 asks that the doctest's reason be pinned, and this pins it. The replacement doctest remains its own fixture, `platform_scope_replace.rs`.

## The other calls

1. **Census categories.** Accepted. The seven law categories are required and filled. Group I is `StorageInternals`. Group L's borrowed scope, fence and session cases are `ScopeConfinement`. Each case has one category, and the row carries the law table's group letter.
2. **Structural-only.** Accepted. Groups I, K and L as listed cover six of the seven required categories. `evaluator_replayed_retained_inputs.rs` places the inert `RetainedInputs` where a `ReplayedRun` is required and expects `E0308`, so the suite can land with every required category non-empty.
3. **K and L categories.** Accepted. The `Deserialize` probe is serialized previous session. Literals are forged receipts. `default` and `reserve_settlement` on `WorkScope` or `ReservedPostchecks` are private constructor. `.clone()` and a second `settle` are cloned or reused.
5. **Other ports.** Accepted. Each misuse is wrapped in `pub fn`, split by `cfg(x8_misuse)`, and paired with a compiling twin. `SettlementReserve::clone` stays a method call and is `E0599`. The `E0451` annotations sit on the literal's first field line.
6. **Fragments.** Accepted. The annotations that name a type or trait carry rustc's full message. `E0308` is `"mismatched types"`. `wrong_fragment` expects rejection when that fragment names another type.
7. **Self-test strength.** Accepted. Beyond the five item 1e shapes, the table adds `wrong_fragment`, `wrong_none_for_coded` and `wrong_two_annotations`. A rejection for a different reason fails the driver.
8. **Surface hygiene.** Accepted. The nested cargo uses the checked `RUSTC` and drops the inherited flag, wrapper and target variables. The dependency directory comes from the artifact paths.
9. **Pin scope and grammar.** Accepted. The scanner is the line-based reader over the root manifest and workspace members. In security's and storage's `[features]`, `default` is the key that fails; another feature that names `scenario-fixtures` is allowed, which is the law's default-feature rule.
10. **`crash-matrix`.** Accepted. The pin matches only `scenario-fixtures`. The unit check that platform's `[features] crash-matrix = []` passes is the rebase addition, and that test passed.
11. **Fixture formatting.** Accepted. `rustfmt --edition 2024 --check` on `cases/` and `selftest/` is clean.
12. **Platform.** Accepted for this host. The driver requires the pinned 1.95.0 toolchain. `NativeTrustReadSession` and the fence cases compiled on this macOS host.
13. **Inventory.** Accepted. See below.

## Inventory v117

v117 is 414580 bytes, sha256 `0601e3fa93ad00a09197dc199aafe74b8102f7d90c62916881ff90d0bd6f3138`. Parent v114 is the pin above. The successor record is 22276 bytes, sha256 `96a896eb0f5db82e40ad47bf04c77f17826775560db5d5c48e999bc3e8de9681`. The subject manifest is 2118 bytes, sha256 `b310afb3b37b6857c23a0be6005c79320168108dcb4712d8deeb3f0bb31e838e`.

v114 has 804 file rows and v117 has 835. Both lists are sorted and have no duplicate paths. The 804 inherited rows are equal by value, including `crates/host/tests/admission_tests.rs`. The 31 added rows are the case and self-test fixtures, each `opensip-host`, role `fixture`, standing `proposed`. `packages`, `pendingDecisions` and `schemaVersion` match v114. The carried unresolved obligations match v114's successor. Sixteen projection rows bind to v114: each stored description equals `before`, and each candidate pointer is the sorted index of that path.

`build_v117.py` takes the parent and its successor record from the lock's selected row. It was not run; it writes the architecture tree.

## Replay

Replayed here with Rust 1.95.0, `cargo test --locked --offline -p opensip-host --test admission_tests`, `CARGO` and `RUSTC` set, and `CARGO_TARGET_DIR` under this review directory (removed afterward): 4 passed, 0 failed, in 20.86 seconds. That is the driver (23 cases and 8 self-tests), the annotation grammar, the vacuous manifest pin, and the pin's refusal table including `crash-matrix`.

`verify_projection.py` against the worktree lock: PASS, 16 rows, 83 corruptions refused. `verify_scratch.py` appending v117 in memory: passed, 78 inventory successors, 72 contract successors, 16 inheritance rows, v117 selected.

The workspace suite, clippy, `cargo fmt --all --check`, `check_package_edges`, `verify_design`, and the lead's reverted mutations were not replayed.

## Verdict

ACCEPT-UNIT. Inventory v117 is ACCEPT on v114. `requiredFindings` is empty on both.
