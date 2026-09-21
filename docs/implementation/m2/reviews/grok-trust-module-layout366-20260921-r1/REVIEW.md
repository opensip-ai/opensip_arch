# Independent review — trust module extraction 366

**Standing:** bounded **mechanical Rust module extraction** of frozen `trust-module-layout-checkpoint-366`. Sixty existing inline bodies (≥1000 B) move into `crates/security/src/trust/` via the existing `include!` convention. Original module declarations, attributes, visibility, and logical ancestry remain in `trust.rs`. This is **not** an algorithm/API/authority change, inventory/runtime selection, five-member `StoreGenerationBindingV1`, current authority, writers, or product installation. Product remains `fa72e50`. Inventory **v54** (693 planned / 579 accounted / 114 future; 633 inherited from 53 + 60 new) is a **separate later review**.

Prior 365 REVIEW `0d1e8a10…9f57` (9071 B), 364 REVIEW `d93e0f3f…4f37`, ADDENDUM `39e812a1…5eac`, and CORRECTION-REVIEW `0a65bc79…b1d7` were read and are **unchanged**.

Python 3.12.13 `-I -B`. rustc/cargo/rustfmt **1.95.0**. Isolated `grok-out/`; freeze workdir **not** overwritten. Native suite: `RUST_TEST_THREADS=1` and `TMPDIR=$(getconf DARWIN_USER_TEMP_DIR)` (`/var/folders/…/T/`, **not** under `/tmp`). Root was not running native tests. No processes outside this job were signalled.

---

## Verification

Archive-pin and every `subject.json` member matched **before** extract. Frozen archive: **7259480 B, 759 members, SHA256 `1e9f064f9d1ee2cb5255cbef68f2f34beea8e2594f85cc2541f9aeceeab71715`**. Standing: “Private366 mechanical trust module extraction; no runtime selection”. Parent 365 rehashed first: **585 / 6959576 B / `99312716fc0d05d8024dcdf3f1adc67b73a665cf638a47bd21f55c56a0a32792`**. Extract rehash: 0 mismatches; **579** product files.

Vs 365:

| Class | Count |
|---|---|
| Unchanged | **518** |
| Changed | **1** (`crates/security/src/trust.rs` 623629 → **8101** B, SHA256 `8716aef7d2ed17d89f618e85cb5906bac5c50b75900822460d251a47b3a1e078`) |
| Added | **60** |
| Removed | **0** |

`Cargo.lock`, `crates/security/Cargo.toml`, `lib.rs`, generated 365 tables, and fixtures are in the 518. Public `pub use root_payload::{NativeTrustReadError, NativeTrustReadSession, ProvisionalSuccessorCounts}` remains. Source/execution locations may change (`include!` files). `original-trust.rs` is byte-identical to 365 `trust.rs`.

Extracted set is exactly the inspector `MODULE` bodies ≥1000 B. Independent leaf split of those 60 files: **36** `tests`/`*_tests` + **24** other modules. Author README says 22 runtime + 38 test/helper; both sum to 60. That grouping difference is **not** a byte defect.

Inspector (`syn = 2.0.119`, `proc-macro2`, `quote`) is **DEVONLY**; it is not a product member and is absent from `crates/security/Cargo.toml`.

---

## Tokens and formatter replay (this review reproduced)

Unformatted expansion after include-target normalization: tokens **byte-equal** (`roundtrip-unformatted-before.tokens` == `…-after.tokens`, SHA256 `7a614b63ae4ce431c7bf48b2d1158b561c632d46c9f53f52614eb59563c3d84b` / 410471 B).

Strict **post-format** tokens are **not** equal. Frozen `format-token-differences.json` has **43** entries (12 delete, 30 replace, 1 insert): optional commas and single-expression match/closure braces. The request’s “42” is **not** this file’s count; do **not** promote either failed comparison to equality. The inspector’s match-arm-only `FormatNormalizer` is retained failed history, not a pass.

Independent `format-replay-r2` (isolated copy; freeze replay dir not written): reconstruct unformatted bodies from 365 `trust.rs` + recorded span/path edits, `lstrip` leading newlines, run pinned `rustfmt --edition 2024`, reproduce **all 579** final file hashes. Candidate unmodified. This is standard-format pipeline evidence, **not** a general Rust semantic theorem.

Author `format-r1` **exit 1**: leading blank-line non-idempotence on the 60 extracted files (stdout shows a removed first-line `-`). **Preserved; not a pass.** `whitespace-only-finalization.json`: **60** files, **one** leading `\n` each; after-pins match frozen product. `security-r1-tested-source.json` differs from the final product **only** on those 60 paths. No code-token/test-body change in that edit.

Author **388 + 4 doctests + Clippy** ran on the **tested-source** image **before** that whitespace edit. This review does **not** claim those author jobs ran on the final frozen bytes.

---

## Live cargo / format (exact checks rerun)

| Kind | Result |
|---|---|
| `rustfmt --check --edition 2024` of **125** security `.rs` | exit 0 |
| Isolated formatter replay | **579/579** hashes |
| `cargo test --offline --locked -p opensip-security` (`RUST_TEST_THREADS=1`, Darwin user `TMPDIR`) **on final frozen bytes** | **388 passed; 0 failed; 2 ignored** (229.22s); **4** compile-fail doctests ok (0.12s). stdout SHA `6970bddb…64ff3` |
| Workspace Clippy `--all-targets -D warnings` | exit 0 (22.28s) |

Live named results: **394**, **same set** as parent 365 (`test-name-comparison.json`). Order differs (serial vs stored order). `ChangedDuringRead` / `OthersWrite`: **0**. Product snapshot after cargo unchanged.

---

## Findings

366 is a parser-guided physical split of already-reviewed trust owners. Algorithms, generated tables, dependencies, fixtures, and public API do not change. Unformatted tokens match; formatted tokens are not claimed equal; formatter replay reconstructs the final 579 hashes. Whitespace finalization is leading-newline only on the 60 new files.

**Actionable 366 source defect:** none that make the 60-file include map, unformatted token roundtrip, formatter replay, 394 named results, or serial 388+4 on the **final** image self-contradictory.

**Account:** author 388/Clippy attach to `security-r1-tested-source` (pre-whitespace). Final image is that source minus 60 leading newlines; this review’s 388/Clippy/fmt125 ran on the final bytes. `format-r1` remains a failed format check. Token-diff count in the frozen JSON is **43**, not 42.

**Must not be counted closed:** inventory v54; five-member store binding; current authority; writers; release; M2–M6; `trust.rs` remaining decomposition of already-external `role_machine` / native files.

---

## Remaining (do not count closed)

Selected inventory still 32. Inventory 54 is a later review. Native authority / source / runtime selection. TCB/history/original T.

---

## Verdicts

- [x] **366 as frozen mechanical extraction:** 759-member archive verified; 518/1/60 vs 365; unformatted tokens equal; post-format tokens **not** equal (43 retained diffs, not promoted); formatter replay 579; rustfmt 125; serial r1 **388 + 4 doctests** on final bytes; Clippy `-D warnings`. Private/uninstalled.
- [ ] **Not** inventory v54, selected-I/current authority, writers, or product installation.
