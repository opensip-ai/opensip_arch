# Independent reviews — corrected 373-r2 harness and private integration 374

This folder holds **two separate verdicts**. Neither is inventory56, runtime26, S9.3, five-member binding, native 755, live source installation, or M2–M6 completion. Frozen 373 REVIEW `5bfc6aaa…bfba` (3412 B) and ADDENDUM `68286ecf…0975` (4081 B) are **unchanged**. Root remains lead.

Toolchain: rustc **1.95.0** Homebrew `59807616e` (2026-04-14); Python **3.12.13** `-I -B` (`source-audit364-env`). No product/frozen/history edits, commits, or pushes.

---

## 1. Corrected author 373-r2 fault harness — `ACCEPT-UNIT`

Evidence/harness successor only. Codec `project_registry.rs` is byte-identical to frozen 373: **10940 B** `f3bb0fb6eaabd4f581fc0a858dc0df9127f375bff07b92fc6ce3db1af0948fe5`. Not a codec-semantics re-review.

Archive `77f5b0de…7e86` / **60592 B / 137 members**; every subject member rehashed (**0** mismatches). `check_faults.py` **5920 B** `f8a824fc94aa4b79c538e5b9aabbc5f00fab0b5074be03b61e7637be85344e7b`.

`check_faults.py` now builds with **explicit** rustc source and `-o` paths in each mutant directory, asserts compiler exit 0 and `lib.is_file()` / `probe.is_file()`, and classifies **only**:

- structured semantic mismatch: `rc==1`, `cases==37412`, every `expected != actual`; or
- running probe typed `assert_eq` panic whose message is `typed getters lost or changed a field` or `projection must preserve exact namespace values and order`, with no `FileNotFoundError`.

Six infrastructure-negative controls (FileNotFound, compiler failed, TimeoutExpired, unrelated panic, empty failures `rc=0`, incomplete `cases=1` mismatch) must raise `AssertionError`. Independent extraction of `classify()` refused all six and accepted the three positive semantic shapes.

Independent replay in a **fresh copy** (`grok-out/fault-replay-373-r2/`) that did **not** contain historical `fault-runs-r2`. Parent identity rlib `0155345b…b8d5` / 11802200 B verified before compile. Live compile command uses `-o` under the replay directory (example: `…/fault-runs-r2/baseline/libproject_registry_prototype.rlib`). Result: **baseline 37412 cases, 0 failures**; **9/9** compiled semantic detections; reasons and mutant `sourceSha256` match author `fault-results.r2.json`; `probeSha256` differs (independent binaries). Extract author results `bccc0fbb…35b0` were **not** overwritten. No live `FileNotFoundError`. Frozen 373 r1 author nine-kill remains invalid FileNotFound, as the 373 ADDENDUM already recorded.

**requiredFindings:** none.

---

## 2. Private integration 374 — `ACCEPT-UNIT`

Private identity placement of the frozen 373 codec. **Not** native custody, recovery, S9.3, selected registry, or runtime26.

Archive `46aeaeb6…bcbe` / **6909112 B / 615 members**; every subject member rehashed (**0** mismatches). Standing: private integration candidate only.

Product **585** files vs baseline `2e90e02087f958a2784aa00ee73652080edc9d29` **583**:

| Class | Count | Check |
| --- | ---: | --- |
| Unchanged vs baseline | **582** | all hashes/bytes equal |
| Changed | **1** | `crates/identity/src/lib.rs` export-only |
| Added | **2** | frozen 373 codec + new tests |

`lib.rs` before `f08e459f…e562` / 1739 B → after `0158775c…60cc` / 2373 B. The only addition is a private `mod project_registry`, prefixed re-exports, an inert-decode comment, and `#[cfg(test)] mod project_registry_tests`. No other product file changed. Identity `Cargo.toml` / `Cargo.lock` / `design-lock.json` unchanged; no new crate dependency; security still does not depend on lifecycle/storage/host.

Prefixed public names (decode-only getters; module is private): `ProjectRegistryDocument`, `ProjectRegistryEntry`, `ProjectRegistryRoot`, `ProjectRegistryStatus`, `ProjectAllocationKind`, `ProjectRootPlatform`, `ProjectIdMarker`, `ProjectRegistryError`, `PROJECT_MARKER_SIZE`, `PROJECT_REGISTRY_CAP`, `PROJECT_REGISTRY_ROW_CAP`. Comment: these decoders never establish native custody, registration, a held lease, or store/operation authority.

Nine regression tests (all exercised through those public names): complete-document refusal; live vs terminal ProjectId; namespace never reused including reverse order; independent live locator vs incarnation; raw POSIX bytes and u64/i64 bounds; canonical spelling (no silent newline/key-order repair); exact 92-byte marker frame; 4096-row cap including `ABANDONED`; projection ACTIVE∪RETIRED while `has_reservations` remains visible.

Independent `cargo test --locked --offline -p opensip-identity --target aarch64-apple-darwin` on a review-local product copy, pinned 1.95, 368 verified vendor, **fresh** `CARGO_TARGET_DIR`, `RUST_TEST_THREADS=1`, Darwin user `TMPDIR`: **52 passed**, 0 failed, 0 ignored, 0 doctests, including the 9 new tests. Author workspace-build exit 0 and provider-boundary receipt (**28** sources / **19** archives; three unavailable probes expected-exit 1, empty stdout) were inspected and are not independently re-executed here. Prior **755** native tests were **not** rerun and are **not** claimed.

**requiredFindings:** none.

---

## Scope / limits

No live activation, product edits, commits, or pushes. Does not select inventory56 or runtime26. Does not grant filesystem authority, writers, crash recovery, full binding, or analyzer implementation. Author 373 r1 `fault-results.r1.json` remains invalid; this harness successor is the corrected evidence.
