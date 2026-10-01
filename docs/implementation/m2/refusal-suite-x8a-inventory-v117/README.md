# Opaque API refusal suite inventory117 (unit X8a)

Adds exactly 31 files to inventory114 (unit X9-0, selected at product daa7b01). They are all fixtures under `crates/host/tests/refusal/`:
- 23 compile-fail cases in `cases/`: group I (1), group K (5) and group L (17, one per existing `compile_fail` doctest);
- 8 must-reject driver self-tests in `selftest/`.

The driver is `crates/host/tests/admission_tests.rs`, which already has its planned row (from inventory v1 onward); the file is new in the product. Inventory117 keeps all 804 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 835 planned files. No crate, dependency, package edge, feature, lock entry or Cargo target is added:
- the driver uses only `std` and `serde_json`, which host already depends on;
- the fixtures are never Cargo targets; no fixture is `main.rs`, so Cargo never discovers one.

The rows are unit X8a of law X8 r3: item 1 (driver, annotation, toolchain check, census and self-test), item 3's groups I, K and L, and item 4f's `scenario-fixtures` source pin.

**What admission_tests.rs holds.**
- `opaque_api_misuse_fails_for_the_intended_reason` is item 1's one test. It:
  - runs the census;
  - runs a nested `cargo check --locked --offline -p opensip-host --message-format=json` into `CARGO_TARGET_TMPDIR/x8-surface`;
  - compiles each case twice with the pinned rustc: the control, and the misuse under `--cfg x8_misuse`;
  - then runs every self-test.
- `annotations_are_parsed_exactly` covers the annotation grammar.
- `scenario_fixtures_stays_out_of_release_manifests` is item 4f's pin. It reads the workspace manifests from `cargo metadata --no-deps`, and passes vacuously until X8b adds the feature.
- `the_feature_pin_refuses_every_release_route` covers the pin's refusals. It also checks that the pin accepts X9's `crash-matrix` table in platform's `[features]`.

**Changes to existing rows.** None. The `admission_tests.rs` row keeps its planned description: malformed joins, replay-invalid Runs, revoked authority and stale fences cannot produce acknowledged authoritative commits.
- X8a adds the compile-fail half of that file.
- X8c adds the behavioural cases (B0 to B8) that the description names.
- The description stays the file's planned purpose. A description-only successor may add the compile-fail driver to it; it is not changed here, so the inherited row stays equal by value.

**Order.** This successor's parent is the inventory the real product lock selects: inventory114 (unit X9-0) at product daa7b01.
- `evidence/build_v117.py` reads the parent, and the successor record that bound its sixteen rows, from the lock's own last `inventorySuccessors` entry, after checking both pins. If X4a's inventory116 (or another unit) integrates first, a rerun rebuilds on that parent with no edit.
- It writes only its own two paths. It refuses to write over any path git already tracks, and refuses while a lock selects inventory117.
- Reruns reproduce the same bytes.
- The number 117 was assigned while X4a (v116) was in flight; succession is by the lock's parent pin, not by number.

**Projection.** The sixteen effective description overrides bound to inventory114 (carried unchanged from inventory111 back to inventory81) stay bound by stable file path, with parent inventory114.
- `verify_projection.py` is inventory114's helper, with only its comment corrected to name its parent. It runs against the real lock at daa7b01, which selects inventory114.
- `evidence/verify_scratch.py` appends inventory117 in memory over the real lock, with a synthetic review and assent. It proves only that everything except the missing independent review and root assent passes.
