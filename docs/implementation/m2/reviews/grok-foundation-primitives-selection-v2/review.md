# Independent Grok review: foundation-primitives-selection v2 (narrow delta)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m2/foundation-primitives-selection-v2-subject.json`
**Manifest SHA-256:** `b8328a23fbffb6c46f52af2f18595cc74f7b32dca76a30489adb4f871c37ac75`
**Members:** 29
**Verdict:** **ACCEPT-DESIGN-UNIT**

Narrow successor that corrects archived v1 S1/S2 **before integration**. v1 had ACCEPT-DESIGN-UNIT, no root assent, and was never installed. This verdict does **not** merge with the provider-workspace unit and does not imply M1 readiness.

Production H-decoder and `RetainedDirectory` adapter bytes are unchanged from v1. This review relies on archived v1 (`docs/implementation/m2/reviews/grok-foundation-primitives-selection-v1/review.json` SHA `640e6f84…b643` / 6904, pin-match) **only** for that unchanged production behavior. v2 independently verifies pins, the two corrections, long-TMPDIR tests, and feature identity.

## Custody and inheritance

29/29 selection members match. Frozen implementation subject `docs/implementation/m2/trials/foundation-primitives-02/subject.json` SHA `b76e18b9…ed89` — **208/208**. Adjacent archive matches `archive-pin.json`. Candidates are exactly the subject minus `successor.json` (28). Parents: accepted contracts-dependency-selection-v1 `c9a74172…3561` / 5972 and inventory v10 `6608fabd…8bc9` / 121810. All 7 map rows match frozen product and inventory v10. Inventory still 20 packages; no extra paths/DAG. Genuine live 8/8 is not approval of these bytes. Private copy only (`review/copy/foundation-v2`). Feature-only intermediate 02 logs remain historical and were not treated as final tests.

**Five of seven owned files are byte-identical to v1.** Changed only:

| Path | v1 | v2 |
| --- | --- | --- |
| `crates/platform/Cargo.toml` | `405242c7…d510` / 324 | `c9fbe6bd…93d6` / 364 |
| `crates/platform/src/filesystem.rs` | `fefca2f1…d4ff` / 8135 | `e3b1c2e2…29ee` / 8530 |

Unchanged: `Cargo.lock`, identity `canonical_tests.rs` / `digests.rs` / `lib.rs`, platform `src/lib.rs`. Production adapter (filesystem.rs bytes before `#[cfg(test)]`) is **byte-identical** to v1.

## Two corrections

**S2 (libc features):** `libc = { version = "=0.2.189", default-features = false }` on the existing macOS/Linux edge. Independent target-filtered metadata: **15** external packages match live 8/8 version/source/features. **libc features remain `[]`.** Lock SHA unchanged `c06da7ac…e17c` (edge already present; features are not encoded in the lock).

**S1 (socket fixture):** only the Unix-socket refusal allocates `Tree::new_in(Path::new("/tmp"))` (unique `0o700` RAII). Other filesystem tests still use ambient `std::env::temp_dir()`. No `#[ignore]`, no skip of the socket assertion, no `set_current_dir`. Independent full workspace tests with `TMPDIR` length **109** (> macOS `sun_path` 104): **30/30 pass**, including `refuses_traversal_links_and_nonregular_entries`.

## Reproduction (private copy, Cargo/rustc 1.95 Homebrew)

PATH without Node; six compiler variables absent.

| Check | Result |
| --- | --- |
| `cargo test --locked --offline --workspace --all-targets` with long TMPDIR | **30/30** |
| `cargo clippy ... -D warnings` | pass |
| `cargo fmt --all --check` | pass |
| contracts dependency check | pass, 11/8 |
| package-edges `--lane host` vs inventory v10 | pass |
| 15 external version/source/feature tuples vs live | all equal; libc `[]` |
| candidate and live locks during commands | unchanged |

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty. Archived v1 S1 and S2 are addressed in this delta; they are not reopened.

## Limits

- M2 preparation only. Neither M1 nor M2 complete. Not Linux qualification, sandbox, release, or fresh blind consumer.
- Unchanged production behavior is accepted by v1 review plus this delta’s byte-identity check, not by re-deriving the full v1 adapter/H-decoder argument.
- Genuine 8/8 lock does not approve these seven files. No v1 or v2 live install in this review.
- Host-build-isolation-01 remains prior-source evidence and is not a claim about these bytes.
